output "s3_bucket_name" {
  value = aws_s3_bucket.photos.bucket
}

output "db_endpoint" {
  value = aws_db_instance.postgres.endpoint
}

output "db_username" {
  value = aws_db_instance.postgres.username
}

output "db_password" {
  value = random_password.db_password.result
  sensitive = true
}

output "ecr_repo_url" {
  value = aws_ecr_repository.django.repository_url
} 