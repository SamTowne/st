from unittest import TestCase, mock
import subprocess
from lambda_function import run_custodian

class TestRunCustodian(TestCase):
    @mock.patch('subprocess.run')
    def test_run_custodian_success(self, mock_run):
        # Arrange
        mock_run.return_value = subprocess.CompletedProcess(args=["custodian", "run", "-s", "s3://custodian-bucket-benjals-272773485930/custodian-output", "/lambda/task/root/policies/*.yml"], returncode=0)
        lamda_task_root = "/lambda/task/root"

        # Act
        run_custodian(lamda_task_root)

        # Assert
        mock_run.assert_called_once_with(
            ["custodian", "run", "-s", "s3://custodian-bucket-benjals-272773485930/custodian-output", "/lambda/task/root/policies/*.yml"], 
            check=True, text=True, stderr=subprocess.STDOUT
        )

    @mock.patch('subprocess.run')
    def test_run_custodian_failure(self, mock_run):
        # Arrange
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, 
            cmd=["custodian", "run", "-s", "s3://custodian-bucket-benjals-272773485930/custodian-output", "/lambda/task/root/policies/*.yml"],
            output='Error running Cloud Custodian'
        )
        lamda_task_root = "/lambda/task/root"

        # Act
        try:
            run_custodian(lamda_task_root)
        except subprocess.CalledProcessError:
            pass

        # Assert
        mock_run.assert_called_once_with(
            ["custodian", "run", "-s", "s3://custodian-bucket-benjals-272773485930/custodian-output", "/lambda/task/root/policies/*.yml"], 
            check=True, text=True, stderr=subprocess.STDOUT
        )