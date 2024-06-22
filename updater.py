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
        print("Verifying `__version__.txt` exists...", end='', flush=True)

        if not os.path.exists(f"{self.PATH}/__version__.txt"):
            print("\rVerifying `__version__.txt` exists...  Failed!", flush=True)

            print("\nThe updater cannot find `__version__.txt`!\nPlease ensure it is present in the projects directory.")
            exit()
        else:
            print("\rVerifying `__version__.txt` exists...  Done!", flush=True)

        print("Loading `__version__.txt`...", end='', flush=True)

        with open(f"{self.PATH}/__version__.txt", "r") as version_file:
            self.version_raw: str = version_file.read()

        print("\rLoading `__version__.txt`...  Done!", flush=True)

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

        self.online_version_raw: str = version_request.text
        
        print("Extracting online version...", end='', flush=True)
        self.online_version: str = self.online_version_raw.split("\n")[0]
        print(f"\rExtracting online version...  {self.online_version}!", flush=True)

        print("Discovering online files...", end='', flush=True)
        self.online_files: List[str] = [filename for filename in self.online_version_raw.splitlines()[1:]]
        print(f"\rDiscovering online files...  {len(self.online_files)} found!", flush=True)

    def get_latest_changes(self) -> None:
        self.parse_online_version()

def main() -> None:
    updater: Updater = Updater()

if __name__ == "__main__":
    main()