import json
from aws_lambda_powertools import Logger
from src.dynamo_utils import write_name, query_gsi, add_winning_number, query_table, scan_gsi
from collections import Counter

logger = Logger()


@logger.inject_lambda_context
def hello(event, context):
    name = 'Stranger'
    body = {
        "message": f"Hi {name}! Python Lambdas are fun and easy."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


@logger.inject_lambda_context
def hello_name(event, context):
    name = event.get('pathParameters', {}).get('name')
    response = write_name(name=name, request_id=context.aws_request_id)
    logger.info(f"response is {response}")
    body = {
        "message": f"Hi {name}! Your name has been logged to dynamo."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}    
    return response


@logger.inject_lambda_context
def add_winner(event, context):
    #TODO get number from event
    number = int(event.get('pathParameters', {}).get('number'))
    logger.info(f"number is: {number}")
    response = add_winning_number(number)
    logger.info(f"response is {response}")
    body = {
        "message": f"Added the winning number of {number}"
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


@logger.inject_lambda_context
def get_winner(event, context):
    # Query for winning number and extract it from response
    number_response = query_table(pk='APPSTATE',sk='COUNT#WINNER')
    if len(number_response) > 0:
        # Get Number from first response There should only be one. 
        number = number_response[0]['number']
        logger.info(f"Number is : {number}")

        # Query for users that have the winning number
        win_result = query_gsi(number)
        logger.info(f"win_result {win_result}")
        # Filter for the user with winning number
        winner_item = [res for res in win_result if res['sk'].startswith('USER#')]
    else:
        return build_html_page(content="No winning number selected")
    
    if len(winner_item) > 0:
        # split off  USER# that we store in dynamo to make user name pretty.
        _,winner = winner_item[0]['sk'].split('#')
        logger.info(f"winner is {winner}")
        page = build_html_page(content=f"Winner is:{winner}")
    else:
        page = build_html_page(content="No winner yet")

    return page

@logger.inject_lambda_context
def show_entrants(event, context):
    # Scan for all users. Scans are generally to be avoided they are expensive because they hit all partitions even if you filter
    users = scan_gsi(sk='USER#') 
    logger.info(f"users are {users}")
    
    #
    if len(users) > 0:
        # split off  USER# that we store in dynamo to make user name pretty.
        user_names = [f"<li>{user['sk'].split('#')[1]}</li>" for user in users]
        
        logger.info(f"user_names are {user_names}")
    
        page = build_html_page(content=f"Entrants are: <ul>{''.join(user_names)}<ul>")
        
    else:
        page = build_html_page(content="No entries yet")
    return page

@logger.inject_lambda_context
def show_unique_entrants(event, context):
    # Scan for all users. Scans are generally to be avoided they are expensive because they hit all partitions even if you filter
    users = scan_gsi(sk='USER#') 
    logger.info(f"users are {users}")
    
    if len(users) > 0:
        # split off  USER# that we store in dynamo to make user name pretty.
        # sk = {user['sk'] for user in users}
        # logger.info(f"sk: {sk}")
        # user_and_count = {user['sk'] for item in sk}
        # logger.info(f"UaC: {user_and_count}")
        # for item in sk:
            
        
        user_names = [user['sk'].split('#')[1] for user in users]
        logger.info(f"user_names_li are {user_names}")
        
        counter = Counter(user_names).most_common(10)
        logger.info(f"Counter is: {counter}")
        counter_content = [f"<li>{item[0]}: {item[1]}</li>" for item in counter]
        page = build_html_page(content=f"Entrants are: <ul>{''.join(counter_content)}<ul>")
    
        # page = build_html_page(content=counter)
        
    else:
        page = build_html_page(content="No entries yet")
    return page

def build_html_page(content):
    # This is dumb. You shouldn't have a lambda serving your front end. This is cheaper/faster/better in S3 + Cloudfront.
    body = f"""<html>
                <style> 

                    body {{
                        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
                        background-size: 400% 400%;
                        animation: gradient 30s ease infinite;
                        height: 100vh;
                    }}

                    @keyframes gradient {{
                        0% {{
                            background-position: 0% 50%;
                        }}
                    
                        50% {{
                            background-position: 100% 50%;
                        }}
                    
                        100% {{
                            background-position: 0% 50%;
                        }}
                    }}
                    h1 {{
                        font-size: 75 
                    }}
                    li:hover {{
                        font-size: 125%
                    }}
                    div {{
                        display: flex;
                        flex-direction: row;
                        top: 25%;
                        align-items: center;
                        justify-content: center;
                        position: relative;
                    }}
                </style>
                <body>
                    <div>
                        <h1>{content}</h1>
                    </div>
                </body>
            </html>
    """
    response = {
        "statusCode": 200,
        "body": body,
        "headers": {
            'Content-Type': 'text/html',
        }
    }
    return response