import time
from sync_logic import perform_sync

def run_sync_loop(sync_config, logger):
    """
    This function maintains a loop that repeatedly synchronizes directories
    and waits a specified interval before re-syncing.
    """
    try:
        while True:
            logger.info(f"Performing synchronization from {sync_config.source} to {sync_config.target}")
            perform_sync(sync_config.source, sync_config.target, logger)
            logger.info(f"Synchronization completed successfully. Waiting {sync_config.interval} seconds until next sync.")
            time.sleep(sync_config.interval)
    except KeyboardInterrupt:
        logger.info("Synchronization process was manually interrupted by the user.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
