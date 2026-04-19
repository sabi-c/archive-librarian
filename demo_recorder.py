"""Demo recorder — drives the app through every screen with simulated state.

Designed to be invoked behind a screen recorder targeting just the app's
window region. Produces a ~50 second narrative of: welcome → login → verify →
dashboard → initiate download → progress → complete → library → help → settings.

Mock data is injected via JS evaluation so we don't actually hit archive.org.
"""
import os, sys, time, threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import webview
from webview_app import API


SCREENS_DIR = ROOT / "ui"


def step(secs):
    time.sleep(secs)


def run_demo():
    time.sleep(2)
    win = webview.windows[0]

    # 01. Welcome
    step(4)

    # 02. Login
    win.load_url(f"file://{SCREENS_DIR}/02_login.html")
    step(2)
    win.evaluate_js("document.getElementById('email').value = 'librarian@example.com';")
    step(0.7)
    win.evaluate_js("document.getElementById('password').value = '••••••••••';")
    step(1.2)
    win.evaluate_js("""
      const s = document.getElementById('login-status');
      s.textContent = '◌ Verifying with archive.org...';
      s.style.color = 'var(--ink)';
    """)
    step(1.4)
    win.evaluate_js("""
      const s = document.getElementById('login-status');
      s.textContent = '✓ archive.org accepted credentials';
    """)
    step(1.8)

    # 03. Dashboard
    win.load_url(f"file://{SCREENS_DIR}/03_dashboard.html")
    step(4.5)

    # 04. Downloading — simulate the full progress cycle live
    win.load_url(f"file://{SCREENS_DIR}/04_downloading.html")
    step(2)
    # Pause the polling and inject a scripted progression
    win.evaluate_js("""
      clearInterval(pollHandle);
      // Inject mock state and let the existing render functions update
      const fakeStates = [
        { url: 'https://archive.org/details/lsd-consciousness-expanding-drug', phase: 'authenticated', message: 'Authenticated with archive.org', percent: 0, current_page: 0, total_pages: 0, status: 'running' },
        { url: 'https://archive.org/details/lsd-consciousness-expanding-drug', phase: 'loaned', message: 'Borrow grant received · token issued', percent: 0, current_page: 0, total_pages: 302, status: 'running' },
        { phase: 'downloading', message: 'Page 64 of 302 · 02:45 remaining', current_page: 64, total_pages: 302, percent: 21, elapsed: '00:18', remaining: '02:45', status: 'running', url: 'https://archive.org/details/lsd-consciousness-expanding-drug' },
        { phase: 'downloading', message: 'Page 142 of 302 · 02:01 remaining', current_page: 142, total_pages: 302, percent: 47, elapsed: '00:42', remaining: '02:01', status: 'running', url: 'https://archive.org/details/lsd-consciousness-expanding-drug' },
        { phase: 'downloading', message: 'Page 218 of 302 · 01:12 remaining', current_page: 218, total_pages: 302, percent: 72, elapsed: '01:08', remaining: '01:12', status: 'running', url: 'https://archive.org/details/lsd-consciousness-expanding-drug' },
        { phase: 'downloading', message: 'Page 287 of 302 · 00:18 remaining', current_page: 287, total_pages: 302, percent: 95, elapsed: '01:42', remaining: '00:18', status: 'running', url: 'https://archive.org/details/lsd-consciousness-expanding-drug' },
        { phase: 'saving', message: 'Assembling PDF...', percent: 100, current_page: 302, total_pages: 302, status: 'running', url: 'https://archive.org/details/lsd-consciousness-expanding-drug' },
        { phase: 'done', message: 'Saved LSD_the_consciousness-expanding_drug.pdf', percent: 100, current_page: 302, total_pages: 302, status: 'running', url: 'https://archive.org/details/lsd-consciousness-expanding-drug' },
      ];
      let idx = 0;
      window._mockTimer = setInterval(() => {
        if (idx >= fakeStates.length) { clearInterval(window._mockTimer); return; }
        const s = fakeStates[idx++];
        // Manually invoke same logic as poll() with our mock
        const titleEl = document.querySelector('.now-title');
        const authorEl = document.querySelector('.now-author');
        if (s.url && titleEl) titleEl.textContent = identifier(s.url).replace(/_/g, ' ').replace(/-/g, ' ').toUpperCase();
        if (s.url && authorEl) authorEl.textContent = s.url;
        const fill = document.querySelector('.progress-fill');
        const progRow = document.querySelector('.progress-row');
        if (s.percent > 0) {
          fill.style.width = s.percent + '%';
          progRow.innerHTML = `<span>Page ${s.current_page} of ${s.total_pages}</span><span>${s.percent}% · ${s.remaining || '—'} remaining</span>`;
        } else if (s.phase === 'authenticated' || s.phase === 'loaned') {
          progRow.innerHTML = `<span>${s.message}</span><span>—</span>`;
        }
        const now = new Date().toLocaleTimeString('en-US', { hour12: false });
        if (s.message) addLog(now, s.message, 'OK');
      }, 1100);
    """)
    step(11)  # let the simulated progression run

    # Complete state
    win.evaluate_js("""
      clearInterval(window._mockTimer);
      const pill = document.getElementById('status-pill');
      pill.textContent = '✓ Complete';
      pill.className = 'status status-good';
      document.querySelector('.progress-fill').style.width = '100%';
    """)
    step(2.5)

    # 05. Library
    win.load_url(f"file://{SCREENS_DIR}/05_library.html")
    step(4)
    # Type in search to show filter
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
      }, 130);
    """)
    step(2.5)
    win.evaluate_js("""
      const s = document.querySelector('.search-input');
      s.value = '';
      s.dispatchEvent(new Event('input'));
    """)
    step(1.5)

    # 07. Help
    win.load_url(f"file://{SCREENS_DIR}/07_help.html")
    step(4.5)

    # 06. Settings (briefly)
    win.load_url(f"file://{SCREENS_DIR}/06_settings.html")
    step(3.5)

    # Back to dashboard
    win.load_url(f"file://{SCREENS_DIR}/03_dashboard.html")
    step(2.5)

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
