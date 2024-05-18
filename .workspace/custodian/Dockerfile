FROM python:3.11-slim-buster
WORKDIR /var/task
ADD . /var/task
RUN apt-get update && \
    apt-get install -y groff-base && \
    pip install --upgrade pip==21.2.4 && \
    pip install awscli==1.20.47 aws-lambda-ric
RUN pip install c7n==0.9.14
CMD [ "lambda_function.lambda_handler" ]