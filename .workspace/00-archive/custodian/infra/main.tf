terraform {
  backend "s3" {
    bucket = "custodian-272773485930-terraform-tfstate"
    key    = "st/.workspace/custodian/infra/custodian.tfstate"
    region = "us-west-2"
  }
}

provider "aws" {
  region = "us-west-2"
  default_tags {
    tags = {
      Environment = "Prod"
      Name        = "Custodian"
      IaCPath     = "st/.workspace/custodian/infra/"
    }
  }
}
