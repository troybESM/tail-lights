import os
import boto3
from aws_lambda_powertools import Logger

logger = Logger()
# Create SQS client
sqs = boto3.client('sqs')

def write_queue(event, context):
    queue_url = os.getenv('SQS_QUEUE_URL', "No Queue URL")
    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'The Whistler'
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'John Grisham'
            },
            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': '6'
            }
        },
        MessageBody=(
            'Information about current NY Times fiction bestseller for '
            'week of 12/11/2016.'
        )
    )

    logger.info(response['MessageId'])
def process_queue(event,context):
    for record in event['Records']:
        payload = record["body"]
        logger.info(f"payload is: {payload}")