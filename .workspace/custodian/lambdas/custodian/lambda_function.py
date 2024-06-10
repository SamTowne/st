import json
import logging
import os
import subprocess

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run_custodian(lambda_task_root):
    """
    Run Cloud Custodian with a specified command.
    """
    logger.info("Running Cloud Custodian...")
    output_dir = "s3://custodian-bucket-benjals-272773485930/custodian-output"
    command = ["custodian", "run", "-s", output_dir, f"{lambda_task_root}/policies/*.yml"]

    try:
        subprocess.run(command, check=True, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        logger.error("Error running Cloud Custodian: {}".format(e))


def handler(event, context):
    """
    AWS Lambda handler function.
    """
    lambda_task_root = os.environ.get('LAMBDA_TASK_ROOT')
    run_custodian(lambda_task_root)
    return {}