"""Configuration for archive-librarian.

Stores user-configurable paths in ~/.archive-librarian/config.toml so the
same package works on any machine without touching the source.
"""

from __future__ import annotations

import os
import sys
import tomllib
import tomli_w
from pathlib import Path
from typing import Any


CONFIG_DIR = Path.home() / ".archive-librarian"
CONFIG_FILE = CONFIG_DIR / "config.toml"


DEFAULTS: dict[str, Any] = {
    "library_dir": str(Path.home() / "Books" / "Archive"),
    "resolution": 3,  # 0=best, higher=lower; default is good balance
    "threads": 50,
}


def _ensure_config_dir() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict[str, Any]:
    """Load config, merging file values over defaults."""
    cfg = dict(DEFAULTS)
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "rb") as f:
                cfg.update(tomllib.load(f))
        except Exception as e:
            print(f"[!] Failed to read {CONFIG_FILE}: {e}", file=sys.stderr)
    return cfg


def save_config(cfg: dict[str, Any]) -> None:
    """Write config to disk."""
    _ensure_config_dir()
    # Only persist non-default keys to keep file minimal & forward-compatible
    persisted = {k: v for k, v in cfg.items() if v != DEFAULTS.get(k)}
    with open(CONFIG_FILE, "wb") as f:
        tomli_w.dump(persisted or cfg, f)


def get_library_dir() -> Path:
    """Return the configured library directory, ensuring it exists."""
    p = Path(load_config()["library_dir"]).expanduser()
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_resolution() -> int:
    return int(load_config().get("resolution", 3))


def set_library_dir(path: str | Path) -> None:
    cfg = load_config()
    cfg["library_dir"] = str(Path(path).expanduser())
    save_config(cfg)
