from httpx_clients.dummyjson_base import DummyJsonBase
from utilities.assertion_helpers import *

dummyjson = DummyJsonBase()


def test_login():
    EXPECTED_RESPONSE_KEYS = ["id", "username", "email", "firstName", "lastName", "gender",
                                   "image", "accessToken",  "refreshToken"]

    response = dummyjson.auth_client.authenticate("emilys","emilyspass")
    # Assertions using Assertion Helpers
    assert_status_code(response, 200)
    json_response_body = assert_json_response(response)
    # Assert Response Body
    assert_login_response_body_structure(json_response_body, EXPECTED_RESPONSE_KEYS)




