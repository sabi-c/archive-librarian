# AQUA POD — Archive Librarian

**Design Concept:** Premium Apple Aqua-era homage (iTunes 4-7 / iPhoto 2 era)

## Aesthetic Pillars

- **Brushed Metal Mastery:** Multi-layer gradient brushed aluminum (title bar + content area) with 1px alternating pinstripe overlay at low opacity—the signature Aqua grain texture reproduced in pure CSS
- **Lickable Buttons:** Rounded candy-pill geometry with vertical white-to-transparent glossy highlight on the top 45%, aqua blue primary action (#1e6bff to #4a9fff gradient), soft outer shadow—tactile visual feedback that screams early-2000s Apple
- **Glass Architecture:** Clean hierarchical window with separate title bar (metal) and content area (pinstriped brushed finish), rounded window corners, three traffic lights at top-left (cosmetic)
- **Typography & Spacing:** Lucida Grande throughout, subtle text shadows, refined line-height—calm and legible, never playful

## Key Features Implemented

1. **Title Bar (Brushed Metal):** Gradient + pinstripe pattern, traffic lights (red/yellow/green), centered app name with subtle text shadow
2. **Primary Hero Button:** Aqua blue lickable candy button with inset white highlight stripe—the visual anchor of the interface
3. **Library Counter:** Blue badge with live-status glow indicator (47 BOOKS)
4. **Recent Downloads Table:** 5-row alternating pinstripe rows, hover highlight to subtle aqua, clean typography hierarchy
5. **ARIA Identity:** Bottom-right circular badge (A) in aqua gradient, "ARIA Librarian" label—subtle brand presence
6. **Status Indicator:** Calm green LED dot + "Library ready" text, Preferences button for settings access

## Technical Execution

- **CSS Brushed Metal:** Linear-gradient 180deg with 5-7 color stops for depth + repeating-linear-gradient overlay for pinstripes (1px light/dark alternation at 2px intervals, ~2-5% opacity)
- **Button Highlight:** CSS `::before` pseudo-element with 45% height, white-to-transparent gradient for top-half gloss
- **Responsive:** Scales gracefully to mobile; pinstripes maintained across all sizes
- **Performance:** Single HTML file, no images, no JavaScript—pure CSS + inline SVG (not used here, but available)

## Iteration: iTunes 4-7 Era (2003-2005)

This design channels the most refined Apple aesthetic: after the brushed metal craze began (Panther) but before the shift to intel simplicity. It's calm, premium, and purposefully *not* playful—the Aqua that made designers believe computers could be beautiful.

---

**File:** `/Users/seb/Projects/archive-librarian/design-concepts/04_aqua.html`  
**Screenshot:** `/Users/seb/Downloads/.../04_aqua.png` (208 KB)

**Signed,** AQUA  
Channeling iTunes 4-7 (2003-2005) — the golden age of brushed metal refinement.
