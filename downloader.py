"""Wrapper around the third-party archive-org-downloader.py.

Calls the upstream script as a subprocess with our credentials and config,
streams stdout+stderr line-by-line to track real progress, then registers
the result in the catalog.
"""

from __future__ import annotations

import re
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Callable

from config import get_library_dir, get_resolution
from creds import get_credentials
from library import add_book


SKILL_DIR = Path(__file__).resolve().parent
DOWNLOADER = SKILL_DIR / "archive-org-downloader.py"


# Progress callback signature: (progress_dict) -> None
ProgressFn = Callable[[dict], None]


# Regexes for parsing MiniGlome's stdout + tqdm stderr
_RE_PAGE_COUNT = re.compile(r"\[\+\] Found (\d+) pages")
_RE_TQDM = re.compile(r"(\d+)%\|.*\|\s*(\d+)/(\d+)\s*\[(\S+)<(\S+),")
_RE_LOGIN = re.compile(r"\[\+\] Successful login")
_RE_LOAN = re.compile(r"\[\+\] Successful loan")
_RE_DONE = re.compile(r'\[\+\] PDF saved as "(.+)"')
_RE_ERROR = re.compile(r"\[-\] (.+)")


def normalize_url(url: str) -> str | None:
    """Reduce any archive.org URL to canonical https://archive.org/details/<id>.

    Accepts:
        https://archive.org/details/foo/page/n5/mode/1up
        https://archive.org/details/foo
        archive.org/details/foo
        foo (raw identifier)
    """
    url = url.strip()
    m = re.search(r"archive\.org/details/([^/?#]+)", url)
    if m:
        return f"https://archive.org/details/{m.group(1)}"
    if re.match(r"^[A-Za-z0-9_\-\.]+$", url):
        return f"https://archive.org/details/{url}"
    return None


def identifier_from_url(url: str) -> str | None:
    m = re.search(r"archive\.org/details/([^/?#]+)", url)
    return m.group(1) if m else None


def _parse_line(line: str, state: dict) -> None:
    """Parse one stdout/stderr line from MiniGlome and update state in place."""
    m = _RE_PAGE_COUNT.search(line)
    if m:
        state["total_pages"] = int(m.group(1))
        state["phase"] = "downloading"
        state["message"] = f"Downloading {m.group(1)} pages..."
        return
    if _RE_LOGIN.search(line):
        state["phase"] = "authenticated"
        state["message"] = "Authenticated with archive.org"
        return
    if _RE_LOAN.search(line):
        state["phase"] = "loaned"
        state["message"] = "Borrow grant received"
        return
    m = _RE_TQDM.search(line)
    if m:
        pct, current, total, elapsed, remaining = m.groups()
        state["phase"] = "downloading"
        state["current_page"] = int(current)
        state["total_pages"] = int(total)
        state["percent"] = int(pct)
        state["elapsed"] = elapsed
        state["remaining"] = remaining
        state["message"] = f"Page {current} of {total} · {remaining} remaining"
        return
    m = _RE_DONE.search(line)
    if m:
        state["phase"] = "saving"
        state["message"] = "Assembling PDF..."
        return
    m = _RE_ERROR.search(line)
    if m:
        state["phase"] = "error"
        state["message"] = m.group(1).strip()
        return


def download(url: str, *, resolution: int | None = None,
             progress: ProgressFn | None = None) -> tuple[bool, str]:
    """Download a single book. Returns (ok, message).

    If `progress` is provided, called with state dict on every meaningful
    update. State keys: phase, message, current_page, total_pages, percent,
    elapsed, remaining.
    """
    canonical = normalize_url(url)
    if not canonical:
        return False, f"Could not parse archive.org URL: {url}"

    email, password = get_credentials()
    if not (email and password):
        return False, "No credentials. Run setup again."

    out_dir = get_library_dir()
    res = resolution if resolution is not None else get_resolution()

    cmd = [
        sys.executable, "-u", str(DOWNLOADER),  # -u for unbuffered stdout
        "-e", email,
        "-p", password,
        "-u", canonical,
        "-d", str(out_dir),
        "-r", str(res),
    ]

    state = {
        "phase": "starting",
        "message": "Starting download...",
        "current_page": 0,
        "total_pages": 0,
        "percent": 0,
        "elapsed": "",
        "remaining": "",
    }
    if progress:
        progress(dict(state))

    try:
        proc = subprocess.Popen(
            cmd,
            cwd=str(out_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
    except Exception as e:
        return False, f"Could not launch downloader: {e}"

    # Stream output, parse progress, push to callback
    full_log = []
    try:
        for raw in proc.stdout:
            # tqdm uses \r in same line; split into virtual lines
            for piece in re.split(r"[\r\n]+", raw):
                piece = piece.strip()
                if not piece:
                    continue
                full_log.append(piece)
                _parse_line(piece, state)
                if progress:
                    progress(dict(state))
    except Exception:
        pass
    proc.wait()

    if proc.returncode != 0:
        # Try to surface a useful error
        last_error = next((l for l in reversed(full_log) if "[-]" in l or "error" in l.lower()), None)
        if last_error:
            return False, last_error
        return False, f"Downloader exited with code {proc.returncode}"

    # Find the produced PDF and register it
    identifier = identifier_from_url(canonical)
    pdfs = sorted(out_dir.glob(f"*{identifier}*.pdf")) if identifier else []
    if not pdfs:
        pdfs = sorted(out_dir.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not pdfs:
        return False, "Download finished but no PDF was found"

    pdf = pdfs[0]
    title = pdf.stem.replace("_", " ")
    page_count = state.get("total_pages", 0)
    if not page_count:
        try:
            from pypdf import PdfReader
            page_count = len(PdfReader(str(pdf)).pages)
        except Exception:
            pass

    add_book(canonical, identifier or pdf.stem, title, pdf, page_count)

    state["phase"] = "done"
    state["message"] = f"Saved {pdf.name}"
    if progress:
        progress(dict(state))

    return True, f"Downloaded: {pdf.name} ({pdf.stat().st_size / 1e6:.1f} MB)"
