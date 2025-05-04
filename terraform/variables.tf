variable "aws_region" {
  description = "AWS régió"
  type        = string
  default     = "eu-central-1"
}

variable "db_instance_class" {
  description = "RDS instance típusa"
  type        = string
  default     = "db.t3.micro"
}

variable "aws_access_key_id" {
  description = "AWS Access Key ID az ECS taskhoz (S3 eléréshez)"
  type        = string
}

variable "aws_secret_access_key" {
  description = "AWS Secret Access Key az ECS taskhoz (S3 eléréshez)"
  type        = string
}

variable "django_secret_key" {
  description = "Django SECRET_KEY"
  type        = string
} 