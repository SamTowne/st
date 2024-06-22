resource "aws_ecr_repository" "repository" {
  name = "custodian-ecr-repository"
##push commands
/*
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 272773485930.dkr.ecr.us-west-2.amazonaws.com
docker build --platform linux/amd64 -t custodian-lambda .
docker tag custodian-ecr-repository:latest 272773485930.dkr.ecr.us-west-2.amazonaws.com/custodian-ecr-repository:latest
docker push 272773485930.dkr.ecr.us-west-2.amazonaws.com/custodian-ecr-repository:latest
aws lambda update-function-code --region us-west-2 --function-name custodian-execution-lambda --image-uri 272773485930.dkr.ecr.us-west-2.amazonaws.com/custodian-ecr-repository:latest
*/
}

resource "aws_ecr_repository" "data_processing_repository" {
  name = "custodian-data-processing"
##push commands
/*
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 272773485930.dkr.ecr.us-west-2.amazonaws.com
docker build -t custodian-data-processing .
docker tag custodian-data-processing:latest 272773485930.dkr.ecr.us-west-2.amazonaws.com/custodian-data-processing:latest
docker push 272773485930.dkr.ecr.us-west-2.amazonaws.com/custodian-data-processing:latest
aws lambda update-function-code --region us-west-2 --function-name custodian-data-processing --image-uri 272773485930.dkr.ecr.us-west-2.amazonaws.com/custodian-ecr-repository:latest
*/
}

resource "aws_ecr_repository" "gpt" {
  name = "gpt"
}