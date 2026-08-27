import json
import logging

from models.product_schema_models import SingleProductSchema, ProductsSchema, CategoriesSchema
from utilities.assertion_helpers import (assert_status_code, assert_json_response)
import pytest


logger = logging.getLogger(__name__)

EXPECTED_OUTER_KEYS = ["products", "total", "skip", "limit"]
EXPECTED_PRODUCTS_KEYS = ["id", "title", "description", "category", "price", "discountPercentage", "rating",
                          "stock", "tags", "sku", "weight", "dimensions", "warrantyInformation",
                          "shippingInformation", "availabilityStatus", "reviews", "returnPolicy",
                          "minimumOrderQuantity", "meta", "thumbnail", "images"]
EXPECTED_CATEGORIES_KEYS = ["slug", "name", "url"]
EXPECTED_CATEGORIES = ["beauty", "fragrances", "furniture", "groceries", "home-decoration", "kitchen-accessories",
                       "laptops", "mens-shirts", "mens-shoes", "mens-watches", "mobile-accessories", "motorcycle",
                       "skin-care", "smartphones", "sports-accessories", "sunglasses", "tablets", "tops", "vehicle",
                       "womens-bags", "womens-dresses", "womens-jewellery", "womens-shoes", "womens-watches"]

EXPECTED_CATEGORIES_TEST_SET = ["womens-jewellery", "sports-accessories", "home-decoration", "mobile-accessories",
                                "sunglasses", "tops", "groceries"]

EXPECTED_ADD_PRODUCT_ECHO_KEYS = ["id", "title", "description", "category", "price", "discountPercentage",  "rating",
                                  "stock", "brand", "thumbnail", "images"]

# ADD PRODUCT POSSIBLE PAYLOADS
valid_payload = {"title": "valid_title", "price": 13.1416, "description": "stock"}
unrecognized_keys_payload = {"cat": "meow", "price": 13.1416, "dog": "woof"}
empty_payload = {}


def test_get_all_products(dummyjson_client):

    response = dummyjson_client.products_client.get_all_products()
    # Assertions
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    # Assert Schema
    ProductsSchema.model_validate(json_response)


def test_get_all_products_limit_to_one(dummyjson_client):
    # Explicitly  and  fixed send a hard coded limit of 1.
    response = dummyjson_client.products_client.get_all_products(limit=1)
    # Assertions
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    # Assert Schema
    ProductsSchema.model_validate(json_response)


def test_get_single_product(dummyjson_client):

    prod_id = 1
    response = dummyjson_client.products_client.get_product_by_id(product_id=prod_id)
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    # Assert Product ID.
    assert (json_response["id"] == prod_id)
    # Schema Validation
    SingleProductSchema.model_validate(json_response)


def test_search_products(dummyjson_client):
    search_pattern = "phone"
    response = dummyjson_client.products_client.search_products(search_term=search_pattern)
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    # Assert Schema
    ProductsSchema.model_validate(json_response)


def test_get_all_products_limit(dummyjson_client):
    response = dummyjson_client.products_client.get_all_products(limit=10)
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    # Assert Schema
    ProductsSchema.model_validate(json_response)


def test_get_all_products_categories(dummyjson_client):
    response = dummyjson_client.products_client.get_all_products_categories()
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    CategoriesSchema.model_validate(json_response)


def test_get_products_category_list(dummyjson_client):
    response = dummyjson_client.products_client.get_product_category_list()
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    # Validate response is a list.
    logger.debug("TEST: Asserting that the response is  a list")
    assert isinstance(json_response, list)


@pytest.mark.parametrize(argnames="category",
                         argvalues=EXPECTED_CATEGORIES_TEST_SET)
def test_get_products_category(dummyjson_client, category: str):
    response = dummyjson_client.products_client.get_product_category(category)
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    ProductsSchema.model_validate(json_response)


@pytest.mark.parametrize(argnames="payload",
                         argvalues=[valid_payload, unrecognized_keys_payload, empty_payload],
                         ids=["valid_payload", "unrecognized_payload", "empty_payload"])
def test_add_product(dummyjson_client, payload):
    response = dummyjson_client.products_client.add_product(**payload)
    assert_status_code(response, 201)
    json_response = assert_json_response(response)

    expected_response_echo = {key: value for key, value in json.loads(response.request.content).items()
                              if key in EXPECTED_ADD_PRODUCT_ECHO_KEYS}
    actual_response = {key: value for key, value in json_response.items() if key != "id"}
    assert expected_response_echo == actual_response
    assert json_response["id"] == 195
