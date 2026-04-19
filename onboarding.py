"""Interactive onboarding walkthrough for new users.

Run via: librarian setup

Walks the user through:
  1. Welcome
  2. Confirming they have an archive.org account (and creating one if not)
  3. Entering and storing credentials securely
  4. Live-testing credentials against archive.org
  5. Choosing where books download to
  6. Walking through how to find a borrowable book on archive.org
  7. Optional: doing a first test download
"""

from __future__ import annotations

import getpass
import sys
import time
import webbrowser
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
    from rich.markdown import Markdown
    HAVE_RICH = True
except ImportError:
    HAVE_RICH = False

from config import get_library_dir, set_library_dir, load_config
from creds import (
    get_credentials,
    set_credentials,
    test_credentials,
    credentials_storage_label,
)
from downloader import download


# ---------------------------------------------------------------------------
# Output helpers (Rich if available, plain text fallback)
# ---------------------------------------------------------------------------

console = Console() if HAVE_RICH else None


def panel(title: str, body: str, color: str = "cyan") -> None:
    if HAVE_RICH:
        console.print(Panel.fit(body, title=title, border_style=color, padding=(1, 2)))
    else:
        bar = "=" * (len(title) + 4)
        print(f"\n{bar}\n  {title}\n{bar}\n{body}\n")


def info(msg: str) -> None:
    if HAVE_RICH:
        console.print(f"[cyan]→[/cyan] {msg}")
    else:
        print(f"-> {msg}")


def ok(msg: str) -> None:
    if HAVE_RICH:
        console.print(f"[green]✓[/green] {msg}")
    else:
        print(f"[OK] {msg}")


def warn(msg: str) -> None:
    if HAVE_RICH:
        console.print(f"[yellow]![/yellow] {msg}")
    else:
        print(f"[!] {msg}")


def err(msg: str) -> None:
    if HAVE_RICH:
        console.print(f"[red]✗[/red] {msg}")
    else:
        print(f"[X] {msg}")


def ask(prompt: str, default: str | None = None) -> str:
    if HAVE_RICH:
        return Prompt.ask(prompt, default=default or None)
    if default:
        v = input(f"{prompt} [{default}]: ").strip()
        return v or default
    return input(f"{prompt}: ").strip()


def confirm(prompt: str, default: bool = True) -> bool:
    if HAVE_RICH:
        return Confirm.ask(prompt, default=default)
    suffix = "[Y/n]" if default else "[y/N]"
    v = input(f"{prompt} {suffix}: ").strip().lower()
    if not v:
        return default
    return v in ("y", "yes")


# ---------------------------------------------------------------------------
# Walkthrough steps
# ---------------------------------------------------------------------------


def step_welcome() -> None:
    body = (
        "[bold]archive-librarian[/bold] downloads books from archive.org as "
        "real PDFs, including borrow-protected titles, so you can read them "
        "offline and keep them in your own library.\n\n"
        "This setup takes about 3 minutes. We'll:\n"
        "  1. Confirm you have an archive.org account\n"
        "  2. Save your credentials securely on this computer\n"
        "  3. Test them against archive.org\n"
        "  4. Pick where books should download to\n"
        "  5. Walk through grabbing your first book"
    ) if HAVE_RICH else (
        "archive-librarian downloads books from archive.org as PDFs.\n"
        "Setup is about 3 minutes. We'll save your credentials securely,\n"
        "test them, pick a download folder, and grab your first book."
    )
    panel("Welcome", body, "cyan")


def step_account() -> None:
    panel(
        "Step 1 of 5 — archive.org account",
        "You need a free archive.org account.\n"
        "If you don't have one, sign up at: [link]https://archive.org/account/signup[/link]",
        "cyan",
    )
    if confirm("Open the signup page in your browser now?", default=False):
        webbrowser.open("https://archive.org/account/signup")
        info("Sign up, verify your email, then come back here.")
        input("Press Enter when you're ready to continue...")


