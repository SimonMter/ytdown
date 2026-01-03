from packaging.version import Version

def is_newer(local: str, remote: str) -> bool:
    print(f"comparing remote version {remote} with local version {local}")
    return Version(remote) > Version(local)
