# SCOUT: Archive Librarian Aesthetic Research

## Top 8 References — What Makes Them Fun

### 1. Pip-Boy 3000 UI (Fallout Series)
The gold standard: glowing green/amber CRT monochrome aesthetic with chunky typography, scan-line effects, and that "retro-futuristic-but-broken" charm. What makes it work: **restricted color palette** creates clarity, **thick borders** (Unicode box drawing) frame content, **data readouts** feel mechanical and important even when trivial. The animation is *slow* (scan-line sweep, fade-in) — never frantic.

### 2. Vault-Tec Terminal Screens (Fallout)
Fallout's in-game green terminals: blinking text, ASCII art logos, THAT beep sound, "USER ACCESSED" messages. What makes it fun: **fake authenticity** — you feel like you're using 1987 mainframe software in a post-apocalyptic vault. **Status indicators** (flashing brackets, progress bars made of `=====`) signal urgency without animation overkill.

### 3. no-more-secrets / Sneakers Effect (Linux TUI)
The "encrypted → decrypted" cascade: garbled characters that scan left-to-right, revealing plaintext. Pure spectacle, but *quick* (under 3 seconds). What works: **motion direction** (top-to-bottom or left-to-right) feels logical, **reveal anticipation** (you wait for the decrypt), **one-time event** (not looping). Great for "download complete" or "conversion done" moments.

### 4. hollywood (Linux Terminal)
Matrix-style terminal hacker aesthetic: split panes, rapid text scrolling, Mission Impossible music (optional). What's compelling: **layered complexity** — multiple processes visible at once create sense of important work happening, **color contrast** (bright text on black), **fast update rate** (feels alive). Downside: overstimulating if left running.

### 5. Textual Python TUI Framework (Demo App)
Modern, responsive TUI with smooth animations, gradient-like color transitions, and proper spacing. What feels fresh: **smooth animations** (fade-in/slide, 200-400ms), **consistent typography** (monospace with breathing room), **state transitions** that feel intentional not chaotic. Example: progressbars that *ease* rather than jump.

### 6. btop / lazygit / k9s (Practical TUIs)
Real-world tools that respect the user: **color as meaning** (red=error, green=ok, yellow=warning), **dense but navigable layouts**, **no gratuitous motion**, **responsive to input**. What's pleasurable: the *reveal* (expand a section to see details), clear visual hierarchy (headers in bright color, data dim), **quick load** (no splash screens).

### 7. neofetch ASCII Art + Gifetch Animation
Static ASCII logo + system info = minimal and charming. Gifetch adds animated GIFs rendered as ASCII. What works: **simplicity** (one image, one purpose), **crafted ASCII art** (not auto-generated), **personality** (retro computing vibes), **no sound effects needed** (visual is enough).

### 8. Vim Startup Screen / htop (Classics)
htop's color-coded process list, Vim's splash banner. Timeless because: **zero fluff**, **instant readability**, **color discipline** (exact palette adhered to), **typeface personality** (monospace communicates "serious tool").

---

## The Pip-Boy Color Palette — Exact Hex Codes

### Primary Colors (From Fallout Games)

| Color | Hex | Usage | Notes |
|-------|-----|-------|-------|
| **Pip-Boy Green** | `#00ff00` | Primary text, highlights, headers | Bright electric green, maximum saturation |
| **Vault-Tec Amber** | `#ffaa00` (approx) | Secondary accents, warnings | Warm orange-yellow, CRT glow feel |
| **Vault-Tec Blue** | `#7ea3cf` | Terminal UI borders/frames | Corporate vault branding |
| **Dark Terminal** | `#000000` | Background | True black for CRT contrast |
| **Dim/Muted Green** | `#005f00` or `#008e00` | Dim text, secondary elements | Lower contrast for background data |
| **Cyan Accent** | `#00ffff` | Focus/selection highlights | High contrast, draws attention |
| **CRT Green (Real Phosphor)** | `#5fff5f` | Alternative "softer" green | More authentic to actual old CRT monitors |

### Decision Tree for Archive Librarian
- **Headers & Primary Action**: Use `#00ff00` (Pip-Boy Green)
- **Warnings & Section Dividers**: Use `#ffaa00` (Vault-Tec Amber)
- **Selected/Hovered Items**: Use `#00ffff` (Cyan)
- **Background**: `#000000` (true black)
- **Dim Status Text**: `#008e00` (dark green)
- **Borders/Frames**: Use Unicode (no color needed) or `#00ff00` when colored

---

## 5 Elements Worth Stealing — Ranked by Impact

### 1. **Color Discipline (Palette Limit)**
*Highest Impact*. Seb's reference file already does this: 4-5 colors max. Every tool in the research that *feels* polished restricts to 3-4 colors. This isn't limitation—it's style. Forces intentional design.
- **For Archive**: Stick to GREEN, AMBER, CYAN, DIM. Nothing else.
- **Why it matters**: Colors become *semantic* (green=go, amber=caution), not decorative.

