"""Read and write the tab backup file."""

import json
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_FILE = "chrome_tabs_backup.json"

# Schemes Chrome is allowed to reopen from a backup. Anything else
# (javascript:, file:, applescript: ...) is skipped.
ALLOWED_SCHEMES = {"http", "https", "chrome", "about"}


def save(tabs, path=DEFAULT_FILE):
    Path(path).write_text(json.dumps(tabs, indent=2, ensure_ascii=False),
                          encoding="utf-8")


def load(path=DEFAULT_FILE):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path}: expected a list of tabs")
    return [t for t in data if isinstance(t, dict) and isinstance(t.get("url"), str)]


def safe_urls(tabs):
    """URLs worth reopening, and the ones skipped (with their scheme)."""
    keep, skipped = [], []
    for tab in tabs:
        url = tab["url"].strip()
        (keep if urlparse(url).scheme.lower() in ALLOWED_SCHEMES else skipped).append(url)
    return keep, skipped
