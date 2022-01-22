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
    global translate_response
    translate_response = ""
    global response

    try:
        review_id = event['pathParameters']['id']
        review_language = event['pathParameters']['language']
        item_response = json.loads(json.dumps(todoList.get_item(review_id)))
        print(item_response)
        review_text = item_response["text"]
        logger.info(review_text)
        translate_response = translate_client.translate_text(
            Text=review_text,
            SourceLanguageCode='auto',
            TargetLanguageCode=review_language
            )
    except KeyError as exc:
        response = {
            "statusCode": 417,
            "body": json.dumps("Error: Key error" + str(exc))
        }
        logger.error(translate_response)

    if (translate_response):
        response = {
            "statusCode": 200,
            "body": json.dumps(translate_response)
        }
        logger.info(response)
    elif response is not None:
        print("we have a problem")
    else:
        response = {
            "statusCode": 400,
            "body": json.dumps("Error: Request has not valid JSON")
        }
    return response
