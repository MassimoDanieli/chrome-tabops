"""Small Tk window with Save / Restore buttons."""

import sys
import tkinter as tk
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tabops import chrome, store  # noqa: E402


def main():
    root = tk.Tk()
    root.title("Chrome TabOps")
    status = tk.Label(root, text="Ready", fg="green")
    status.pack()

    def save_tabs():
        tabs = chrome.get_tabs()
        store.save(tabs)
        status.config(text=f"Saved {len(tabs)} tabs", fg="green")

    def restore_tabs():
        try:
            urls, skipped = store.safe_urls(store.load())
        except FileNotFoundError:
            status.config(text="No backup yet: save first", fg="red")
            return
        for url in urls:
            chrome.open_url(url)
        note = f" ({len(skipped)} skipped)" if skipped else ""
        status.config(text=f"Restored {len(urls)} tabs{note}", fg="green")

    tk.Button(root, text="Save Tabs", command=save_tabs).pack(pady=10)
    tk.Button(root, text="Restore Tabs", command=restore_tabs).pack(pady=10)
    root.mainloop()


if __name__ == "__main__":
    main()
