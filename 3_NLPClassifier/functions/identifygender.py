import os
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.client('dynamodb')
sagemaker = boto3.client('sagemaker-runtime')
def handler(event, context):
    print('Received event: ' + json.dumps(event, indent=2))
    ids = event['ID'].split(',')
    table_name=os.environ['table_name']
    sagemaker_endpoint=os.environ['sagemaker_endpoint']
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
            if 'FirstName' in items[0]:
                firstName = items[0]['FirstName']['S']
                response = sagemaker.invoke_endpoint(
                        EndpointName=sagemaker_endpoint,
                        Body=firstName,
                        ContentType='text/csv'
                    )
                response = json.loads(response['Body'].read().decode('utf-8'))
                print(response)
                gender = response[firstName]
                response = dynamodb.update_item(
                    ExpressionAttributeNames={'#GD': 'Gender'},
                    ExpressionAttributeValues={':gd' : {'S': gender}},
                    Key={'ID': {'S': id}, 'PostedTime': {'S': postedtime}},
                    ReturnValues='ALL_NEW',
                    TableName=table_name,
                    UpdateExpression='SET #GD = :gd'
                )
                responses.append('{} - {}'.format(response['Attributes']['FirstName']['S'], response['Attributes']['Gender']['S']))
        except Exception as e:
            print('Actual error is: {0}'.format(e))
    return responses
