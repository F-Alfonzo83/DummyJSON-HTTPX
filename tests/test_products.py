from utilities.assertion_helpers import *
from httpx_clients.dummyjson_base import DummyJsonBase

dummyjson = DummyJsonBase()
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


def test_get_all_products():

    response = dummyjson.products_client.get_all_products()
    # Assertions
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    assert_product_response_body_structure(json_response=json_response,
                                           expected_product_keys=EXPECTED_PRODUCTS_KEYS,
                                           expected_outer_keys=EXPECTED_OUTER_KEYS)


def test_get_all_products_limit_to_one():
    # Explicitly  and  fixed send a hard coded limit of 1.
    response = dummyjson.products_client.get_all_products(limit=1)
    # Assertions
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    assert_product_response_body_structure(json_response=json_response,
                                           expected_product_keys=EXPECTED_PRODUCTS_KEYS,
                                           expected_outer_keys=EXPECTED_OUTER_KEYS)


def test_get_single_product():

    response = dummyjson.products_client.get_product_by_id(product_id=1)
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    assert_product_response_body_structure(json_response=json_response,
                                           expected_product_keys=EXPECTED_PRODUCTS_KEYS)


def test_search_products():
    response = dummyjson.products_client.search_products(search_term=".")
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    assert_product_response_body_structure(json_response=json_response,
                                           expected_product_keys=EXPECTED_PRODUCTS_KEYS,
                                           expected_outer_keys=EXPECTED_OUTER_KEYS)


def test_get_all_products_limit():
    response = dummyjson.products_client.get_all_products(limit=10)
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    assert_product_response_body_structure(json_response=json_response,
                                           expected_product_keys=EXPECTED_PRODUCTS_KEYS,
                                           expected_outer_keys=EXPECTED_OUTER_KEYS)


def test_get_all_products_categories():
    response = dummyjson.products_client.get_all_products_categories()
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    assert_products_categories_response(json_response=json_response,
                                        expected_categories_keys=EXPECTED_CATEGORIES_KEYS)


def test_get_products_category_list():
    response = dummyjson.products_client.get_product_category_list()
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    # Validate response is a list.
    logger.debug("TEST: Asserting that the response is  a list")
    assert isinstance(json_response, list)
    assert_categories_list_response(json_response=json_response,
                                    expected_categories=EXPECTED_CATEGORIES)


@pytest.mark.parametrize(argnames="category",
                         argvalues=EXPECTED_CATEGORIES_TEST_SET)
def test_get_products_category(category: str):
    response = dummyjson.products_client.get_product_category(category)
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    assert_product_response_body_structure(json_response=json_response,
                                           expected_outer_keys=EXPECTED_OUTER_KEYS,
                                           expected_product_keys=EXPECTED_PRODUCTS_KEYS)
