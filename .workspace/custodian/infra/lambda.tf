resource "aws_lambda_function" "lambda" {
  function_name = "custodian-lambda-function"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # filename = "${base64sha256(file("path_to_your_zip_file"))}"
  filename      = "path_to_your_zip_file"
  source_code_hash = filebase64sha256("path_to_your_zip_file")
  runtime       = "python3.8"
}