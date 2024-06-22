import pytest
import boto3
from moto import mock_aws
from unittest.mock import MagicMock, patch
import gzip
import io

from lambda_function import(
    get_db_connection_parameters,
    get_secret, 
    process_data, 
    insert_into_documentdb
)

@mock_aws
def test_get_db_connection_parameters():
    ssm = boto3.client('ssm')
    ssm.put_parameter(Name='/custodian/endpoint', Value='test-endpoint', Type='String')
    ssm.put_parameter(Name='/custodian/port', Value='test-port', Type='String')
    ssm.put_parameter(Name='/custodian/collection', Value='test-collection', Type='String')

    parameters = get_db_connection_parameters()
    assert parameters == {'endpoint': 'test-endpoint', 'port': 'test-port', 'collection': 'test-collection'}

@mock_aws
def test_get_secret():
    secretsmanager = boto3.client('secretsmanager')
    secretsmanager.create_secret(Name='custodian-db', SecretString='{"username": "test-user", "password": "test-pass", "port": "test-port"}')
    secret = get_secret()
    assert secret == {'username': 'test-user', 'password': 'test-pass', 'port': 'test-port'}

@mock_aws
def test_process_data():
    s3 = boto3.client('s3', region_name='us-east-1')
    s3.create_bucket(Bucket='test-bucket')
    
    # Compress the test data
    test_data = 'test-data'
    test_data_compressed = io.BytesIO()
    with gzip.GzipFile(fileobj=test_data_compressed, mode='w') as gzip_file:
        gzip_file.write(test_data.encode('utf-8'))
    
    s3.put_object(Bucket='test-bucket', Key='test-object', Body=test_data_compressed.getvalue())
    s3_object = {'key': 'test-object'}
    data = process_data(s3_object, 'test-bucket')
    assert data == test_data

@patch('pymongo.MongoClient')
def test_insert_into_documentdb(mocked_client):
    parameters = {"collection": "mocked-collection", "endpoint": "mocked-endpoint"}
    mocked_db = MagicMock()
    mocked_collection = MagicMock()
    mocked_client.return_value.__getitem__.return_value = mocked_db
    mocked_db.__getitem__.return_value = mocked_collection
    try:
        insert_into_documentdb(mocked_client.return_value, {"test": "data"}, parameters)
    except Exception as e:
        print(f"Exception: {e}")
        raise
    mocked_collection.insert_one.assert_called_with({"test": "data"})