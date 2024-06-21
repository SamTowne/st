resource "aws_lambda_function" "lambda" {
  function_name = "custodian-execution-lambda"
  role          = aws_iam_role.lambda_role.arn

  image_uri    = "${aws_ecr_repository.repository.repository_url}:latest"
  package_type = "Image"

  timeout     = 120
  memory_size = 350
  architectures = ["arm64"]
  environment {
    variables = {
      ENV = "prod"
      REGIONS_PARAMETER_PATH = aws_ssm_parameter.regions_parameter.name
      BUCKET_NAME_PARAMETER_PATH = aws_ssm_parameter.bucket_name_parameter.name
    }
  }
}

resource "aws_lambda_function" "data-processing" {
  function_name = "custodian-data-processing-lambda"
  role          = aws_iam_role.lambda_role.arn

  image_uri    = "${aws_ecr_repository.data_processing_repository.repository_url}:latest"
  package_type = "Image"

  timeout     = 60
  memory_size = 128
  architectures = ["arm64"]
}

resource "aws_cloudwatch_log_group" "custodian-exec" {
  name = "/aws/lambda/custodian-execution-lambda"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "data-proc" {
  name = "/aws/lambda/custodian-data-processing-lambda"
  retention_in_days = 30
}