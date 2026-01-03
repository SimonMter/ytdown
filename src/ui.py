
import tkinter as tk
from tkinter import ttk, messagebox
from yt_dlp.metadata import fetch_metadata, extract_video_formats
from yt_dlp.manager import run_yt_dlp

class YTDownUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ytdown")
        self.geometry("600x400")

        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar()

        tk.Label(self, text="YouTube URL").pack(anchor="w", padx=10)
        tk.Entry(self, textvariable=self.url_var).pack(fill="x", padx=10)

        tk.Button(self, text="Load info", command=self.load_info).pack(pady=5)

        self.info_label = tk.Label(self, text="")
        self.info_label.pack(anchor="w", padx=10)

        self.format_box = ttk.Combobox(self, textvariable=self.format_var)
        self.format_box.pack(fill="x", padx=10)

        tk.Button(self, text="Download", command=self.download).pack(pady=10)

        self.formats = []

    def load_info(self):
        try:
            info = fetch_metadata(self.url_var.get())
            self.info_label.config(
                text=f"{info['title']} ({info.get('duration', '?')}s)"
            )

            self.formats = extract_video_formats(info)
            display = [
                f"{f['id']} | {f['res']} | {f['ext']}"
                for f in self.formats
            ]
            self.format_box["values"] = display
            if display:
                self.format_box.current(0)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def download(self):
        if not self.format_box.current() >= 0:
            return

        fmt = self.formats[self.format_box.current()]
        run_yt_dlp([
            self.url_var.get(),
            "-f", fmt["id"]
        ])

if __name__ == "__main__":
    YTDownUI().mainloop()

