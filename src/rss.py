import json
from aws_lambda_powertools import Logger
logger = Logger()


@logger.inject_lambda_context
def addEntry(event, context):
    logger.info(event)
    response = {"statusCode": 200, "body": json.dumps(event)}
    return response
