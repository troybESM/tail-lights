import os
import boto3
import datetime
from aws_lambda_powertools import Logger
from boto3.dynamodb.conditions import Key

logger = Logger()
# Create ddb resource
ddb = boto3.resource('dynamodb')
table = ddb.Table(os.getenv("TABLE", "No Table"))


def get_ttl(date):
    # Get TTL
    now = datetime.datetime.now()
    td = datetime.timedelta(days=10)
    TTL = now + td
    return round(TTL.timestamp())


def add_show(show, request_id):
    # Update Count and keep the new value
    count_response = table.update_item(
        Key={
            'pk': 'SHOW#META',
            'sk': 'SHOW#ACCESSED'
        },
        UpdateExpression='ADD #s :val',
        ExpressionAttributeNames={
            "#s": 'number'
        },
        ExpressionAttributeValues={
            ':val': 1
        },
        ReturnValues="UPDATED_NEW"
    )
    
    # Store new Item
    description = ""
    TTL = get_ttl(date="<Show Date>")
    response = table.put_item(
        Item={
            'pk': f'SHOW#{count_response["Attributes"]["number"]}',
            'sk': f'SHOW#{show["date"]}',
            'approved': False,
            'active': True,
            'title': '',
            'GSI1PK': 'SHOW',
            'GSI1SK': f'SHOW#{request_id}',
            'GSI1DATA': {
                'description': show['description'][0:100],
                'title': '',
                'date': show['date'],
                'time': '',
                'location': show['location'],
            },
            **show
            # 'date': '',
            # 'location': {
            #     'address': '',
            #     'city': '',
            #     'state': '',
            #     'zip': ''
            # },
            # 'description': description,
            # 'eventTimes': {
            #     'reg': '',
            #     'awards': ''
            # },
            # 'contact': {
            #     'name': '',
            #     'email': '',
            #     'addr': '',
            #     'site': ''
            # },
            # 'socialLinks': {
            #     'fb': '',
            #     'x': '',
            #     'insta': '',
            #     'mast': ''
            # },
            # 'sponsors': [
            #     {
            #         'name': '',
            #         'links': ''
            #     }
            # ]
            # 'TTL': TTL
        }
    )
    logger.info(f"Added Item: {response}")
    return response


def query_gsi_pk_only(pk, gsi):
    response = table.query(
        IndexName=gsi,
        KeyConditionExpression=Key('GSI1PK').eq(pk)
    )
    return response['Items']


def scan_gsi(sk):
    response = table.scan(
        IndexName="GSI1",
        Limit=200,
        FilterExpression=Key('pk').eq
    )
    return response['Items']

def decrease_count():
    count_response = table.update_item(
        Key={
            'pk': 'SHOW#META',
            'sk': 'SHOW#ACCESSED'
        },
        UpdateExpression='ADD #s :val',
        ExpressionAttributeNames={
            "#s": 'number'
        },
        ExpressionAttributeValues={
            ':val': -1
        },
        ReturnValues="UPDATED_NEW"
    )
    current_count = count_response['Attributes']['number']
    return current_count


def add_winning_number(number):
    response = table.update_item(
        Key={
            'pk': 'APPSTATE',
            'sk': 'COUNT#WINNER'
        },
        UpdateExpression='Set #s = :val',
        ExpressionAttributeNames={
            "#s": 'number'
        },
        ExpressionAttributeValues={
            ':val': number
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


def query_table(pk, sk):
    response = table.query(
        KeyConditionExpression=Key('pk').eq(pk) & Key('sk').eq(sk)
    )
    return response['Items']


