terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
  cloud {
    organization = "lab-bme-test-org"
    workspaces { name = "photoalbum-mvp" }
  }
}

provider "aws" {
  region = "eu-central-1"
}

resource "aws_s3_bucket" "photos" {
  bucket = "photoalbum-mvp-photos-${random_id.suffix.hex}"
  force_destroy = true
}

resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_db_instance" "postgres" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "15.10"
  instance_class       = "db.t3.micro"
  db_name              = "photoalbum"
  username             = "photoalbum"
  password             = random_password.db_password.result
  skip_final_snapshot  = true
  publicly_accessible  = true
  vpc_security_group_ids = [aws_security_group.rds.id]
}

resource "random_password" "db_password" {
  length  = 16
  special = false
}

resource "aws_ecr_repository" "django" {
  name = "photoalbum-mvp-django"
}

resource "aws_ecs_cluster" "main" {
  name = "photoalbum-mvp-cluster"
}

# --- Security Group for ALB and ECS ---
resource "aws_security_group" "alb" {
  name        = "photoalbum-alb-sg"
  description = "Allow HTTP inbound traffic"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "ecs" {
  name        = "photoalbum-ecs-sg"
  description = "Allow traffic from ALB"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "rds" {
  name        = "photoalbum-rds-sg"
  description = "Allow PostgreSQL inbound traffic from ECS tasks"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs.id]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# --- Data sources for default VPC and subnets ---
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# --- IAM Role for ECS Task Execution ---
resource "aws_iam_role" "ecs_task_execution" {
  name = "photoalbum-ecs-task-execution"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy_attachment" "ecs_s3_access" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# --- CloudWatch Log Group ---
resource "aws_cloudwatch_log_group" "django" {
  name              = "/ecs/photoalbum-django"
  retention_in_days = 30
}

# --- ECS Task Definition ---
resource "aws_ecs_task_definition" "django" {
  family                   = "photoalbum-django"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.ecs_task_execution.arn
  container_definitions    = jsonencode([
    {
      name      = "django"
      image     = "${aws_ecr_repository.django.repository_url}:latest"
      essential = true
      portMappings = [{ containerPort = 8080, hostPort = 8080 }]
      environment = [
        { name = "DATABASE_URL", value = "postgres://${aws_db_instance.postgres.username}:${urlencode(random_password.db_password.result)}@${aws_db_instance.postgres.endpoint}/photoalbum" },
        { name = "USE_S3", value = "True" },
        { name = "AWS_S3_OBJECT_PARAMETERS", value = "{\"CacheControl\": \"max-age=86400\"}" },
        { name = "AWS_S3_REGION_NAME", value = var.aws_region },
        { name = "SECRET_KEY", value = var.django_secret_key },
        { name = "AWS_STORAGE_BUCKET_NAME", value = aws_s3_bucket.photos.bucket },
        { name = "DEBUG", value = "True" },
        { name = "CORS_ALLOW_ALL_ORIGINS", value = "True" },
        { name = "CORS_ALLOW_CREDENTIALS", value = "True" },
        { name = "ALLOWED_HOSTS", value = "*" }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group = aws_cloudwatch_log_group.django.name
          awslogs-region = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
      healthCheck = {
        command = ["CMD-SHELL", "curl -f http://localhost:8080/health/ || exit 1"]
        interval = 60
        timeout = 10
        retries = 3
        startPeriod = 120
      }
    }
  ])
}

# --- ALB ---
resource "aws_lb" "alb" {
  name               = "photoalbum-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = data.aws_subnets.default.ids

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lb_target_group" "django" {
  name     = "photoalbum-django-tg-${random_id.suffix.hex}"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = data.aws_vpc.default.id
  target_type = "ip"
  health_check {
    path                = "/health/"
    protocol            = "HTTP"
    matcher             = "200-399"
    interval            = 60
    timeout             = 10
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }

  lifecycle {
    create_before_destroy = true
    replace_triggered_by = [
      aws_lb.alb
    ]
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.alb.arn
  port              = 8080
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.django.arn
  }

  lifecycle {
    create_before_destroy = true
  }
}

# --- ECS Service ---
resource "aws_ecs_service" "django" {
  name            = "photoalbum-django-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.django.arn
  launch_type     = "FARGATE"
  desired_count   = 1
  network_configuration {
    subnets          = data.aws_subnets.default.ids
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.django.arn
    container_name   = "django"
    container_port   = 8080
  }
  depends_on = [aws_lb_listener.http]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_s3_bucket_public_access_block" "photos" {
  bucket = aws_s3_bucket.photos.id

  block_public_acls   = false
  block_public_policy = false
  ignore_public_acls  = false
  restrict_public_buckets = false
} 