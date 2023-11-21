import os
import datetime

def create_log_file_name(logs_dir="logs"):
    """
    Creates a log file name for script actions in the logs directory.

    :param logs_dir: The directory to store log files.
    :return: The full path to the script actions log file.
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    logs_path = os.path.join(script_dir, logs_dir)

    # Create logs directory if it doesn't exist
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

    return os.path.join(logs_path, "script_actions.log")

def log_action(log_file_path, message):
    """
    Logs an action related to the script.

    :param log_file_path: Path to the script log file.
    :param message: Message to log.
    """
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
