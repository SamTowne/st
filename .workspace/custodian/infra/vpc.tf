resource "aws_vpc_endpoint" "ssm_endpoint" {
  vpc_id       = "vpc-1cd09664"
  service_name = "com.amazonaws.us-west-2.ssm"
  vpc_endpoint_type = "Interface"
  subnet_ids = ["subnet-9fee12d5", "subnet-1704d76f"]
  security_group_ids = ["sg-490baa63"]
  private_dns_enabled = true
}

resource "aws_vpc_endpoint" "secretsmanager_endpoint" {
  vpc_id       = "vpc-1cd09664"
  service_name = "com.amazonaws.us-west-2.secretsmanager"
  vpc_endpoint_type = "Interface"
  subnet_ids = ["subnet-9fee12d5", "subnet-1704d76f"]
  security_group_ids = ["sg-490baa63"]
  private_dns_enabled = true
}