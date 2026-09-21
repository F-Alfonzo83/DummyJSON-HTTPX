import time
import httpx
import pytest
from models.auth_schema_models import AuthSchema
from utilities.assertion_helpers import (assert_status_code,
                                         assert_json_response)
from utilities.logger import _logger

logger = _logger(__name__)


def test_login(dummyjson_client,  default_user_credentials):
    response = dummyjson_client.auth_client.authenticate(username=default_user_credentials.username,
                                                         password=default_user_credentials.password)
    # Assertions using Assertion Helpers
    assert_status_code(response, 200)
    json_response_body = assert_json_response(response)
    # Assert vs JSON Model
    logger.debug("TEST: Validating Schema against Model")
    schema_validation = AuthSchema.model_validate(json_response_body)
    #  Assert logged user
    logger.debug("TEST: Validating logged user Schema against Model")
    assert schema_validation.username == default_user_credentials.username


def test_retrieve_token(dummyjson_client, default_user_credentials):
    auth_token = dummyjson_client.auth_client.retrieve_auth_token(username=default_user_credentials.username,
                                                                  password=default_user_credentials.password)
    logger.debug("TEST: Assert the Token is a String")
    assert isinstance(auth_token, str), f"TEST FAIL: Auth Token is not a String. Got : {type(auth_token)}"
    logger.debug("TEST: Validating the Token is not an emtpy string")
    assert len(auth_token) > 0, (f"TEST FAIL: The length of the auth token is not valid\n"
                                 f"Given Length: {len(auth_token)!r} ")


def test_auth_token_request_time_and_expires_setters(dummyjson_client, default_user_credentials):
    expiration_time = 25
    logger.debug("TEST: Setting initial timer")
    initial_time = time.time()
    dummyjson_client.auth_client.retrieve_auth_token(username=default_user_credentials.username,
                                                     password=default_user_credentials.password,
                                                     expires_in_mins=expiration_time)
    logger.debug("TEST: Setting final timer")
    final_time = time.time()
    logger.debug("TEST: Validate matching expires in  timer")
    assert dummyjson_client.auth_client.auth_token_expires_in == expiration_time, \
        f"TEST FAIL: Times do not  match: Expected time: {expiration_time}, "\
        f"Actual: {dummyjson_client.auth_client.auth_token_expires_in}"
    logger.debug("TEST: Validate request time within the execution")
    assert (initial_time <= dummyjson_client.auth_client.auth_token_request_time <= final_time), \
        f"TEST FAIL: Request time not within expected boundaries: \n"\
        f"Initial Time: {initial_time}\n || Request time: {dummyjson_client.auth_client.auth_token_request_time} "\
        f"|| Final Time: {final_time}"


def test_negative_authenticate_invalid_user(dummyjson_client, default_user_credentials):
    response = dummyjson_client.auth_client.authenticate(username=default_user_credentials.username+"1",
                                                         password=default_user_credentials.password)
    assert_status_code(response, 400)
    json_response_body = assert_json_response(response)
    assert json_response_body == {"message": "Invalid credentials"}


def test_negative_retrieve_auth_token_invalid_user(dummyjson_client, default_user_credentials):
    with pytest.raises(httpx.HTTPStatusError) as request_error_wrapper:
        dummyjson_client.auth_client.retrieve_auth_token(username=default_user_credentials.username+"1",
                                                         password=default_user_credentials.password)
    assert_status_code(request_error_wrapper.value.response, 400)
    assert request_error_wrapper.value.response.json() == {"message": "Invalid credentials"}, \
        f"TEST FAIL: Error message does not match: {request_error_wrapper.value.response.json()}"


def test_negative_retrieve_auth_token_invalid_password(dummyjson_client, default_user_credentials):
    with pytest.raises(httpx.HTTPStatusError) as request_error_wrapper:
        dummyjson_client.auth_client.retrieve_auth_token(username=default_user_credentials.username,
                                                         password=default_user_credentials.password+"1")
    assert_status_code(request_error_wrapper.value.response, 400)
    assert request_error_wrapper.value.response.json() == {"message": "Invalid credentials"}, \
        f"TEST FAIL: Error message does not match: {request_error_wrapper.value.response.json()}"
