# Dropbox Uploader

A simple script to archive the contents of a folder and upload it to dropbox.

[![License](https://img.shields.io/github/license/ItsMestro/dropbox-uploader "License")](/LICENSE) [![Discord Server](https://discordapp.com/api/guilds/128856147162562560/widget.png?style=shield "Discord Server")](https://discord.mestro.cc)  
[![Latest Version](https://img.shields.io/github/v/release/ItsMestro/dropbox-uploader?label=Latest%20Version "Latest Version")](https://github.com/ItsMestro/dropbox-uploader/releases/latest)
 ![Total Downloads](https://img.shields.io/github/downloads/ItsMestro/dropbox-uploader/DropboxUploader.exe?label=Downloads "Total Downloads")

---

## Installation

### Run with Python

Clone the repository:

```shell
git clone https://github.com/ItsMestro/dropbox-uploader
cd dropbox-uploader
```

Run the script to generate the sample config:

```shell
python dropbox-uploader.py
```

In case of errors due to missing dependencies, install them using pip:

```shell
pip install missing-package
```

### Run with pre-built binaries

Binaries are currently only built for **Windows**.

Grab the latest version **[here](https://github.com/ItsMestro/dropbox-uploader/releases/latest)**

After running the program for the first time a sample config is generated.

---

## dbu-config.yml

The program will check for a `dbu-config.yml` file in the working directory and creates a sample file if not found.

- `source_folder` - A path on disk that should point to the folder with the files that should be archived.
  - The path can either be relative or absolute.
- `zip_name` - The name of the resulting zip file to be uploaded.
- `dropbox_path` - Location in Dropbox to upload the file to.
- `access_token` - The access token for a Dropbox app
  - The app can be created at [Dropbox App Console](https://www.dropbox.com/developers/apps)
    - Go to **Create app**
    - Select `Scoped access` and `Full Dropbox`
    - Name the app whatever you want
    - Go into **Permissions** and enable `files.content.write`
    - Go back to **Settings** and click `Generate` on **Generated access token** to acquire your access token

---

## License

The code of this repository is licensed under the [MIT licence](https://opensource.org/licenses/MIT). Please see [the license file](LICENSE) for more information. [tl;dr](https://tldrlegal.com/license/mit-license) you can do whatever you want as long as you include the original copyright and license notice in any copy of the software/source.

This however *does not cover* the usage of the "Nanolight" branding in any software, resources, advertising or promotion as this is protected by trademark law.
