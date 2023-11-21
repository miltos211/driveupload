import subprocess  # Used to execute shell commands (Rclone in this case)
import os           # Provides functions for interacting with the operating system
import datetime     # Used for working with dates and times
import time         # Used for scheduling the script to run at intervals
from log_helper import create_log_file_name, log_action  # Importing logging functions
import configparser # Used for reading configuration files
import json         # Used for parsing JSON data

# Read configuration from config.cfg
config = configparser.ConfigParser()
config_file = "config.cfg"
config.read(config_file)

# Extracting configuration values
RCLONE_EXECUTABLE = config.get('Rclone', 'RCLONE_EXECUTABLE', fallback="rclone.exe")
UPLOAD_DIRECTORY = config.get('Files', 'UPLOAD_DIRECTORY', fallback="E:\\Git\\Test upload files\\")
REMOTE_DIR = config.get('Remote', 'REMOTE_DIR', fallback="rclone_test")
SYNC_INTERVAL_MINUTES = config.getint('Schedule', 'SYNC_INTERVAL_MINUTES', fallback=5)

def log_config_status(log_file_path, config_exists, config_file):
    """
    Logs the status of the configuration file.
    """
    if config_exists:
        log_action(log_file_path, f"Config file '{config_file}' exists and was read successfully.")
    else:
        log_action(log_file_path, f"Config file '{config_file}' not found. Using default settings.")

def get_file_info(local_path):
    """
    Gets the file size and last modified time of the given file.
    """
    file_size = os.path.getsize(local_path)
    last_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(local_path)).strftime('%Y-%m-%d %H:%M:%S')
    return file_size, last_modified_time

def is_rclone_installed(executable_path, log_file_path):
    """
    Checks if Rclone is installed at the given executable path and logs the outcome.
    """
    if os.path.isfile(executable_path):
        log_action(log_file_path, f"Rclone executable found at {executable_path}")
        return True
    else:
        log_action(log_file_path, f"Rclone executable not found at {executable_path}")
        return False

def get_remote_file_list(executable_path, remote_dir):
    """
    Retrieves the list of files and their last modified times from the remote directory.
    """
    full_remote_path = f"gdrive:{remote_dir}"
    try:
        result = subprocess.run([executable_path, "lsjson", full_remote_path], capture_output=True, text=True, check=True)
        file_list = json.loads(result.stdout)
        # Convert to naive datetime objects by removing timezone
        return {file['Path']: datetime.datetime.fromisoformat(file['ModTime']).replace(tzinfo=None) for file in file_list}
    except subprocess.CalledProcessError as e:
        log_action(log_file_path, f"Error fetching remote file list: {e}")
        return {}

def sync_file(file_path, log_file_path, executable_path, remote_dir, file_mtime):
    """
    Syncs a single file to the remote directory.
    """
    file_size, _ = get_file_info(file_path)
    log_action(log_file_path, f"Syncing file: {file_path} (Size: {file_size} bytes, Last Modified: {file_mtime})")

    rclone_log_file = os.path.join(os.path.dirname(log_file_path), "rclone_errors.log")

    if not is_rclone_installed(executable_path, log_file_path):
        return

    try:
        command = [executable_path, "copy", file_path, f"gdrive:{remote_dir}", "--log-file", rclone_log_file]
        subprocess.run(command, shell=True, check=True, text=True)
        log_action(log_file_path, f"Command executed successfully: {' '.join(command)}")
    except subprocess.CalledProcessError as e:
        error_message = f"An error occurred: {str(e)}"
        log_action(log_file_path, f"Command failed: {' '.join(command)}\nError: {error_message}")

def sync_directory(local_directory, log_file_path, executable_path, remote_dir):
    """
    Syncs all files in a local directory with the specified directory in Google Drive.
    """
    if not os.path.isdir(local_directory):
        log_action(log_file_path, f"Directory {local_directory} does not exist. Skipping sync.")
        return

    remote_files = get_remote_file_list(executable_path, remote_dir)

    for filename in os.listdir(local_directory):
        file_path = os.path.join(local_directory, filename)
        if os.path.isfile(file_path):
            file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

            if filename not in remote_files or file_mtime > remote_files.get(filename, datetime.datetime.min):
                sync_file(file_path, log_file_path, executable_path, remote_dir, file_mtime)
            else:
                log_action(log_file_path, f"File {filename} is up-to-date. Skipping.")

def main():
    script_log_file = create_log_file_name()
    config_exists = os.path.exists(config_file)
    log_config_status(script_log_file, config_exists, config_file)

    while True:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{current_time} - Sync running."
        print(log_message)
        log_action(script_log_file, log_message)

        sync_directory(UPLOAD_DIRECTORY, script_log_file, RCLONE_EXECUTABLE, REMOTE_DIR)

        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{current_time} - Sync completed. Waiting for next sync in {SYNC_INTERVAL_MINUTES} minutes."
        print(log_message)
        log_action(script_log_file, log_message)

        time.sleep(SYNC_INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    main()
