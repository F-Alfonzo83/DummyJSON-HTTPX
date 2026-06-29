import logging
import httpx
from configurations.config_loader import ConfigLoader

config = ConfigLoader()

class AuthClient:
    def __init__(self, logger: logging.Logger, client: httpx.Client):
        self.client = client
        self.logger = logger

    def authenticate(self, username:str, password:str, expires_in_mins:int = 60):
        json_body = {
            "username": username,
            "password": password,
            "expiresInMins": expires_in_mins
                    }
        self.logger.info("Authenticating")
        response = self.client.post(f"/{config.login_url()}", json=json_body)
        response.raise_for_status()
        return response

