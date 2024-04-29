import logging

def setup_logging(log_file='logs/synchronization.log'):
    # Get an existing logger or create a new one if it doesn't exist.
    logger = logging.getLogger('sync_logger')
    
    # Prevent adding multiple handlers to the logger if it's already set up.
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # File handler to log messages into a file.
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Console handler to output messages to the standard output.
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Higher threshold to avoid cluttering the console with debug messages.

        # Define output formats for each handler.
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)

        # Attach handlers to the logger.
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
