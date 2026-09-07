import json
import logging
from models import product_schema_models
from models.product_schema_models import SingleProductSchema, ProductsSchema, CategoriesSchema, ProductCategoryList
from utilities.assertion_helpers import (assert_status_code, assert_json_response, assert_search_pattern_in_response)
import pytest


logger = logging.getLogger(__name__)


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
    query = "phone"
    response = dummyjson_client.products_client.search_products(search_term=query)
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    # Assert Schema
    ProductsSchema.model_validate(json_response)
    # Assert response returns at least 1 value for a valid search.
    assert json_response["total"] > 0, \
        f"TEST ERROR: Expected at least one result for '{query}'. Obtained: {json_response['total']}"
    # Assert Search pattern is on the response
    assert_search_pattern_in_response(json_response, query)


def test_negative_search_products(dummyjson_client):
    query = "zzznomatches"
    response = dummyjson_client.products_client.search_products(search_term=query)
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    # Assert no elements are back.
    assert json_response["total"] == 0, \
        f"TEST ERROR: Expected ZERO matches for '{query}'. Obtained: {json_response['total']}"


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
    model = CategoriesSchema.model_validate(json_response)
    # Retrieve the "slug" entries from the validated model.
    response_slugs = [item.slug for item in model.root]
    # Compare length of the lists.
    assert len(response_slugs) == len(product_schema_models.PRODUCT_CATEGORIES), \
        (f"The entries on the response: {len(response_slugs)} "
         f"and the expected response {len(product_schema_models.PRODUCT_CATEGORIES)} are different in length")
    # Compare the results of the Response Vs the List of expected elements.
    assert set(response_slugs) == set(product_schema_models.PRODUCT_CATEGORIES), \
        (f"The entries on the response and the expected response are different in content: "
         f"{set(product_schema_models.PRODUCT_CATEGORIES) - set(response_slugs)}")


def test_get_products_category_list(dummyjson_client):
    response = dummyjson_client.products_client.get_product_category_list()
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    model = ProductCategoryList.model_validate(json_response)
    response_category = model.root
    # Assert the Length of both lists.
    assert len(response_category) == len(product_schema_models.PRODUCT_CATEGORIES), \
        f"The length of the Response:({len(response_category)}) does not match "\
        f"the length of the expected response: ({len(product_schema_models.PRODUCT_CATEGORIES)})"
    # Assert the entries  match
    assert set(response_category) == set(product_schema_models.PRODUCT_CATEGORIES), \
        f"Mismatch: {set(product_schema_models.PRODUCT_CATEGORIES) - set(response_category)}"


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
