FROM python:3.11-slim-buster
WORKDIR /var/task
ADD . /var/task
ADD policies /var/task/policies
RUN apt-get update -y
RUN apt-get install -y groff-base
RUN pip install --upgrade pip==21.2.4
RUN pip install boto3==1.18.20
#RUN pip install aws-lambda-ric
RUN pip install -v c7n==0.9.36
CMD [ "lambda_function.lambda_handler" ]