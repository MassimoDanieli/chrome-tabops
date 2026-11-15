"""Command line: python -m tabops save | restore"""

import argparse
import platform
import sys

from . import chrome, store


def main(argv=None):
    parser = argparse.ArgumentParser(prog="tabops", description="Save and restore Google Chrome tabs (macOS).")
    sub = parser.add_subparsers(dest="command", required=True)
    s = sub.add_parser("save", help="save every open tab to a JSON file")
    s.add_argument("--file", default=store.DEFAULT_FILE)
    s.add_argument("--close", action="store_true", help="close all Chrome windows after saving")
    r = sub.add_parser("restore", help="reopen the tabs saved in a JSON file")
    r.add_argument("--file", default=store.DEFAULT_FILE)
    args = parser.parse_args(argv)

    if platform.system() != "Darwin":
        print("Chrome TabOps currently supports macOS only.", file=sys.stderr)
        return 1

    if args.command == "save":
        tabs = chrome.get_tabs()
        store.save(tabs, args.file)
        print(f"Saved {len(tabs)} tabs to {args.file}")
        if args.close:
            chrome.close_all_windows()
            print("All Chrome windows closed.")
        return 0

    try:
        tabs = store.load(args.file)
    except FileNotFoundError:
        print(f"No backup at {args.file}: run 'save' first.", file=sys.stderr)
        return 1
    urls, skipped = store.safe_urls(tabs)
    for url in urls:
        chrome.open_url(url)
    print(f"Restored {len(urls)} tabs from {args.file}")
    if skipped:
        print(f"Skipped {len(skipped)} URLs with an unsupported scheme.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
