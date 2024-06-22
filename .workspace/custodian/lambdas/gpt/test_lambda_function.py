import pytest
import boto3
from unittest.mock import MagicMock, patch
from pymongo import MongoClient
import json
import gzip
import io
import importlib
import sys

# Mock httpx before importing lambda_function
sys.modules['httpx'] = MagicMock()

from lambda_function import(
    get_db_connection_parameters,
    get_secret, 
    process_data, 
    pygptscript_summarize_collection,
)

@patch('boto3.client')
def test_get_db_connection_parameters(mocked_client):
    # Create a mock SSM client
    mocked_ssm = MagicMock()
    mocked_client.return_value = mocked_ssm

    # Mock the response of get_parameters_by_path
    mocked_ssm.get_parameters_by_path.return_value = {
        'Parameters': [
            {'Name': '/custodian/docdb_endpoint', 'Value': 'test-endpoint'},
            {'Name': '/custodian/docdb_collection', 'Value': 'test-collection'}
        ]
    }

    # Get parameters
    parameters = get_db_connection_parameters()

    # Assert that get_parameters_by_path was called with the correct arguments
    mocked_ssm.get_parameters_by_path.assert_called_once_with(Path='/custodian', WithDecryption=True)

    # Assert
    assert parameters == {'docdb_endpoint': 'test-endpoint', 'docdb_collection': 'test-collection'}

@patch('boto3.client')
def test_get_secret(mocked_client):
    # Create a mock Secrets Manager client
    mocked_secretsmanager = MagicMock()
    mocked_client.return_value = mocked_secretsmanager

    # Mock the response of get_secret_value
    secret_string = json.dumps({"username": "test", "password": "test"})
    mocked_secretsmanager.get_secret_value.return_value = {'SecretString': secret_string}

    # Call get_secret with a specific secret name
    secret = get_secret('custodian-db')

    # Assert that get_secret_value was called with the correct arguments
    mocked_secretsmanager.get_secret_value.assert_called_once_with(SecretId='custodian-db')

    # Assert that the returned secret is correct
    assert secret == {"username": "test", "password": "test"}

@patch('boto3.client')
def test_process_data(mocked_client):
    # Create a mock S3 client
    mocked_s3 = MagicMock()
    mocked_client.return_value = mocked_s3

    # Compress the test data
    test_data = {'key': 'value'}
    test_data_str = json.dumps(test_data)
    test_data_compressed = io.BytesIO()
    with gzip.GzipFile(fileobj=test_data_compressed, mode='w') as gzip_file:
        gzip_file.write(test_data_str.encode('utf-8'))

    # Mock the response of get_object
    mocked_s3.get_object.return_value = {'Body': io.BytesIO(test_data_compressed.getvalue())}

    s3_object = {'key': 'test-object'}
    data = process_data(s3_object, 'test-bucket')

    # Assert that get_object was called with the correct arguments
    mocked_s3.get_object.assert_called_once_with(Bucket='test-bucket', Key='test-object')

    # Assert that the returned data is correct
    assert data == test_data


def test_summarize_collection():
    with patch('gptscript.gptscript.GPTScript') as MockGPTScript:
        # Reload lambda_function module to apply the patch
        importlib.reload(sys.modules['lambda_function'])

        # Arrange
        instance = MockGPTScript.return_value
        instance.summarize.return_value = "Summary"
        collection = [{"key1": "value1"}, {"key2": "value2"}]

        # Act
        result = pygptscript_summarize_collection(collection)

        # Assert
        assert isinstance(result, str)
        instance.summarize.assert_called_once()