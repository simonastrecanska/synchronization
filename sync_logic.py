import os
import shutil
import atexit
from concurrent.futures import ThreadPoolExecutor
import json

def get_mod_time(path):
    # Return the last modification time of a file or directory.
    return os.path.getmtime(path)

def load_mod_log():
    # Load the synchronization log from JSON file.
    mod_log_path = os.path.join(os.path.dirname(__file__), 'logs', 'sync_mod_log.json')
    if os.path.exists(mod_log_path):
        with open(mod_log_path, 'r') as f:
            return json.load(f)
    return {}

def save_mod_log(mod_log):
    # Save the current state of the synchronization log to a JSON file.
    mod_log_path = os.path.join(os.path.dirname(__file__), 'logs', 'sync_mod_log.json')
    with open(mod_log_path, 'w') as f:
        json.dump(mod_log, f)

def delete_mod_log():
    # Remove the synchronization log file when the program terminates.
    mod_log_path = os.path.join(os.path.dirname(__file__), 'logs', 'sync_mod_log.json')
    try:
        os.remove(mod_log_path)
    except OSError as e:
        print(f"Error: {e.strerror}")

# Ensure the synchronization log is cleaned up at program exit.
atexit.register(delete_mod_log)

def copy_file_or_directory(src_path, dest_path, logger):
    try:
        if os.path.islink(src_path):
            # Handle symbolic links separately to ensure they link correctly without copying the data.
            link_target = os.readlink(src_path)
            if os.path.exists(dest_path):
                os.remove(dest_path)
            os.symlink(link_target, dest_path)
            logger.info(f"Created symlink: {dest_path} -> {link_target}")
        elif os.path.isdir(src_path):
            # Ensure directories are created if they don't exist in the target.
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
                logger.info(f"Created directory: {dest_path}")
        else:
            # Copy files from source to destination.
            shutil.copy2(src_path, dest_path)
            logger.info(f"Copied file: {src_path} to {dest_path}")
    except Exception as e:
        logger.error(f"Failed to copy {src_path} to {dest_path}: {str(e)}")

def compare_and_sync_files(source, target, logger, mod_log):
    with ThreadPoolExecutor() as executor:
        future_to_file = {}
        # Walk through the source directory and prepare to synchronize each item.
        for root, dirs, files in os.walk(source):
            for name in dirs + files:
                src_path = os.path.join(root, name)
                dest_path = os.path.join(target, rel_path)
                future = executor.submit(copy_file_or_directory, src_path, dest_path, logger)
                future_to_file[future] = (src_path, dest_path)

        for future in future_to_file:
            src_path, dest_path = future_to_file[future]
            try:
                future.result()
            except Exception as e:
                logger.error(f"Error processing {src_path}: {str(e)}")

def delete_extra_files(source, target, logger, mod_log):
    # Remove any files or directories in the target that are not present in the source.
    for root, dirs, files in os.walk(target, topdown=False):
        for name in dirs + files:
            target_path = os.path.join(root, name)
            if not os.path.exists(os.path.join(source, os.path.relpath(target_path, target))):
                try:
                    if os.path.isdir(target_path):
                        shutil.rmtree(target_path)
                    else:
                        os.remove(target_path)
                    logger.info(f"Removed {target_path}")
                except Exception as e:
                    logger.error(f"Failed to remove {target_path}: {str(e)}")

def perform_sync(source, target, logger):
    logger.info("Starting synchronization process...")
    mod_log = load_mod_log()
    compare_and_sync_files(source, target, logger, mod_log)
    delete_extra_files(source, target, logger, mod_log)
    save_mod_log(mod_log)
    logger.info("Synchronization complete.")
