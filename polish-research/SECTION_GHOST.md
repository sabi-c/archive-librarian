# Archive Librarian v2.0 — Adversarial Audit Report
## GHOST Review

---

## CRITICAL FINDINGS

### 1. **Hard Page Flashes on Navigation** (webview_app.py:59)
**Severity:** CRITICAL — User-facing jank on every screen transition.

Every `navigate()` call uses `load_url()` with a bare file:// URL. This causes the browser to fully reload the page, flashing the background color (#f3ead2) and clearing all script state.

```python
def navigate(self, screen: str) -> None:
    """Switch to a different screen by name (without .html)."""
    target = SCREENS_DIR / f"{screen}.html"
    if target.exists():
        webview.windows[0].load_url(f"file://{target}")  # <- Full reload = flash
```

Each of the 6 screens triggers this (welcome → login → dashboard → library → downloading → settings). No fade, no cross-dissolve, just a white flash. The riso aesthetic demands *ink transitions*.

**Fix:** Use `evaluate_js()` to swap `.container` innerHTML and update state via JS, OR add CSS `transition: opacity 0.3s` to body + temporarily set to 0 during navigation.

---

### 2. **No Loading States Between API Calls** (ui/02_login.html:64–87, ui/03_dashboard.html:112–120)
**Severity:** CRITICAL — App feels broken during network delays.

The login flow (verify → test credentials → navigate) has visual feedback (◌ states), BUT:
- `download_start()` (dashboard) has no loading state; button just sits there
- `library_books()` on dashboard loads with placeholder "Loading..." (good) but then never updates if API fails
- No spinner, no disabled button, no timeout handling

**Example:** Dashboard button at line 52 of ui/03_dashboard.html calls `startDownload()`, which shows a prompt, then silently navigates to 04_downloading even before checking if the download actually started.

```javascript
async function startDownload() {
  const url = prompt('Paste an archive.org URL:\n\nLooks like: https://archive.org/details/SOMETHING');
  if (!url) return;
  const result = await window.pywebview.api.download_start(url);
  if (result.ok) {
    window.pywebview.api.navigate('04_downloading');  // <- Navigates BEFORE download is really running
  } else {
    alert(result.message);  // <- Alert is 1997 UX
  }
}
```

**Fix:** Add a `<div id="spinner">` with CSS spinner. Set `display: none` by default, show on API calls, hide on response. Use in-UI toast instead of `alert()`.

---

### 3. **The Download State Machine Is Fake** (ui/04_downloading.html:116–147)
**Severity:** CRITICAL — UI shows static mock data; doesn't reflect real download state.

The downloading screen polls `download_status()` every 1500ms (good pattern), BUT:
- The "Now title" always shows "LSD: The Consciousness-Expanding Drug" from hardcoded HTML
- The progress bar is hardcoded to 64%
- The log entries are hardcoded (14:32:08, 14:32:09, etc.)
- Polling updates the title from URL ID (line 126), BUT if no real data flows, it's still fake

```javascript
const titleEl = document.querySelector('.now-title');
if (s.url && titleEl) titleEl.textContent = identifier(s.url).replace(/_/g, ' ').replace(/-/g, ' ').toUpperCase();
// This works IF s.url exists, but the rest of the page doesn't reflect real state.
```

**Actual jank:** When you hit "Download Book" → url prompt → navigate to downloading, you see fake data for 2 seconds while the backend actually starts. User doesn't know if it's real or demo.

**Fix:** Backend must send real title/pages/size/progress in `download_status()`. Screens must be JS-only (no hardcoded HTML book data). Update log entries dynamically.

---

### 4. **Dashboard "Library by Domain" Bar Chart Is Fake** (ui/03_dashboard.html:62–68)
**Severity:** CRITICAL — Doesn't reflect actual library contents.

```html
<div class="activity-bars">
  <div class="bar" style="height:80%;" data-domain="Phil"></div>
  <div class="bar" style="height:60%;" data-domain="Health"></div>
  <div class="bar" style="height:95%;" data-domain="Science"></div>
  <!-- etc — hardcoded heights -->
</div>
```

This is static mockup. Backend has no concept of "domain" categorization (no category field in book metadata). The UI pretends it does.

**Related:** The library.html filter chips (line 62–69) list Philosophy/Science/Health/Tech/Craft with counts, but these don't update from real data either. They're hardcoded.

