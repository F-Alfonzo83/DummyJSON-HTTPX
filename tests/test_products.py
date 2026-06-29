from utilities.assertion_helpers import *
from httpx_clients.dummyjson_base import DummyJsonBase

dummyjson = DummyJsonBase()


def test_get_all_products():
    EXPECTED_OUTER_KEYS = ["products", "total", "skip", "limit"]
    EXPECTED_PRODUCTS_KEYS = ["id", "title", "description", "category", "price", "discountPercentage", "rating",
                              "stock", "tags", "sku", "weight", "dimensions", "warrantyInformation",
                              "shippingInformation", "availabilityStatus", "reviews", "returnPolicy",
                              "minimumOrderQuantity", "meta", "thumbnail", "images"]

    response = dummyjson.products_client.get_all_products()
    # Assertions
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    assert_product_response_body_structure(json_response=json_response,
                                           expected_product_keys=EXPECTED_PRODUCTS_KEYS,
                                           expected_outer_keys=EXPECTED_OUTER_KEYS)


def test_get_single_product():
    EXPECTED_PRODUCT_KEYS = ["id", "title", "description", "category", "price", "discountPercentage", "rating",
                             "stock", "tags", "sku", "weight", "dimensions", "warrantyInformation",
                             "shippingInformation", "availabilityStatus", "reviews", "returnPolicy",
                             "minimumOrderQuantity", "meta", "thumbnail", "images"]

    response = dummyjson.products_client.get_product_by_id(product_id=1)
    assert_status_code(response, 200)
    json_response = assert_json_response(response)
    assert_product_response_body_structure(json_response=json_response,
                                           expected_product_keys=EXPECTED_PRODUCT_KEYS)
