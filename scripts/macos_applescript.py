
import subprocess

def get_tabs_macos():
    result = subprocess.run([
        "osascript", "-e",
        '''set output to ""
tell application "Google Chrome"
  repeat with w in windows
    repeat with t in tabs of w
      set output to output & (URL of t) & "|" & (title of t) & linefeed
    end repeat
  end repeat
end tell
return output'''
    ], stdout=subprocess.PIPE)

    lines = result.stdout.decode("utf-8").strip().splitlines()
    tab_list = []
    for line in lines:
        if "|" in line:
            url, title = line.split("|", 1)
            tab_list.append({"url": url.strip(), "title": title.strip()})
    return tab_list