**Fix:** Backend must compute actual domain/category counts from downloaded books. Update bar heights and filter chip counts via JS on page load.

---

### 5. **No Error States — What Happens on Network Failure?**
**Severity:** CRITICAL — Graceful degradation missing.

Scenarios with no handling:

a) **Login fails:** Shows "✗ Failed" status text (line 83, 02_login.html). Does user stay on page? Try again? Button disabled? *No state change.* Button is still clickable, will retry forever.

b) **Download fails:** The 04_downloading screen polls every 1.5s. If status='error', it sets a red pill (line 134–140). But what then? Does user stay stuck on downloading screen? No "Back" button, no retry.

c) **Library fetch fails:** 03_dashboard.html loads "Loading..." (line 74). If `library_books()` throws, the list never updates. Stuck forever.

**Fix:** All API calls need try-catch + user-facing error recovery. Download error screen needs "Retry" and "Back to Dashboard" buttons. Library error needs "Try Again" button.

---

## POLISH FINDINGS

### 6. **No Keyboard Shortcuts**
Modern Mac apps expect: `Cmd+W` close, `Cmd+R` refresh, `Cmd+L` for library. None exist.

**Location:** JavaScript in each screen has no `keydown` listeners (except 02_login.html line 87 for Enter).

**Fix:** Add global keyboard handler in webview_app.py or in every HTML:
```javascript
document.addEventListener('keydown', e => {
  if (e.metaKey && e.key === 'w') window.pywebview.api.quit();
  if (e.metaKey && e.key === 'r') window.location.reload();
  if (e.metaKey && e.key === 'l') window.pywebview.api.navigate('05_library');
});
```

---

### 7. **No Empty States**
- **Library with 0 books:** Shows "Library is empty. Download your first book." (line 101, 03_dashboard.html) — fine, but styling doesn't change. Background still has accent bars, still looks like a data table.
- **Settings with no credentials:** Shows "(not set)" but form layout doesn't change; looks half-filled.
- **Library filter with 0 results:** Shows "No books yet" but doesn't gray out other filters or show "try different search".

**Fix:** Add CSS `.empty-state` class with centered, larger text, muted accent bars, different background. Use in template conditionals.

---

