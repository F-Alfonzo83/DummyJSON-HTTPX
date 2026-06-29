import logging
import httpx
from configurations.config_loader import ConfigLoader

config = ConfigLoader()


class ProductsClient:
    def __init__(self, client: httpx.Client, logger: logging.Logger):
        self.client = client
        self.logger = logger

    def get_all_products(self) -> httpx.Response:
        response = self.client.get(f"/{config.products_url().lstrip('/')}")
        return response

    def get_product_by_id(self, product_id: str) -> httpx.Response:
        response = self.client.get(f"/{config.products_url().lstrip('/')}/{product_id}")
        return response
