import json
from aws_lambda_powertools import Logger
from src.dynamo_utils import add_show, query_gsi_pk_only, query_table
from collections import Counter

logger = Logger()


@logger.inject_lambda_context
def get_all(event, context):
    shows = query_gsi_pk_only(pk='SHOW', gsi='GSI1')
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': "true",
        },
    response = {"statusCode": 200,"headers": headers, "body": json.dumps(shows)}

    return response

@logger.inject_lambda_context
def get(event, context):
    show_id = event.get('pathParameters', {}).get('show_id')
    logger.info(f"show_id = {show_id}")
    show = query_table(pk=show_id)
    logger.info(f"show = {show}")
    headers = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Credentials': "true",
    },
    response = {"statusCode": 200,"headers": headers, "body": json.dumps(show)}

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
    # Parse Body
    logger.info(f"add function event is {event}")
    body = json.loads(event.get('body'))
    logger.info(f"body is: {body}")
    
    # Get Show Object

    # Add Show
    response = add_show(body, request_id=context.aws_request_id)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        logger.info(f"response is {response}")
        resp_body = {
            "message": f"Added show {response['added_item']}"
        }
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': "true",
        },
        response = {"statusCode": 200,"headers": headers, "body": json.dumps(resp_body)}
    else:
        response = {"statusCode": 451, "body": "Request Accepted, Failed adding show"}

    return response
