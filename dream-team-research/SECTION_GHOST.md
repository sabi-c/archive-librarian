# GHOST Architecture Audit: Archive Librarian

## The Architectural Tension

The tension is **irreconcilable as currently scoped**: Seb wants a Pip-Boy/Vault-Tec ASCII aesthetic (which requires interactive Terminal control with input, color, borders, real-time updates) but also wants his non-technical brother to double-click an .app and never see Terminal at all. These are not compatible without adding a third-party runtime. The osascript dialog framework has **no path** to ASCII aesthetics — it is fundamentally modal, blocking, and hostile to stateful TUIs. Trying to bolt ASCII art onto dialogs produces novelty, not usability.

---

## Path Comparison: A Through E

### Path A: Enhanced dialogs (osascript + ASCII banners)
**Pros:**
- Zero new dependencies
- Brother sees exactly zero Terminal
- Dialogs already work cross-platform
- Installation remains trivial

**Cons:**
- ASCII banners in modal dialogs are kitsch, not functional
- Pip-Boy aesthetic *requires* full screen control (borders, colors, cursor movement)
- Scrollable multi-line art kills UX ("read the banner, click OK" is tedium)
- Maintenance: every dialog becomes a text art editor
- Seb will hate it in 2 weeks — it's a costume on a skeleton

**Hidden costs:**
- Temptation to add fancier ASCII creates unmaintainable string concatenation hell
- Dialog width limits (macOS caps around 600px) make art distorted
- Keychain integration stays but dialogs feel disconnected from the "theme"

**6-month failure mode:** Seb ships one ASCII banner, realizes it looks sad, removes it, then spends 3 hours designing the "perfect" banner that still looks out of place in a dialog. Brother doesn't care.

---

### Path B: Launch Terminal for TUI (Textual)
**Pros:**
- Seb gets full ASCII control: Pip-Boy UI, colors, real-time updates, responsiveness
- Brother still double-clicks — Terminal appears automatically
- Textual is mature, 200+ stars, actively maintained
- Can keep download logic isolated (subprocess calls Terminal, waits)

**Cons:**
- Brother now sees Terminal for **every interaction**, even trivial ones
- Terminal window becomes a permanent visual presence
- Crashes in Terminal feel more threatening than dialog failures
- macOS Terminal theming differs across Macs; design looks different everywhere
- Requires bundling Textual in the venv (adds disk + complexity)

**Hidden costs:**
- Terminal window positioning is OS-dependent — may not appear in focus
- If user closes Terminal mid-operation, graceful recovery is hard
- Copy-paste workflows break (Terminal focus vs Finder)
- Debugging is now "look at Terminal" not "dialog shows the error"
- Brother closes it mid-operation because he doesn't know what it is

**6-month failure mode:** Brother gets spooked by Terminal, calls Seb asking why "the black window" opened, closes it mid-download, corrupts the PDF. Seb adds a "don't close this" warning in big letters. Brother closes it anyway.

---

### Path C: Bundle terminal emulator (alacritty in .app)
**Pros:**
- Full TUI aesthetic, zero external Terminal
- Control the window size, theme, font globally
- .app boundary is clean: everything stays self-contained

**Cons:**
- **Bundling alacritty makes the .dmg 80+ MB**, currently 14 MB
- macOS may block it as "unsigned binary" — another gatekeeper dialog
- Alacritty itself has zero macOS-specific affordances
- Code signing complexity: bundled binary must match app's signature
- Updates require rebuilding .dmg from scratch
- Support burden: "the window won't open" is now your fault, not macOS's

**Hidden costs:**
- PyInstaller + alacritty = delicate dance. Update PyInstaller version? Alacritty breaks.
- Brother needs to grant Terminal access in System Preferences anyway
- Notarization (Apple's binary gatekeeper) rejects unsigned bundled binaries
- Distribution: GitHub releases now ship 80 MB .dmg, GitHub Pages hates you

**6-month failure mode:** Apple updates alacritty's code-signing requirements, your .app stops launching. New user downloads .dmg, gets "damaged file" error (it's actually a signature issue, but looks like corruption).

---

