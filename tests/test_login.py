import os
from dotenv import load_dotenv
from utilities.assertion_helpers import (assert_status_code,
                                         assert_login_response_body_structure,
                                         assert_json_response)

load_dotenv()


def test_login(dummyjson_client):
    EXPECTED_RESPONSE_KEYS = ["id", "username", "email", "firstName", "lastName", "gender",
                              "image", "accessToken", "refreshToken"]

    response = dummyjson_client.auth_client.authenticate(username=os.getenv("DEFAULT_USER_NAME"),
                                                         password=os.getenv("DEFAULT_USER_PASS"))
    # Assertions using Assertion Helpers
    assert_status_code(response, 200)
    json_response_body = assert_json_response(response)
    # Assert Response Body
    assert_login_response_body_structure(json_response_body, EXPECTED_RESPONSE_KEYS)
