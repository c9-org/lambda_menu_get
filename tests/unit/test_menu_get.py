import json
import pytest
import boto3
from moto import mock_aws
from boto3 import resource
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from src.app import lambda_handler

@pytest.fixture()
def apigw_event() ->  APIGatewayProxyEvent:
    with open("events/unit-test-event.json", encoding='utf-8') as f:
        return APIGatewayProxyEvent(json.load(f))

@mock_aws
def create_db_table():
    db = resource('dynamodb', region_name='us-east-1')
    db.create_table(
        TableName='cloud9-takeaway',
        KeySchema=[
            {'AttributeName': 'event_type', 'KeyType': 'HASH'},
            {'AttributeName': 'name', 'KeyType': 'RANGE'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'event_type', 'AttributeType': 'S'},
            {'AttributeName': 'name', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )

@mock_aws
def insert_menu_data_into_table():
    db = resource('dynamodb', region_name='us-east-1')
    menu_table = db.Table('cloud9-takeaway')

    # prepare the sample payload
    data = {
        "id": "4889a379-af62-4c62-9011-e53639870b1b",
        "event_type": "happy_hours",
        "name": "Chicken Salad",
        "price": "245",
        "url": "https://dk1pbmkqs58wc.cloudfront.net/ipl_epl/Ramen_Bowl_235.jpg"
    }

    menu_table.put_item(
        Item=data
    )

@mock_aws
def get_menu_data_from_table(event_type: str):
    db = resource('dynamodb', region_name='us-east-1')
    menu_table = db.Table('cloud9-takeaway')
    menu_response = menu_table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('event_type').eq(event_type)
    )
    return menu_response

@mock_aws
def test_event_type_exists(apigw_event: dict) -> None:
    # to mock out the actual operation, the DB/TABLE/DATA needs to be there first
    create_db_table()
    insert_menu_data_into_table()
    # mock the actual lambda
    response = lambda_handler(apigw_event, "")
    assert response.get('statusCode') == 200


@mock_aws
def test_menu_exists(apigw_event: dict) -> None:
    # to mock out the actual operation, the DB/TABLE/DATA needs to be there first
    create_db_table()
    insert_menu_data_into_table()
    # mock the actual lambda
    response = lambda_handler(apigw_event, "")
    assert len(response.get('body')) > 0
