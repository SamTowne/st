FROM public.ecr.aws/lambda/python:3.8
WORKDIR /var/task
COPY . .
RUN pip install -r requirements.txt
CMD [ "lambda_handler.lambda_handler" ]