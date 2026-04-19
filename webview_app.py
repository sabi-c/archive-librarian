"""Archive Librarian v2.0 — pywebview app hosting the RISO HTML UI.

Replaces the osascript dialog flow with a real native Cocoa window rendering
the riso-aesthetic HTML/CSS designs. Python-JS bridge exposes the existing
backend (creds.py, downloader.py, library.py, config.py) to the UI layer.
"""

from __future__ import annotations

import os
import sys
import threading
import webbrowser
from pathlib import Path
from typing import Any

# Make sibling modules importable from frozen .app bundle or source
if hasattr(sys, "_MEIPASS"):
    BASE = Path(sys._MEIPASS)
    sys.path.insert(0, str(BASE))
else:
    BASE = Path(__file__).resolve().parent
    sys.path.insert(0, str(BASE))

import webview

from config import get_library_dir, get_resolution, load_config, set_library_dir
from creds import (
    credentials_storage_label,
    delete_credentials,
    get_credentials,
    set_credentials,
    test_credentials,
)
from downloader import download
from library import all_books, book_count, total_size_mb


SCREENS_DIR = BASE / "ui"


# ---------------------------------------------------------------------------
# Python API — exposed to JavaScript via pywebview's js_api parameter
# ---------------------------------------------------------------------------


class API:
    """All methods here are callable from JS as `pywebview.api.<method>()`.

    Returns must be JSON-serializable.
    """

    # --- Navigation ---------------------------------------------------------

    def navigate(self, screen: str) -> None:
        """Switch to a different screen by name (without .html)."""
        target = SCREENS_DIR / f"{screen}.html"
        if target.exists():
            webview.windows[0].load_url(f"file://{target}")

    def open_external(self, url: str) -> None:
        webbrowser.open(url)

    def open_path(self, path: str) -> None:
        os.system(f'open "{Path(path).expanduser()}"')

    # --- Credentials --------------------------------------------------------

    def credentials_status(self) -> dict[str, Any]:
        email, password = get_credentials()
        return {
            "set": bool(email and password),
            "email": email or "",
            "storage": credentials_storage_label(),
        }

    def credentials_save(self, email: str, password: str) -> dict[str, Any]:
        if not (email and password):
            return {"ok": False, "message": "Email and password required."}
        if not set_credentials(email, password):
            return {"ok": False, "message": "Could not save to Keychain."}
        return {"ok": True, "message": f"Saved credentials for {email}."}

    def credentials_test(self, email: str, password: str) -> dict[str, Any]:
        if not (email and password):
            email, password = get_credentials()
        if not (email and password):
            return {"ok": False, "message": "No credentials to test."}
        ok, msg = test_credentials(email, password)
        return {"ok": ok, "message": msg, "email": email}

    def credentials_delete(self) -> dict[str, Any]:
        ok = delete_credentials()
        return {"ok": ok, "message": "Credentials removed." if ok else "Delete failed."}

    # --- Config -------------------------------------------------------------

    def config(self) -> dict[str, Any]:
        cfg = load_config()
        return {
            "library_dir": str(get_library_dir()),
            "resolution": get_resolution(),
            "credentials_storage": credentials_storage_label(),
        }

    def choose_library_dir(self) -> dict[str, Any]:
        result = webview.windows[0].create_file_dialog(
            webview.FOLDER_DIALOG,
            directory=str(get_library_dir().parent),
        )
        if not result:
            return {"ok": False, "path": str(get_library_dir())}
        new_path = result[0] if isinstance(result, (list, tuple)) else result
        set_library_dir(new_path)
        return {"ok": True, "path": new_path}

    # --- Library ------------------------------------------------------------

    def library_summary(self) -> dict[str, Any]:
        books = all_books()
        return {
            "count": book_count(),
            "total_mb": total_size_mb(),
            "library_dir": str(get_library_dir()),
        }

    def library_books(self, limit: int = 100) -> list[dict]:
        books = sorted(
            all_books(),
            key=lambda b: b.get("downloaded_at", ""),
            reverse=True,
        )
        return books[:limit]

    def library_timeline(self, months: int = 6) -> list[dict]:
        """Books acquired per month for the last N months. Real data only."""
        from datetime import datetime, timedelta
        from collections import OrderedDict
        now = datetime.utcnow()
        # Build buckets for last N months, oldest first
        buckets = OrderedDict()
        for i in range(months - 1, -1, -1):
            month_start = (now.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
            label = month_start.strftime("%b").upper()
            buckets[month_start.strftime("%Y-%m")] = {"label": label, "count": 0}
        for b in all_books():
            ts = b.get("downloaded_at", "")
            if not ts:
                continue
            try:
                d = datetime.fromisoformat(ts.replace("Z", "+00:00").replace("+00:00", ""))
                key = d.strftime("%Y-%m")
                if key in buckets:
                    buckets[key]["count"] += 1
            except Exception:
                continue
        return list(buckets.values())

    def library_open(self) -> None:
        os.system(f'open "{get_library_dir()}"')

    def book_open(self, pdf_path: str) -> None:
        os.system(f'open -a Preview "{pdf_path}"')

    # --- Download -----------------------------------------------------------

    _download_state: dict[str, Any] = {"status": "idle", "message": "", "url": ""}

    def download_start(self, url: str) -> dict[str, Any]:
        if not url or not url.strip():
            return {"ok": False, "message": "URL required."}
        if self._download_state.get("status") == "running":
            return {"ok": False, "message": "Download already in progress."}

        self._download_state = {
            "status": "running",
            "message": "Starting download...",
            "url": url.strip(),
        }

        def _run():
            try:
                ok, msg = download(url.strip())
                self._download_state = {
                    "status": "done" if ok else "error",
                    "message": msg,
                    "url": url.strip(),
                }
            except Exception as e:
                self._download_state = {
                    "status": "error",
                    "message": f"Download crashed: {e}",
                    "url": url.strip(),
                }

        threading.Thread(target=_run, daemon=True).start()
        return {"ok": True, "message": "Started."}

    def download_status(self) -> dict[str, Any]:
        return dict(self._download_state)

    # --- App lifecycle ------------------------------------------------------

    def quit(self) -> None:
        for w in webview.windows:
            w.destroy()


# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------


def first_screen() -> Path:
    """Pick the screen to show on launch — welcome if no creds, dashboard otherwise."""
    email, password = get_credentials()
    name = "03_dashboard" if (email and password) else "01_welcome"
    return SCREENS_DIR / f"{name}.html"


def main() -> int:
    api = API()
    start = first_screen()
    webview.create_window(
        title="Archive Librarian",
        url=f"file://{start}",
        js_api=api,
        width=1100,
        height=900,
        min_size=(900, 700),
        background_color="#f3ead2",
        text_select=True,
        confirm_close=False,
    )
    webview.start(debug=False, gui="cocoa" if sys.platform == "darwin" else None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
