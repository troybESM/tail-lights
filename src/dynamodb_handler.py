import os
import boto3
from aws_lambda_powertools import Logger
from src.dynamo_utils import write_name,decrease_count

logger = Logger()
# Create ddb resource
ddb = boto3.resource('dynamodb')

table = ddb.Table(os.getenv("TABLE", "No Table"))


@logger.inject_lambda_context
def write_item(event, context): 
    # Write new Item to table
    response = write_name(name='TB',request_id=context.aws_request_id)
    return response

@logger.inject_lambda_context
def process_stream(event,context):
    logger.info(event)

@logger.inject_lambda_context
def process_ttl_stream(event,context):
    for record in event['Records']:
        logger.info(f"Record: {record}")
        # Only decrement counter if a user record delete triggered.
        if record['dynamodb']['OldImage']['sk']['S'].startswith("USER#"):
            logger.info(f"Removing this record: {record['dynamodb']['OldImage']}")
            new_count = decrease_count()
            logger.info(f"new count is: {new_count}")
