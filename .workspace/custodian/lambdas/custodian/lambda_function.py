import glob
import logging
import os
import subprocess

import boto3
import botocore.session

session = botocore.session.get_session()
session.set_config_variable(('retries'), {'max_attempts': 1})

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def validate_event(event):
    """
    Validate the event data.
    """
    logger.info("Validating event data...")
    required_keys = ['rule_name']
    for key in required_keys:
        if key not in event:
            raise ValueError(f"Missing '{key}' key in event")
    if not isinstance(event['rule_name'], str):
        raise ValueError("Invalid 'rule_name' value in event")


def get_parameters_from_ssm():
    """
    Retrieve parameters from AWS SSM Parameter Store.
    """
    logger.info("Retrieving parameters from SSM Parameter Store...")
    try:
        ssm = boto3.client('ssm')
        bucket_name = ssm.get_parameter(Name=os.environ['BUCKET_NAME_PARAMETER_PATH'])['Parameter']['Value']
        regions = ssm.get_parameter(Name=os.environ['REGIONS_PARAMETER_PATH'])['Parameter']['Value'].split(',')
        return bucket_name, regions
    except Exception as e:
        logger.error(f"Error getting parameters from SSM: {e}")
        raise


def get_account_id():
    """
    Retrieve the AWS account ID.
    """
    logger.info("Getting account ID...")
    try:
        sts = boto3.client('sts')
        return sts.get_caller_identity()['Account']
    except Exception as e:
        logger.error(f"Error getting account ID: {e}")
        raise


def run_custodian(region, output_path, rule_name):
    """
    Run Cloud Custodian for each policy file in the specified rule directory
    """
    logger.info(f"Running Cloud Custodian for business rule {rule_name} in region {region}...")
    logger.info(f"Writing results to {output_path}")
    policy_files = glob.glob(f'/var/task/policies/{rule_name}/*.yml')

    for policy_file in policy_files:
        run_command = f'custodian run --cache-period=0 --region {region} --output-dir={output_path} {policy_file}'
        try:
            logger.info(f"Running custodian: {run_command}")
            run_process = subprocess.Popen(run_command, shell=True, stdout=subprocess.PIPE)
            run_process.wait()
            run_command_output = run_process.stdout.read()
            if run_command_output:
                logger.info(run_command_output)
        except Exception as e:
            logger.error(f"Error running Cloud Custodian: {e}")
            raise


def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    """
    validate_event(event)
    bucket_name, regions = get_parameters_from_ssm()
    account_id = get_account_id()
    os.environ['C7N_CACHE_DIR'] = '/tmp' # Set the cache directory for Cloud Custodian
    rule_name = event['rule_name']
    for region in regions:
        output_path = f"s3://{bucket_name}/custodian-run-logs/account={account_id}/region={region}"
    run_custodian(region, output_path, rule_name)
    return 'Success'


if __name__ == "__main__":
    # For local testing
    event = {
        'rule_name': 'aws-required-tags'
    }
    lambda_handler(event, None)