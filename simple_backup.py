import configparser
import os
import shutil
from datetime import datetime

def read_config(file_path):
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

def list_sources(sources):
    print("Available sources to backup:")
    for idx, (name, path) in enumerate(sources.items(), start=1):
        print(f"{idx}. {name} ({path})")

def select_source(sources):
    while True:
        try:
            choice = int(input("Select a source to backup (number): "))
            if 1 <= choice <= len(sources):
                return list(sources.items())[choice - 1]
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def backup_source(source_name, source_path, backup_destination):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(backup_destination, source_name, timestamp)
    os.makedirs(backup_dir, exist_ok=True)
    shutil.copytree(source_path, os.path.join(backup_dir, os.path.basename(source_path)))
    print(f"Backup of {source_name} completed successfully.")

def main():
    config = read_config('setup.conf')
    backup_destination = config['backup']['BACKUP_DESTINATION']
    sources = parse_sources(config)
    
    list_sources(sources)
    source_name, source_path = select_source(sources)
    backup_source(source_name, source_path, backup_destination)

if __name__ == "__main__":
    main()
