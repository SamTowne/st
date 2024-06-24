data "aws_secretsmanager_secret_version" "this" {
  secret_id = aws_secretsmanager_secret.this.id
}

locals {
  secret_value = jsondecode(data.aws_secretsmanager_secret_version.this.secret_string)
}

resource "aws_docdb_cluster" "docdb" {
  cluster_identifier      = "custodian"
  engine                  = "docdb"
  master_username         = local.secret_value.username
  master_password         = local.secret_value.password
  backup_retention_period = 5
  preferred_backup_window = "07:00-09:00"
  skip_final_snapshot     = true
  port                    = local.secret_value.port
}

resource "aws_docdb_cluster_instance" "cluster_instance" {
  identifier         = "custodian-instance"
  cluster_identifier = aws_docdb_cluster.docdb.id
  instance_class     = "db.t3.medium"
}