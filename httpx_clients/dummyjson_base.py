import httpx
from http.cookiejar import CookieJar, DefaultCookiePolicy

from configurations import config_loader
from httpx_clients.auth_client import AuthClient
from httpx_clients.products_client import ProductsClient
from utilities.hooks import request_hook, response_hook
from utilities.logger import _logger

config = config_loader.ConfigLoader()


class DummyJsonBase:
    """Defines a Base for the requests that will be sent to DummyJson.
    Attributes:

    Notes:
        Cookies are not allowed to be set in  order to prevent the scenario  where login  in  creates
        authentication cookies that may affect negative tests involving authentication.
    """

    def __init__(self):
        """Creates a base  HTTPX Client object used to build requests.

        Provides base features such as base url, headers and logger

        Arguments:
            BASE_URL (str): The Base URL, acquired from configurations module.
            self.logger (logging.Logger): Logger object used to log activities.
            self.dummyjson_client (httpx.Client): Dummy HTTP Client object.
            self.request_hook_logger (function): Logger hook used to log requests.
            self.response_hook_logger (function): Logger hook used to log responses.
            policy (DefaultCookiePolicy): Local Variable. A default cookie policy for the Client.
            cookie_jar (CookieJar): Local Variable. A custom cookie jar for the Client that does
            not allow  cookies to be set.

        Example:
                dummyjson = DummyJsonBase()
                dummyjson.auth_client.authenticate("user","pass")
        """
        self.BASE_URL = config.base_url()
        self.logger = _logger(__name__)

        # Does not allow domains to write cookies. Purpose is to avoid the  client to be populated with cookies
        # that may affect negative tests with Cookies that contain auth parameters.
        policy = DefaultCookiePolicy(allowed_domains=[])
        cookie_jar = CookieJar(policy=policy)

        self.request_hook_logger = request_hook(self.logger)
        self.response_hook_logger = response_hook(self.logger)
        self.dummyjson_client = httpx.Client(base_url=self.BASE_URL,
                                             headers={'Content-Type': 'application/json'},
                                             event_hooks={"request": [self.request_hook_logger],  # Must be a list
                                                          "response": [self.response_hook_logger]},  # Must be list
                                             timeout=config.client_timeout,
                                             cookies=cookie_jar)

        # Clients
        # Authentication Clients:
        # General:
        self.auth_client = AuthClient(client=self.dummyjson_client, logger=self.logger)
        # Products Client
        self.products_client = ProductsClient(client=self.dummyjson_client, logger=self.logger)

    def close_client(self):
        self.dummyjson_client.close()
