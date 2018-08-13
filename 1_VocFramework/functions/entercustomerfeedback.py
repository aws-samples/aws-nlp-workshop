import os
import json
import uuid
import boto3
from datetime import datetime
dynamodb = boto3.client('dynamodb')
def lambda_handler(event, context):
    print('Received event: ' + json.dumps(event, indent=2))
    table_name=os.environ['table_name']
    firstname = event['FirstName']
    lastname = event['LastName']
    feedback = ''
    if 'Feedback' in event:
        feedback = event['Feedback']
    data_event_isactive = 'no'
    try:
        if feedback == '':
            response = dynamodb.update_item(
                TableName=table_name,
                Key={
                    'ID':{'S':str(uuid.uuid4())},
                    'PostedTime':{'S':datetime.now().isoformat()}
                },
                AttributeUpdates={
                    'FirstName':{'Value': {'S':firstname}},
                    'LastName':{'Value': {'S':lastname}}
                }
            )
        else:
            response = dynamodb.update_item(
                TableName=table_name,
                Key={
                    'ID':{'S':str(uuid.uuid4())},
                    'PostedTime':{'S':datetime.now().isoformat()}
                },
                AttributeUpdates={
                    'FirstName':{'Value': {'S':firstname}},
                    'LastName':{'Value': {'S':lastname}},
                    'Feedback':{'Value': {'S':feedback}}
                }
            )
        print(response)
        return response['ResponseMetadata']['HTTPStatusCode']
    except Exception as e:
        print('Actual error is: {0}'.format(e))
        return e