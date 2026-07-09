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
        json_body = {
            "username": username,
            "password": password,
            "expiresInMins": expires_in_mins
        }
        self.logger.info("Authenticating")
        response = self.client.post(f"/{config.login_url()}", json=json_body)
        response.raise_for_status()
        self.auth_token_request_time = time.time()
        self.auth_token_expires_in = expires_in_mins
        return response
