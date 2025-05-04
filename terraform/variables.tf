variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "eu-central-1"
}

variable "db_instance_class" {
  description = "RDS instance típusa"
  type        = string
  default     = "db.t3.micro"
}

variable "aws_access_key_id" {
  description = "AWS Access Key ID"
  type        = string
  sensitive   = true
}

variable "aws_secret_access_key" {
  description = "AWS Secret Access Key"
  type        = string
  sensitive   = true
}

variable "django_secret_key" {
  description = "Django Secret Key"
  type        = string
  sensitive   = true
} 