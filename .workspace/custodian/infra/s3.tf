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