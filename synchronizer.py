import time
from sync_logic import perform_sync

def synchronize_directories(args, logger):
    """This function maintains a loop that repeatedly synchronizes directories
    and waits a specified interval before re-syncing."""
    try:
        while True:
            logger.info(f"Performing synchronization from {args.source} to {args.target}")
            perform_sync(args.source, args.target, logger)
            logger.info(f"Synchronization completed successfully. Waiting {args.interval} seconds until next sync.")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        logger.info("Synchronization process was manually interrupted by the user.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
