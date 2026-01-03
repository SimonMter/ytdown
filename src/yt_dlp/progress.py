
import re

PROGRESS_RE = re.compile(
    r"\[download\]\s+(\d+\.\d+)%.*?at\s+([\d\.]+\w+/s).*?ETA\s+(\d+:\d+)"
)

def parse_progress(line: str):
    m = PROGRESS_RE.search(line)
    if not m:
        return None
    return {
        "percent": float(m.group(1)),
        "speed": m.group(2),
        "eta": m.group(3),
    }