### Path D: Web UI in pywebview (Pip-Boy CSS)
**Pros:**
- Full visual control via CSS/HTML — true Pip-Boy aesthetic with glowing effects, green monospace
- Runs in a normal window, feels native
- Seb gets the vibe; brother sees a "normal app"
- Zero Terminal, zero external dependencies
- Single window, can embed PDF viewer (use pypdf + PIL)

**Cons:**
- pywebview requires WebKit (system-installed on macOS, but adds 2–3 MB to package)
- HTML/CSS expertise needed for actual Pip-Boy look (not trivial)
- Responsive layout is a second codebase (HTML/JS vs Python)
- Debugging web layout on mac is annoying (browser dev tools vs runtime)
- Brother sees a "Chrome window" not "the app" — less native feel

**Hidden costs:**
- Transitions: osascript dialogs vs webview windows need careful state handoff
- Security: webview can access local filesystem if misconfigured — auditable issue
- JavaScript in the view layer: another language to maintain
- PDF viewer in web: must use PDF.js or embed a canvas — library dependency
- Notarization: pywebview itself may need signing (depends on how it wraps WebKit)

**6-month failure mode:** Seb designs gorgeous Pip-Boy UI in CSS. Brother updates macOS. WebKit version changes. Fonts render differently. Seb spends 2 days tweaking CSS to handle macOS 15.4 WebKit quirks.

---

### Path E: Dual-track UX (dialogs for brother, TUI flag for Seb)
**Pros:**
- Brother keeps osascript simplicity forever
- Seb gets a `--tui` flag or env var to launch Textual
- No fragmentation: shared download/config/library logic
- Zero install friction for brother (no Terminal bundled)
- Seb can iterate on TUI without breaking dialogs

**Cons:**
- Code branching: every interaction path duplicates (dialog call vs TUI call)
- Testing burden: both paths must work, always
- Seb secretly never uses the dialog path, it rots
- Brother can't access TUI (doesn't know flag exists, wouldn't use it)
- Installation docs now list two modes — confusing

**Hidden costs:**
- UI logic split across gui_dialogs.py + new tui_*.py modules
- Download progress callback: dialog path uses polling, TUI path uses live events
- Error handling branches: dialogs show errors modally, TUI overwrites the screen
- Maintenance: bug in "brother mode" doesn't catch until 6 months later

**6-month failure mode:** Seb uses `--tui` exclusively, finds bugs in dialog onboarding that he never tested. Brother encounters them during fresh install. Error messages are mismatched between paths. Seb apologizes, patches dialog path, doesn't test it.

---

## My Verdict: Path D (Web UI in pywebview)

**Recommendation: Invest in Path D — pywebview + CSS-styled Pip-Boy window.**

**Why:**
1. **The core need is met**: Seb gets Pip-Boy aesthetics (green glow, monospace, UI chrome) without Terminal theater. Brother sees a normal Mac application window, not a shell prompt.
2. **Fewest hidden costs**: No Terminal visibility, no bundled binaries, no second codebase language beyond Python+HTML/CSS. Notarization is identical to current .app.
3. **Clean refactor**: Current osascript calls → pywebview window methods. Config/creds/library logic stays untouched. Download subprocess stays subprocess.
4. **PDF preview is native**: Can render first page of downloaded books inline using pypdf + Pillow. Pip-Boy aesthetic serves the function.
5. **Scaling story**: If Seb wants to add metadata, tags, search — web UI handles it. Dialogs scale to chaos at 5 features.

**What gets sacrificed:**
- The brother's experience stays "a series of dialog boxes" in the refactor. BUT: those boxes can now include progress bars, inline help, and better error context. Pywebview window is still more visually coherent than 8 stacked dialogs.
- Seb loses the "Terminal hacker aesthetic" he might secretly want (typing commands). That's not what his brother needs, and it's not what an .app bundle for non-technical users should do.

**Implementation order:**
1. Refactor dialogs → pywebview window (keep same flow, translate osascript calls to webview JS)
2. Build Pip-Boy CSS (green monospace, scanlines, glow effects)
3. Embed PDF preview for library view
4. Add progress indicator for downloads
5. Style the whole app with the aesthetic

