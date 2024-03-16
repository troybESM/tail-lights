""""
A lambda custom authorizer for API KEY tokens.
A very basic implementation that checks a hardcoded api key.
This could easily be a call to duo, okta, cognito, etc
"""
from aws_lambda_powertools import Logger

logger = Logger()

ACCESS_TOKEN = "123abc"


def generate_policy(effect, resource):
    # The auth lambda needs to return this AWS policy document to API Gateway
    
    principalId = "userid|placeholder"  # this would be obtained from db lookup of the api key
    policyDocument = {
        "Version": "2012-10-17",
        "Statement": [
            {"Action": "execute-api:Invoke", "Effect": effect, "Resource": resource}
        ],
    }
    authResponse = {"principalId": principalId, "policyDocument": policyDocument}
    return authResponse

@logger.inject_lambda_context
def handler(event, context):
    logger.info(f"event {event}")
    #  Handler of the custom auth lambda. This will receive an event from API Gateway in the form:
    #   {'type': 'TOKEN', 'routeArn': 'arn:aws:execute-api:...', 'authorizationToken': 'Bearer 123abc'}
    
    # Check if token is a valid api key
    # This sections is where you can do your JWT stuff, or integrate with a source
    try:
        token = event["authorizationToken"].split()[1]
    except:
        return generate_policy('Deny', event["methodArn"])
    if token == ACCESS_TOKEN:
        return generate_policy('Allow', event["methodArn"])

    return generate_policy('Deny', event["methodArn"])