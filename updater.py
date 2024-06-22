# Updater for Eatventure-Bot: https://github.com/CaptainDeathead/Eatventure-Bot

"""
DO NOT MODIFY THIS CODE AS IT MAY BREAK YOUR INSTALL
----------------------------------------------------
"""

import os
import requests
import traceback
from typing import List

class Updater:
    PATH: str = os.getcwd()

    RAW_GITHUB_BASE_URL: str = "https://raw.githubusercontent.com/CaptainDeathead/Eatventure-Bot/main"

    def __init__(self) -> None:
        self.load_installed()
        self.get_latest_changes()
        self.download_and_install()

    def load_version(self) -> None:
        print("Verifying '__version__.txt' exists...", end='', flush=True)

        if not os.path.exists(f"{self.PATH}/__version__.txt"):
            print("\rVerifying '__version__.txt' exists...  Failed!", flush=True)

            print("\nThe updater cannot find '__version__.txt'!\nPlease ensure it is present in the projects directory.")
            exit()
        else:
            print("\rVerifying '__version__.txt' exists...  Done!", flush=True)

        print("Loading '__version__.txt'...", end='', flush=True)

        with open(f"{self.PATH}/__version__.txt", "r") as version_file:
            self.version_raw: str = version_file.read()

        print("\rLoading '__version__.txt'...  Done!", flush=True)

    def parse_version(self) -> None:
        print("Extracting version...", end='', flush=True)
        self.version: str = self.version_raw.split("\n")[0]
        print(f"\rExtracting version...  {self.version}!", flush=True)

        print("Discovering installed files...", end='', flush=True)
        self.installed_files: List[str] = [filename for filename in self.version_raw.splitlines()[1:]]
        print(f"\rDiscovering installed files...  {len(self.installed_files)} found!", flush=True)

    def load_installed(self) -> None:
        self.load_version()
        self.parse_version()

    def parse_online_version(self) -> None:
        print(f"Requesting the latest version at '{self.RAW_GITHUB_BASE_URL}/__version__.txt'...", end='', flush=True)

        try: version_request = requests.get(f"{self.RAW_GITHUB_BASE_URL}/__version__.txt")
        except requests.RequestException:
            print(f"\rRequesting the latest version at '{self.RAW_GITHUB_BASE_URL}/__version__.txt'...  Failed!\n", flush=True)
            print(traceback)
            print("Please ensure you are connected to the internet!")
            exit()

        if version_request.status_code >= 400:
            print(f"\rRequesting the latest version at '{self.RAW_GITHUB_BASE_URL}/__version__.txt'...  ERROR: {version_request.status_code}!\n", flush=True)
            print("Please ensure you are connected to the internet!")
            exit()

        print(f"\rRequesting the latest version at '{self.RAW_GITHUB_BASE_URL}/__version__.txt'...  Done!", flush=True)

        self.online_version_raw: str = version_request.text
        
        print("Extracting online version...", end='', flush=True)
        self.online_version: str = self.online_version_raw.split("\n")[0]
        print(f"\rExtracting online version...  {self.online_version}!", flush=True)

        print("Discovering online files...", end='', flush=True)
        self.online_files: List[str] = [filename for filename in self.online_version_raw.splitlines()[1:]]
        print(f"\rDiscovering online files...  {len(self.online_files)} found!", flush=True)

    def contrast_differences(self) -> None:
        self.needs_update: bool = False

        print("Comparing versions...", end='', flush=True)
        if self.version == self.online_version:
            print("\rComparing versions...  Same!", flush=True)

            print("Comparing file counts...", end='', flush=True)
            if len(self.installed_files) != len(self.online_files):
                print("\rComparing file counts...  Different!", flush=True)
                self.needs_update = True
            else:
                print("\rComparing file counts...  Same!", flush=True)
        else:
            print("\rComparing versions...  Different!", flush=True)
            self.needs_update = True

    def get_latest_changes(self) -> None:
        self.parse_online_version()
        self.contrast_differences()

    def download_file(self, filename: str) -> None:
        print(f"Downloading '{filename}'...", end='', flush=True)

        try: file_request = requests.get(f"{self.RAW_GITHUB_BASE_URL}/{filename}")
        except requests.RequestException:
            print(f"\rDownloading '{filename}'...  Failed!\n", flush=True)
            print(traceback)
            print("Please ensure you are connected to the internet!")
            exit()

        if file_request.status_code >= 400:
            print(f"\rDownloading '{filename}'...  ERROR: {file_request.status_code}!\n", flush=True)
            print("Please ensure you are connected to the internet!")
            exit()

        print(f"Downloading '{filename}'...  Done!", flush=True)

        print(f"-Installing '{filename}'...", end='', flush=True)
        with open(f"{self.PATH}/{filename}", "wb") as newfile:
            newfile.write(file_request.content)
        print(f"-Installing '{filename}'...  Done!", flush=True)

    def download_and_install(self) -> None:
        print(f"Needs update...  {self.needs_update}")

        if not self.needs_update:
            print("\nNo update required!")
            self.complete_function()

        for filename in self.online_files:
            self.download_file(filename)

        print(f"\n{len(self.online_files)} files have been installed over {len(self.installed_files)} files.\nAll updates complete!")

def main() -> None:
    updater: Updater = Updater()

if __name__ == "__main__":
    main()
    from main import main as run_bot_gui