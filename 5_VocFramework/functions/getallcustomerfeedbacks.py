import os
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb')
def lambda_handler(event, context):
    print('Received event: ' + json.dumps(event, indent=2))
    table_name=os.environ['table_name']
    table = dynamodb.Table(table_name)
    try:
        response = table.scan(
            FilterExpression=Attr('Feedback').exists(),
            ProjectionExpression = 'ID,FirstName,LastName,Feedback,PostedTime,Sentiment,Gender'
        )
        items = response['Items']    
        return items
    except Exception as e:
        print('Actual error is: {0}'.format(e))
        return e