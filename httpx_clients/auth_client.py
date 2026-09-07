import json
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

    def authenticate(self, username: str, password: str, expires_in_mins: int | None = 60):
        json_body = {
            "username": username,
            "password": password,
            "expiresInMins": expires_in_mins
        }
        self.logger.info("Authenticating")
        response = self.client.post(f"/{config.login_url()}", json=json_body)
        self.retrieve_auth_token(response)
        return response

    def retrieve_auth_token(self, auth_response: httpx.Response) -> str | None:
        if auth_response.status_code == 200:
            self.auth_token_request_time = time.time()
            self.auth_token_expires_in = json.loads(auth_response.request.content)['expiresInMins']
            self.auth_token = auth_response.json()["accessToken"]
            return self.auth_token
        else:
            logging.error("Authentication failed")
            self.auth_token = None
            return None
