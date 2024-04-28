import os

def validate_directory(path, logger, is_source=False):
    """Check if the directory exists and log if it does not."""
    if not os.path.exists(path):
        if is_source:
            logger.error(f"Source directory does not exist: {path}")
        else:
            logger.error(f"Target directory does not exist: {path}")
        return False
    return True