---

## Pre-Rebuild Code Cleanup Required

The codebase is **surprisingly clean**, but three things block a clean refactor:

### 1. **gui_dialogs.py is a god module** (241 lines)
Every interaction goes through osascript. Refactoring to pywebview means:
- Dialogs become REST-ish calls from webview → Python (or direct HTML form submissions)
- Currently tight coupling: main_app.py calls `gui.confirm()`, waits for bool
- Needs decoupling: webview events + callbacks instead

**Fix:** Extract a `UIAdapter` protocol:
```python
class UIAdapter(Protocol):
    def confirm(self, title, message, default_yes=True) -> bool: ...
    def text_input(self, title, message, default="") -> str | None: ...
    # etc
```
Then `OSAScriptUI` and `WebviewUI` both implement it. Forces clean boundaries.

### 2. **No async/event handling**
Current flow: `main_menu_loop()` is a blocking while-True. Each interaction blocks until dialog closes.
Pywebview needs non-blocking UI: user clicks button, webview emits event, handler runs async.

**Fix:** Introduce a simple state machine in main_app.py:
```python
class AppState(Enum):
    MAIN_MENU = 1
    DOWNLOADING = 2
    SETTINGS = 3
```
Pass state + handler callbacks to the UI layer. UI emits events, main app updates state.

### 3. **Download progress isn't wired to UI**
`downloader.py` calls subprocess silently. No progress callback.
With webview, want to show download %, speed, ETA in real time.

**Fix:** Add a progress callback to `download()`:
```python
def download(url: str, on_progress: Callable[[int], None] | None = None) -> tuple[bool, str]:
    # Parse downloader output, call on_progress(percent)
```
Osascript path: ignores callback. Webview path: updates progress bar in real time.

---

## Failure Mode at 6 Months: If We Ship Path D

**The worst case:**

1. **CSS maintenance nightmare**: Seb designs beautiful Pip-Boy UI in CSS. A macOS update changes system font rendering. Glyphs that looked perfect at 13px now render at 13.2px, breaking the monospace grid. Seb spends 4 hours tweaking rem units and font-family fallbacks.

2. **WebKit divergence**: pywebview on Intel Mac vs Apple Silicon renders fonts slightly differently. Seb ships the .app. User on Intel Mac reports "the text looks fuzzy." Turns out to be a WebKit rendering quirk. No easy fix without bundling platform-specific WebKit.

3. **Brother can't distinguish app from browser**: He gets an error dialog ("PDF viewer needs update") and clicks "Allow," giving the pywebview window full filesystem access. Security UX debt.

4. **PDF viewer complexity**: Seb wants to show book covers in the library. Adds PDF.js for preview. PDF.js is 2MB of JavaScript. Adds complexity to the bundle. First update introduces a PDF that crashes PDF.js. Support request: "my library is broken."

5. **The download subprocess still hangs**: Webview window is responsive, but download_subprocess is still blocking. Brother thinks the app froze. Clicks the red button. PDF corrupts.

**Mitigation:**
- Lock pywebview version in requirements.txt + pin Textual (if dual-track) to tested combo
- Keep CSS minimal; default to system fonts, avoid clever transforms
- Never implement custom PDF viewer — just "open in Preview" with a button
- Run downloader in a thread pool, emit progress events to webview
- Test on both Intel + Apple Silicon before release

---

## One Thing I'd Kill

If I were running this project, I would **kill the idea of a fancy library browsing UI inside the app itself**. 

The brother doesn't need a Pip-Boy library browser. He needs to:
1. Download a book
2. See it downloaded
3. Open it

That's three operations. The app does 1 + 2. #3 should be "click 'View Library' → Finder opens." Don't build a custom PDF viewer or book grid inside the app. It's maintenance forever and the brother already has Preview.app.

**Use that saved complexity to make the download flow bulletproof instead.** Real-time progress, resumable transfers, clear error messages. That's the UX win.

---

**GHOST**

*If you want this to live past 2026, choose the dullest path: move the shell prompt outside the user's sight (Path B or D) and make downloading a book take 3 clicks and 5 seconds. Aesthetics are free if the core function doesn't fail.*
