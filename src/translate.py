import logging
import boto3
import json
import todoList

global translate_client
translate_client = boto3.client('translate')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(event)
    global data
    data = json.loads(event['body'])
    logger.info(data)
    global translate_response
    translate_response = ""
    global response
    
    try:
        review_text = data['text']
        translate_response = translate_client.translate_text(
            Text=review_text,
            SourceLanguageCode='auto',
            TargetLanguageCode='en'
            )
        logger.error(translate_response)
    except KeyError as exc:
        response = {
            "statusCode": 417,
            "body": json.dumps("Error: Key error")
        }

    if (translate_response):
        response = {
            "statusCode": 200,
            "body": json.dumps(translate_response)
        }
    elif (response != None):
        print ("we have a problem")
    else:
        response = {
            "statusCode": 400,
            "body": json.dumps("Error: Request has not valid JSON")
        }
    return response
