from packaging.version import Version

def is_newer(local: str, remote: str) -> bool:
    return Version(remote) > Version(local)
