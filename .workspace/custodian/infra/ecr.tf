resource "aws_ecr_repository" "repository" {
  name = "custodian-ecr-repository"
}

/*
# Build your Docker image
docker build -t my-image .

# Authenticate Docker to your ECR registry
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin your-ecr-repo-uri

# Tag your Docker image with the ECR repository URI
docker tag my-image:latest your-ecr-repo-uri:latest

# Push your Docker image to the ECR repository
docker push your-ecr-repo-uri:latest
*/