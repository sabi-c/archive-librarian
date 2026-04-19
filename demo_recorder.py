"""Demo recorder — launches the app and walks through screens for video capture."""
import os, sys, time, threading, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import webview
from webview_app import API


SCREENS_DIR = ROOT / "ui"
OUTPUT = "/Users/seb/Downloads/Manual Library/Seb's Mind/Seb's Mind/Note inbox/archive-librarian-v2-demo.mov"


def run_demo():
    """Drive the UI through the screen flow."""
    time.sleep(2)  # let window settle
    win = webview.windows[0]

    # Welcome (already loaded)
    time.sleep(3)

    # Navigate to login
    win.load_url(f"file://{SCREENS_DIR}/02_login.html")
    time.sleep(2)
    # Type email + password into the form
    win.evaluate_js("document.getElementById('email').value = 'librarian@example.com';")
    time.sleep(0.8)
    win.evaluate_js("document.getElementById('password').value = '••••••••••';")
    time.sleep(1.2)
    # Show success without actually hitting the API
    win.evaluate_js("""
      document.getElementById('login-status').textContent = '✓ archive.org accepted credentials';
      document.getElementById('login-status').style.color = 'var(--ink)';
    """)
    time.sleep(2)

    # Navigate to dashboard (real data shows)
    win.load_url(f"file://{SCREENS_DIR}/03_dashboard.html")
    time.sleep(4)

    # Navigate to library
    win.load_url(f"file://{SCREENS_DIR}/05_library.html")
    time.sleep(4.5)

    # Type in the search box
    win.evaluate_js("""
      const s = document.querySelector('.search-input');
      s.focus();
      const text = 'walden';
      let i = 0;
      const iv = setInterval(() => {
        s.value = text.substring(0, i+1);
        s.dispatchEvent(new Event('input'));
        i++;
        if (i >= text.length) clearInterval(iv);
      }, 150);
    """)
    time.sleep(3)
    # Clear search
    win.evaluate_js("""
      const s = document.querySelector('.search-input');
      s.value = '';
      s.dispatchEvent(new Event('input'));
    """)
    time.sleep(1.5)

    # Settings
    win.load_url(f"file://{SCREENS_DIR}/06_settings.html")
    time.sleep(4)

    # Back to dashboard for the closer
    win.load_url(f"file://{SCREENS_DIR}/03_dashboard.html")
    time.sleep(3)

    # Done — close the window which exits webview.start()
    win.destroy()


def main():
    api = API()
    webview.create_window(
        title="Archive Librarian",
        url=f"file://{SCREENS_DIR}/01_welcome.html",
        js_api=api,
        width=1100, height=900,
        background_color="#f3ead2",
    )
    threading.Thread(target=run_demo, daemon=True).start()
    webview.start(debug=False, gui="cocoa")


if __name__ == "__main__":
    main()
