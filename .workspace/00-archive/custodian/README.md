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

## Development Setup

This project uses Python 3.12. To ensure that you're using the correct version of Python and to isolate your environment, we recommend using `pyenv` and `virtualenv`.

### Installing pyenv and virtualenv

If you haven't installed `pyenv` and `virtualenv` yet, you can do so by following the instructions on their respective GitHub pages:

- [pyenv](https://github.com/pyenv/pyenv)
- [virtualenv](https://virtualenv.pypa.io/en/latest/)

### Setting up the Python version

Once you have `pyenv` installed, you can install the required Python version and set it for the current directory:

```bash
pyenv install 3.12.3
pyenv local 3.12.3
virtualenv venv
source venv/bin/activate
```
