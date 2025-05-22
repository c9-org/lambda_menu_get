import json
import pytest
from moto import mock_aws
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from src.app import lambda_handler

@pytest.fixture()
def apigw_event() ->  APIGatewayProxyEvent:
    with open(f"../events/unit-test-event.json") as f:
        return APIGatewayProxyEvent(json.load(f))
    

@mock_aws
def test_event_type_exists(apigw_event: dict) -> None:
    response = lambda_handler(apigw_event, "")
    print(response)
    assert response.get('statusCode') == 200


@mock_aws
def test_menu_exists(apigw_event: dict) -> None:
    response = lambda_handler(apigw_event, "")
    items = response.get('body')['Items']
    assert len(items) > 0