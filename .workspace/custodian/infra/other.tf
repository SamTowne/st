resource "aws_iam_role" "lambda_role" {
  name = "custodian-lambda-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}



resource "aws_ecr_repository" "repository" {
  name = "custodian-ecr-repository"
}

resource "aws_s3_bucket" "bucket1" {
  bucket = "custodian-bucket1"
  acl    = "private"
}

resource "aws_s3_bucket" "bucket2" {
  bucket = "custodian-bucket2"
  acl    = "private"
}