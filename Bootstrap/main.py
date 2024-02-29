import requests
import subprocess
import zipfile
from io import BytesIO
import os
import shutil
import sys

github_user = 'AndoniSalcedo'
repository = 'k8sh'
#launcher_version_file = '/path/to/launcher_version.txt'
application_version_file = './application_version.txt'
application_path = './app'
#temp_path = '/temporary/path/for/update'

# Utility functions
def get_latest_github_version(item_type):
    url = f"https://api.github.com/repos/{github_user}/{repository}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if item_type == 'launcher':
            return data['tag_name']  # Assumes the release tag includes the launcher version
        elif item_type == 'application':
            return data['tag_name'], data['zipball_url']
    return None, None

def read_current_version(item_type):
    version_file = launcher_version_file if item_type == 'launcher' else application_version_file
    try:
        with open(version_file, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return '0.0.0'  # Default version if the file is not found

def update_version(item_type, new_version):
    version_file = launcher_version_file if item_type == 'launcher' else application_version_file
    with open(version_file, 'w') as file:
        file.write(new_version)

def download_and_extract_zip(zip_url, destination_path):
    response = requests.get(zip_url)
    if response.status_code == 200:
        zip_in_memory = BytesIO(response.content)
        with zipfile.ZipFile(zip_in_memory) as zip_ref:
            members = zip_ref.namelist()
            for member in members:
                adjusted_path = os.path.join(destination_path, "/".join(member.split("/")[1:]))
                if member.endswith('/'):
                    os.makedirs(adjusted_path, exist_ok=True)
                else:
                    
                    with zip_ref.open(member) as source, open(adjusted_path, "wb") as target:
                        shutil.copyfileobj(source, target)
                        
        return True
    else:
        return False

# Update logic
def update_if_needed():
    """current_launcher_version = read_current_version('launcher')
    new_launcher_version, _ = get_latest_github_version('launcher')
     if new_launcher_version and new_launcher_version != current_launcher_version:
        # Update launcher
        print("Updating launcher...")
        if download_and_extract_zip(_, temp_path):  # Assumes you have a specific URL to download the launcher
            update_version('launcher', new_launcher_version)
            # Here you would add logic to overwrite the current launcher with the new one
            subprocess.Popen(["python", __file__])  # Restart the launcher
            exit() """

    current_application_version = read_current_version('application')
    new_application_version, zip_url_application = get_latest_github_version('application')
    if new_application_version and new_application_version != current_application_version:
        # Update application
        print("Updating application...")
        if download_and_extract_zip(zip_url_application, application_path):
            update_version('application', new_application_version)
            print("Application updated.")

# Launcher start
if __name__ == "__main__":
    update_if_needed()

    subprocess.run(["python", os.path.join(application_path, "main.py")]  + sys.argv[1:])
