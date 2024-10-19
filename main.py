import os
from functions.discord_handler import start_discord_bot

# Constants for GitHub repository ZIP download
GITHUB_REPO_ZIP_URL = "https://github.com/YourUsername/YourRepo/archive/refs/heads/main.zip"
UPDATE_STATUS_FILE = "update_status.txt"
LOCAL_FUNCTIONS_PATH = os.path.join(os.getcwd(), "functions")
TEMP_ZIP_PATH = os.path.join(os.getcwd(), "repo_update.zip")

allowed_users = ["border", "bob", "User"]

def check_update_status():
    if os.path.exists(UPDATE_STATUS_FILE):
        with open(UPDATE_STATUS_FILE, "r") as f:
            status = f.read().strip()
            if status == "update=true":
                return True
    return False

def reset_update_flag():
    with open(UPDATE_STATUS_FILE, "w") as f:
        f.write("update=false")

def download_and_update_files():
    print("Checking for updates from GitHub...")

    # Lazy import the required modules for the update process
    import requests
    import zipfile
    import os

    # Download the GitHub repository ZIP file directly to disk
    response = requests.get(GITHUB_REPO_ZIP_URL, auth=("your_username", "your_token"))
    
    if response.status_code == 200:
        # Save the ZIP file to a temporary location
        with open(TEMP_ZIP_PATH, "wb") as temp_zip:
            temp_zip.write(response.content)
        print("Downloaded latest code from GitHub.")

        # Extract only the /functions directory from the ZIP file
        with zipfile.ZipFile(TEMP_ZIP_PATH, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                # Process only files inside the /functions directory
                if file_info.filename.startswith("YourRepo-main/functions/") and not file_info.is_dir():
                    file_name = os.path.basename(file_info.filename)
                    local_file_path = os.path.join(LOCAL_FUNCTIONS_PATH, file_name)

                    # If new or updated, write the file to disk
                    if not os.path.exists(local_file_path) or zip_ref.read(file_info) != open(local_file_path, 'rb').read():
                        with open(local_file_path, "wb") as file:
                            file.write(zip_ref.read(file_info))
                        print(f"Updated: {file_name}")

        # Clean up: delete the temporary ZIP file
        os.remove(TEMP_ZIP_PATH)

    else:
        print(f"Failed to download repo. Status code: {response.status_code}")

def evasion():
    print("hello vro <3")

def main():
    username = os.getlogin()
    if username in allowed_users:
        if check_update_status():
            download_and_update_files()
            reset_update_flag()
        else:
            print("No update flag set. Proceeding without update.")
    else:
        evasion()
        return

    start_discord_bot()

if __name__ == "__main__":
    main()
