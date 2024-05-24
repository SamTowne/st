terraform {
  backend "s3" {
    bucket = "custodian-272773485930-terraform-tfstate"
    key    = "st/.workspace/custodian/policy-test-infra/test-infra.tfstate"
    region = "us-west-2"
  }
}

provider "aws" {
  region = "us-west-2"
  default_tags {
    tags = {
      PolicyTestInfra = "true"
      Name            = "PolicyTestInfra"
      IaCPath         = "st/.workspace/custodian/policy-test-infra/"
    }
  }
}