import datetime
from datetime import UTC

import pytest
import json

from utilities.logger import _logger
from models import product_schema_models
from models.product_schema_models import (SingleProductSchema, ProductsSchema, CategoriesSchema,
                                          ProductCategoryList, UpdateProductSchema, DeleteProductSchema)
from utilities.assertion_helpers import (assert_status_code, assert_json_response,
                                         assert_search_pattern_in_response)
from httpx_clients.auth_client import build_auth_header

logger = _logger(__name__)


EXPECTED_CATEGORIES_TEST_SET = ["womens-jewellery", "sports-accessories", "home-decoration", "mobile-accessories",
                                "sunglasses", "tops", "groceries"]

EXPECTED_ADD_PRODUCT_ECHO_KEYS = ["id", "title", "description", "category", "price", "discountPercentage",  "rating",
                                  "stock", "brand", "thumbnail", "images"]

EXPIRED_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJlbWlseXMiLCJlbWFpbCI6ImVtaWx\
5LmpvaG5zb25AeC5kdW1teWpzb24uY29tIiwiZmlyc3ROYW1lIjoiRW1pbHkiLCJsYXN0TmFtZSI6IkpvaG5zb24iLCJnZW5kZXIiOiJmZW1h\
bGUiLCJpbWFnZSI6Imh0dHBzOi8vZHVtbXlqc29uLmNvbS9pY29uL2VtaWx5cy8xMjgiLCJpYXQiOjE3OTA4NjQ1MDQsImV4cCI6MTc5MDg2O\
DEwNH0.Q_3cLHQUfqbyRhIEETC8Euz5pQhYMsxq4SEck-ewzjI"  # nosec B105 -
# expired token for the public demo account, used only to trigger "Token Expired!"

PARAMS_INVALID_PRODUCT_IDS = [
    pytest.param(0, id="product_id_equals_0"),
    pytest.param(195, id="product_id_equals_195"),
    pytest.param("abc", id="product_id_is_letter_string"),
    pytest.param("12$", id="product_id_is_special_characters"),
]

PARAMS_INVALID_AUTH_TOKENS = [
    pytest.param(lambda token: {"Authorization": f"Bearer {EXPIRED_TOKEN}"},
                 401,
                 "Token Expired!",
                 id="expired_token"),
    pytest.param(lambda token: {"Authorization": f"Bearer {EXPIRED_TOKEN.split("a")[1]}"},
                 401,
                 "Invalid/Expired Token!",
                 id="invalid_token"),
    pytest.param(lambda token: {},
                 401,
                 "Access Token is required",
                 id="no_token"),
    pytest.param(lambda token: {"Authorization": f"Some {token}"},
                 500,
                 "invalid token",
                 id="malformed_token")
]

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


def test_put_update_product_title(dummyjson_client, auth_token):
    item_id = 1
    payload = {"title":  "Modified Title"}
    response = dummyjson_client.products_client.update_product(product_id=item_id,
                                                               headers=build_auth_header(auth_token),
                                                               request_body=payload)
    assert_status_code(response, 200)
    json_body = assert_json_response(response)
    model = UpdateProductSchema.model_validate(json_body)
    assert f"/auth/products/{item_id}" == response.request.url.path, \
        "TEST ERROR: Request was not sent to the correct URL"
    assert model.id == item_id
    assert model.title == payload["title"]


def test_delete_product(dummyjson_client, auth_token):
    delta = datetime.timedelta(seconds=3)
    item_id = 1

    time_before = datetime.datetime.now(tz=UTC)
    response = dummyjson_client.products_client.delete_product(product_id=item_id,
                                                               headers=build_auth_header(auth_token))
    time_after = datetime.datetime.now(tz=UTC)
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    model = DeleteProductSchema.model_validate(json_response)
    assert "authorization" in response.request.headers, \
        "TEST ERROR: Request Header does not contain authorization"
    assert f"/auth/products/{item_id}" == response.request.url.path, \
        "TEST ERROR: Request was not sent to the correct URL"
    assert item_id == model.id, f"TEST ERROR: Item ID mismatch: {item_id} != {model.id}"
    assert time_before-delta <= model.deleted_on <= time_after+delta, \
        "TEST ERROR: Time not within expected range"


@pytest.mark.parametrize("prod_id", PARAMS_INVALID_PRODUCT_IDS)
def test_negative_get_product_id_invalid_values(dummyjson_client, prod_id):
    response = dummyjson_client.products_client.get_product_by_id(product_id=prod_id)
    assert_status_code(response, 404)
    json_response = assert_json_response(response)
    assert json_response["message"] == f"Product with id '{prod_id}' not found"


@pytest.mark.parametrize("prod_id", PARAMS_INVALID_PRODUCT_IDS)
def test_negative_delete_product_id_invalid_values(dummyjson_client, auth_token,  prod_id):
    response = dummyjson_client.products_client.delete_product(product_id=prod_id,
                                                               headers=build_auth_header(auth_token))
    assert_status_code(response, 404)
    json_response = assert_json_response(response)
    assert json_response["message"] == f"Product with id '{prod_id}' not found"


@pytest.mark.parametrize("craft_bad_auth, expected_status,expected_message", PARAMS_INVALID_AUTH_TOKENS)
def test_negative_delete_product_invalid_tokens(dummyjson_client,
                                                craft_bad_auth,
                                                expected_status,
                                                expected_message, auth_token):
    response = dummyjson_client.products_client.delete_product(product_id=1,
                                                               headers=craft_bad_auth(auth_token))
    assert_status_code(response, expected_status)
    json_response = assert_json_response(response)
    assert json_response["message"] == expected_message


@pytest.mark.parametrize("prod_id", PARAMS_INVALID_PRODUCT_IDS)
def test_negative_update_product_id_invalid_values(dummyjson_client, auth_token, prod_id):
    response = dummyjson_client.products_client.update_product(product_id=prod_id,
                                                               headers=build_auth_header(auth_token),
                                                               request_body={"title": "Modified Title"})
    assert_status_code(response, 404)
    json_response = assert_json_response(response)
    assert json_response["message"] == f"Product with id '{prod_id}' not found"


@pytest.mark.parametrize("craft_bad_auth, expected_status,expected_message", PARAMS_INVALID_AUTH_TOKENS)
def test_negative_update_product_invalid_tokens(dummyjson_client, auth_token,
                                                craft_bad_auth,
                                                expected_status,
                                                expected_message):
    response = dummyjson_client.products_client.update_product(product_id=1,
                                                               headers=craft_bad_auth(auth_token),
                                                               request_body={"title": "Modified Title"})
    assert_status_code(response, expected_status)
    json_response = assert_json_response(response)
    assert json_response["message"] == expected_message


@pytest.mark.parametrize("category_id", [
    pytest.param(" ", id="blank_space_category_id"),
    pytest.param("smartphone", id="category_does_not_exist_(misspelled)"),
    pytest.param("shawarma", id="category_does_not_exist_(not_real)"),
    pytest.param("$%", id="category_does_not_exist(special_characters)"),
])
def test_negative_get_item_category_with_invalid_categories(dummyjson_client, category_id):
    response = dummyjson_client.products_client.get_product_category(category=category_id)
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    ProductsSchema.model_validate(json_response)
    assert json_response["total"] == 0
    assert json_response["skip"] == 0
    assert json_response["limit"] == 0
