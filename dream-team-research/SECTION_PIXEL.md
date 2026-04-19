# PDF Viewing UX — Archive Librarian
## PIXEL's Research & Design Proposal

---

## The Actual Question: What Does "View PDFs" Mean for This User?

Archive Librarian users aren't building academic PDFs libraries with complex metadata. They downloaded a book from archive.org because they want to **read it**. The viewing experience should answer three questions in sequence:

1. **Browse:** "Which book do I want to read right now?" (discovery, not search)
2. **Preview:** "Is this the right one? Confirmation that you got what you wanted before opening."
3. **Read:** "Actually open the PDF and read it."

Currently, all three stages collapse into Finder — users see filenames in a folder, which fails at stages 1 and 2. We need to close that gap *inside the app*, then hand off to reading.

---

## PDF View Options — Effort vs Aesthetic vs Fit

| Approach | Effort | Aesthetic Fit | Library Size Impact | Right For This App? |
|----------|--------|---------------|---------------------|---------------------|
| **macOS Preview launch** (`open -a Preview`) | 5 min | Native, zero friction | None | ✓ **Primary read action** |
| **Finder open** (current) | 0 | System default, confusing | None | ✗ Doesn't solve the problem |
| **Quick Look** (`qlmanage -p`) | 10 min | Slick, native, animated | None | ~ **Good preview, not reading** |
| **PyMuPDF page rendering** (in TUI) | 3 hrs | On-brand retro, tiny text | 20-50 MB per 100 PDFs | ✗ Text too small to read |
| **PDF.js in pywebview** | 6 hrs | Modern, not retro | 100+ MB app bloat | ✗ Over-engineered |
| **Chafa/catimg ASCII art** | 4 hrs | Very on-brand, novelty | None | ~ **Fun demo, not practical** |
| **Calibre-style book manager** | 12 hrs | On-brand UI, separate app | None | ✗ Defeats "brother-grade simple" |

---

## Recommended UX Flow — Keystroke by Keystroke

**Goal:** User opens app → finds book → reads it in 3-4 steps, no friction.

```
┌─ Main Menu ─────────────────────────────────────┐
│  "Archive Librarian"                            │
│  Library: 47 books (3.2 GB)                     │
│                                                  │
│  [Download Book] [View Library] [Settings] [Quit]
└──────────────────────────────────────────────────┘

User clicks: "View Library"

┌─ Library Browser (NEW) ──────────────────────────┐
│ 47 books • Sort by [Title ▼] [Downloaded ▼]     │
│ ─────────────────────────────────────────────────│
│                                                  │
│ The Hobbit (8.3 MB) ← thumbnail cover here      │
│   🔖 Downloaded 3 days ago                      │
│   [Open] [Read] [Delete] [Info]                 │
│                                                  │
│ Dune (12.1 MB)                                  │
│   🔖 Downloaded 1 week ago                      │
│   [Open] [Read] [Delete] [Info]                 │
│                                                  │
│ ...                                              │
└──────────────────────────────────────────────────┘

User clicks: "Read" (or "Open")
↓
→ System Preview.app opens, PDF is readable
→ User reads
→ Closes Preview, back to Finder (not back to app — that's fine)
```

**The flow in detail:**
1. Main menu → "View Library"
2. Library browser shows all books with minimal metadata (title, size, date)
3. User scans, finds book they want
4. User clicks "Read" 
5. `open -a Preview /path/to/book.pdf` launches
6. User reads in Preview (native, full-featured, fast)
7. User closes Preview when done

**Why this works:**
- No app bloat (Preview exists on every Mac)
- Zero performance hit
- Users get a professional, responsive PDF viewer they already know
- Library browser stays lightweight
- Users can still open Finder for organization if they want

---

## ASCII Cover Art Experiment — Feasibility & Recommendation

**Concept:** Show ASCII-rendered PDF covers as thumbnails in the library browser. *Very* on-brand with Pip-Boy aesthetic.

