# Rclone Sync Utility

This Python utility syncs files from a specified local directory to a Google Drive folder using Rclone. It's designed to run at regular intervals, checking if files have already been uploaded before syncing.

## Features

- **Sync Files to Google Drive**: Syncs files from a specified local directory to a Google Drive folder.
- **Incremental Sync**: Only uploads files that have been modified since the last upload, based on file modification times.
- **Regular Intervals**: Runs the sync operation at configurable intervals.
- **Avoids Unnecessary Uploads**: Checks if a file already exists in the remote directory and skips uploading if it's up to date.
- **Rclone Installation Check**: Verifies the presence of the Rclone executable before attempting to sync.
- **Error Logging**: Logs errors and operations related to Rclone and the script itself in separate log files.
- **Configurable**: All key parameters, such as paths and intervals, can be configured in a `config.cfg` file.

## Configuration

Edit `config.cfg` to set up the utility:

- `[Rclone]` section for the Rclone executable path.
- `[Files]` section to specify the local directory containing files to be uploaded.
- `[Remote]` section to set the Google Drive folder for syncing.
- `[Schedule]` to set the interval for running the sync operation.

Example `config.cfg`:

[Rclone]
# Path to the Rclone executable
RCLONE_EXECUTABLE = C:\\rclone-v1.64.2\\rclone.exe

[Files]
# Directory where the files to be uploaded are located
UPLOAD_DIRECTORY = E:\\Git\\Test upload files\\

[Remote]
# Remote directory in Google Drive to sync the files
REMOTE_DIR = rclone_test

[Schedule]
# Interval in minutes to run the sync operation (default is 5 minutes)
SYNC_INTERVAL_MINUTES = 5

Usage
To use the utility, run main_app.py with Python. The script will handle file syncing based on the configured settings.

```python
python main_app.py
```
Logs
script_actions.log: Logs script operations, configuration status, and other script-related activities.
rclone_errors.log: Captures Rclone command outputs and errors (created only when relevant data exists).

Technical Details
Datetime Handling: The script standardizes datetime objects to naive (timezone-unaware) for consistent file modification time comparisons.
Rclone Commands: Utilizes Rclone for file operations, requiring correct configuration and path specification.
File Comparison: Compares local and remote files based on names and modification times to determine the necessity of syncing.
