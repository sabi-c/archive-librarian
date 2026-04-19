# Archive Librarian — WINAMP CLASSIC Design Concept

## Overview
Pure nostalgia homage to Winamp 2.x (1999). This is the Y2K media player skin adapted for book downloading — rectangular, brushed-metal UI with LED-green displays and that unmistakable dense, banded aesthetic.

## Design DNA

- **Primary Inspiration**: Winamp 2 main window, EQ panel, playlist stacked layout
- **Color Palette**: Dark gunmetal (#2a2a2a), brushed-metal gradients (#444-#1a1a1a), LED green (#0eff0e), LED amber (#ffaa00), warning red (#ff4040)
- **Typography**: Monospace (Courier), ALL CAPS, microscopic readouts with text-shadow glow — that classic "digital display" feeling
- **Shape Language**: Rectangular, banded three-panel layout (MAIN / EQ-STYLE / PLAYLIST). Multi-window aesthetic with sunken bevels and highlight strips (#777 inset).

## Key Features

1. **Title Bar**: Classic blue gradient Windows 95 style with minimize/maximize/close buttons
2. **Main Display Panel**: Shows "047 BOOKS", "STATUS: READY", "CURATOR: ARIA" in glowing green LED text on black
3. **Transport Controls**: ◄PREV, ⏸PAUSE, ▶DL (primary amber button), ⚙SET — exact Winamp button morphology
4. **Library Activity EQ**: Six vertical bars (Philosophy, Health, Tech, History, Fiction, Spirituality) proportional to collection size — replaces audio EQ with domain metrics
5. **Recent Downloads Playlist**: Striped table with book titles, file sizes, hover effects, current-track highlighting
6. **Scrollbar**: Custom styled with that brushed-metal gradient look
7. **Footer**: "WINAMP v2.99 ENHANCED • 1999-2026" — the joke baked in

## Technical Implementation

- **HTML/CSS only** — no JavaScript, no dependencies
- **Linear gradients** for brushed-metal bevels and transitions
- **Text-shadow** for LED glow effect (#0eff0e bloom)
- **Border inset/outset** for classic 90s button morphology
- **Monospace fonts** to match original 8-10px readouts
- **Responsive scrollbar styling** (webkit) to match the theme

## Sample Books in Playlist

- The Tao Te Ching (287K)
- Walden by Thoreau (512K)
- Meditations by Marcus Aurelius (198K)
- The Power of Now (421K)
- A Brief History of Time (689K)
- Zen and the Art of Motorcycle Maintenance (445K)
- The Selfish Gene (334K)
- Deep Work (267K)

## Design Choices

**Why This Works**:
- Instantly recognizable to anyone who used Winamp in the 1999-2005 era
- Dense UI maximizes information per pixel — true to original
- The EQ bar metaphor translates perfectly: audio spectrum → knowledge domain distribution
- Monospace + LED text creates that "hacker tool" vibe for a librarian interface
- Multi-panel stacking (main/EQ/playlist) mirrors actual Winamp window arrangement

**Constraints Honored**:
- No modernization — this is deliberately retro
- True 1999 Winamp proportions (280px wide, banded layout)
- LED green (#0eff0e) throughout, not muted or trendy
- All caps display text matching original readouts
- Beveled buttons with proper border inset/outset

## File Locations

- HTML: `/Users/seb/Projects/archive-librarian/design-concepts/03_winamp.html`
- Screenshot: `/Users/seb/Downloads/Manual Library/Seb's Mind/Seb's Mind/Note inbox/archive-librarian-concepts/03_winamp.png` (56KB)
- Markdown: `/Users/seb/Projects/archive-librarian/design-concepts/03_winamp.md`
