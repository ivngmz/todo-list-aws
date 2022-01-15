import os
import json
import boto3

from utils import decimalencoder
from utils.todoTableClass import todoTableClass


if os.environ["ENVIRONMENT"] == "LOCAL":
    dynamodb = None
else:
    dynamodb = boto3.resource("dynamodb")


def translate(event, context):
    mytable = todoTableClass(dynamodb)

    source_language = 'auto'  # AmazonComprehend autodetecta el lenguaje origen
    target_language = event['pathParameters']['lang']

    result = mytable.translate_todo(event['pathParameters']['id'],
                                    source_language,
                                    target_language)

    response = {
                "statusCode": 200,
                "body": json.dumps(result.get('TranslatedText'),
                                   cls=decimalencoder.DecimalEncoder)
            }

    return response