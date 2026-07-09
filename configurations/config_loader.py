import sys
import yaml
from pathlib import Path

from urllib3.util.util import reraise


class ConfigLoader:

    URL_FILE_LOCATOR = Path(__file__).parent / "url_paths.yaml"

    try:
        with open(URL_FILE_LOCATOR, "r", encoding="utf-8") as yaml_file:
            url_path = yaml.safe_load(yaml_file)
    except FileNotFoundError as fnf_error:
        print(f"File {URL_FILE_LOCATOR} not found.\nSystem Error: {fnf_error}")
        sys.exit(1)
    except yaml.YAMLError as yaml_error:
        print(f"Error Loading /Parsing yaml file.\nSystem Error: {yaml_error}")
        sys.exit(1)

    def base_url(self):
        return self.url_path["dummy_json"]["testing_env"]["base_url"]

    def login_url(self):
        return self.url_path["dummy_json"]["testing_env"]["authenticate"]["login"]

    def products_url(self):
        return self.url_path["dummy_json"]["testing_env"]["products"]["base_products"]

    def products_search_url(self):
        return self.url_path["dummy_json"]["testing_env"]["products"]["search"]

    def products_categories_url(self):
        return self.url_path["dummy_json"]["testing_env"]["products"]["categories"]

    def products_category_list_url(self):
        return self.url_path["dummy_json"]["testing_env"]["products"]["category_list"]

    def products_category_url(self):
        return self.url_path["dummy_json"]["testing_env"]["products"]["category"]

    def products_add_product_url(self):
        return self.url_path["dummy_json"]["testing_env"]["products"]["add_product"]


# Testing Section

if __name__ == "__main__":
    loader = ConfigLoader()
    print(loader.base_url())
    print(loader.login_url())
    print(loader.products_url())
    print(loader.products_search_url())
    print(loader.products_categories_url())
    print(loader.products_category_list_url())
    print(loader.products_category_url())
    print(loader.products_add_product_url())
