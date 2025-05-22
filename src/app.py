import json
import boto3
from boto3 import resource

def lambda_handler(event, context):
    query_params = event['queryStringParameters'] or {}
    event_type = query_params.get('event_type')
    response = ''

    if not event_type:
        return {
            'statusCode': 400,
            'body': 'Bad request. Event Type is required v5.'
        }

    try:
        # print(f"Event Type: {event_type}")
        # get menu based on event_type
        db = resource('dynamodb', region_name='us-east-1')
        menu_table = db.Table('cloud9-takeaway')
        response = menu_table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('event_type').eq(event_type)
        )
        # print(json.dumps(response['Items']))
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])
        }
    except Exception as err:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(err)})
        }
