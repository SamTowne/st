#!/usr/bin/env python3

import os
import subprocess
import sys

# Define variables
region = "us-west-2"
account_id = "272773485930"
repo_url = f"{account_id}.dkr.ecr.{region}.amazonaws.com"

# Define a list of dictionaries, each containing the short name, function/ECR repository name, and Dockerfile path
lambdas = [
    {
        "short_name": "data_proc",
        "name": "custodian-data-processing-lambda",
        "dockerfile_path": f"{os.getenv('HOME')}/repos/st/.workspace/custodian/lambdas/data-processing/Dockerfile",
        "ecr_repo": "custodian-data-processing",
    },
    {
        "short_name": "custodian_exec",
        "name": "custodian-execution-lambda",
        "dockerfile_path": f"{os.getenv('HOME')}/repos/st/.workspace/custodian/lambdas/custodian/Dockerfile",
        "ecr_repo": "custodian-ecr-repository",
    }
]

def build_and_push(short_name):
    # Find the lambda with the given short name
    lambda_info = next((l for l in lambdas if l["short_name"] == short_name), None)

    if lambda_info is None:
        print(f"Error: Unknown short name '{short_name}'")
        return

    # Run pytest
    pytest_dir = os.path.dirname(lambda_info["dockerfile_path"])
    print(f"Running tests for {lambda_info['name']} in {pytest_dir}...")
    result = subprocess.run(["pytest", pytest_dir], text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Tests failed, aborting. Output was:\n{result.stdout}")
        return

    # Login to ECR
    subprocess.run(f"aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {repo_url}", shell=True, check=True)

    # Change to dockerfile dir
    os.chdir(os.path.dirname(lambda_info['dockerfile_path']))

    # Build Docker image
    subprocess.run(f"docker build -t {lambda_info['name']} -f {lambda_info['dockerfile_path']} .", shell=True, check=True)

    # Tag Docker image
    subprocess.run(f"docker tag {lambda_info['name']}:latest {repo_url}/{lambda_info['name']}:latest", shell=True, check=True)

    # Push Docker image to ECR
    subprocess.run(f"docker push {repo_url}/{lambda_info['ecr_repo']}:latest", shell=True, check=True)

    # Update Lambda function
    result = subprocess.run(f"aws lambda update-function-code --region {region} --function-name {lambda_info['name']} --image-uri {repo_url}/{lambda_info['ecr_repo']}:latest > /dev/null 2>&1", shell=True, check=True)
    if result.returncode == 0:
        print(f"Successfully updated {lambda_info['name']}")
    else:
        print(f"Error updating {lambda_info['name']}")

# Check if any arguments were passed
if len(sys.argv) == 1:
    print(f"Usage: {sys.argv[0]} <short_name>")
    print("Available short names:")
    for lambda_info in lambdas:
        print(f"  {lambda_info['short_name']}")
    sys.exit(1)

# Build and push for each argument
for short_name in sys.argv[1:]:
    build_and_push(short_name)