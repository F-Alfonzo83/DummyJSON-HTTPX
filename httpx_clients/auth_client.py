import logging
import time
import httpx
from configurations.config_loader import ConfigLoader

config = ConfigLoader()


class AuthClient:
    def __init__(self, logger: logging.Logger,
                 client: httpx.Client) -> None:
        self.client = client
        self.logger = logger
        # Class Attributes
        self.auth_token = None
        self.auth_token_request_time = None
        self.auth_token_expires_in = None

    def authenticate(self, username: str, password: str, expires_in_mins: int = 60):
        '''Authenticates to DummyJSON.

        The 'authenticate' method performs the call to the authentication endpoint, but does not guarantee
        a token. It's only purpose is to execute POST call to the endpoint. Returns  the response value
        whatever if positive or  negative.

        Args:
            username (str) : The username to authenticate
            password (str) : The password of the user
            expires_in_mins (int): Defaults to 60

        Returns:
            response: (httpx.Response) : Response object
        '''
        json_body = {
            "username": username,
            "password": password,
            "expiresInMins": expires_in_mins
        }
        self.logger.info("Authenticating")
        response = self.client.post(f"/{config.login_url()}", json=json_body)
        return response

    def retrieve_auth_token(self, username: str, password: str, expires_in_mins: int = 60) -> str:
        '''Retrieves the authentication token.

        Makes use of the authenticate method  and extracts the authentication token from the response.

        Args:
            username (str) : The username to authenticate
            password (str) : The password of the user
            expires_in_mins (int): Defaults to 60

        Raises:
            httpx.HTTPStatusError: Raises an error in case the authentication fails.

        Returns:
            (str) Authentication token
        '''

        auth_response = self.authenticate(username=username,
                                          password=password,
                                          expires_in_mins=expires_in_mins)
        auth_response.raise_for_status()

        self.auth_token = auth_response.json()["accessToken"]
        self.auth_token_request_time = time.time()
        self.auth_token_expires_in = expires_in_mins
        return self.auth_token
