resource "aws_lambda_function" "lambda" {
  function_name = "custodian-execution-lambda"
  role          = aws_iam_role.lambda_role.arn

  image_uri    = "${aws_ecr_repository.repository.repository_url}:latest"
  package_type = "Image"

  timeout     = 60
  memory_size = 350
}

resource "aws_lambda_function" "data-processing" {
  function_name = "custodian-data-processing-lambda"
  role          = aws_iam_role.lambda_role.arn

  image_uri    = "${aws_ecr_repository.data_processing_repository.repository_url}:latest"
  package_type = "Image"

  timeout     = 60
  memory_size = 128
}