resource "aws_ssm_parameter" "docdb_endpoint" {
  name  = "/custodian/docdb_endpoint"
  type  = "String"
  value = aws_docdb_cluster.docdb.endpoint
}

resource "aws_ssm_parameter" "docdb_collection" {
  name  = "/custodian/docdb_collection"
  type  = "String"
  value = "custodian-data"
}

resource "aws_ssm_parameter" "docdb_database" {
  name  = "/custodian/docdb_database"
  type  = "String"
  value = "custodian"
}

resource "aws_ssm_parameter" "regions_parameter" {
  name  = "/custodian/config/regions"
  type  = "StringList"
  value = local.aws_regions_for_custodian_to_scan
}

resource "aws_ssm_parameter" "bucket_name_parameter" {
  name  = "/custodian/config/bucket_name"
  type  = "String"
  value = module.s3_bucket_custodian.s3_bucket_id
}