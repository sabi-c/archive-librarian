# Archive Librarian — Risograph Edition

## Design Overview

A **two-color risograph print aesthetic** for the Archive Librarian UI, inspired by contemporary independent publishing and editorial design. The concept treats the library interface as a publication — numbered index entries, halftone dot patterns, and tactile print production techniques.

## Key Design Principles

- **Two-Ink Palette**: Deep ultramarine blue (#1638a8) + cream/bone (#f3ead2), with terracotta accent (#c8543a) at <5% for misregistration ghosts
- **Halftone Signature**: Circular dot patterns render the book counter and decorative bars; varying dot density suggests depth and quality
- **Print Physicality**: Textured grain background, subtle misregistration (cyan/red ghost layers at 2px offset), block-form button with shadow depth
- **Editorial Typography**: Heavy bold sans-serif (Söhne Breit / Druk aesthetic), all-caps, tight tracking, numbered entry sequence like a magazine TOC
- **Zine Spirit**: Borders, dividing rules, publication footer (artist/librarian credit), layout mimics screen-printed collateral

## Component Breakdown

1. **Wordmark** — "ARCHIVE LIBRARIAN" split across two lines, 72px bold, with terracotta text-shadow for misregistration effect
2. **Counter Block** — Halftone circle (85% dot opacity) with "47 BOOKS" label, inline display
3. **Divider Rule** — 2px solid line, 48px margin above/below
4. **Primary Button** — "DOWNLOAD LIBRARY" all-caps, 20px padding, blue solid fill, 4px offset shadow on hover
5. **Publication Index** — Five recent books numbered 01–05 in three-column grid (number, title, date), separated by hairline borders
6. **Status Badge** — Small checkmark + "READY" label, bordered box, 10px font
7. **Footer** — "ARIA, LIBRARIAN" credit + print method descriptor, all small caps

## Visual Assets

- **Halftone Patterns**: SVG-generated dot grids (8–12px period) embedded as data URLs
- **Texture**: Fractal noise filter applied to background at 0.9 base frequency, 4 octaves, layered opacity for tactile grain
- **Misregistration**: Dual border layers (cyan and magenta) offset by 2px each, 12–15% opacity for subtlety
- **Accent Bars**: Decorative halftone blocks positioned top-right and bottom-left at 25% opacity

## Color Reference

| Name | Hex | Usage |
|------|-----|-------|
| Primary Blue | #1638a8 | Text, borders, fills, buttons |
| Cream/Bone | #f3ead2 | Background, negative space |
| Terracotta Accent | #c8543a | Ghost misregistration, minimal accents |

## Typography

- **Display (Wordmark)**: 72px, 900 weight, -2px letter-spacing, uppercase
- **Labels**: 14px–12px, 600–700 weight, 1–2px letter-spacing, uppercase
- **Body**: 14px, 600 weight, 0.5px letter-spacing, uppercase
- **Meta**: 10–11px, 500 weight, opacity 0.5–0.6

## Responsive Notes

- Breakpoint at 768px reduces wordmark to 48px, adjusts grid layout for mobile
- Counter block and index entries remain readable at all sizes
- Button maintains 20px padding for touch targets

---

**Design Direction**: Contemporary risograph studio aesthetic (Risotto Studio / Hato Press lineage). Two-color print constraints drive intentional design choices — halftone dot density becomes the visual vocabulary, texture conveys craftsmanship, and offset registration suggests analog imperfection as a feature.