def step_credentials() -> tuple[str, str] | None:
    panel(
        "Step 2 of 5 — Credentials",
        f"Your password will be stored in [bold]{credentials_storage_label()}[/bold].\n"
        "It is never written to a plaintext file or sent anywhere except archive.org.",
        "cyan",
    )

    existing_email, existing_password = get_credentials()
    if existing_email and existing_password:
        info(f"Found existing credentials for {existing_email}")
        if not confirm("Replace them?", default=False):
            return existing_email, existing_password

    email = ask("archive.org email")
    if not email:
        err("Email required.")
        return None
    password = getpass.getpass("archive.org password (hidden as you type): ")
    if not password:
        err("Password required.")
        return None

    if not set_credentials(email, password):
        err("Could not save credentials. Check permissions and try again.")
        return None
    ok(f"Saved credentials for {email}")
    return email, password


def step_test_credentials(email: str, password: str) -> bool:
    panel(
        "Step 3 of 5 — Verifying with archive.org",
        "Hitting the archive.org login endpoint to confirm your credentials work.\n"
        "(Takes ~5 seconds.)",
        "cyan",
    )
    info("Testing...")
    success, message = test_credentials(email, password)
    if success:
        ok(message)
        return True
    err(message)
    warn("If this is wrong, run [bold]librarian setup[/bold] again to re-enter.")
    return False


def step_library_dir() -> Path:
    current = get_library_dir()
    panel(
        "Step 4 of 5 — Where books download",
        f"Default: [bold]{current}[/bold]\n\n"
        "Books, the catalog, and any future markdown conversions will live here.",
        "cyan",
    )
    if confirm("Use the default location?", default=True):
        return current
    new = ask("Enter the folder path", default=str(current))
    set_library_dir(new)
    p = Path(new).expanduser()
    p.mkdir(parents=True, exist_ok=True)
    ok(f"Library set to {p}")
    return p


def step_walkthrough() -> None:
    body = (
        "Most books on archive.org are [bold]borrow-only[/bold] — you have to "
        "click 'Borrow for 1 hour' (or 14 days) before you can download.\n\n"
        "[bold]How to grab a book:[/bold]\n"
        "  1. Open [link]https://archive.org[/link] and sign in\n"
        "  2. Search for the book you want\n"
        "  3. On the book's page, click the orange [bold]Borrow for 1 hour[/bold] button\n"
        "  4. Once the book opens in the reader, copy the URL from your browser\n"
        "     (it looks like https://archive.org/details/SOMETHING)\n"
        "  5. Paste it into [bold]librarian download <URL>[/bold]\n\n"
        "[dim]Tip: Some books are borrow-only, some are openly downloadable.[/dim]\n"
        "[dim]This tool handles both — you just need to be logged in for the borrow ones.[/dim]"
    ) if HAVE_RICH else (
        "How to grab a book:\n"
        "  1. Open https://archive.org and sign in\n"
        "  2. Search for the book\n"
        "  3. Click 'Borrow for 1 hour' on the book's page\n"
        "  4. Copy the URL once the book opens (https://archive.org/details/SOMETHING)\n"
        "  5. Paste it into: librarian download <URL>"
    )
    panel("Step 5 of 5 — How to grab a book", body, "cyan")


def step_first_download() -> None:
    panel(
        "Optional — Test download",
        "Want to do a test run now? Paste any archive.org book URL.\n"
        "[dim]Skip with Enter if you'd rather try later.[/dim]",
        "cyan",
    )
    url = ask("Book URL (or press Enter to skip)", default="")
    if not url:
        info("Skipped. Run [bold]librarian download <URL>[/bold] anytime.")
        return
    success, message = download(url)
    (ok if success else err)(message)


def run_onboarding() -> int:
    step_welcome()
    print()
    step_account()
    print()
    creds = step_credentials()
    if not creds:
        return 1
    print()
    if not step_test_credentials(*creds):
        warn("Credentials saved but failed the live test. You can still try downloads.")
    print()
    step_library_dir()
    print()
    step_walkthrough()
    print()
    step_first_download()
    print()
    panel(
        "Setup complete",
        "You're ready. Useful commands:\n\n"
        "  [bold]librarian download <URL>[/bold]   — download a book\n"
        "  [bold]librarian list[/bold]              — show your library\n"
        "  [bold]librarian status[/bold]            — check credentials + paths\n"
        "  [bold]librarian help[/bold]              — full command list",
        "green",
    )
    return 0


if __name__ == "__main__":
    sys.exit(run_onboarding())