### 2. **Controlled Motion with Purpose**
*High Impact*. Animation should have a *reason*: progress reveal (page flip, decryption cascade), state transition (open→close), or busy indicator (breathing orb). NOT decoration.
- **For Archive**: The floating orb is perfect. Page-flip animation is perfect. No rainbow cycles or pointless blinking.
- **Why**: Motion catches eyes. Pointless motion exhausts attention.

### 3. **Unicode Box Drawing for Depth**
*High Impact*. Thick borders (╔═╗ vs ┌─┐) create visual weight and "retro-hardware" feel. Frames create information hierarchy.
- **For Archive**: Use thick boxes for sections. Seb's reference file does this. Build on it.
- **Why**: Humans parse borders as "container boundaries." More containment = more perceived complexity = feels sophisticated.

### 4. **Dense but Scannable Layout**
*Medium Impact*. Don't space things out for breathing room (that's GUI thinking). Use alignment, character-width constraints, and aligned columns. Example: 80-char lines like old terminals.
- **For Archive**: Menu options left-aligned, values right-aligned, separator line between sections.
- **Why**: Mimics real terminal software. Users expect compact density.

### 5. **One Subtle Sound Effect (Optional)**
*Medium Impact*. A single beep or quiet "success" sound on action completion. NO background music. NO notification sounds.
- **For Archive**: Perhaps a single quiet tone when download starts, or when conversion finishes. Sparingly.
- **Why**: Audio is 50% of "feels real." One carefully chosen sound > ten cheap bleeps.

---

## What to AVOID — Anti-Patterns

### 1. **Rainbow Color Cycling**
Nothing kills retro aesthetic faster than cycling through all 256 colors. Pip-Boy never does this. Only *change* color when state changes (downloading→converting→done).

### 2. **Gratuitous Animations**
Sliding sidebars, rotating spinners, unnecessary fades. If animation doesn't convey progress or state, cut it. Example: a progress bar that eases from 0→100% is good. A sidebar that slides in from left is bad (all that motion, no information).

### 3. **Too Many Fonts or Font Styles**
Terminal = monospace. Full stop. Bold, dim, and color are enough. Don't use italics (many terminals don't support them). Don't mix monospace + proportional.

### 4. **Blinking Text** (The 90s Mistake)
Blinking is associated with *errors* (lost connection, crash). Don't use it. Period. Use color change or highlight instead.

### 5. **Clickable Elements** (GUI Creep)
TUIs are keyboard-driven. Don't add mouse click regions or buttons that look like GUI buttons. Use vim-like motions (hjkl, arrow keys) and clear hotkey labels.

### 6. **Over-Elaborated ASCII Art**
Huge 10-line logos everywhere are cluttered. Seb's reference has this right: small, focused orbs and book animations. One strong visual per screen, not five.

### 7. **Missing Context**
Show what mode you're in (EDIT, DOWNLOAD, CONVERT). Show exit instructions (press 'q' to quit). Show next steps. Fallout terminals do this—every screen has status.

---

## One Weird Thing I Found (That You Didn't Ask For)

**Windows Terminal now has built-in retro CRT effects** (scan lines, screen glow, phosphor decay). Searching for CRT info, I found that Windows Terminal added these as optional filters in 2024. This means there's an emerging pattern: terminals are *gaming* the nostalgia angle. The Pip-Boy didn't invent this—it *perfected* it. Real old CRT monitors (especially green phosphor screens) had afterglow, where text would linger briefly when scrolling. This is *not* a bug you want to emulate, but it's fascinating that Fallout nailed the aesthetic so completely that Windows built it as a feature.

---

## References

- [Classic Fallout Pip-Boy Color Palette](https://www.color-hex.com/color-palette/18872)
- [Green Pip Boy Color Palette](https://www.color-hex.com/color-palette/1017284)
- [Pip-Boy 3000 Fallout Wiki](https://fallout.fandom.com/wiki/Pip-Boy_3000)
- [Fallout Terminal Configuration GitHub](https://github.com/LeonardLeroy/Fallout-Terminal-Configuration)
- [Hollywood Terminal - Linux TUI](https://github.com/dustinkirkland/hollywood)
- [No More Secrets - Sneakers Decryption Effect](https://github.com/bartobri/no-more-secrets)
- [Textual Python TUI Framework](https://textual.textualize.io/)
- [Awesome TUIs List](https://github.com/rothgar/awesome-tuis)
- [Terminal Colors Overview](https://chrisyeh96.github.io/2020/03/28/terminal-colors.html)
- [neofetch Customization](https://github.com/dylanaraps/neofetch)
- [Textual - 7 Things Learned Building a TUI Framework](https://www.textualize.io/blog/7-things-ive-learned-building-a-modern-tui-framework/)

---

**SCOUT signing off.** The weirdest find: actual Fallout *terminal mods* exist where people transform their system GRUB bootloader into a full Vault-Tec theme. Someone's booting their Linux machine into a Fallout terminal. That's peak aesthetic commitment.
