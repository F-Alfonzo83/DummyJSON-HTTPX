import json
import logging
from json import JSONDecodeError


def request_hook(logger: logging.Logger):
    """Closure function for logging HTTPX requests.

    Args:
        logger: (logging.Logger object) An instance of the logging Python  library

    Returns:
        log_requests: (function) Logging function
    """
    def logs_requests(request):
        SENSITIVE_REQUEST_VALUES = ["username", "password"]

        logger.debug(f"Request Hook : RM: {request.method} | RURL: {request.url}")
        # Check if the request contains a request body content
        if request.content:
            try:
                request_body = json.loads(request.content)
                curated_body = {key: ("***REDACTED***" if key in SENSITIVE_REQUEST_VALUES else value)
                                for key, value in request_body.items()}
                logger.debug(f"Request Hook: RB: {curated_body}")
            except JSONDecodeError:
                logger.warning("Request Body is not JSON")
    return logs_requests


def response_hook(logger: logging.Logger):
    """Closure function for logging HTTPX responses.

    Args:
        logger: (logging.Logger object) An instance of the logging Python  library

    Returns:
        log_response: (function) Logging function
    """
    def logs_responses(response):
        response.read()

        if response.status_code >= 500:
            logger.error(f"Response Hook : RC: {response.status_code} | REL {response.elapsed.total_seconds()}"
                         f"\nMessage: 500 Level Error")

        elif response.status_code >= 400:
            logger.warning(f"Response Hook : RC: {response.status_code} | REL {response.elapsed.total_seconds()}"
                           f"\nMessage: 400 Level Error: Check request / parameters")

        else:
            logger.debug(f"Response Hook : RC: {response.status_code} | REL {response.elapsed.total_seconds()}")

    return logs_responses
