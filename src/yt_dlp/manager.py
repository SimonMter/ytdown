
import subprocess
from pathlib import Path
import shutil
import sys

def find_yt_dlp() -> Path:
    local = Path(sys.argv[0]).resolve().parent / "yt-dlp"
    if local.exists():
        return local

    system = shutil.which("yt-dlp")
    if system:
        return Path(system)

    raise RuntimeError("yt-dlp not found")

def run_yt_dlp(args: list[str]) -> int:
    yt_dlp = find_yt_dlp()
    cmd = [str(yt_dlp)] + args

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in proc.stdout:
        print(line, end="")

    return proc.wait()

