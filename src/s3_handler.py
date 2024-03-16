import os
import boto3
from aws_lambda_powertools import Logger

logger = Logger()
# Create S3 client
s3 = boto3.client('s3')

@logger.inject_lambda_context
def write_file(event, context):
    bucket = os.getenv('BUCKET', "No bucket")
    key_prefix = os.getenv("KEY_PREFIX", "No prefix found")
    key = f"{key_prefix}{context.aws_request_id}.txt"
    logger.info(f"Key is {key}")
    body = b'All your base.'
    s3.put_object(Body=body, Bucket = bucket, Key=key)
    
@logger.inject_lambda_context
def process_event(event,context):
    logger.info(f"event is {event}")
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        response = s3.get_object(Bucket=bucket, Key=key)
        data = response['Body'].read().decode('utf-8')
        logger.info(f"contents of file: {data}")
        # Some Processing goes here