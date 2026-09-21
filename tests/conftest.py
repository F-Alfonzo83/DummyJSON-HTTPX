import os
from typing import NamedTuple

import pytest
from dotenv import load_dotenv

from httpx_clients.dummyjson_base import DummyJsonBase


load_dotenv()


class Credentials(NamedTuple):
    username: str
    password: str


@pytest.fixture(scope="session")
def dummyjson_client():
    """Creates  an instance of the DummyJsonBase class.

    The instance of the DummyJsonBase holds inside it access to all the client modules such as authentication,
    products and more all consolidated inside one  single client.

    Scope:  Session Scope to provide a single client for the  whole  session.

    Examples:
        dummyjson_client.auth_client.authenticate
        dummyjson_client.products_client.get_all_products

    Yields: client (DummyJsonBase)
    """
    # Initialize Client (whole)
    client = DummyJsonBase()
    # Yield the Client
    yield client

    # On End: Close the Client
    client.close_client()


@pytest.fixture(scope="session")
def auth_token(dummyjson_client, default_user_credentials):
    """Retrieves the authorization token from the dummy client and passes it to the test.

    Scope:  Session Scope considering that a single token should last up to 60 minutes.

    Returns: (str) Authorization token string
    """
    auth_token = dummyjson_client.auth_client.retrieve_auth_token(username=default_user_credentials.username,
                                                                  password=default_user_credentials.password)
    return auth_token


@pytest.fixture(scope="session")
def default_user_credentials():
    """Provides credentials of the default user.

    Makes use of a namedTuple to  provide the username and password for the default user.

    Returns:
        Credentials: NamedTuple object containing the username and password ready to be used for authentication.

    Examples:
        default_user_credentials.username, default_user_credentials.password
    """

    credentials = Credentials(username=os.environ["DEFAULT_USER_NAME"],
                              password=os.environ["DEFAULT_USER_PASS"])
    return credentials
