import json
import logging

import base64


def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel("INFO")

    body = event['body']
    logger.info(body)
    decoded_bytes = base64.b64decode(body)

    decoded_string = decoded_bytes.decode()
    logger.info(decoded_string)
    data = json.loads(decoded_string)
    validation_code = data[0]['data']['validationCode']

    response = {"statusCode": 200,
                "body": json.dumps({"validationResponse": validation_code})
                }

    return response
