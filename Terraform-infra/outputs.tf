output "ec2_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.real_estate_server.public_ip
}

output "s3_bucket_name" {
  description = "S3 Bucket name"
  value       = aws_s3_bucket.app_bucket.id
}

output "dynamodb_table_name" {
  description = "DynamoDB table name"
  value       = aws_dynamodb_table.real_estate_db.name
}

