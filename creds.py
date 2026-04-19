"""Credential management for archive-librarian.

Uses macOS Keychain when available (`security` command). Falls back to a
0600-permission file at ~/.archive-librarian/credentials for other platforms.

Public API:
    get_credentials() -> tuple[str | None, str | None]
    set_credentials(email, password) -> bool
    delete_credentials() -> bool
    test_credentials(email, password) -> tuple[bool, str]   # live login check
"""

from __future__ import annotations

import os
import platform
import subprocess
import sys
from pathlib import Path

import requests

from config import CONFIG_DIR


SERVICE = "archive.org"
LEGACY_FILE = CONFIG_DIR / "credentials"


# ---------------------------------------------------------------------------
# Keychain (macOS) helpers
# ---------------------------------------------------------------------------


def _is_macos() -> bool:
    return platform.system() == "Darwin"


def _keychain_get_email() -> str | None:
    r = subprocess.run(
        ["security", "find-generic-password", "-s", SERVICE, "-g"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        return None
    for line in (r.stdout + r.stderr).splitlines():
        line = line.strip()
        if line.startswith('"acct"'):
            try:
                return line.split("=", 1)[1].strip().strip('"')
            except IndexError:
                continue
    return None


def _keychain_get_password(email: str) -> str | None:
    r = subprocess.run(
        ["security", "find-generic-password", "-s", SERVICE, "-a", email, "-w"],
        capture_output=True, text=True,
    )
    return r.stdout.strip() if r.returncode == 0 else None


def _keychain_set(email: str, password: str) -> bool:
    # Delete then add to avoid duplicates
    subprocess.run(
        ["security", "delete-generic-password", "-s", SERVICE, "-a", email],
        capture_output=True,
    )
    r = subprocess.run(
        [
            "security", "add-generic-password",
            "-s", SERVICE,
            "-a", email,
            "-w", password,
            "-U",
            "-D", "application password",
            "-j", "Archive.org login (archive-librarian)",
        ],
        capture_output=True, text=True,
    )
    return r.returncode == 0


def _keychain_delete(email: str) -> bool:
    r = subprocess.run(
        ["security", "delete-generic-password", "-s", SERVICE, "-a", email],
        capture_output=True,
    )
    return r.returncode == 0


# ---------------------------------------------------------------------------
# File-fallback (Linux / Windows)
# ---------------------------------------------------------------------------


def _file_get() -> tuple[str | None, str | None]:
    if not LEGACY_FILE.exists():
        return None, None
    try:
        lines = LEGACY_FILE.read_text().strip().splitlines()
        email = next((l.split("=", 1)[1] for l in lines if l.startswith("email=")), None)
        password = next((l.split("=", 1)[1] for l in lines if l.startswith("password=")), None)
        return email, password
    except Exception:
        return None, None


def _file_set(email: str, password: str) -> bool:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    LEGACY_FILE.write_text(f"email={email}\npassword={password}\n")
    os.chmod(LEGACY_FILE, 0o600)
    return True


def _file_delete() -> bool:
    if LEGACY_FILE.exists():
        LEGACY_FILE.unlink()
    return True


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_credentials() -> tuple[str | None, str | None]:
    if _is_macos():
        email = _keychain_get_email()
        if email:
            return email, _keychain_get_password(email)
        # Fall through to file in case user moved across machines
    return _file_get()


def set_credentials(email: str, password: str) -> bool:
    if _is_macos():
        return _keychain_set(email, password)
    return _file_set(email, password)


def delete_credentials() -> bool:
    if _is_macos():
        email = _keychain_get_email()
        if email:
            return _keychain_delete(email)
        return True
    return _file_delete()


def credentials_storage_label() -> str:
    return "macOS Keychain" if _is_macos() else f"file ({LEGACY_FILE})"


# ---------------------------------------------------------------------------
# Live test against archive.org
# ---------------------------------------------------------------------------


def test_credentials(email: str, password: str) -> tuple[bool, str]:
    """Test login against archive.org using the same flow as the downloader.

    Mirrors archive-org-downloader.py's login() exactly so a green here
    guarantees downloads will work.
    """
    import json
    try:
        s = requests.Session()
        # Step 1: GET to obtain a CSRF token
        r = s.get("https://archive.org/services/account/login/", timeout=15)
        try:
            token_data = r.json()
        except Exception:
            return False, f"unexpected token response (HTTP {r.status_code})"
        if not token_data.get("success"):
            return False, "archive.org didn't issue a login token"
        token = token_data["value"]["token"]

        # Step 2: POST credentials with token
        resp = s.post(
            "https://archive.org/services/account/login/",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=json.dumps({"username": email, "password": password, "t": token}),
            timeout=20,
        )
        try:
            body = resp.json()
        except Exception:
            return False, f"login returned non-JSON (HTTP {resp.status_code})"

        if body.get("success"):
            return True, "archive.org accepted credentials"
        if body.get("value") == "bad_login":
            return False, "archive.org rejected credentials (wrong email or password)"
        return False, f"login failed: {body.get('value', 'unknown error')}"
    except requests.exceptions.RequestException as e:
        return False, f"network error: {e}"
    except Exception as e:
        return False, f"error: {e}"
