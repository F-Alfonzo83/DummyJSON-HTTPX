import logging

def request_hook(logger: logging.Logger):
    """Closure function for logging HTTPX requests.

    Args:
        logger: (logging.Logger object) An instance of the logging Python  library

    Returns:
        log_requests: (function) Logging function
    """
    def logs_requests(request):
        logger.debug(f"Request Hook : RM: {request.method} | RURL: {request.url}")
        if request.content:
            logger.debug(f"Request Hook: RB : {request.content}")
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

