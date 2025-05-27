resource "aws_dynamodb_table" "real_estate_db" {
  name         = var.db_table_name
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "listing_id"
    type = "S"
  }

  hash_key = "listing_id"

  tags = {
    Name = "RealEstateDB"
  }
}

