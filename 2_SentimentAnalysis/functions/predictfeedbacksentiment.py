import os
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.client('dynamodb')
comprehend = boto3.client('comprehend')
def handler(event, context):
    print('Received event: ' + json.dumps(event, indent=2))
    ids = event['ID'].split(',')
    table_name=os.environ['table_name']
    responses = []
    for id in ids:
        try:
            response = dynamodb.scan(
                ExpressionAttributeNames={'#ID': 'ID'},
                ExpressionAttributeValues={':id' : {'S': id}},
                FilterExpression='#ID = :id',
                TableName=table_name
            )
            items = response['Items']
            postedtime = items[0]['PostedTime']['S']
            if 'Feedback' in items[0]:
                feedback = items[0]['Feedback']['S']
                response = comprehend.detect_sentiment(Text=feedback, LanguageCode='en')
                sentiment = response['Sentiment']
                print(sentiment)
                response = dynamodb.update_item(
                    ExpressionAttributeNames={'#ST': 'Sentiment'},
                    ExpressionAttributeValues={':st' : {'S': sentiment}},
                    Key={'ID': {'S': id}, 'PostedTime': {'S': postedtime}},
                    ReturnValues='ALL_NEW',
                    TableName=table_name,
                    UpdateExpression='SET #ST = :st'
                )
                responses.append('{} - {}'.format(response['Attributes']['ID']['S'], response['Attributes']['Sentiment']['S']))
        except Exception as e:
            print('Actual error is: {0}'.format(e))
    return responses