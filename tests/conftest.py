import pytest
from httpx_clients.dummyjson_base import DummyJsonBase


@pytest.fixture(scope="session")
def dummyjson_client():
    # Initialize Client (whole)
    client = DummyJsonBase()
    # Yield the Client
    yield client

    # On End: Close the Client
    client.close_client()
