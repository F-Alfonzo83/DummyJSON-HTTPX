import pytest

from httpx_clients.auth_client import build_auth_header
from utilities.logger import _logger

logger = _logger(__name__)

test_data = [
    pytest.param({"token": "123456"},
                 {"Authorization": "Bearer 123456"},
                 id="default_prefix"),
    pytest.param({"token": ""},
                 {"Authorization": "Bearer "},          # trailing space is deliberate
                 id="default_prefix_empty_token"),
    pytest.param({"prefix": "TestPrefix", "token": "TestToken"},
                 {"Authorization": "TestPrefix TestToken"},
                 id="explicit_prefix_and_token"),
    pytest.param({"prefix": "", "token": ""},
                 {"Authorization": " "},                # single space, both blank
                 id="empty_prefix_and_token"),
]


@pytest.mark.unit
@pytest.mark.parametrize("test_input, expected", test_data)
def test_build_auth_header(test_input, expected):
    # Test expectancy
    output = build_auth_header(**test_input)
    logger.debug("UNIT TEST: Validating the response matches expected header")
    assert output == expected, \
        f"TEST FAILED: Function output does not match expected header: {output} != {expected}"
