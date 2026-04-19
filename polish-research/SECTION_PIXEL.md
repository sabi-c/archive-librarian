# Archive Librarian v2.0 Polish Proposal
## UX Microinteraction Design — RISO Aesthetic

---

## TOP 5 POLISH ITEMS (Ranked by Feel Impact)

### 1. **Page-Flip Transition (Screen Transitions)**
**Impact:** Makes navigation feel intentional, physical, bookish. Transforms hard flash into a characteristic interaction.

**Implementation:** Replace `load_url()` flash with a registration-snap page-flip effect. Current hardness → tactile moment.

```css
/* Add to _riso_base.css or per-screen inline */
@keyframes flip-page-out {
  0% { opacity: 1; transform: perspective(1200px) rotateY(0deg); }
  100% { opacity: 0; transform: perspective(1200px) rotateY(90deg); }
}

@keyframes flip-page-in {
  0% { opacity: 0; transform: perspective(1200px) rotateY(-90deg); }
  100% { opacity: 1; transform: perspective(1200px) rotateY(0deg); }
}

.container {
  animation: flip-page-in 0.45s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.container.exiting {
  animation: flip-page-out 0.35s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
```

**Wiring:** Add before `pywebview.api.navigate()` calls:
```javascript
document.querySelector('.container').classList.add('exiting');
await new Promise(r => setTimeout(r, 350));
pywebview.api.navigate(target);
```

---

### 2. **Ink-Press Button Feedback (Button Microinteractions)**
**Impact:** Buttons feel *stamped* — satisfying tactile ghost.

**Current:** 4px shadow → 1px translate on hover. Predictable.  
**New:** Shadow intensifies + slight scale-down + subtle rotation for press feel.

```css
.button-primary {
  box-shadow: 4px 4px 0 rgba(22, 56, 168, 0.2);
  transition: all 0.12s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.button-primary:hover {
  transform: translate(1px, 1px) scale(0.98) rotate(-0.5deg);
  box-shadow: 3px 3px 0 rgba(22, 56, 168, 0.15), 
              0 0 0 3px rgba(200, 84, 58, 0.08);
}

.button-primary:active {
  transform: translate(0, 0) scale(0.96) rotate(0deg);
  box-shadow: 1px 1px 0 rgba(22, 56, 168, 0.1), 
              inset 0 2px 4px rgba(22, 56, 168, 0.1);
}
```

---

### 3. **Halftone Progress Indicator (Loading States)**
**Impact:** Replaces generic spinners with RISO-native animation. "Dot density fills" instead of rotation.

**Design:** Halftone dot grid that increases opacity/density as progress increases. No spinning—pure density animation.

```css
.progress-fill {
  height: 100%;
  width: 64%;
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="20" height="36"><defs><pattern id="p" x="0" y="0" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="3.8" fill="%231638a8"/></pattern></defs><rect width="20" height="36" fill="url(%23p)"/></svg>');
  transition: width 0.3s ease;
  /* NEW: Density pulse */
  animation: density-pulse 0.8s ease-in-out infinite;
  background-size: 20px 36px;
}

@keyframes density-pulse {
  0%, 100% { opacity: 0.7; filter: brightness(1); }
  50% { opacity: 1; filter: brightness(1.15); }
}

/* For indeterminate states (ARIA working): */
.progress-fill.indeterminate {
  width: 35%;
  opacity: 0.6;
  animation: density-pulse 1.2s ease-in-out infinite, 
             slide-right 2s ease-in-out infinite;
}

@keyframes slide-right {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(400%); }
}
```

**Usage in 04_downloading.html:**
```html
<div class="progress-bar">
  <div class="progress-fill" id="progress"></div>
</div>
```

---

### 4. **Input Caret & Paper-Flash (Input Field Polish)**
**Impact:** Subtle sensory detail. Caret + micro-animation on keypress suggests *pen on paper*.

```css
.field-input {
  width: 100%;
  background: transparent;
  border: none;
  border-bottom: 2px solid var(--ink);
  padding: 14px 0;
  font-family: inherit;
  font-size: 18px;
  font-weight: 700;
  color: var(--ink);
  outline: none;
  letter-spacing: 0.5px;
  caret-color: var(--ghost);
  caret-width: 3px;
  /* NEW: Paper texture flash on input */
  transition: background 0.15s ease;
}

.field-input:focus {
  border-bottom-color: var(--ghost);
  background: linear-gradient(to bottom, 
    transparent 0%, 
    rgba(200, 84, 58, 0.04) 50%, 
    transparent 100%);
}

/* Validation states */
.field-input.valid {
  border-bottom-color: #4a7c4e;
  caret-color: #4a7c4e;
}

.field-input.error {
  border-bottom-color: var(--ghost);
  caret-color: var(--ghost);
}

.field-input.error:focus {
  background: linear-gradient(to bottom, 
    rgba(200, 84, 58, 0.05) 0%, 
    rgba(200, 84, 58, 0.08) 50%, 
    rgba(200, 84, 58, 0.05) 100%);
}
```

---

### 5. **Book Row Halftone Overlay on Hover (Hover States)**
**Impact:** Library table becomes interactive & tactile. Subtle highlight respects restraint.

**Current:** `.book-row:hover { background: var(--paper-deep); }` — too flat.  
**New:** Halftone overlay that *reveals* behind the row on hover.

