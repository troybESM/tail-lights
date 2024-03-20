import json
from aws_lambda_powertools import Logger
from src.dynamo_utils import query_gsi_pk_only

logger = Logger()


@logger.inject_lambda_context
def addEntry(event, context):
    logger.info(event)
    response = {"statusCode": 200, "body": json.dumps(event)}
    return response


@logger.inject_lambda_context
def get(event, context):
    shows = query_gsi_pk_only(pk='SHOW', gsi='GSI1')
    show_element_list = []
    for show in shows:
        show_element_list.append(f"""
            <item>
                <title>{show['GSI1DATA']['title']}</title>
                <description>{show['GSI1DATA']['description']}</description>
                <link>https://ua1l68fqx9.execute-api.us-east-2.amazonaws.com/dev-main/shows/{show['pk']}</link>
            </item>
        """)

    body = f"""
        <rss version="2.0">
        <channel>
        <title>Old Cars Only</title>
        <description>For all of your car show needs</description>
        <link>indyautoscene.tektrek.io</link>
        {''.join(show_element_list)}
        </channel>
        </rss>
"""
    response = {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/xml'
        },
         "body": body
        }
    return response
