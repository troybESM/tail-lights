import json
from aws_lambda_powertools import Logger
from src.dynamo_utils import add_show
from collections import Counter

logger = Logger()


@logger.inject_lambda_context
def get_all(event, context):
    name = 'Stranger'
    body = {
        "message": f"Hi {name}! Python Lambdas are fun and easy."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


# @logger.inject_lambda_context
# def get(event, context):
#     name = event.get('pathParameters', {}).get('name')
#     response = write_name(name=name, request_id=context.aws_request_id)
#     logger.info(f"response is {response}")
#     body = {
#         "message": f"Hi {name}! Your name has been logged to dynamo."
#     }

#     response = {"statusCode": 200, "body": json.dumps(body)}
#     return response


@logger.inject_lambda_context
def add(event, context):
    logger.info(f"add function event is {event}")
    logger.info(f"add function context is {context}")

    show = event.get('pathParameters', {}).get('show')
    logger.info(f"show is: {show}")
    response = add_show(show, request_id=context.aws_request_id)
    logger.info(f"response is {response}")
    body = {
        "message": f"Added show! "
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
