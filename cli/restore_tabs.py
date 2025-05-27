
import json
import subprocess

with open("chrome_tabs_backup.json", "r") as f:
    tabs = json.load(f)

for tab in tabs:
    subprocess.run([
        "osascript", "-e",
        f'tell application "Google Chrome" to open location "{tab["url"]}"'
    ])

print(f"🔁 Restored {len(tabs)} tabs to Chrome")
