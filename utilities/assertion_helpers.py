import json
import httpx
import pytest
from utilities.logger import _logger

# Instantiate a Logger for the Assertions Helper Module
logger = _logger(__name__)


def assert_status_code(response: httpx.Response, expected_status_code: int = 200):
    logger.info("TEST: Asserting status code")
    assert response.status_code == expected_status_code, \
        f"{response.request.method} - {response.request.url} -> {response.status_code}"


def assert_json_response(response: httpx.Response):
    logger.info("TEST: Asserting Response is of type: JSON")
    try:
        json_response: json = response.json()
    except json.decoder.JSONDecodeError as json_error:
        print(f"Error decoding JSON response.\nSystem error: {json_error}")
        pytest.fail()
    return json_response


def assert_search_pattern_in_response(json_response: dict, search_pattern: str):
    logger.info("TEST: Asserting Search pattern found in response")
    for product in json_response["products"]:
        assert (search_pattern in product["title"].lower() or
                search_pattern in product["description"].lower())


def assert_host(value):
    EXPECTED_HOSTS = ["cdn.dummyjson.com",
                      "dummyjson.com"]

    if value.host not in EXPECTED_HOSTS:
        raise ValueError("Bad Host")
    return value
