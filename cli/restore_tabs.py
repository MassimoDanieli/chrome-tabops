"""Kept for the old usage: python cli/restore_tabs.py [--file F]"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tabops.cli import main  # noqa: E402

sys.exit(main(["restore", *sys.argv[1:]]))
