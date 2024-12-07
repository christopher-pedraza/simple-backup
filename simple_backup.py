import configparser
import os
import shutil
import subprocess
import sys
from datetime import datetime

def create_default_config(file_path):
    config = configparser.ConfigParser()
    config['backup'] = {
        'BACKUP_DESTINATIONS': '\ndestination_name_1 = C:\\path\\to\\destination1\ndestination_name_2 = C:\\path\\to\\destination2',
        'SOURCES': '\nsource_name_1 = C:\\path\\to\\source1\nsource_name_2 = C:\\path\\to\\source2',
        'ALWAYS_BACKUP_ALL_SOURCES': 'False',
        'ALWAYS_BACKUP_TO_ALL_DESTINATIONS': 'False'
    }
    with open(file_path, 'w') as configfile:
        config.write(configfile)
    print(f"Default configuration file created at {file_path}")
    directory = os.path.dirname(os.path.abspath(file_path))
    subprocess.Popen(f'explorer "{directory}\\setup.conf"')
    print("Please modify the configuration file and restart the application.")
    input("Press ENTER to exit.")
    sys.exit()

def read_config(file_path):
    if not os.path.exists(file_path):
        create_default_config(file_path)
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def parse_sources(config):
    sources = {}
    for line in config['backup']['SOURCES'].splitlines():
        if '=' in line:
            name, path = line.split('=', 1)
            sources[name.strip()] = path.strip()
    return sources

def parse_destinations(config):
    destinations = {}
    for line in config['backup']['BACKUP_DESTINATIONS'].splitlines():
        if '=' in line:
            name, path = line.split('=', 1)
            destinations[name.strip()] = path.strip()
    return destinations

def list_sources(sources):
    print("Available sources to backup:")
    for idx, (name, path) in enumerate(sources.items(), start=1):
        print(f"{idx}. {name} ({path})")

def list_destinations(destinations):
    print("Available destinations for backup:")
    for idx, (name, path) in enumerate(destinations.items(), start=1):
        print(f"{idx}. {name} ({path})")

def select_source(sources, always_backup_all_sources):
    if always_backup_all_sources:
        return sources.items()
    while True:
        try:
            choice = int(input("Select a source to backup (number): "))
            if 1 <= choice <= len(sources):
                return [list(sources.items())[choice - 1]]
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def select_destination(destinations, always_backup_to_all_destinations):
    if always_backup_to_all_destinations:
        return destinations.items()
    while True:
        try:
            choice = int(input("Select a destination for backup (number): "))
            if 1 <= choice <= len(destinations):
                return [list(destinations.items())[choice - 1]]
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def backup_source(source_name, source_path, backup_destination, destination_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(backup_destination, source_name, timestamp)
    os.makedirs(backup_dir, exist_ok=True)
    shutil.copytree(source_path, os.path.join(backup_dir, os.path.basename(source_path)))
    print(f"Backup of {source_name} completed successfully to {destination_name} ({backup_dir})")

def main():
    config = read_config('setup.conf')
    sources = parse_sources(config)
    destinations = parse_destinations(config)
    
    always_backup_all_sources = config['backup'].getboolean('ALWAYS_BACKUP_ALL_SOURCES')
    always_backup_to_all_destinations = config['backup'].getboolean('ALWAYS_BACKUP_TO_ALL_DESTINATIONS')
    
    list_sources(sources)
    selected_sources = select_source(sources, always_backup_all_sources)
    
    list_destinations(destinations)
    selected_destinations = select_destination(destinations, always_backup_to_all_destinations)
    
    for source_name, source_path in selected_sources:
        for destination_name, backup_destination in selected_destinations:
            backup_source(source_name, source_path, backup_destination, destination_name)

if __name__ == "__main__":
    main()
