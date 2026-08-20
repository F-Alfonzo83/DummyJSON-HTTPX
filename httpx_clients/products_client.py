import logging
import httpx
from configurations.config_loader import ConfigLoader

config = ConfigLoader()


class ProductsClient:
    def __init__(self, client: httpx.Client, logger: logging.Logger):
        self.client = client
        self.logger = logger

    def get_all_products(self, limit: int = None, skip: int = None, select: str = None,
                         sortBy: str = None, order: str = None) -> httpx.Response:

        # Grab Arguments passed to the Function
        parameter_candidates = {"limit": limit, "skip": skip, "select": select,
                                "sortBy": sortBy, "order": order}
        # Filter out arguments
        params = {key: value for key, value in parameter_candidates.items() if value is not None}

        response = self.client.get(f"/{config.products_url().lstrip('/')}",
                                   params=params)
        return response

    def get_product_by_id(self, product_id: int) -> httpx.Response:
        response = self.client.get(f"/{config.products_url().lstrip('/')}/{product_id}")
        return response

    def search_products(self, search_term: str) -> httpx.Response:
        response = self.client.get(f"/{config.products_search_url().lstrip('/')}",
                                   params={"q": search_term})
        return response

    def get_all_products_categories(self) -> httpx.Response:
        response = self.client.get(f"/{config.products_categories_url().strip('/')}")
        return response

    def get_product_category_list(self) -> httpx.Response:
        response = self.client.get(f"/{config.products_category_list_url().lstrip('/')}")
        return response

    def get_product_category(self, category: str) -> httpx.Response:
        response = self.client.get(f"/{config.products_category_url().lstrip('/')}/{category}")
        return response

    def add_product(self, title: str | None = None, description: str | None = None, category: str | None = None,
                    price: float | None = None, stock: int | None = None, **kwargs) -> httpx.Response:

        parameters_received = locals()
        request_body = {key: value for key, value in parameters_received.items(
        ) if value is not None and key != "self" and key != "kwargs"}
        request_body.update(kwargs)

        response = self.client.post(f"/{config.products_add_product_url().lstrip('/')}",
                                    json=request_body)
        return response
