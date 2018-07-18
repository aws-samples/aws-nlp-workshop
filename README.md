# Serverless NLP Workshop

In this workshop you will explore the AWS services needed to enhance your a voice-of-the-customer application with Natural Langage Processing techniques.  The application architecture uses [Amazon Comprehend](https://aws.amazon.com/comprehend/), [Amazon SageMaker](https://aws.amazon.com/sagemaker/), [AWS Lambda](https://aws.amazon.com/lambda/), [Amazon API Gateway](https://aws.amazon.com/api-gateway/), [Amazon S3](https://aws.amazon.com/s3/), [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) and [Amazon ECR](https://aws.amazon.com/ecr/). 
  
Amazon Comprehend provides Natural Language Processing service needed to predict the sentiment from the feedback entered by users. Amazon SageMaker is used to orchestrate the machine learning process needed to predict gender of the user from name. S3 hosts static web resources including HTML, CSS, JavaScript, and image files which are loaded in the user's browser. JavaScript executed in the browser sends and receives data from a public backend API built using Lambda and API Gateway. DynamoDB provides a  persistence layer where data can be stored by the API's Lambda function. ECR is used to host the machine learning training code. Finally, Python binding for Keras - machine learning framework is used to create the model needed for gender prediction.

## Prerequisites

### AWS Account

In order to complete this workshop you'll need an AWS Account with access to create AWS IAM, S3, DynamoDB, Lambda, API Gateway, Comprehend, and Sagemaker. The code and instructions in this workshop assume only one student is using a given AWS account at a time. If you try sharing an account with another student, you'll run into naming conflicts for certain resources. You can work around these by appending a unique suffix to the resources that fail to create due to conflicts, but the instructions do not provide details on the changes required to make this work.

All of the resources you will launch as part of this workshop are eligible for the AWS free tier if your account is less than 12 months old. See the [AWS Free Tier page](https://aws.amazon.com/free/) for more details.

### Browser

We recommend you use the latest version of Chrome to complete this workshop.

## Modules

This workshop is broken up into multiple modules. You must complete each module before proceeding to the next. The first module has a slidedeck to understand the context, then second module explores the use of Amazon Comprehend, the next model helps you build a TensorFlow Model in Sagemaker, and in the last module we build the complete voice-of-the-customer application using a CloudFormation template. 

1. [NLP workshop Slides](Presentation-AWS-NLP-workshop.pptx) - 15 mins
2. [Using Amazon Comprehend to add sentiment analysis](2_SentimentAnalysis) - 30 mins
3. [Create your own NLP classifier](3_NLPClassifier) - 60 mins
4. [Create a summarizer](Coming soon)
5. [Creating a VOC application framework](5_VocFramework) - 15 mins

## Cleanup
After you have completed the workshop you can delete all of the resources that were created in the following order.
1. Delete Cloudformation stack created in Step #4
2. Delete the Sagemaker deployment instance
3. Delete the Sagemaker notebook instance
