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

    _download_state: dict[str, Any] = {
        "status": "idle", "phase": "", "message": "", "url": "",
        "current_page": 0, "total_pages": 0, "percent": 0,
        "elapsed": "", "remaining": "",
    }

    def _progress_cb(self, p: dict) -> None:
        s = self._download_state
        s.update(p)

    def download_start(self, url: str) -> dict[str, Any]:
        if not url or not url.strip():
            return {"ok": False, "message": "URL required."}
        if self._download_state.get("status") == "running":
            return {"ok": False, "message": "Download already in progress."}

        self._download_state = {
            "status": "running",
            "phase": "starting",
            "message": "Starting download...",
            "url": url.strip(),
            "current_page": 0, "total_pages": 0, "percent": 0,
            "elapsed": "", "remaining": "",
        }

        def _run():
            try:
                ok, msg = download(url.strip(), progress=self._progress_cb)
                self._download_state["status"] = "done" if ok else "error"
                self._download_state["message"] = msg
                if ok:
                    # Background metadata enrichment — fire-and-forget
                    threading.Thread(target=self._enrich_last, daemon=True).start()
            except Exception as e:
                self._download_state["status"] = "error"
                self._download_state["message"] = f"Crashed: {e}"

        threading.Thread(target=_run, daemon=True).start()
        return {"ok": True, "message": "Started."}

    def download_retry(self) -> dict[str, Any]:
        url = self._download_state.get("url", "")
        if not url:
            return {"ok": False, "message": "No previous URL to retry."}
        # Reset state and re-trigger
        self._download_state = {**self._download_state, "status": "idle"}
        return self.download_start(url)

    def download_status(self) -> dict[str, Any]:
        return dict(self._download_state)

    def download_cancel(self) -> dict[str, Any]:
        # Best-effort: mark as cancelled. The subprocess will continue but state
        # tells the UI to stop polling and show cancelled.
        self._download_state["status"] = "cancelled"
        self._download_state["message"] = "Cancelled by user."
        return {"ok": True}

    # --- Metadata enrichment (Open Library) --------------------------------

    def _enrich_last(self) -> None:
        """After a successful download, fetch rich metadata from archive.org's own
        metadata API (more reliable than Open Library for archive.org books)."""
        try:
            import requests
            from library import save_catalog, load_catalog
            cat = load_catalog()
            books = cat.get("books", [])
            if not books:
                return
            latest = books[-1]
            ident = latest.get("identifier", "")
            if not ident or latest.get("enriched"):
                return
            # archive.org metadata API returns everything in one shot
            r = requests.get(f"https://archive.org/metadata/{ident}", timeout=10)
            if r.status_code == 200:
                data = r.json()
                meta = data.get("metadata", {})
                # Title prefer real title over filename-derived
                if meta.get("title"):
                    latest["title"] = meta["title"]
                # Authors / creators
                creator = meta.get("creator")
                if isinstance(creator, list):
                    latest["author"] = ", ".join(creator)
                elif creator:
                    latest["author"] = creator
                # Publication year
                date = meta.get("date") or meta.get("year") or ""
                if date:
                    latest["year"] = str(date)[:4]
                # Subjects — keep as list
                subjects = meta.get("subject")
                if isinstance(subjects, list):
                    latest["subjects"] = subjects[:10]
                elif subjects:
                    latest["subjects"] = [s.strip() for s in subjects.split(";")][:10]
                # Publisher + language for completeness
                if meta.get("publisher"):
                    latest["publisher"] = meta["publisher"] if isinstance(meta["publisher"], str) else (meta["publisher"][0] if meta["publisher"] else "")
                if meta.get("language"):
                    latest["language"] = meta["language"] if isinstance(meta["language"], str) else (meta["language"][0] if meta["language"] else "")
                # Domain — heuristic from subjects (very rough first cut)
                latest["domain"] = self._guess_domain(latest.get("subjects", []))
            latest["enriched"] = True
            save_catalog(cat)
        except Exception as e:
            # Silent — enrichment is best-effort
            pass

    @staticmethod
    def _guess_domain(subjects: list) -> str:
        """Heuristic: bucket subjects into our 8 top-level domains."""
        if not subjects:
            return ""
        text = " ".join(s.lower() for s in subjects)
        rules = [
            ("Philosophy", ["philosophy", "ethics", "metaphysics", "stoic", "buddhism", "religion", "spirituality", "tao", "zen"]),
            ("Science", ["science", "physics", "biology", "chemistry", "psychedelic", "consciousness", "neurology", "drug", "lsd", "research"]),
            ("Health", ["health", "medicine", "nutrition", "wellness", "psychology", "therapy", "anatomy", "fitness"]),
            ("History", ["history", "war", "political", "biography", "memoir", "historical"]),
            ("Tech", ["technology", "computing", "software", "internet", "engineering", "computer"]),
            ("Business", ["business", "economics", "management", "finance", "leadership", "marketing"]),
            ("Craft", ["art", "design", "music", "craft", "writing", "drawing", "literature"]),
            ("Reference", ["dictionary", "encyclopedia", "reference", "handbook", "guide"]),
        ]
        for domain, keywords in rules:
            if any(k in text for k in keywords):
                return domain
        return "Other"

    # --- Help / diagnostics ------------------------------------------------

    def help_diagnostics(self) -> dict[str, Any]:
        """Bundle of diagnostic info for support — copyable to clipboard."""
        import platform
        email, password = get_credentials()
        cfg = load_config()
        return {
            "version": "3.0.0",
            "macos": platform.mac_ver()[0],
            "python": platform.python_version(),
            "library_dir": str(get_library_dir()),
            "library_count": book_count(),
            "credentials_set": bool(email and password),
            "credentials_email": email or "(none)",
            "config": cfg,
        }

    def help_self_test(self) -> dict[str, Any]:
        """Verify the downloader chain works against archive.org's login endpoint."""
        email, password = get_credentials()
        if not (email and password):
            return {"ok": False, "step": "credentials", "message": "No credentials set."}
        ok, msg = test_credentials(email, password)
        if not ok:
            return {"ok": False, "step": "login", "message": msg}
        # Ping archive.org to verify it's reachable
        try:
            import requests
            r = requests.get("https://archive.org/services/account/login/", timeout=10)
            if r.status_code != 200:
                return {"ok": False, "step": "reachability", "message": f"archive.org returned HTTP {r.status_code}"}
        except Exception as e:
            return {"ok": False, "step": "reachability", "message": f"Network error: {e}"}
        return {"ok": True, "message": "All systems healthy. Login + network OK."}

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
