import subprocess
from pathlib import Path
import os

YT_DLP = Path("yt-dlp.exe" if os.name == "nt" else "yt-dlp")

def ensure_yt_dlp():
    if not YT_DLP.exists():
        download_yt_dlp()
    else:
        update_yt_dlp()

def download_yt_dlp():
    subprocess.run(
        ["yt-dlp", "-U"],
        check=False
    )

def update_yt_dlp():
    subprocess.run(
        [str(YT_DLP), "-U"],
        check=False
    )
