import boto3
import json
import logging

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def upload_feedback_to_s3(s3_props):
    try:
        s3_client = boto3.client('s3')
        s3_client.put_object(
            Bucket=s3_props['Bucket'],
            Key=s3_props['Key'],
            Body=s3_props['Body'],
            ContentType='application/json'
        )
        logger.info("Feedback data uploaded to S3 successfully")
    except Exception as e:
        logger.error(f"Error uploading feedback data to S3: {str(e)}")
        raise

def lambda_handler(event, context):
    try:
        logger.info("Received event: %s", json.dumps(event))

        # Extract S3 properties from the event
        json_data = json.loads(event['body'])['s3Props']

        if json_data:
            upload_feedback_to_s3(json_data)

        return {
            'statusCode': 200,
            'body': json.dumps('Feedback dumped in S3')
        }
    except Exception as e:
        # Handle unexpected exceptions and raise a runtime error
        error_message = f"Unhandled error: {str(e)}"
        logger.error(error_message)
        raise RuntimeError(error_message)
