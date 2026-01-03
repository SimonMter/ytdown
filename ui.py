
import tkinter as tk
from tkinter import ttk
import json

def get_local_version():
    with open("version.json") as f:
        return json.load(f)["version"]

def create_ui():
    window = tk.Tk()
    window.title("ytdown")
    window.geometry("300x100")

    main_frame = ttk.Frame(window, padding=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    version_label = ttk.Label(main_frame, text=f"Current version: {get_local_version()}")
    version_label.pack(pady=10)

    window.mainloop()
