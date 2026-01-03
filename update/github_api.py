import requests

GITHUB_API = "https://api.github.com/repos/{owner}/{repo}/releases/latest"

def get_latest_release (owner : str, repo: str):
    print("requesting latest release...")
    url = GITHUB_API.format(owner=owner, repo=repo)
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    print(r.json())
    return r.json()
