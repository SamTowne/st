#!/usr/bin/env python3

import glob
import logging
import os
import subprocess
import sys

# Set up logging
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

# Add a StreamHandler to send log messages to stdout
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

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
    },
    {
        "short_name": "gpt",
        "name": "custodian-gpt-lambda",
        "dockerfile_path": f"{os.getenv('HOME')}/repos/st/.workspace/custodian/lambdas/gpt/Dockerfile",
        "ecr_repo": "gpt",
    }
]

def build_and_push(short_name):
    LOGGER.info(f"Building and pushing {short_name}...")
    # Find the lambda with the given short name
    lambda_info = next((l for l in lambdas if l["short_name"] == short_name), None)

    if lambda_info is None:
        LOGGER.error(f"Error: Unknown short name '{short_name}'")
        LOGGER.info("Available short names:")
        for lambda_info in lambdas:
            LOGGER.info(f"  {lambda_info['short_name']}")
        return

    # Run pytest with a timeout
    pytest_dir = os.path.dirname(lambda_info["dockerfile_path"])
    LOGGER.info(f"Running tests for {lambda_info['name']} in {pytest_dir}...")
    try:
        result = subprocess.run(["pytest", pytest_dir], timeout=5)
    except subprocess.TimeoutExpired:
        LOGGER.error("Tests took too long to complete, aborting.")
        return

    if result.returncode != 0:
        LOGGER.error(f"Tests failed, aborting.")
        return
    
    # Run custodian policy validation command for 'custodian_exec'
    if short_name == 'custodian_exec':
        custodian_policy_files = glob.glob(os.path.join(pytest_dir, 'policies', '*.yml'))
        for policy_file in custodian_policy_files:
            LOGGER.info(f"Running custodian policy validation for {lambda_info['name']} on {policy_file}...")
            # Replace 'custodian validate policies.yml' with your actual command
            result = subprocess.run(['custodian', 'validate', policy_file], text=True, capture_output=True)
            if result.returncode != 0:
                LOGGER.error(f"Custodian policy validation failed for {policy_file}, aborting deployment. {result.stdout}")
                LOGGER.error(result.stderr)
                return
    
    # Check AWS credentials
    LOGGER.info("Checking AWS credentials...")
    try:
        result = subprocess.run(['aws', 'sts', 'get-caller-identity'], text=True, capture_output=True, timeout=10)
    except subprocess.TimeoutExpired:
        LOGGER.error("AWS credentials check is hanging, possibly due to missing or incorrect AWS credentials.")
        LOGGER.info("Please ensure your AWS credentials are set correctly and have the necessary permissions.")
        return

    if result.returncode != 0:
        LOGGER.error("AWS credentials check failed, aborting deployment.")
        LOGGER.error(result.stderr)
        return
    else:
        LOGGER.info("AWS credentials check passed.")
        LOGGER.info(f"AWS caller identity: {result.stdout}")

    # Get ECR login password
    LOGGER.info(f"Getting ECR login password for {lambda_info['name']}...")
    try:
        result = subprocess.run(['aws', 'ecr', 'get-login-password', '--region', region], text=True, capture_output=True, timeout=10)
    except subprocess.TimeoutExpired:
        LOGGER.error("ECR get-login-password command is hanging, possibly due to missing or incorrect AWS credentials.")
        return

    if result.returncode != 0:
        LOGGER.error(f"Error getting ECR login password: {result.stderr}")
        return
    else:
        ecr_password = result.stdout

    # Login to Docker
    LOGGER.info(f"Logging in to Docker for {lambda_info['name']}...")
    try:
        result = subprocess.run(['docker', 'login', '--username', 'AWS', '--password-stdin', repo_url], input=ecr_password, text=True, capture_output=True, timeout=10)
    except subprocess.TimeoutExpired:
        LOGGER.error("Docker login command is hanging, possibly due to a network issue or incorrect ECR repository URL.")
        return

    if result.returncode != 0:
        LOGGER.error(f"Error logging in to Docker: {result.stderr}")
    else:
        LOGGER.info("Successfully logged in to ECR")
    
    # Change to dockerfile dir
    os.chdir(os.path.dirname(lambda_info['dockerfile_path']))

    # Build Docker image
    LOGGER.info(f"Building Docker image for {lambda_info['name']}...")
    subprocess.run(f"docker build --platform linux/arm64 -t {lambda_info['name']} -f {lambda_info['dockerfile_path']} .", shell=True, check=True)

    # Tag Docker image
    subprocess.run(f"docker tag {lambda_info['name']}:latest {repo_url}/{lambda_info['ecr_repo']}:latest", shell=True, check=True)

    # Push Docker image to ECR
    LOGGER.info(f"Pushing Docker image to ECR for {lambda_info['name']}...")
    subprocess.run(f"docker push {repo_url}/{lambda_info['ecr_repo']}:latest", shell=True, check=True)

    # Update Lambda function
    LOGGER.info(f"Updating Lambda function code for {lambda_info['name']}...")
    result = subprocess.run(f"aws lambda update-function-code --region {region} --function-name {lambda_info['name']} --image-uri {repo_url}/{lambda_info['ecr_repo']}:latest > /dev/null 2>&1", shell=True, check=True)
    if result.returncode == 0:
        print(f"Successfully updated {lambda_info['name']}")
    else:
        print(f"Error updating {lambda_info['name']}")

# Check if any arguments were passed
if len(sys.argv) == 1:
    LOGGER.info(f"Usage: {sys.argv[0]} <short_name>")
    LOGGER.info("Available short names:")
    for lambda_info in lambdas:
        LOGGER.info(f"  {lambda_info['short_name']}")
    sys.exit(1)

# Build and push for each argument
for short_name in sys.argv[1:]:
    build_and_push(short_name)