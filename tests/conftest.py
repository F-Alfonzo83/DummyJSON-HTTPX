import os

import pytest
from dotenv import load_dotenv

from httpx_clients.dummyjson_base import DummyJsonBase


load_dotenv()


@pytest.fixture(scope="session")
def dummyjson_client():
    """Creates  an instance of the DummyJsonClient class.

    The instance of the DummyJsonClient holds inside it access to all the client modules such as authentication,
    products and more all consolidated inside one  single client.

    Scope:  Session Scope to provide a single client for the  whole  session.

    Examples:
        client.auth_client.authenticate
        client.products_client.get_products

    Yields: client (DummyJsonClient)

    Notes: Upon yield, closes the client.
    """
    # Initialize Client (whole)
    client = DummyJsonBase()
    # Yield the Client
    yield client

    # On End: Close the Client
    client.close_client()


@pytest.fixture(scope="session")
def auth_token(dummyjson_client):
    """Retrieves the authorization token from the dummy client and passes it to the test.

    Scope:  Session Scope considering that a single token should last up to 60 minutes.

    Returns: (str) Authorization token string
    """
    auth_token = dummyjson_client.auth_client.retrieve_auth_token(username=os.environ["DEFAULT_USER_NAME"],
                                                                  password=os.environ["DEFAULT_USER_PASS"])
    return auth_token


@pytest.fixture(scope="session")
def default_user_credentials():
    username = os.environ["DEFAULT_USER_NAME"]
    password = os.environ["DEFAULT_USER_PASS"]
    return username, password
