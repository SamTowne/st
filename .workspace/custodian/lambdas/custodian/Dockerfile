FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY policies ./policies
copy lambda_handler.py ./

CMD ["lambda_function.lambda_handler"]