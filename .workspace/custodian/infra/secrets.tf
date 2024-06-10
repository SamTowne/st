# docdb
resource "aws_secretsmanager_secret" "this" {
  name = "custodian-db"
  description = "Secret for custodian database"
}

resource "aws_secretsmanager_secret_version" "this" {
  secret_id = aws_secretsmanager_secret.this.id
  secret_string = jsonencode({
    username = "placeholder_value"
    password = "placeholder_value"
    port     = "placeholder_value"
  })
  lifecycle {
    ignore_changes = [secret_string]
  }
}