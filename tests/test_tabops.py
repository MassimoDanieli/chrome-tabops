import json
import subprocess

import pytest

from tabops import chrome, cli, store


class FakeRun:
    def __init__(self, stdout=b""):
        self.calls = []
        self.stdout = stdout

    def __call__(self, cmd, **kwargs):
        self.calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, stdout=self.stdout, stderr=b"")


def test_parse_tabs_handles_pipes_and_blank_lines():
    out = f"https://a.example/x|y{chrome.SEP}A | title\n\nhttps://b.example{chrome.SEP}B\n"
    assert chrome.parse_tabs(out) == [
        {"url": "https://a.example/x|y", "title": "A | title"},
        {"url": "https://b.example", "title": "B"},
    ]


def test_open_url_passes_url_as_argument_not_code(monkeypatch):
    fake = FakeRun()
    monkeypatch.setattr(subprocess, "run", fake)
    evil = 'https://x.example/" & (do shell script "touch /tmp/pwned") & "'
    chrome.open_url(evil)
    cmd = fake.calls[0]
    assert cmd[:2] == ["osascript", "-e"]
    assert evil not in cmd[2]          # never inside the script text
    assert cmd[3] == evil              # only as argv
    assert "item 1 of argv" in cmd[2]


def test_safe_urls_skips_dangerous_schemes():
    urls = ["https://ok.example", "javascript:alert(1)", "file:///etc/passwd", "chrome://settings"]
    tabs = [{"url": u} for u in urls]
    keep, skipped = store.safe_urls(tabs)
    assert keep == ["https://ok.example", "chrome://settings"]
    assert skipped == ["javascript:alert(1)", "file:///etc/passwd"]


def test_load_rejects_non_list_and_ignores_bad_entries(tmp_path):
    p = tmp_path / "b.json"
    p.write_text(json.dumps({"url": "x"}))
    with pytest.raises(ValueError):
        store.load(p)
    p.write_text(json.dumps([{"url": "https://a"}, {"title": "no url"}, "junk"]))
    assert store.load(p) == [{"url": "https://a"}]


def test_cli_save_does_not_close_windows_unless_asked(monkeypatch, tmp_path):
    monkeypatch.setattr(cli.platform, "system", lambda: "Darwin")
    fake = FakeRun(stdout=f"https://a{chrome.SEP}A\n".encode())
    monkeypatch.setattr(subprocess, "run", fake)
    f = tmp_path / "t.json"
    assert cli.main(["save", "--file", str(f)]) == 0
    assert json.loads(f.read_text()) == [{"url": "https://a", "title": "A"}]
    assert not any(chrome.CLOSE_WINDOWS in c for c in fake.calls)
    assert cli.main(["save", "--file", str(f), "--close"]) == 0
    assert any(chrome.CLOSE_WINDOWS in c for c in fake.calls)


def test_cli_restore(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(cli.platform, "system", lambda: "Darwin")
    fake = FakeRun()
    monkeypatch.setattr(subprocess, "run", fake)
    f = tmp_path / "t.json"
    assert cli.main(["restore", "--file", str(f)]) == 1  # missing file: clear error
    f.write_text(json.dumps([{"url": "https://a"}, {"url": "javascript:x"}]))
    assert cli.main(["restore", "--file", str(f)]) == 0
    assert [c[3] for c in fake.calls] == ["https://a"]
    assert "Skipped 1" in capsys.readouterr().err


def test_non_macos_exits(monkeypatch):
    monkeypatch.setattr(cli.platform, "system", lambda: "Linux")
    assert cli.main(["save"]) == 1


def test_old_script_paths_import(tmp_path):
    # README usage: python cli/save_tabs.py from any directory used to fail with ImportError
    code = "import runpy,sys; sys.argv=['x','--help']; runpy.run_path('cli/save_tabs.py')"
    r = subprocess.run(["python3", "-c", code], capture_output=True, text=True)
    assert "ModuleNotFoundError" not in r.stderr
