from version import __version__, debug
from yt_dlp.manager import run_yt_dlp


def main():
    #main logic goes here
    if debug: print(f"running ytdown debug: {__version__}")

    run_yt_dlp([
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    ])
    
if __name__ == "__main__":
    main()
