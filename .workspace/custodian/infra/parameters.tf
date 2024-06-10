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