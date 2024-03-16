import os
import json
import boto3
from aws_lambda_powertools import Logger

logger = Logger()
# Create S3 client
sns = boto3.client('sns')

@logger.inject_lambda_context
def write_topic(event, context):
    # Get topic from env var
    topic_arn = os.getenv('TOPIC', 'No topic found')
    # Generate message
    message = {
        'buy_it': 'use_it',
        'break_it': 'fix_it',
        'trash_it': 'change_it',
        'mail': 'upgrade_it'
    }
    response = sns.publish(
        TargetArn=topic_arn,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure = 'json'
    )
    logger.info(f"response: {response}")

@logger.inject_lambda_context
def process_topic(event,context):
    logger.info(f"event {event}")
    for record in event['Records']:
        logger.info(record)
        # Some Processing goes here