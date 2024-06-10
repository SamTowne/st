module "s3_bucket_custodian" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "2.0.0"

  bucket = "custodian-bucket-benjals-272773485930"
  acl    = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "sse" {
  bucket = module.s3_bucket_custodian.s3_bucket_id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.data-processing.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = module.s3_bucket_custodian.s3_bucket_arn
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = module.s3_bucket_custodian.s3_bucket_id

  lambda_function {
    lambda_function_arn = aws_lambda_function.data-processing.arn
    events              = ["s3:ObjectCreated:*"]
  }
}