#!/usr/bin/env python3

import os
import tarfile
from datetime import datetime
import argparse

def validate_directory(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Directory '{path}' does not exist.")
    if not os.path.isdir(path):
        raise NotADirectoryError(f"'{path}' is not a directory.")

def create_archive(log_dir, archive_dir):
    os.makedirs(archive_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    archive_name = f"logs_{timestamp}.tar.gz"
    archive_path = os.path.join(archive_dir, archive_name)

    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(log_dir, arcname=os.path.basename(log_dir))
    return archive_path

def log_operation(archive_path, log_file_path):
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    log_message = f"{datetime.now()} - Archived: {archive_path}\n"
    with open(log_file_path, "a") as log_file:
        log_file.write(log_message)

def main():
    parser = argparse.ArgumentParser(description="Log Archive Tool")
    parser.add_argument("log_directory", help="Path to the log directory to archive")
    parser.add_argument("--archive_dir", default="../archives", help="Path to store archives")
    parser.add_argument("--log_file", default="../logs/archive.log", help="Path for the log file")
    args = parser.parse_args()

    log_dir = args.log_directory
    archive_dir = args.archive_dir
    log_file_path = args.log_file

    try:
        validate_directory(log_dir)
        archive_path = create_archive(log_dir, archive_dir)
        print(f"Logs archived successfully to {archive_path}")
        log_operation(archive_path, log_file_path)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