**Technical path:**
1. Extract first page of each PDF with `pdftoimage` or PyMuPDF
2. Convert to 40×60 character ASCII art with `chafa` or similar
3. Cache in library metadata
4. Render in TUI

**Real-world issues:**
- **Setup complexity:** adds 3 dependencies (pdftoimage/imagemagick, chafa, caching logic)
- **Speed:** first-time extraction slow for large libraries (200+ books = 5+ min)
- **Limited value:** ASCII covers are small, can't really identify books (all become gray blocks)
- **Maintenance:** if PDFs get deleted externally, cache gets stale

**Recommendation:** **Skip this.** The novelty is fun for a demo, but:
- Users identify books by title + metadata, not cover art
- The overhead isn't worth it for a macOS .app
- Show title, size, download date instead — that's how users actually find books

**Bonus:** If you *really* want visual appeal, generate a simple colored dot or letter (first initial) next to each title. Instant, no deps, same brain effect.

---

## Library Browser Sketch — Text Mockup

```
┌─────────────────────────────────────────────────────┐
│  Archive Librarian – Library                        │
├─────────────────────────────────────────────────────┤
│  📁 ~/Books/Archive  (3.2 GB / 47 books)            │
│                                                     │
│  Sort:  [↓ Title]  [Date]  [Size]      [↺ Refresh] │
│                                                     │
├─────────────────────────────────────────────────────┤
│ ☆ The Hobbit (8.3 MB)                              │
│   Saved 3 days ago • archive.org/details/...       │
│   [Read] [Delete] [ℹ More Info]                    │
│                                                     │
│ ☆ Dune: Part One (12.1 MB)                         │
│   Saved 1 week ago • archive.org/details/...       │
│   [Read] [Delete] [ℹ More Info]                    │
│                                                     │
│ ☆ Foundation (9.7 MB)                              │
│   Saved 2 weeks ago • archive.org/details/...      │
│   [Read] [Delete] [ℹ More Info]                    │
│                                                     │
│ ☆ 1984 (6.2 MB)                                    │
│   Saved 1 month ago • archive.org/details/...      │
│   [Read] [Delete] [ℹ More Info]                    │
│                                                     │
│ ... (scroll to see more)                           │
│                                                     │
├─────────────────────────────────────────────────────┤
│  [← Back to Main Menu]     [⚙ Settings]            │
└─────────────────────────────────────────────────────┘
```

**Key design choices:**
- **One book per row:** scannable, not overwhelming
- **Metadata below title:** date + size answer "when did I get this?" and "is it big?"
- **Three action buttons:** Read (primary, arrow key), Delete, Info
- **Archive.org link preserved:** user can click to revisit original source
- **Sort options:** title (default), date (most recent first), size
- **Refresh button:** rescan folder in case files added externally

---

## Implementation Path

**Phase 1 (Quick):** Upgrade `do_view_library()` in `main_app.py`
- Load `library.all_books()`
- Build a simple dialog showing title + size + download date
- Add "Read" button that calls `open -a Preview`
- Add "Delete" button that removes from catalog and filesystem

**Phase 2 (Nice-to-have):** Multi-select + batch operations
- Checkbox per row
- "Delete selected", "Export selected", etc.

**Phase 3 (Future):** Smart sorting, search, collections
- Full browse UX with TUI or PySimpleGUI

---

## Polish Detail (The Thing Nobody Asked For)

When a user clicks "Read" and Preview opens, **add a tiny automation:** if the PDF has 0 pages recorded in the catalog, use `pdfinfo` to count pages on first read, then cache it. Then next time they browse, they see "The Hobbit (311 pages, 8.3 MB)" — suddenly the library feels more *real* and curated, like they're building something.

---

**Signed,**  
**PIXEL** ✦

*Note: This design assumes Seb is the primary user (brother-grade simple means: his friends & family should be able to use it without asking questions). The PDF viewer is Preview; the app's job is just to get them there, then get out of the way.*
