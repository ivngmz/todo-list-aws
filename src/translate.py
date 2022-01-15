import boto3
import json

translate_client = boto3.client('translate')

def lambda_handler(event,context):
    review_text = event['text']
    translate_response = translate_client.translate_text(
            Text=review_text,
            SourceLanguageCode='auto',
            TargetLanguageCode='en'
    )
    response = {
            "statusCode": 200,
            "body": json.dumps(translate_response)
    }
    return response
