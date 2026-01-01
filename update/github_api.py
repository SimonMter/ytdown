import request

GITHUB_API = "https://api.github.com/repos/{owner}/{repo}/releases/latest"

def get_latest_release (owner : str, repo: str):
    url = GITHUB_API.format(owner=owner, repo=repo)
    r = request.get(url, timeout=10)
    r.raise_for_status()
    return r.json()
