
import tkinter as tk
from scripts.macos_applescript import get_tabs_macos
import subprocess
import json

root = tk.Tk()
root.title("Chrome TabOps")

status = tk.Label(root, text="Ready", fg="green")
status.pack()

def save_tabs():
    tabs = get_tabs_macos()
    with open("chrome_tabs_backup.json", "w") as f:
        json.dump(tabs, f, indent=2)
    status.config(text=f"Saved {len(tabs)} tabs")

def restore_tabs():
    with open("chrome_tabs_backup.json", "r") as f:
        tabs = json.load(f)
    for tab in tabs:
        subprocess.run([
            "osascript", "-e",
            f'tell application "Google Chrome" to open location "{tab["url"]}"'
        ])
    status.config(text=f"Restored {len(tabs)} tabs")

tk.Button(root, text="Save Tabs", command=save_tabs).pack(pady=10)
tk.Button(root, text="Restore Tabs", command=restore_tabs).pack(pady=10)

root.mainloop()
