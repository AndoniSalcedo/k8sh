#!/usr/bin/env python3

import requests
import subprocess
import zipfile
from io import BytesIO
import os
import shutil
import sys

script_path = os.path.dirname(os.path.abspath(__file__))

github_user = "AndoniSalcedo"
repository = "k8sh"
# launcher_version_file = '/path/to/launcher_version.txt'
application_version_file = os.path.join(script_path, "../application_version.txt")
application_path = os.path.join(script_path, "../app")
# temp_path = '/temporary/path/for/update'


# Utility functions
def get_latest_github_version(item_type):
    url = f"https://api.github.com/repos/{github_user}/{repository}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if item_type == "launcher":
            return data[
                "tag_name"
            ]  # Assumes the release tag includes the launcher version
        elif item_type == "application":
            return data["tag_name"], data["zipball_url"]
    return None, None


def read_current_version(item_type):
    version_file = (
        launcher_version_file if item_type == "launcher" else application_version_file
    )
    try:
        with open(version_file, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "0.0.0"  # Default version if the file is not found


def update_version(item_type, new_version):
    version_file = (
        launcher_version_file if item_type == "launcher" else application_version_file
    )
    with open(version_file, "w") as file:
        file.write(new_version)


def download_and_extract_zip(zip_url, destination_path):
    response = requests.get(zip_url)
    if response.status_code == 200:
        zip_in_memory = BytesIO(response.content)
        with zipfile.ZipFile(zip_in_memory) as zip_ref:
            members = zip_ref.namelist()
            for member in members:
                adjusted_path = os.path.join(
                    destination_path, "/".join(member.split("/")[1:])
                )
                if member.endswith("/"):
                    os.makedirs(adjusted_path, exist_ok=True)
                else:

                    with zip_ref.open(member) as source, open(
                        adjusted_path, "wb"
                    ) as target:
                        shutil.copyfileobj(source, target)

        return True
    else:
        return False


def update_if_needed():

    current_application_version = read_current_version("application")
    new_application_version, zip_url_application = get_latest_github_version(
        "application"
    )
    if (
        new_application_version
        and new_application_version != current_application_version
    ):
        # Update application
        print("Updating application...")
        if download_and_extract_zip(zip_url_application, application_path):
            update_version("application", new_application_version)

            subprocess.run(
                [
                    "pip3",
                    "install",
                    "-r",
                    os.path.join(application_path, "requirements.txt"),
                ]
                + sys.argv[1:]
            )

            print("Application updated.")


def main():
    update_if_needed()

    subprocess.run(
        ["python3", os.path.join(application_path, "init.py")] + sys.argv[1:]
    )


if __name__ == "__main__":
    main()
