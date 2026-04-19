# STIPPLE — Archive Librarian Halftone Portrait Concept

## Concept
A full-bleed halftone stipple portrait of **ARIA, the Librarian**, rendered in dense black dots on cream paper. The portrait dominates the upper 60% of the interface. Type and controls occupy the bottom 40%, creating a vertical composition that reads as a **printed book cover or vintage editorial layout**.

## Visual Direction
- **Spirit**: The ASCII cat portrait referenced, but applied to a stylized librarian figure—eyes hidden behind round glasses, holding open books, rendered entirely in a dot-grid halftone at varying opacity levels
- **Color Palette**:
  - Cream base: `#f0e8d0` (off-white, warm paper tone)
  - Deep black stipple: `#0a0a0a` (near-black for maximum contrast)
  - Single accent: None (reserved for future interactive states—could be deep blue `#1c4ba0` or vintage red `#b03a28`)
- **Aesthetic**: Monochromatic, editorial, tactile—evokes 19th-century wood-cut portraiture and mid-century print design

## Key Elements

### Portrait (SVG-rendered halftone)
- **Composition**: Face with round glasses, shoulders with books held on both sides
- **Technique**: Circles with varying radii and opacity create tonal depth
  - Hair/dark areas: 3–5px circles at 70–90% opacity
  - Midtones (face, shoulders): 2–3px circles at 40–60% opacity
  - Highlights (forehead, cheeks): 1–2px circles at 30–40% opacity
- **No gradient**: Pure opacity modulation, true halftone aesthetic
- **Dashed border**: Dotted/dashed frame around entire window (matching the cat reference)

### Type Hierarchy
1. **Wordmark**: "ARCHIVE LIBRARIAN" — monospace caps, 11px, tight letter-spacing, all-caps
2. **Caption**: "ARIA, YOUR LIBRARIAN" — small serif italic, 13px
3. **Counter**: "47 BOOKS" — monospace, 10px
4. **Recent list**: Numbered (1–4) serif, 12px
5. **Status**: "READY" with dot indicator, monospace, 10px
6. **Button**: "DOWNLOAD" — monospace, 10px, small black block

### Controls
- **DOWNLOAD button**: Small, unobtrusive, black on cream, tight padding
- **Settings gear**: Minimal icon in corner
- **Status indicator**: Dot + text, left-aligned
- **Recent downloads**: Four-item list, minimal spacing

## Layout Grid
- **Width**: 880px (slightly wider than tall for portrait window aspect)
- **Height**: ~1280px total (portrait fills ~730px, controls ~200px, margins)
- **Aspect ratio**: Portrait region is 1:1.1 (slightly taller than wide)
- **Typography baseline**: All type sits on cream, no color changes

## Implementation Notes
- Built in vanilla HTML + inline CSS + SVG
- No external fonts (system stack only)
- Background: subtle animated noise texture (opacity 0.03) for print-ready feel
- Print-friendly: shadows and background gradients disable on `@media print`
- Responsive: max-width 100% on mobile, maintains dashed border

## Color Reference
```
Cream:      #f0e8d0 (main background)
Deep black: #0a0a0a (stipple, text, borders)
Accent (reserved): #1c4ba0 (LIFE blue) or #b03a28 (vintage red)
```

## Channels & References
- **Artist/Era**: Echoes of **Ben Day process** (Roy Lichtenstein's era) crossed with **wood-cut portraiture** and the **ASCII cat aesthetic** (contemporary digital minimalism meets print tradition)
- **Inspiration**: British Library rare-book frontispiece, vintage Criterion Collection DVD packaging, letterpress handiwork
