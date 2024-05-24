import logging
import subprocess

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run_custodian():
    """
    Run Cloud Custodian with a specified command.
    """
    logger.info("Running Cloud Custodian...")
    command = ["custodian", "run", "-s", ".", "/var/task/policies/*.yml"]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        logger.info("Cloud Custodian output: " + output.decode())
    except subprocess.CalledProcessError as e:
        logger.error("Error running Cloud Custodian: " + e.output.decode())


def handler(event, context):
    """
    AWS Lambda handler function.
    """
    run_custodian()
    return {}