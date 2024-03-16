import os
import json
import boto3
from aws_lambda_powertools import Logger
# import pyodbc
# import mysql.connector
# import psycopg2
# from pymongo import MongoClient

logger = Logger()
# Create db client
db_url = os.getenv("DB_URL","No URL found")
# You can add the connection to db here. If it is defined outside of the lambda the connection will be re-used for as long as the instance is alive. 
# Some DBs don't like this though so this may need to be moved inside of the handler.

# Sql Server. This information would be stored in a secret, shown here for clarity
# ss_conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};Server={db_url};Database=mydatabase;Port=myport;User ID=myuserid;Password=mypassword') 

# MySQL. This information would be stored in a secret, shown here for clarity
# mysql_conn = mysql.connector.connect(host=db_url, user='myuserid', password='mypassword', database='mydatabase')

# postgres. This information would be stored in a secret, shown here for clarity
# pg_conn = psycopg2.connect(f'host={db_url} dbname=mydatabase user=myuserid password=mypassword')

# mongodb  This information would be stored in a secret, shown here for clarity
# mongo_conn = MongoClient(db_url, 27017, username='myuserid', password='mypassword')
# mongo_db = mongo_conn[mydatabase]

@logger.inject_lambda_context
def process(event,context):
    logger.info(f"event {event}")
    # Some Processing goes here