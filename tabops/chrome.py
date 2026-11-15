"""Talk to Google Chrome on macOS through AppleScript (osascript)."""

import subprocess

# ASCII unit separator: cannot appear in a URL or a tab title, unlike "|".
SEP = "\x1f"

LIST_TABS = '''set sep to character id 31
set output to ""
tell application "Google Chrome"
  repeat with w in windows
    repeat with t in tabs of w
      set output to output & (URL of t) & sep & (title of t) & linefeed
    end repeat
  end repeat
end tell
return output'''

# The URL is passed as an argument, never pasted into the script text:
# a URL containing a quote can no longer turn into AppleScript code.
OPEN_URL = '''on run argv
  tell application "Google Chrome" to open location (item 1 of argv)
end run'''

CLOSE_WINDOWS = 'tell application "Google Chrome" to close windows'


def _osascript(script, *args):
    return subprocess.run(
        ["osascript", "-e", script, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )


def parse_tabs(output):
    tabs = []
    for line in output.splitlines():
        if SEP not in line:
            continue
        url, title = line.split(SEP, 1)
        url = url.strip()
        if url:
            tabs.append({"url": url, "title": title.strip()})
    return tabs


def get_tabs():
    result = _osascript(LIST_TABS)
    return parse_tabs(result.stdout.decode("utf-8"))


def open_url(url):
    _osascript(OPEN_URL, url)


def close_all_windows():
    _osascript(CLOSE_WINDOWS)
