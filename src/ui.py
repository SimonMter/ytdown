import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from threading import Thread
from PIL import Image, ImageTk
import logging

from yt_dlp.metadata import fetch_metadata, download_thumbnail
from yt_dlp.manager import run_yt_dlp_stream
from yt_dlp.progress import parse_progress

# ===== Logging =====
logging.basicConfig(
    filename="ytdown.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ===== Presets =====
QUALITY_PRESETS = {
    "Best": "bv*+ba/b",
    "1080p": "bv*[height<=1080]+ba/b",
    "720p": "bv*[height<=720]+ba/b",
    "480p": "bv*[height<=480]+ba/b",
}


class YTDownUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YTDown")
        self.geometry("820x600")

        # ===== Variables =====
        self.url = tk.StringVar()
        self.mode = tk.StringVar(value="video")
        self.quality = tk.StringVar(value="Best")
        self.format = tk.StringVar(value="mp4")
        self.output_dir = tk.StringVar(value=str(Path.home()))

        self.info = None
        self.thumb_img = None

        self.download_button = None
        self.progress = None
        self.progress_label = None
        self.format_combo = None

        self._build_ui()

    # ===== UI BUILD =====
    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(fill="both", expand=True)

        # URL input
        ttk.Label(main, text="Video URL").pack(anchor="w")
        ttk.Entry(main, textvariable=self.url).pack(fill="x")
        ttk.Button(main, text="Load info", command=self.load_info).pack(pady=5)

        # Info & thumbnail
        info_frame = ttk.Frame(main)
        info_frame.pack(fill="x", pady=10)

        self.thumb_label = ttk.Label(info_frame)
        self.thumb_label.pack(side="left")

        self.meta_label = ttk.Label(info_frame, text="", justify="left")
        self.meta_label.pack(side="left", padx=10)

        # Options frame
        opts = ttk.LabelFrame(main, text="Download Options", padding=10)
        opts.pack(fill="x")

        # Mode
        ttk.Radiobutton(opts, text="Video", variable=self.mode, value="video").grid(row=0, column=0)
        ttk.Radiobutton(opts, text="Audio only", variable=self.mode, value="audio").grid(row=0, column=1)

        # Quality
        ttk.Label(opts, text="Quality").grid(row=1, column=0, sticky="w")
        ttk.Combobox(opts, textvariable=self.quality,
                     values=list(QUALITY_PRESETS.keys()), state="readonly").grid(row=1, column=1)

        # Format
        ttk.Label(opts, text="Format").grid(row=2, column=0, sticky="w")
        self.format_combo = ttk.Combobox(opts, textvariable=self.format,
                                         values=["mp4", "webm", "mkv", "mp3", "opus"],
                                         state="readonly")
        self.format_combo.grid(row=2, column=1)

        # Output folder
        ttk.Label(opts, text="Save to").grid(row=3, column=0, sticky="w")
        ttk.Entry(opts, textvariable=self.output_dir).grid(row=3, column=1, sticky="ew")
        ttk.Button(opts, text="Browse", command=self.choose_dir).grid(row=3, column=2)
        opts.columnconfigure(1, weight=1)

        # Update format options when mode changes
        self.mode.trace_add("write", self._update_formats)

        # Progress
        self.progress = ttk.Progressbar(main, length=400)
        self.progress.pack(pady=10)

        self.progress_label = ttk.Label(main, text="")
        self.progress_label.pack()

        # Download button
        self.download_button = ttk.Button(main, text="Download", command=self.start_download)
        self.download_button.pack(pady=10)

    # ===== FORMAT VALIDATION =====
    def _update_formats(self, *args):
        if self.mode.get() == "audio":
            self.format_combo["values"] = ["mp3", "opus"]
            if self.format.get() not in ["mp3", "opus"]:
                self.format.set("mp3")
        else:
            self.format_combo["values"] = ["mp4", "webm", "mkv"]
            if self.format.get() not in ["mp4", "webm", "mkv"]:
                self.format.set("mp4")

    # ===== DIRECTORY CHOOSER =====
    def choose_dir(self):
        d = filedialog.askdirectory()
        if d:
            self.output_dir.set(d)

    # ===== LOAD METADATA =====
    def load_info(self):
        try:
            logger.info("Fetching metadata for URL: %s", self.url.get())
            self.info = fetch_metadata(self.url.get())

            text = (
                f"{self.info['title']}\n"
                f"By {self.info.get('uploader','?')}\n"
                f"Duration: {self.info.get('duration', '?')}s"
            )
            self.meta_label.config(text=text)
            logger.info("Metadata loaded: %s", self.info['title'])

            # Download and show thumbnail
            thumb = Path("thumb.jpg")
            download_thumbnail(self.info["thumbnail"], thumb)
            img = Image.open(thumb).resize((240, 135))
            self.thumb_img = ImageTk.PhotoImage(img)
            self.thumb_label.config(image=self.thumb_img)

        except Exception as e:
            logger.error("Error loading metadata: %s", e)
            messagebox.showerror("Error", str(e))

    # ===== DOWNLOAD LOGIC =====
    def start_download(self):
        # Validate audio format
        self.progress["value"] = 0
        self.progress_label.config(text="")

        if self.mode.get() == "audio" and self.format.get() not in ["mp3", "opus"]:
            messagebox.showwarning(
                "Invalid format",
                f"{self.format.get()} is a video format. Please select mp3 or opus for audio only."
            )
            return

        self.download_button["state"] = "disabled"
        Thread(target=self._download_thread, daemon=True).start()

    def _download_thread(self):
        args = [self.url.get(), "-P", self.output_dir.get()]

        if self.mode.get() == "audio":
            args += ["-x", "--audio-format", self.format.get()]
        else:
            args += ["-f", QUALITY_PRESETS[self.quality.get()],
                     "--remux-video", self.format.get()]

        logger.info("Starting download with args: %s", args)
        try:
            for line in run_yt_dlp_stream(args):
                logger.debug(line)
                prog = parse_progress(line)
                if prog:
                    self.progress.after(0, lambda p=prog: self._update_progress(p))
        except Exception as e:
            logger.error("Download error: %s", e)
            messagebox.showerror("Download error", str(e))
        finally:
            self.progress.after(0, lambda: self._update_progress({
                "percent": 100,
                "speed": "0B/s",
                "eta": "0s"
            }))
            self.progress.after(0, lambda: messagebox.showinfo("Download complete", "Your download has finished!"))
            self.download_button.after(0, lambda: self.download_button.config(state="normal"))

    def _update_progress(self, prog):
        self.progress["value"] = prog["percent"]
        self.progress_label.config(
            text=f"{prog['percent']}% · {prog['speed']} · ETA {prog['eta']}"
        )


if __name__ == "__main__":
    YTDownUI().mainloop()
