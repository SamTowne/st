# Custodian

## Data Collection
- Configure Cloud Custodian with your policies
- Set up Cloud Custodian to run on a schedule using CloudWatch Events
- Configure Cloud Custodian to store output in an S3 bucket

## Data Processing
- Write a Lambda function that gets triggered on S3 bucket events
- In the function, fetch the new data from S3 and process it
- Insert the processed data into DocumentDB

## Data API
- Write a Lambda function that fetches data from DocumentDB based on API requests
- Set up API Gateway to trigger the Lambda function and return the data

## Frontend
- Build a static website with HTML/CSS/JavaScript
- Use JavaScript to fetch data from your API and display it on the website
- Host the website on S3 and configure it for static website hosting