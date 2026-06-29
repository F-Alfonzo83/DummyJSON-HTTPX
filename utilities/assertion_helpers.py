import json
import httpx
import pytest
from utilities.logger import _logger

# Instantiate a Logger for the Assertions Helper Module
logger = _logger(__name__)


def assert_status_code(response: httpx.Response, expected_status_code: int = 200):
    logger.info(f"TEST: Asserting status code")
    assert response.status_code == expected_status_code


def assert_json_response(response: httpx.Response):
    logger.info("TEST: Asserting Response is of type: JSON")
    try:
        json_response: json = response.json()
    except json.decoder.JSONDecodeError as json_error:
        print(f"Error decoding JSON response.\nSystem error: {json_error}")
        pytest.fail()
    return json_response


def assert_login_response_body_structure(json_response: dict, expected_body_keys: list[str]):
    logger.info(f"TEST: Asserting Authentication response body structure")
    for value in expected_body_keys:
        assert value in json_response
        assert json_response[value] is not None


def assert_product_response_body_structure(
        json_response: dict, expected_product_keys: list[str], expected_outer_keys: list[str] = None):
    logger.info("TEST: Asserting Product Response Body")
    # All of this will be executed only if  There is an outer layer.
    if expected_outer_keys:
        logger.debug("TEST: Asserting Product Response body outer structure")
        for value in expected_outer_keys:
            assert value in json_response
        # Assert Total, Skip and Limit
        logger.debug("TEST: Asserting Total is Integer")
        assert isinstance(json_response["total"], int)
        logger.debug("TEST: Asserting Total is major than Zero")
        assert json_response["total"] > 0
        logger.debug("TEST: Asserting Limit matches number of fetched products")
        assert json_response["limit"] == len(json_response["products"])
        logger.debug("TEST: Asserting Product list inner structure")

        first_index = json_response["products"][0]
        last_index = json_response["products"][-1]
        middle_index = json_response["products"][len(json_response["products"]) // 2]

        logger.debug("TEST: Asserting expected keys inside Products list.")
        for value in expected_product_keys:
            assert value in first_index
            assert value in middle_index
            assert value in last_index

        logger.debug("TEST: Asserting Product ID is a number and over 0")
        assert first_index["id"] > 0
        assert middle_index["id"] > 0
        assert last_index["id"] > 0
        logger.debug("TEST: Asserting Price is a float and over 0")
        assert isinstance(first_index["price"], float)
        assert isinstance(middle_index["price"], float)
        assert isinstance(last_index["price"], float)
        logger.debug("TEST: Asserting Stock is an Integer")
        assert isinstance(first_index["stock"], int)
        assert isinstance(middle_index["stock"], int)
        assert isinstance(last_index["stock"], int)

    else:

        # In case there is no Outer Layer. Single Product
        logger.debug("TEST: Asserting Product list inner structure")
        for value in expected_product_keys:
            assert value in json_response
        logger.debug("TEST: Asserting Product ID is a number and over 0")
        assert json_response["id"] > 0
        logger.debug("TEST: Asserting Price is a float and over 0")
        assert isinstance(json_response["price"], float)
        logger.debug("TEST: Asserting Stock is an Integer")
        assert isinstance(json_response["stock"], int)
