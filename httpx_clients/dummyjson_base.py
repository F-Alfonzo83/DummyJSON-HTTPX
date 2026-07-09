import httpx

from configurations import config_loader
from httpx_clients.auth_client import AuthClient
from httpx_clients.products_client import ProductsClient
from utilities.hooks import request_hook, response_hook
from utilities.logger import _logger

config = config_loader.ConfigLoader()


class DummyJsonBase:
    """Defines a Base for the requests that will be sent to DummyJson."""

    def __init__(self):
        """Creates a base  HTTPX Client object used to build requests.

        Provides base features such as base url, headers and logger

        Arguments:
            BASE_URL (str): The Base URL, acquired from configurations module.
            self.logger (logging.Logger): Logger object used to log activities.
            self.dummyjson_client (httpx.Client): Dummy HTTP Client object.
            self.request_hook_logger (function): Logger hook used to log requests.
            self.response_hook_logger (function): Logger hook used to log responses.

        Example:
                dummyjson = DummyJsonBase()
                dummyjson.auth_client.authenticate("user","pass")
        """
        self.BASE_URL = config.base_url()
        self.logger = _logger(__name__)

        self.request_hook_logger = request_hook(self.logger)
        self.response_hook_logger = response_hook(self.logger)
        self.auth_token = None

        self.dummyjson_client = httpx.Client(base_url=self.BASE_URL,
                                             headers={'Content-Type': 'application/json'},
                                             event_hooks={"request": [self.request_hook_logger],  # Must be a list
                                                          "response": [self.response_hook_logger]})  # Must be a list

        # Clients
        # Authentication Clients:
        # General:
        self.auth_client = AuthClient(client=self.dummyjson_client, logger=self.logger)
        # Products Client
        self.products_client = ProductsClient(client=self.dummyjson_client, logger=self.logger)

    def retrieve_auth_token(self, username: str, password: str, expires_in: int):
        """Retrieves the authorization token for the given username and password.

        Args:
            username (str) Username
            password (str) Password
            expires_in (int) - Optional:  Expiration time. Defaults to 60

        Returns:
            auth_token (str) Authorization token. Stores  as class variable.

        Notes:
            Must be called to populate the authorization token.
        """
        response = self.auth_client.authenticate(username, password, expires_in)
        response_json = response.json()
        token = response_json["accessToken"]
        self.auth_token = token
