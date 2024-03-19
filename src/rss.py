import json
from aws_lambda_powertools import Logger
logger = Logger()


@logger.inject_lambda_context
def addEntry(event, context):
    logger.info(event)
    response = {"statusCode": 200, "body": json.dumps(event)}
    return response


@logger.inject_lambda_context
def get(event, context):
    body = '''
        <?xml version="1.0" encoding="utf-8"?>
        <rss version="2.0">
        <channel>
        <title>Sample Feed</title>
        <description>For documentation &lt;em&gt;only&lt;/em&gt;</description>
        <link>http://example.org/</link>
        <pubDate>Sat, 07 Sep 2002 00:00:01 GMT</pubDate>
        <!-- other elements omitted from this example -->
        <item>
        <title>First entry title</title>
        <link>http://example.org/entry/3</link>
        <description>Watch out for &lt;span style="background-image:
        url(javascript:window.location='http://example.org/')"&gt;nasty
        tricks&lt;/span&gt;</description>
        <pubDate>Thu, 05 Sep 2002 00:00:01 GMT</pubDate>
        <guid>http://example.org/entry/3</guid>
        <!-- other elements omitted from this example -->
        </item>
        </channel>
        </rss>
'''
    response = {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/xml'
        },
         "body": body
        }
    return response
