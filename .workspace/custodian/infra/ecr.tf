resource "aws_ecr_repository" "repository" {
  name = "custodian-ecr-repository"
}

/*
# Authenticate Docker to your ECR registry
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 272773485930.dkr.ecr.us-west-2.amazonaws.com

# Build
docker build -t custodian-ecr-repository .

# Tag your Docker image with the ECR repository URI
docker tag custodian-ecr-repository:latest 272773485930.dkr.ecr.us-west-2.amazonaws.com/custodian-ecr-repository:latest

# Push your Docker image to the ECR repository
docker push 272773485930.dkr.ecr.us-west-2.amazonaws.com/custodian-ecr-repository:latest

*/