variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "Amazon Linux Machine Image ID"
  type        = string
  default     = "ami-08b5b3a93ed654d19"
}

variable "key_name" {
  description = "AWS Key Pair name for SSH access"
  type        = string
  default     = "real-estate-main"
}

variable "bucket_name" {
  description = "S3 bucket name for storing media files"
  type        = string
  default     = "my-realestate-app-bucket"
}

variable "db_table_name" {
  description = "DynamoDB table name"
  type        = string
  default     = "RealEstateListings"
}

