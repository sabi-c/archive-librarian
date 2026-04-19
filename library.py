"""Library catalog — tracks downloaded books in library.json."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from config import get_library_dir


def catalog_path() -> Path:
    return get_library_dir() / "library.json"


def load_catalog() -> dict[str, Any]:
    p = catalog_path()
    if not p.exists():
        return {"books": [], "updated": None}
    try:
        with open(p) as f:
            return json.load(f)
    except Exception:
        return {"books": [], "updated": None}


def save_catalog(cat: dict[str, Any]) -> None:
    cat["updated"] = datetime.utcnow().isoformat() + "Z"
    with open(catalog_path(), "w") as f:
        json.dump(cat, f, indent=2)


def add_book(url: str, identifier: str, title: str, pdf_path: Path, page_count: int = 0) -> None:
    cat = load_catalog()
    # Deduplicate by identifier
    cat["books"] = [b for b in cat.get("books", []) if b.get("identifier") != identifier]
    cat["books"].append({
        "identifier": identifier,
        "title": title,
        "url": url,
        "pdf_path": str(pdf_path),
        "pdf_size_mb": round(pdf_path.stat().st_size / 1e6, 1) if pdf_path.exists() else 0,
        "page_count": page_count,
        "downloaded_at": datetime.utcnow().isoformat() + "Z",
    })
    save_catalog(cat)


def all_books() -> list[dict]:
    return load_catalog().get("books", [])


def book_count() -> int:
    return len(all_books())


def total_size_mb() -> float:
    return round(sum(b.get("pdf_size_mb", 0) for b in all_books()), 1)
