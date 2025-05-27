resource "aws_iam_role" "app_role" {
  name = "RealEstateAppRole"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "app_policy" {
  name        = "RealEstateAppPolicy"
  description = "Permissions for accessing S3 and DynamoDB"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": [
        "${aws_s3_bucket.app_bucket.arn}",
        "${aws_s3_bucket.app_bucket.arn}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:*"
      ],
      "Resource": "${aws_dynamodb_table.real_estate_db.arn}"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "app_role_attach" {
  role       = aws_iam_role.app_role.name
  policy_arn = aws_iam_policy.app_policy.arn
}

