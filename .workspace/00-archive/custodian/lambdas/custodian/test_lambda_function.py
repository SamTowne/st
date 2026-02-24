import unittest
from unittest import TestCase
import os
from unittest.mock import patch, MagicMock, call
import subprocess
import boto3
from botocore.stub import Stubber

from lambda_function import (
    lambda_handler,
    get_parameters_from_ssm,
    get_account_id,
    run_custodian,
)

# get_parameters_from_ssm
class TestGetParametersFromSsm(TestCase):
    @patch.dict(os.environ, {'BUCKET_NAME_PARAMETER_PATH': '/custodian/config/bucket_name',
                            'REGIONS_PARAMETER_PATH': '/custodian/config/regions'})  # Add other environment variables as needed
    @patch('boto3.client')
    def test_get_parameters_from_ssm(self, mock_client):
        # Arrange
        expected_bucket_name = 'my_bucket'
        expected_regions = 'us-west-2,us-east-1'
        mock_ssm = MagicMock()
        mock_ssm.get_parameter.side_effect = [
            {'Parameter': {'Value': expected_bucket_name}},
            {'Parameter': {'Value': expected_regions}}
        ]
        mock_client.return_value = mock_ssm

        # Act
        actual_bucket_name, actual_regions = get_parameters_from_ssm()

        # Assert
        self.assertEqual(expected_bucket_name, actual_bucket_name)
        self.assertEqual(expected_regions.split(','), actual_regions)

    @patch('boto3.client')
    def test_get_parameters_from_ssm_error(self, mock_client):
        # Arrange
        mock_ssm = MagicMock()
        mock_ssm.get_parameter.side_effect = Exception('An error occurred')
        mock_client.return_value = mock_ssm

        # Act / Assert
        with self.assertRaises(Exception):
            get_parameters_from_ssm()

# get_account_id
class TestGetAccountId(TestCase):
    @patch('boto3.client')
    def test_get_account_id(self, mock_client):
        # Arrange
        expected_account_id = '123456789012'
        mock_sts = MagicMock()
        mock_sts.get_caller_identity.return_value = {'Account': expected_account_id}
        mock_client.return_value = mock_sts

        # Act
        actual_account_id = get_account_id()

        # Assert
        self.assertEqual(expected_account_id, actual_account_id)

# run_custodian
class TestRunCustodian(unittest.TestCase):
    @patch('subprocess.Popen')
    @patch('glob.glob')
    def test_run_custodian(self, mock_glob, mock_popen):
        # Arrange
        mock_glob.return_value = ['/var/task/policies/rule_name/policy1.yml']
        mock_popen.return_value.wait.return_value = None
        mock_popen.return_value.stdout.read.return_value = 'output'
        region = 'us-west-2'
        output_path = 's3://my_bucket/custodian-run-logs/account=123456789012/region=us-west-2'
        rule_name = 'tag-compliance'

        # Act
        run_custodian(region, output_path, rule_name)

        # Assert
        mock_glob.assert_called_once_with('/var/task/policies/tag-compliance/*.yml')
        mock_popen.assert_has_calls([
            call('custodian run --cache-period=0 --region us-west-2 --output-dir=s3://my_bucket/custodian-run-logs/account=123456789012/region=us-west-2 /var/task/policies/rule_name/policy1.yml', shell=True, stdout=subprocess.PIPE),
            call().wait(),
            call().stdout.read(),
        ])

# lambda_handler
class TestLambdaHandler(unittest.TestCase):
    @patch.dict(os.environ, {'BUCKET_NAME_PARAMETER_PATH': '/custodian/config/bucket_name',
                             'REGIONS_PARAMETER_PATH': '/custodian/config/regions'})
    @patch('boto3.client')
    # Mock the SSM client
    def test_lambda_handler(self, mock_boto3_client):
        mock_ssm = MagicMock()
        mock_ssm.get_parameter.side_effect = [
            {'Parameter': {'Value': 'my_bucket'}},
            {'Parameter': {'Value': 'us-west-2,us-east-1'}}
        ]
        mock_sts = MagicMock()
        mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
        mock_boto3_client.side_effect = [mock_ssm, mock_sts]
        output = lambda_handler({'rule_name': 'tag-compliance'}, {})
        self.assertIsNotNone(output)
        mock_ssm.get_parameter.assert_any_call(Name='/custodian/config/bucket_name')
        mock_ssm.get_parameter.assert_any_call(Name='/custodian/config/regions')
        mock_sts.get_caller_identity.assert_called_once()

if __name__ == '__main__':
    unittest.main()
