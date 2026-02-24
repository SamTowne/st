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
from gptscript.gptscript import GPTScript

# Set up logging
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

# Set up a botocore config with no retries
config = Config(retries={'max_attempts': 0})


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


def get_docdb_collection(client, collection_name):
    try:
        db = client['custodian']
        collection = db[collection_name]
        return collection
    except ClientError as e:
        print(f"Error retrieving collection: {e}")
        raise e


def summarize_text_with_gptscript(text):
    gpt = GPTScript()
    return gpt.summarize(text)

def pygptscript_summarize_collection(collection):
    LOGGER.info("Summarizing collection using py gptscript")
    text = ""
    for document in collection:
        text += json.dumps(document, indent=4) + "\n\n"
    summary = summarize_text_with_gptscript(text)
    return summary


def handler(event, context):
    """
    AWS Lambda handler function.
    """
    LOGGER.info("Running gpt lambda function")
    parameters = get_db_connection_parameters()
    db_secret = get_secret("custodian-db")
    client = configure_docdb_client(parameters, db_secret)
    collection = get_docdb_collection(client, parameters['docdb_collection'])
    openai_api_key = get_secret('openai-api-key')
    if not openai_api_key:
        LOGGER.error("OpenAI API key not found")
    os.environ['OPENAI_API_KEY'] = openai_api_key['openai_api_key']
    gpt_summary = pygptscript_summarize_collection(parameters['docdb_collection'])
    LOGGER.info(f"Summary: {gpt_summary}")