```css
.book-row {
  display: grid;
  grid-template-columns: 60px 60px 1fr 100px 80px 100px;
  gap: 16px;
  align-items: center;
  padding: 16px 0;
  border-top: 1px solid var(--ink);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: background 0.2s ease;
}

.book-row::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="80" height="30"><defs><pattern id="dots2" x="0" y="0" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="3" fill="%231638a8"/></pattern></defs><rect width="80" height="30" fill="url(%23dots2)"/></svg>');
  opacity: 0;
  pointer-events: none;
  z-index: 0;
  transition: opacity 0.2s ease;
}

.book-row:hover {
  background: rgba(200, 84, 58, 0.03);
}

.book-row:hover::before {
  opacity: 0.12;
}

/* Ensure text stays above overlay */
.book-row > * {
  position: relative;
  z-index: 1;
}
```

---

## TRANSITION RECOMMENDATION: PAGE-FLIP

**Why this one?** Fits RISO perfectly—books literally flip pages. Feels intentional, not a Flash replacement. Registers emotionally.

**Full Keyframe Set:**

```css
/* Smooth perspective-based page flip with registration snap */
@keyframes flip-out {
  0% {
    opacity: 1;
    transform: perspective(1400px) rotateY(0deg) translateZ(0);
  }
  50% {
    opacity: 0.8;
  }
  100% {
    opacity: 0;
    transform: perspective(1400px) rotateY(-85deg) translateZ(100px);
  }
}

@keyframes flip-in {
  0% {
    opacity: 0;
    transform: perspective(1400px) rotateY(85deg) translateZ(100px);
  }
  50% {
    opacity: 0.8;
  }
  100% {
    opacity: 1;
    transform: perspective(1400px) rotateY(0deg) translateZ(0);
  }
}

.container {
  animation: flip-in 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

.container.exiting {
  animation: flip-out 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
}
```

**Integration:** Call before navigation in pywebview callbacks.

---

## EMPTY & ERROR STATES

### Empty States

**Dashboard (0 Books):**
```
┌─────────────────────────────────────┐
│  [halftone empty shelf illustration] │
│                                      │
│  "THE STACKS ARE QUIET"              │
│                                      │
│  Download your first book to begin   │
│  the archive. Tap the button below.  │
│                                      │
│  [Download Book Button]              │
└─────────────────────────────────────┘
```

**Library Index (0 Results):**
```
┌──────────────────────┐
│ [search icon dots]   │
│                      │
│ "NO VOLUMES MATCH"   │
│                      │
│ Try a different      │
│ search term or filter│
└──────────────────────┘
```

**ARIA Voice (from status pill):**
- "Library is empty. Download your first book."
- "No volumes match that search."
- "Stacks are loading, please wait."

### Error States

**Login Failure:**
```css
.field-input.error {
  border-bottom-color: var(--ghost);
  background: linear-gradient(to bottom, 
    rgba(200, 84, 58, 0.05) 0%, 
    rgba(200, 84, 58, 0.08) 50%, 
    rgba(200, 84, 58, 0.05) 100%);
}

/* Add misregistration intensification */
.container.error::before,
.container.error::after {
  border-width: 3px;
  opacity: 0.25; /* increased from 0.15 */
  transform: translate(4px, -4px) rotate(0.5deg); /* more exaggerated */
}
```

**Visual Stamp** (replaces generic error alert):
```html
<div class="error-stamp">
  <div class="stamp-text">PROOF REJECTED</div>
  <div class="stamp-detail">Credentials invalid · Try again</div>
</div>
```

```css
@keyframes stamp-bounce {
  0%, 100% { transform: rotate(-12deg) scale(0.95); }
  50% { transform: rotate(-12deg) scale(1.05); }
}

.error-stamp {
  border: 3px solid var(--ghost);
  padding: 24px;
  text-align: center;
  font-weight: 900;
  font-size: 18px;
  text-transform: uppercase;
  letter-spacing: 3px;
  color: var(--ghost);
  transform: rotate(-12deg);
  animation: stamp-bounce 0.5s ease-out;
}
```

**Download Failure:**
Status pill changes from `● ARIA Working` → `✗ Failed · Tap to retry` (terracotta color, border intensifies).

---

## WHAT I'D SKIP (& Why)

1. **Sound effects (paper rustle, thunk).** 
   - Reason: RISO is *visual*. Sound adds complexity without reinforcing the aesthetic. Too easy to make corny. Skip it.

2. **Animated halftone background on every screen.** 
   - Reason: Static halftone accents are enough. Moving patterns tire the eye and cheapen the feel. Restraint > motion.

3. **Drawer/slide-in navigation panels.** 
   - Reason: Current icon button nav is fast and clean. Drawer animation adds 200ms overhead for no UX gain.

4. **Smooth scroll between list items.** 
   - Reason: Library index works best with instant scroll. Books don't float. Scrollbar stays minimal.

5. **Per-book "reading progress" indicator in the grid.** 
   - Reason: Adds visual noise. Archive Librarian is *download manager*, not reading app. Scope creep.

---

## ARIA'S VOICE (Status Messaging)

### Page Load / Navigation
- "Opening stacks…"
- "Retrieving your library…"
- "Ready to browse."

### Download States
- "ARIA is verifying archive.org…"
- "Borrow token issued · Beginning acquisition…"
- "Page 193 of 302 · Standing by."
- "Acquisition complete · Library refreshing…"

### Error / Retry
- "Network connection lost. Retrying…"
- "Proof rejected. Check credentials and try again."
- "Download interrupted. Tap to resume."

### Empty Library
- "The stacks are quiet. Download your first book to begin."
- "No volumes in this domain yet."

---

## SMALLEST DETAIL, BIGGEST DIFFERENCE

The **caret color change to terracotta on focus** (#c8543a, the misregistration ghost color). It's one line of CSS—`caret-color: var(--ghost);`—but it tells the user: "This app *knows* RISO. Every detail counts." A user will never consciously notice it, but they'll feel the thoughtfulness.

**Sign: PIXEL**  
*Polish is the skin of intention.*
