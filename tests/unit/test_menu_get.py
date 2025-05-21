import json
import pytest
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent


@pytest.fixture()
def apigw_event() ->  APIGatewayProxyEvent:
    with open(f"events/unit-test-event.json") as f:
        return APIGatewayProxyEvent(json.load(f))
    

def test_lambda_handler(apigw_event: dict) -> None:
    pass