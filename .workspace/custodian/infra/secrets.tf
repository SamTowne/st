# docdb
resource "aws_secretsmanager_secret" "this" {
  name = "custodian-db"
  description = "Secret for custodian database"
}

resource "aws_secretsmanager_secret_version" "this" {
  secret_id = aws_secretsmanager_secret.this.id
  secret_string = jsonencode({
    username       = "placeholder_value"
    password       = "placeholder_value"
    port           = "placeholder_value"
  })
  lifecycle {
    ignore_changes = [secret_string]
  }
}

# Open API Key
resource "aws_secretsmanager_secret" "openai_api_key" {
  name = "custodian-openai-api-key"
  description = "Secret for custodian openai api key"
}

resource "aws_secretsmanager_secret_version" "open_api_key" {
  secret_id = aws_secretsmanager_secret.openai_api_key.id
  secret_string = jsonencode({
    openai_api_key  = "placeholder_value"
  })
  lifecycle {
    ignore_changes = [secret_string]
  }
}