### 8. **Window Chrome Missing**
- **Title bar:** Says "Archive Librarian" (good) but no version or screen context. Should show "Archive Librarian — Dashboard" or similar.
- **Resizing:** Set min_size (900, 700) in webview_app.py:206, but no max_size. Window can stretch to full screen, breaking the RISO box aesthetic (it's meant to be ~950px max-width).
- **Traffic lights:** Standard Cocoa, fine, but no custom styling to match the aesthetic.

**Fix:** Update `create_window()` title dynamically via JS when navigating. Set `max_size=(1200, 1000)`. Consider custom CSS for Cocoa window chrome (if pywebview supports it).

---

### 9. **Focus Management Issues**
- **Login screen:** Has `autofocus` on email input (good, line 35 of 02_login.html), but if user already has credentials saved, it pre-fills email (line 91) but doesn't auto-focus password.
- **No back-button focus:** After downloading completes and navigates to dashboard, focus is lost (no `document.activeElement` management).
- **Tab order:** Never tested; likely follows DOM order, which is fine but untested.

**Fix:** Add `setTimeout(() => document.getElementById('password').focus(), 50)` after pre-fill. After navigation, set focus to main heading or first interactive element.

---

### 10. **Hardcoded Mock Data in Library View** (ui/05_library.html:73–128)
Library screen shows 7 hardcoded book rows (LSD, Tao Te Ching, Walden, etc.). These are replaced at runtime (line 169–181) IF the JS runs, but on first load, user sees the mock data flash and then update. No placeholder skeleton.

**Fix:** On page load, show a skeleton loader (gray bars in place of book rows) instead of real book data.

---

### 11. **No Visual Feedback on Button Hover** (mostly okay, but inconsistent)
- Primary buttons: hover adds `:hover { transform: translate(1px, 1px)...}` (line 140, _riso_base.css) — nice
- Secondary buttons: hover just inverts colors (line 152) — flat
- Icon buttons (dashboard menu, line 9 of 03_dashboard.html): hover inverts — flat
- Filter chips (line 13 of 05_library.html): hover inverts — flat

The primary button is the only one with movement feedback. Others feel static.

**Fix:** Add `transition: all 0.15s ease` to all buttons. Icon buttons should get slight scale or shadow on hover.

---

### 12. **No Disabled Button States**
- Download button while download is running: no `disabled` attribute, no visual change.
- Submit buttons during API calls: no `disabled` state.

If user mashes "Download Book" or "Verify", they'll trigger multiple API calls.

**Fix:** Add `button.disabled = true` during async operations, update CSS for `button:disabled { opacity: 0.5; cursor: not-allowed; }`.

---

## NITPICKS

### 13. **Progress Bar Not Animated** (ui/04_downloading.html:44–48)
The `.progress-fill` width updates via CSS `transition: width 0.3s ease` (good), but the fill color is a halftone pattern that doesn't animate. Looks static even when width changes.

**Fix:** Consider a sliding pattern or pulsing opacity.

---

### 14. **Halftone Circle Not Optimized** (ui/_riso_base.css:119–125)
The halftone circle is a 100px × 100px SVG pattern. On retina screens, this might look pixelated.

**Fix:** Use `background-size: contain` or `background-repeat: round` to scale pattern correctly.

---

### 15. **Form Validation UX** (ui/02_login.html)
If user clicks "Verify" with empty fields, status message appears in inline red text (line 69). Good. But message disappears if user starts typing. No re-validation on blur.

**Fix:** Add real-time validation: on blur, check email format. On input, clear error state.

---

## THE TWO-WINDOW MYSTERY — VERDICT

**Finding:** No evidence in production code. `demo_recorder.py` creates ONE window (line 83):
```python
webview.create_window(
    title="Archive Librarian",
    url=f"file://{SCREENS_DIR}/01_welcome.html",
    js_api=api,
    width=1100, height=900,
    background_color="#f3ead2",
)
```

`webview_app.py` also creates ONE window (line 200). Both use `webview.start(debug=False)`, not `debug=True`.

**Hypothesis:** The two windows in the demo recording are likely:
1. Screen recording software (ScreenFlow, QuickTime) showing the window border + a system notification or menu bar item
2. OR a transient file-picker dialog from `create_file_dialog()` (line 107) that appeared during settings, left briefly visible

**Verdict:** Not a code bug. Likely demo artifact or OS dialog. If it happens again, check `create_file_dialog()` for dialog-not-dismissing bugs (rare in pywebview).

---

## PRE-IMPLEMENTATION CLEANUP

Before adding polish, refactor:

### A. **Extract API State to Shared JS Module**
Currently each screen reimplements `escapeHTML()`, `fmtDate()`, polling loops. Create `shared.js`:
```javascript
// shared.js
const API = window.pywebview.api;
const fmtDate = iso => { /* ... */ };
const escapeHTML = s => { /* ... */ };
```
Include in all screens: `<script src="shared.js"></script>`.

**Files:** Create `/Users/seb/Projects/archive-librarian/ui/shared.js`.

---

### B. **Separate Mock Data from Real Data**
Downloading screen and Library screen both have hardcoded book data. Extract to a separate mock file:
- `ui/mock-books.js` — contains fake book data
- In dev mode: include it; in prod: don't.

**Files:** Create `/Users/seb/Projects/archive-librarian/ui/mock-books.js`.

---

### C. **Centralize Loading/Error UI Components**
Every screen needs spinners, error messages, toast notifications. Create a component system:
```javascript
// ui/components.js
const Spinner = { show: () => {...}, hide: () => {...} };
const Toast = { success: (msg) => {...}, error: (msg) => {...} };
```

**Files:** Create `/Users/seb/Projects/archive-librarian/ui/components.js`.

---

## FINAL VERDICT

**The Good:** The riso aesthetic is consistent and distinctive. Python backend is clean. HTML structure is semantic. CSS is well-organized.

**The Bad:** No transitions, no loading states, no error handling, mock data shipped as real. App feels **fast but unfinished** — like a prototype with no defensive UX.

**Surprise Finding:** The hardcoded book titles in 05_library.html (lines 73–128) are *never rendered*. The JavaScript completely replaces them on load (line 169). So they're dead code. But on first page load, users see them flash before the real data loads. This is the "feels janky" moment.

---

**GHOST**

One finding surprised me most: **the dashboard bar chart doesn't reflect any real data in the backend.** The concept of "Library by Domain" (Philosophy, Health, Science, Tech, History, Craft) is pure fiction. No book metadata includes a domain/category field. The UI invents categories that don't exist, then hardcodes fake distribution. It's a facade app — beautiful facade, but hollow.
