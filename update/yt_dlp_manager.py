import subprocess
import shutil
from pathlib import Path

YT_DLP = Path("yt-dlp")

def is_apt_version():
    result = subprocess.run(["which", "yt-dlp"], capture_output=True, text=True)
    return "/usr/bin" in result.stdout


def ensure_yt_dlp():
    if is_apt_version():
        print("yt-dlp installed via apt -> skip auto-update")
        return
    if not YT_DLP.exists():
        download_yt_dlp()
    else:
        update_yt_dlp()

def download_yt_dlp():
    print("Downloading YT_DLP")
    subprocess.run(
        ["yt-dlp", "-U"],
        check=False
    )

def update_yt_dlp():
    print("Updating YT_DLP")
    subprocess.run(
        [str(YT_DLP), "-U"],
        check=False
    )
