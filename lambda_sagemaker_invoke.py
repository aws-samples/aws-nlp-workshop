from __future__ import print_function

import json
import urllib
import boto3

print('Loading function')

sm = boto3.client('sagemaker-runtime')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    try:
        response = sm.invoke_endpoint(
            EndpointName='tensorboard-names-2018-03-20-22-40-47-154',
            Body='{"name":"Pratap"}',
            ContentType='application/json',
            Accept='*/*')
        body = response['Body']
        json_str = body.read()
        json_data = json.loads(json_str)
        outputs = json_data['outputs']
        gender = outputs['Gender']
        #prediction = float(str(gender['floatVal']))
        print("Prediction: (Male if Less that .5 and Female if > 0.5 ) with confidence" + str(gender['floatVal']))

        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error')
        raise e
