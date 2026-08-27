import os
from dotenv import load_dotenv
from models.auth_schema_models import AuthSchema
from utilities.assertion_helpers import (assert_status_code,
                                         assert_json_response)
from utilities.logger import _logger
load_dotenv()

logger = _logger(__name__)


def test_login(dummyjson_client):
    response = dummyjson_client.auth_client.authenticate(username=os.getenv("DEFAULT_USER_NAME"),
                                                         password=os.getenv("DEFAULT_USER_PASS"))
    # Assertions using Assertion Helpers
    assert_status_code(response, 200)
    json_response_body = assert_json_response(response)
    # Assert vs JSON Model
    logger.debug("TEST: Validating Schema against Model")
    schema_validation = AuthSchema.model_validate(json_response_body)
    #  Assert logged user
    logger.debug("TEST: Validating logged user")
    assert schema_validation.username == os.getenv("DEFAULT_USER_NAME")
