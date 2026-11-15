# Chrome TabOps

[![Python CI](https://github.com/MassimoDanieli/chrome-tabops/actions/workflows/python-ci.yml/badge.svg)](https://github.com/MassimoDanieli/chrome-tabops/actions/workflows/python-ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Save and restore your Google Chrome tabs. No external dependencies.

## Usage

```bash
python -m tabops save                 # every open tab → chrome_tabs_backup.json
python -m tabops save --close         # …and then close all Chrome windows
python -m tabops restore              # reopen them
python -m tabops save --file ~/tabs.json

python gui/chrome_tabs_gui.py         # small window with Save / Restore
```

The old commands still work: `python cli/save_tabs.py [--close]`, `python cli/restore_tabs.py`.

On restore, only `http`, `https`, `chrome` and `about` URLs are reopened; anything
else in the file (`javascript:`, `file:` …) is skipped and counted.

## Platform support

| Platform | Supported |
|----------|-----------|
| macOS    | ✅ Yes (AppleScript) |
| Windows  | ⏳ Not yet |
| Linux    | ⏳ Not yet |

## Development

```bash
pip install flake8 pytest
flake8 cli/ gui/ tabops/ tests/
pytest -q        # osascript is mocked, runs on any OS
```
