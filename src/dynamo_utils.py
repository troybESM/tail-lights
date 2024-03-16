import os
import boto3
import datetime 
from aws_lambda_powertools import Logger
from boto3.dynamodb.conditions import Key

logger = Logger()
# Create ddb resource
ddb = boto3.resource('dynamodb')
table = ddb.Table(os.getenv("TABLE", "No Table"))

def get_ttl():
    # Get TTL
    now = datetime.datetime.now()
    td = datetime.timedelta(minutes=10)
    TTL = now + td
    return round(TTL.timestamp())

def write_name(name,request_id):
    # Update Count and keep the new value
    count_response = table.update_item(
        Key={
            'pk': 'APPSTATE',
            'sk': 'COUNT#ACCESSED'
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
    current_count = count_response['Attributes']['number']
    
    # Store new Item
    TTL = get_ttl()
    name_response = table.put_item(
        Item={
            'pk': f"REQ#{request_id}",
            'sk': f"USER#{name}",
            'number': current_count,
            'TTL': TTL
        }
    )
    logger.info(f"utils response {name_response}")
    return name_response

def decrease_count():
    count_response = table.update_item(
        Key={
            'pk': 'APPSTATE',
            'sk': 'COUNT#ACCESSED'
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
    response= table.query(
        KeyConditionExpression = Key('pk').eq(pk) & Key('sk').eq(sk)
    )
    return response['Items']

def scan_gsi(sk):
    response= table.scan(
        IndexName="number-name",
        Limit=200,
        FilterExpression = Key('sk').begins_with(sk)
    )
    return response['Items']

def query_gsi(query):
    response= table.query(
        IndexName="number-name",
        KeyConditionExpression = Key('number').eq(query)
    )
    return response['Items']