import logging
import json
import base64

import boto3
from botocore.exceptions import ClientError
from pymongo import MongoClient
from botocore.config import Config

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set up a botocore config with no retries
config = Config(retries={'max_attempts': 0})


def check_event(event):
    """
    Check the event data for required fields.
    """
    if 'Records' not in event:
        logger.error("Event data is missing the 'Records' field")
        raise ValueError("Invalid event data")

    return True

def get_secret():
    """
    Retrieve secret from AWS Secrets Manager.
    """
    secret_name = "custodian-db"
    try:
        secretsmanager = boto3.client('secretsmanager', config=config)
        response = secretsmanager.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        logger.error("Error retrieving secret: {}".format(e))
        raise e

    if 'SecretString' in response:
        secret = response['SecretString']
    else:
        secret = base64.b64decode(response['SecretBinary'])

    return json.loads(secret)


def get_db_connection_parameters():
    """
    Retrieve parameters from AWS SSM Parameter Store.
    """
    path = '/custodian'
    parameters = {}
    ssm = boto3.client('ssm', config=config)
    try:
        response = ssm.get_parameters_by_path(Path=path, WithDecryption=True)
        for param in response['Parameters']:
            param_name = param['Name'].split('/')[-1]  # Get the last part of the parameter name
            parameters[param_name] = param['Value']
    except ClientError as e:
        logger.error("Error retrieving parameters: {}".format(e))
        raise e
    return parameters


def process_data(s3_object, bucket_name):
    """
    Retrieve data from S3 object.
    """
    logger.info("Processing data from S3")
    s3 = boto3.client('s3', config=config)
    try:
        response = s3.get_object(Bucket=bucket_name, Key=s3_object)
        data = response['Body'].read().decode('utf-8')
    except ClientError as e:
        logger.error("Error retrieving data from S3: {}".format(e))
        raise e

    return data


def configure_docdb_client(parameters, secret):
    """
    Configure the DocumentDB client.
    """
    logger.info("Configuring DocumentDB client")
    client = MongoClient(f'mongodb://{secret["username"]}:{secret["password"]}@{parameters["endpoint"]}:{secret["port"]}/')
    return client


def insert_into_documentdb(client, data, parameters):
    """
    Insert the data into the specified DocumentDB collection.
    """
    logger.info("Inserting data into DocumentDB")
    try:
        logger.info(f"Parameters: {parameters}")
        logger.info(f"Data: {data}")
        db = client['custodian']
        collection = parameters['collection']
        logger.info(f"DB: {db}")
        logger.info(f"Collection: {collection}")
        db[collection].insert_one(data)
    except Exception as e:
        logger.error("Error inserting data into DocumentDB: {}".format(e))
        raise e


def handler(event, context):
    """
    AWS Lambda handler function.
    """
    logger.info("Running data-processing lambda function")
    valid_event = check_event(event)
    if not valid_event:
        logger.error("Invalid event data")
        return
    s3_object = event['Records'][0]['s3']['object']
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    logger.info("Processing data from S3 object: {}".format(s3_object))
    parameters = get_db_connection_parameters()
    data = process_data(s3_object, bucket_name)
    secret = get_secret()
    client = configure_docdb_client(parameters, secret)
    insert_into_documentdb(client, data, parameters)