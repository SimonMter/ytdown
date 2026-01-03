#!/usr/bin/env python3

import json
import sys
import subprocess
import requests
from pathlib import Path

from update.github_api import get_latest_release
from update.versioning import is_newer
from update.yt_dlp_manager import ensure_yt_dlp
from ui import create_ui

OWNER = "SimonMter"
REPO = "ytdown"

APP_EXE = Path(sys.argv[0])
NEW_EXE = APP_EXE.with_name("ytdown_new.exe")

def get_local_version():
    with open("version.json") as f:
        return json.load(f)["version"]

def check_app_update():
    print("Checking for app updates")
    release = get_latest_release(OWNER, REPO)
    remote_version = release["tag_name"].lstrip("v")

    if is_newer(get_local_version(), remote_version):
        return release
    return None

def download_new_exe(release):
    for asset in release["assets"]:
        if asset["name"] == "ytdown.exe":
            url = asset["browser_download_url"]
            r = requests.get(url, stream=True)
            with open(NEW_EXE, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            return True
    return False

def run_updater():
    print("running updater")
    subprocess.Popen([
        sys.executable,
        "updater.py",
        str(APP_EXE),
        str(NEW_EXE)
    ])
    sys.exit(0)

def user_confirms_update():
    return True  # testing only

def main():
    ensure_yt_dlp()

    release = check_app_update()
    if release:
        if user_confirms_update():
            if download_new_exe(release):
                run_updater()

    create_ui()

if __name__ == "__main__":
    main()
