FROM python:3.11-slim-buster
WORKDIR /var/task
COPY . /var/task
COPY policies /var/task/policies
RUN apt-get update -y
COPY requirements.txt .
RUN pip install --upgrade pip==21.2.4
RUN pip install -r requirements.txt
CMD [ "lambda_function.lambda_handler" ]