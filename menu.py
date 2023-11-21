import configparser
import subprocess
import os

CONFIG_FILE = 'config.cfg'
MAIN_APP_SCRIPT = 'main_app.py'

def read_config():
    """ Reads the configuration file and returns a ConfigParser object. """
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def write_config(config):
    """ Writes the modified configuration back to the file. """
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def run_sync():
    """ Executes the main_app.py script to perform file synchronization. """
    subprocess.run(['python', MAIN_APP_SCRIPT])

def change_config():
    """ Allows the user to change settings in the configuration file. """
    config = read_config()

    while True:
        config_options = list()

        # Collect configuration settings and display them as numbered options
        print("\nConfiguration Menu:")
        for section in config.sections():
            for setting in config[section]:
                config_options.append((section, setting))
                print(f"{len(config_options)}) {section}.{setting}: {config[section][setting]}")
        print(f"{len(config_options) + 1}) Return to main menu")

        choice = input("Select a number to change the setting or return: ")

        # Handle return to main menu
        if choice == str(len(config_options) + 1):
            break

        # Validate and process the choice
        if choice.isdigit() and 1 <= int(choice) <= len(config_options):
            section, setting = config_options[int(choice) - 1]
            new_value = input(f"Enter new value for {section}.{setting} (current: {config[section][setting]}): ")
            config[section][setting] = new_value
            write_config(config)
            print(f"{section}.{setting} updated to {new_value}. Configuration updated.\n")
        else:
            print("Invalid choice. Please try again.")

def show_main_menu():
    """ Shows the main interactive menu for the user to choose actions. """
    while True:
        print("\nMain Menu:")
        print("1) Run File Synchronization")
        print("2) Change Configuration Settings")
        print("9) Exit")

        choice = input("Enter your choice (or '9' to exit): ")

        if choice == '1':
            run_sync()
        elif choice == '2':
            change_config()
        elif choice == '9':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    show_main_menu()
