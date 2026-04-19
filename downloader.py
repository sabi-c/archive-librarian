"""Wrapper around the third-party archive-org-downloader.py.

Calls the upstream script as a subprocess with our credentials and config,
then registers the result in the catalog.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from config import get_library_dir, get_resolution
from creds import get_credentials
from library import add_book


SKILL_DIR = Path(__file__).resolve().parent
DOWNLOADER = SKILL_DIR / "archive-org-downloader.py"


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


def download(url: str, *, resolution: int | None = None) -> tuple[bool, str]:
    """Download a single book. Returns (ok, message)."""
    canonical = normalize_url(url)
    if not canonical:
        return False, f"Could not parse archive.org URL: {url}"

    email, password = get_credentials()
    if not (email and password):
        return False, "No credentials. Run: librarian setup"

    out_dir = get_library_dir()
    res = resolution if resolution is not None else get_resolution()

    cmd = [
        sys.executable, str(DOWNLOADER),
        "-e", email,
        "-p", password,
        "-u", canonical,
        "-d", str(out_dir),
        "-r", str(res),
    ]

    print(f"\nDownloading: {canonical}")
    print(f"Output: {out_dir}")
    print(f"Resolution: {res} (0=best, 10=fastest)\n")

    proc = subprocess.run(cmd, cwd=str(out_dir))
    if proc.returncode != 0:
        return False, f"Downloader exited with code {proc.returncode}"

    # Try to find the produced PDF and register it
    identifier = identifier_from_url(canonical)
    pdfs = sorted(out_dir.glob(f"*{identifier}*.pdf")) if identifier else []
    # Fallback: any newly-modified PDF
    if not pdfs:
        pdfs = sorted(out_dir.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not pdfs:
        return False, "Download finished but no PDF was found in the output dir"

    pdf = pdfs[0]
    title = pdf.stem.replace("_", " ")
    page_count = 0
    try:
        from pypdf import PdfReader
        page_count = len(PdfReader(str(pdf)).pages)
    except Exception:
        pass  # page count is optional

    add_book(canonical, identifier or pdf.stem, title, pdf, page_count)
    return True, f"Downloaded: {pdf.name} ({pdf.stat().st_size / 1e6:.1f} MB)"
