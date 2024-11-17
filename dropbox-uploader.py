import json
import os
import sys
import zipfile
from pathlib import Path

import requests
import yaml


def input_prompt(text="Press any key to exit..."):
    if os.name == "nt":
        os.system("pause")
    else:
        os.system(f'read -n1 -r -p "{text}"')


UPLOAD_URL = "https://content.dropboxapi.com/2/files/upload"

DEFAULT_YAML = """
# Any files within this folder will be put inside the zip archive
# This can be relative or absolute
# Is by default relative to script location
source_folder: ./dist

# The name of the resulting zip file to be uploaded
zip_name: My Zip File

# Folder for the uploaded file in dropbox
# This is the root folder by default
# If the file already exists it will be replaced by the new version and keep any sharing settings
dropbox_path: /

# Generated Access Token for app
# Can be created and found at https://www.dropbox.com/developers/apps
#
# Go to "Create app"
# Choose "Scoped access" > "Full Dropbox" and give the app whatever name you want
# Go into "Permissions" and enable "files.content.write"
# Back in "Settings" click "Generate" on "Generated access token" and place it below instead of the placeholder text
access_token: token-here
"""

path = None

if getattr(sys, "frozen", False):
    path = Path(sys.executable).resolve()
elif __file__:
    path = Path(__file__).resolve()
else:
    print("Error trying to get script path")
    input_prompt()
    sys.exit()

yaml_config = path.with_name("dbu-config.yml")

if not yaml_config.exists():
    with yaml_config.open("w+") as file:
        file.write(DEFAULT_YAML)

    print(f'Created "{yaml_config.name}" in the same folder as this program')
    print("Configure those settings and run this program again")
    input_prompt()

    sys.exit()

try:
    with yaml_config.open("r") as file:
        config = yaml.safe_load(file)
except Exception as e:
    print("Error when trying to load config")
    print(e)
    input_prompt()

    sys.exit()

if not isinstance(config, dict):
    print("Config file is malformed")
    input_prompt()

    sys.exit()

if source_folder := config.get("source_folder", False):
    source_path = Path(source_folder).resolve()
    if not source_path.exists():
        print(
            'The value for "source_folder" in the config is not a valid path or does not exist'
        )
        input_prompt()
        sys.exit()
else:
    print('Config file is missing "source_folder"')
    input_prompt()
    sys.exit()

if name := config.get("zip_name", False):
    zip_name = f'{name[:-4] if name.endswith(".zip") else name}.zip'
    archive_path = path.with_name(zip_name)
else:
    print('Config file is missing "zip_name"')
    input_prompt()
    sys.exit()

if dropbox_folder := config.get("dropbox_path", False):
    if dropbox_folder.startswith("./"):
        dropbox_folder = dropbox_folder[-1:]
    dropbox_path = Path(dropbox_folder).joinpath(zip_name)
else:
    print('Config file is missing "dropbox_path"')
    input_prompt()
    sys.exit()

if token := config.get("access_token"):
    access_token = token
    if access_token == "token-here" or access_token == "":
        print(
            "Make sure to follow the instructions on adding your access token in the config file!"
        )
        input_prompt()
        sys.exit()
else:
    print('Config file is missing "access_token"')
    input_prompt()
    sys.exit()


try:
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zip:
        for file in source_path.rglob("*"):
            zip.write(file, file.relative_to(source_path))

    with requests.Session() as session:
        params = {
            "mode": "overwrite",
            "mute": True,
            "path": dropbox_path.as_posix(),
        }
        session.headers.update(
            {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/octet-stream",
                "Dropbox-API-Arg": json.dumps(params),
            }
        )

        with archive_path.open("rb") as payload:
            response = session.post(url=UPLOAD_URL, data=payload)

        try:
            archive_path.unlink()
        except:
            print(
                "Warning: Unable to remove .zip archive for cleanup. Will continue anyways"
            )

        if not (response.ok):
            print("Upload Failed!")
            print(f"{response.status_code} {response.reason}")
            print(response.text)
            input_prompt()
            sys.exit()

        print(response.json())
        print("File uploaded successfully!")
        input_prompt()
except Exception as e:
    try:
        archive_path.unlink()
    except:
        pass
    print("Unexpected error occured. Bonk Nano!")
    print(e)
    input_prompt()
