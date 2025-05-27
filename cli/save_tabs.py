
import json
import subprocess
import platform
import sys
from scripts.macos_applescript import get_tabs_macos

OS = platform.system()

if OS != "Darwin":
    print("This script currently supports macOS only.")
    sys.exit(1)

print("🔄 Saving Chrome tabs...")
tabs = get_tabs_macos()

with open("chrome_tabs_backup.json", "w") as f:
    json.dump(tabs, f, indent=2)

print(f"✅ Saved {len(tabs)} tabs to chrome_tabs_backup.json")

subprocess.run(["osascript", "-e", 'tell application "Google Chrome" to close windows'])
print("🧨 All Chrome windows closed.")
