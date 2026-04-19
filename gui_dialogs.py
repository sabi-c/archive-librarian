"""Native macOS dialogs via osascript.

Avoids the Terminal-typing-and-Enter dance for non-technical users.
On non-macOS systems, falls back to plain stdin prompts.

Public API mirrors what onboarding/CLI need:
    info(title, message)
    confirm(title, message) -> bool
    text_input(title, message, default="") -> str | None
    secure_input(title, message) -> str | None
    choose_folder(title, default_path=None) -> Path | None
    error(title, message)
    success(title, message)
"""

from __future__ import annotations

import platform
import subprocess
from pathlib import Path


def _is_macos() -> bool:
    return platform.system() == "Darwin"


def _osascript(script: str) -> tuple[int, str, str]:
    """Run an AppleScript snippet, return (returncode, stdout, stderr)."""
    proc = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def _escape(s: str) -> str:
    """Escape a string for inclusion in an AppleScript double-quoted literal."""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def info(title: str, message: str) -> None:
    """Informational dialog with an OK button."""
    if _is_macos():
        script = f'''
        display dialog "{_escape(message)}" ¬
            with title "{_escape(title)}" ¬
            buttons {{"OK"}} default button 1 ¬
            with icon note
        '''
        _osascript(script)
    else:
        print(f"\n=== {title} ===\n{message}\n")
        input("Press Enter to continue...")


def choose_button(
    title: str,
    message: str,
    buttons: list[str],
    default: str | None = None,
) -> str | None:
    """Multi-button dialog. Returns the button text clicked, or None on cancel.

    macOS limits dialogs to 3 buttons; if more are passed, falls back to
    `choose from list` for a proper menu.
    """
    if not _is_macos():
        print(f"\n{title}\n{message}\n")
        for i, b in enumerate(buttons, 1):
            print(f"  {i}. {b}")
        try:
            n = int(input("Choose a number: "))
            return buttons[n - 1]
        except (ValueError, IndexError):
            return None

    if len(buttons) <= 3:
        button_list = ", ".join(f'"{_escape(b)}"' for b in buttons)
        default_clause = f' default button "{_escape(default or buttons[-1])}"'
        script = f'''
        try
            set theBtn to button returned of (display dialog "{_escape(message)}" ¬
                with title "{_escape(title)}" ¬
                buttons {{{button_list}}}{default_clause} ¬
                with icon note)
            return theBtn
        on error number -128
            return "__CANCELLED__"
        end try
        '''
        rc, out, _ = _osascript(script)
        if rc != 0 or out == "__CANCELLED__":
            return None
        return out

    # 4+ buttons: use choose from list
    items = ", ".join(f'"{_escape(b)}"' for b in buttons)
    default_clause = f' default items {{"{_escape(default or buttons[0])}"}}'
    script = f'''
    set theChoice to (choose from list {{{items}}} ¬
        with title "{_escape(title)}" ¬
        with prompt "{_escape(message)}"{default_clause} ¬
        OK button name "Choose" cancel button name "Quit")
    if theChoice is false then
        return "__CANCELLED__"
    else
        return item 1 of theChoice as string
    end if
    '''
    rc, out, _ = _osascript(script)
    if rc != 0 or out == "__CANCELLED__":
        return None
    return out


def confirm(title: str, message: str, default_yes: bool = True) -> bool:
    """Yes/No dialog. Returns True on Yes, False on No."""
    if _is_macos():
        default_btn = "Yes" if default_yes else "No"
        script = f'''
        set theResult to button returned of (display dialog "{_escape(message)}" ¬
            with title "{_escape(title)}" ¬
            buttons {{"No", "Yes"}} default button "{default_btn}" ¬
            with icon note)
        return theResult
        '''
        rc, out, _ = _osascript(script)
        return rc == 0 and out == "Yes"
    suffix = "[Y/n]" if default_yes else "[y/N]"
    v = input(f"{title} — {message} {suffix}: ").strip().lower()
    if not v:
        return default_yes
    return v in ("y", "yes")


def text_input(title: str, message: str, default: str = "") -> str | None:
    """Single-line text input. Returns the string, or None if cancelled."""
    if _is_macos():
        script = f'''
        try
            set theAnswer to text returned of (display dialog "{_escape(message)}" ¬
                with title "{_escape(title)}" ¬
                default answer "{_escape(default)}" ¬
                buttons {{"Cancel", "OK"}} default button "OK" ¬
                with icon note)
            return theAnswer
        on error number -128
            return "__CANCELLED__"
        end try
        '''
        rc, out, _ = _osascript(script)
        if rc != 0 or out == "__CANCELLED__":
            return None
        return out
    prompt = f"{title} — {message}"
    if default:
        v = input(f"{prompt} [{default}]: ").strip()
        return v or default
    return input(f"{prompt}: ").strip() or None


def secure_input(title: str, message: str) -> str | None:
    """Password-style input. Returns the string, or None if cancelled."""
    if _is_macos():
        script = f'''
        try
            set thePassword to text returned of (display dialog "{_escape(message)}" ¬
                with title "{_escape(title)}" ¬
                default answer "" ¬
                buttons {{"Cancel", "OK"}} default button "OK" ¬
                with icon note ¬
                with hidden answer)
            return thePassword
        on error number -128
            return "__CANCELLED__"
        end try
        '''
        rc, out, _ = _osascript(script)
        if rc != 0 or out == "__CANCELLED__":
            return None
        return out
    import getpass
    return getpass.getpass(f"{title} — {message}: ") or None


def choose_folder(title: str, default_path: str | Path | None = None) -> Path | None:
    """Native folder picker. Returns the chosen Path, or None if cancelled."""
    if _is_macos():
        default_clause = ""
        if default_path:
            p = str(Path(default_path).expanduser())
            default_clause = f' default location POSIX file "{_escape(p)}"'
        script = f'''
        try
            set theFolder to (choose folder with prompt "{_escape(title)}"{default_clause})
            return POSIX path of theFolder
        on error number -128
            return "__CANCELLED__"
        end try
        '''
        rc, out, _ = _osascript(script)
        if rc != 0 or out == "__CANCELLED__":
            return None
        return Path(out.rstrip("/"))
    p = input(f"{title} (folder path): ").strip()
    return Path(p).expanduser() if p else None


def error(title: str, message: str) -> None:
    """Error dialog (red icon)."""
    if _is_macos():
        script = f'''
        display dialog "{_escape(message)}" ¬
            with title "{_escape(title)}" ¬
            buttons {{"OK"}} default button 1 ¬
            with icon stop
        '''
        _osascript(script)
    else:
        print(f"\n[ERROR] {title}: {message}\n")


def success(title: str, message: str) -> None:
    """Success dialog (caution icon repurposed; macOS doesn't expose a check)."""
    if _is_macos():
        script = f'''
        display dialog "{_escape(message)}" ¬
            with title "{_escape(title)}" ¬
            buttons {{"Great"}} default button 1 ¬
            with icon note
        '''
        _osascript(script)
    else:
        print(f"\n[OK] {title}: {message}\n")
