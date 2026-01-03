
import json
import subprocess
from .manager import find_yt_dlp
import urllib.request
from pathlib import Path 

def fetch_metadata(url: str) -> dict:
    yt_dlp = find_yt_dlp()

    proc = subprocess.run(
        [str(yt_dlp), "--dump-json", "--no-playlist", url],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip())

    return json.loads(proc.stdout)

def extract_video_formats(info: dict):
    formats = []
    for f in info.get("formats", []):
        if f.get("vcodec") != "none":
            formats.append({
                "id": f["format_id"],
                "ext": f["ext"],
                "res": f.get("resolution"),
                "fps": f.get("fps"),
                "filesize": f.get("filesize"),
                "vcodec": f.get("vcodec"),
            })
    return formats

def download_thumbnail(url: str, target: Path):
    urllib.request.urlretrieve(url, target)
