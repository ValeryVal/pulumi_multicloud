import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(f"this is event: {event}")

    return {
        "statusCode": 200,
        "body": "Lambda is triggered!!"
    }