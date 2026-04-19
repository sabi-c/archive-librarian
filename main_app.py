"""GUI entry point for the bundled .app.

Launched by double-clicking Archive Librarian.app. Runs entirely through
native macOS dialogs — no Terminal interaction at all.

Flow:
  1. First launch: no credentials → run onboarding wizard
  2. Subsequent launches: show main menu (Download / View Library / Settings / Quit)
  3. Download Book: prompt for URL, download, ask if user wants another
"""

from __future__ import annotations

import sys
import subprocess
from pathlib import Path

# When running from a PyInstaller bundle, sys._MEIPASS is the temp dir
# containing bundled data files. Use that for finding archive-org-downloader.py
if hasattr(sys, "_MEIPASS"):
    sys.path.insert(0, sys._MEIPASS)
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import gui_dialogs as gui
from config import get_library_dir
from creds import get_credentials
from downloader import download
from library import all_books, book_count, total_size_mb
from onboarding import run_onboarding


def needs_setup() -> bool:
    email, password = get_credentials()
    return not (email and password)


def main_menu_loop() -> None:
    """Show the main menu in a loop until user quits."""
    while True:
        # Use a dialog with multiple buttons as the menu
        choice = gui.choose_button(
            "Archive Librarian",
            f"What would you like to do?\n\n"
            f"Library: {book_count()} books ({total_size_mb()} MB)",
            buttons=["Download Book", "View Library", "Settings", "Quit"],
            default="Download Book",
        )
        if choice == "Download Book":
            do_download_flow()
        elif choice == "View Library":
            do_view_library()
        elif choice == "Settings":
            do_settings()
        elif choice in (None, "Quit"):
            break


def do_download_flow() -> None:
    """Loop: prompt for URL, download, ask if user wants another."""
    while True:
        url = gui.text_input(
            "Download a book",
            "Paste the archive.org URL of the book you want to download.\n\n"
            "It should look like:\nhttps://archive.org/details/SOMETHING",
        )
        if not url:
            return
        gui.info(
            "Downloading...",
            "The book is downloading now. This window will close and the "
            "download will run in the background. You'll get a notification "
            "when it's done.\n\nThis can take a few minutes for large books.",
        )
        ok, message = download(url)
        if ok:
            again = gui.confirm(
                "✓ Download complete",
                f"{message}\n\nDownload another book?",
                default_yes=False,
            )
            if not again:
                return
        else:
            retry = gui.confirm(
                "✗ Download failed",
                f"{message}\n\nTry again with a different URL?",
                default_yes=False,
            )
            if not retry:
                return


def do_view_library() -> None:
    """Open the library folder in Finder."""
    library = get_library_dir()
    library.mkdir(parents=True, exist_ok=True)
    subprocess.run(["open", str(library)])


def do_settings() -> None:
    """Re-run the setup wizard for credentials/folder changes."""
    confirmed = gui.confirm(
        "Settings",
        "This will run the setup wizard again so you can update your "
        "archive.org login or change where books are saved.\n\nContinue?",
        default_yes=True,
    )
    if confirmed:
        run_onboarding()


def main() -> int:
    try:
        if needs_setup():
            return run_onboarding()
        main_menu_loop()
        return 0
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        gui.error(
            "Something went wrong",
            f"An unexpected error occurred:\n\n{e}\n\n"
            "If this keeps happening, contact whoever sent you this app.",
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
