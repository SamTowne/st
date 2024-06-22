import logging
import json
import base64
from urllib.parse import unquote
import gzip
import os

import boto3
from botocore.exceptions import ClientError
from pymongo import MongoClient
from botocore.config import Config

# Set up logging
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

# Set up a botocore config with no retries
config = Config(retries={'max_attempts': 0})


def check_event(event):
    """
    Check the event data for required fields.
    """
    if 'Records' not in event:
        LOGGER.error("Event data is missing the 'Records' field")
        raise ValueError("Invalid event data")

    return True

def get_secret(secret_name):
    """
    Retrieve secret from AWS Secrets Manager.
    """
    try:
        secretsmanager = boto3.client('secretsmanager', config=config)
        response = secretsmanager.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        LOGGER.error("Error retrieving secret: {}".format(e))
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
        LOGGER.error("Error retrieving parameters: {}".format(e))
        raise e
    LOGGER.info(f"Parameters: {parameters}")
    return parameters



def process_data(s3_object, bucket_name):
    """
    Retrieve data from S3 object.
    """
    LOGGER.info("Processing data from S3")
    s3 = boto3.client('s3', config=config)
    data = None
    try:
        object_key = unquote(s3_object['key'])
        LOGGER.info(f"Bucket: {bucket_name}, Key: {object_key}")
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        gzip_file = gzip.GzipFile(fileobj=response['Body'])
        data = gzip_file.read().decode('utf-8')
        data = json.loads(data)
    except Exception as e:
        LOGGER.error("Error retrieving data from S3: {}".format(e))
        raise e

    return data

def configure_docdb_client(parameters, secret):
    """
    Configure the DocumentDB client.
    """
    LOGGER.info("Configuring DocumentDB client")
    try:
        client = MongoClient(
            f'mongodb://{secret["username"]}:{secret["password"]}@'
            f'{parameters["docdb_endpoint"]}:{secret["port"]}/'
            f'?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0'
            f'&readPreference=secondaryPreferred&retryWrites=false'
        )
    except Exception as e:
        LOGGER.error("Error configuring DocumentDB client: {}".format(e))
        raise e
    return client


def insert_into_documentdb(client, data, parameters):
    """
    Insert the data into the specified DocumentDB collection.
    """
    LOGGER.info("Inserting data into DocumentDB")
    try:
        LOGGER.info(f"Parameters: {parameters}")
        LOGGER.info(f"Data: {data}")
        db = client['custodian']
        collection = parameters['docdb_collection']
        LOGGER.info(f"DB: {db}")
        LOGGER.info(f"Collection: {collection}")
        db[collection].insert_one(data)
    except Exception as e:
        LOGGER.error("Error inserting data into DocumentDB: {}".format(e))
        raise e


def handler(event, context):
    """
    AWS Lambda handler function.
    """
    LOGGER.info("Running data-processing lambda function")
    valid_event = check_event(event)
    if not valid_event:
        LOGGER.error("Invalid event data")
        return
    LOGGER.info("Event data: {}".format(event))
    s3_object = event['Records'][0]['s3']['object']
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    LOGGER.info("Processing data from S3 object: {}".format(s3_object))
    parameters = get_db_connection_parameters()
    data = process_data(s3_object, bucket_name)
    db_secret = get_secret("custodian-db")
    client = configure_docdb_client(parameters, db_secret)
    insert_into_documentdb(client, data, parameters)