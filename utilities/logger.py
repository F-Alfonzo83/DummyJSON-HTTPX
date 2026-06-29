import logging

def _logger(name):

    #Instantiate the Logger
    logger = logging.getLogger(name)
    # Set General Level of the  Logger
    logger.setLevel(logging.DEBUG)

    #Create Handler
    console_handler = logging.StreamHandler()
    # Create Formatter
    logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Set Formatter
    console_handler.setFormatter(logger_formatter)
    #Set Log Level for Handler
    console_handler.setLevel(logging.DEBUG)
    #Add Handler to Logger.
    logger.addHandler(console_handler)
    #Return the Logger
    return logger