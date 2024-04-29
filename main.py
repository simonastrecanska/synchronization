import argparse
import os
from logger import setup_logging
from utils import validate_directory
from synchronizer import synchronize_directories

def parse_args():
    # Setup the argument parser
    parser = argparse.ArgumentParser(description="Synchronize two folders at regular intervals.")
    parser.add_argument('source', help='Source directory path')
    parser.add_argument('target', help='Target directory path')
    parser.add_argument('log_file', help='Log file path')
    parser.add_argument('interval', type=int, nargs='?', default=100, help='Synchronization interval in seconds (default: 300)')
    return parser.parse_args()

def main():
    args = parse_args()
    logger = setup_logging(args.log_file)

    if not validate_directory(args.source, logger, is_source=True):
        return
    if not validate_directory(args.target, logger):
        os.makedirs(args.target)
        logger.info(f"Target directory created: {args.target}")

    synchronize_directories(args, logger)

if __name__ == "__main__":
    main()
