"""Native macOS onboarding for non-technical users.

Run via: librarian setup
Or invoked automatically by Install Archive Librarian.command after install.

Uses native dialogs for every interaction. Terminal stays in the background
showing progress, but the user never types into Terminal.
"""

from __future__ import annotations

import sys
import webbrowser
from pathlib import Path

from config import get_library_dir, set_library_dir
from creds import (
    get_credentials,
    set_credentials,
    test_credentials,
    credentials_storage_label,
)
from downloader import download
import gui_dialogs as gui


# ---------------------------------------------------------------------------
# Walkthrough steps
# ---------------------------------------------------------------------------


def step_welcome() -> bool:
    return gui.confirm(
        "Welcome to Archive Librarian",
        "Archive Librarian downloads books from archive.org as PDFs you can keep on your computer — including borrow-protected ones.\n\n"
        "Setup takes about 3 minutes. We will:\n\n"
        "• Confirm you have an archive.org account (free)\n"
        "• Save your login securely on this computer\n"
        "• Test that login against archive.org\n"
        "• Pick where to save your books\n"
        "• Show you how to grab your first book\n\n"
        "Ready to start?",
        default_yes=True,
    )


def step_account() -> bool:
    has_account = gui.confirm(
        "Step 1 of 5 — archive.org account",
        "Do you already have a free account on archive.org?",
        default_yes=True,
    )
    if not has_account:
        gui.info(
            "Create a free account",
            "We'll open archive.org's signup page in your browser.\n\n"
            "Sign up with any email, verify your email address (check your inbox), then come back here and click Continue.",
        )
        webbrowser.open("https://archive.org/account/signup")
        gui.info(
            "When ready",
            "After you've signed up and verified your email, click OK to continue setup.",
        )
    return True


def step_credentials() -> tuple[str, str] | None:
    existing_email, existing_password = get_credentials()
    if existing_email and existing_password:
        keep = gui.confirm(
            "Step 2 of 5 — Login",
            f"You already have credentials saved for:\n\n{existing_email}\n\n"
            f"Stored in: {credentials_storage_label()}\n\n"
            "Want to keep these and skip ahead?",
            default_yes=True,
        )
        if keep:
            return existing_email, existing_password

    gui.info(
        "Step 2 of 5 — Login",
        "Next, enter your archive.org email and password.\n\n"
        f"Your password is stored in {credentials_storage_label()} — encrypted, like Safari saves your passwords. It's never written to a plain file or shared with anyone except archive.org.",
    )

    email = gui.text_input(
        "archive.org email",
        "What's the email address you use for archive.org?",
    )
    if not email:
        gui.error("Cancelled", "Setup cancelled. You can run it again anytime.")
        return None

    password = gui.secure_input(
        "archive.org password",
        f"Enter the password for {email}.\n\n(Hidden as you type. Click OK when done.)",
    )
    if not password:
        gui.error("Cancelled", "Setup cancelled. You can run it again anytime.")
        return None

    if not set_credentials(email, password):
        gui.error("Couldn't save", "Failed to save credentials. Try again.")
        return None

    return email, password


def step_test_credentials(email: str, password: str) -> bool:
    gui.info(
        "Step 3 of 5 — Verifying",
        "Now we'll check that your login works by signing in to archive.org.\n\nThis takes a few seconds.",
    )
    print("\n→ Testing credentials against archive.org...", flush=True)
    success_flag, message = test_credentials(email, password)
    if success_flag:
        gui.success(
            "✓ Login confirmed",
            f"archive.org accepted your credentials. You're good to go.\n\nLogged in as: {email}",
        )
        print(f"✓ {message}")
        return True

    gui.error(
        "✗ Login failed",
        f"archive.org didn't accept those credentials.\n\nReason: {message}\n\n"
        "Double-check by signing in to archive.org in your browser. If that works, run setup again and try once more.",
    )
    print(f"✗ {message}")
    return False


def step_library_dir() -> Path:
    current = get_library_dir()
    use_default = gui.confirm(
        "Step 4 of 5 — Where to save books",
        f"Books will be saved here by default:\n\n{current}\n\n"
        "Use this folder?\n\n(Click No to choose a different folder.)",
        default_yes=True,
    )
    if use_default:
        return current

    chosen = gui.choose_folder(
        "Choose a folder for your books",
        default_path=current.parent if current.exists() else Path.home(),
    )
    if not chosen:
        gui.info("Keeping default", f"Using the default folder: {current}")
        return current

    set_library_dir(chosen)
    gui.success("Library folder set", f"Books will save to:\n\n{chosen}")
    return chosen


def step_walkthrough() -> None:
    gui.info(
        "Step 5 of 5 — How to grab a book",
        "Here's how to download any book from archive.org:\n\n"
        "1. Go to archive.org in your browser and sign in.\n\n"
        "2. Search for the book you want.\n\n"
        "3. On the book's page, click the orange 'Borrow for 1 hour' button.\n\n"
        "4. The book opens in a reader. Copy the URL from your browser's address bar — it looks like https://archive.org/details/SOMETHING\n\n"
        "5. Come back to Archive Librarian and paste it. Done.\n\n"
        "Some books don't need the borrow step — those download directly. Either way, this app handles it.",
    )


def step_first_download() -> None:
    do_test = gui.confirm(
        "Want to download a book right now?",
        "Optional — paste an archive.org URL and we'll download a book to test the whole flow.\n\nOr skip for later.",
        default_yes=True,
    )
    if not do_test:
        return
    url = gui.text_input(
        "Book URL",
        "Paste the archive.org URL of the book you want to download:",
    )
    if not url:
        return
    print(f"\n→ Downloading {url}...", flush=True)
    print("This can take a few minutes depending on the book size.\n")
    ok, message = download(url)
    if ok:
        gui.success("Download complete", message)
    else:
        gui.error("Download failed", message)


def step_done() -> None:
    library = get_library_dir()
    gui.success(
        "Setup complete",
        f"You're ready. Books will save to:\n\n{library}\n\n"
        "To download more books, double-click 'Download Book' on your Desktop, or open Archive Librarian again from the same folder.\n\n"
        "Have fun.",
    )


def run_onboarding() -> int:
    if not step_welcome():
        print("Setup cancelled by user.")
        return 1
    step_account()
    creds = step_credentials()
    if not creds:
        return 1
    step_test_credentials(*creds)
    step_library_dir()
    step_walkthrough()
    step_first_download()
    step_done()
    return 0


if __name__ == "__main__":
    sys.exit(run_onboarding())
