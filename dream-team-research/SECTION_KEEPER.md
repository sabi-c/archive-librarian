# Archive Librarian: Catalog & Persona Design
**By KEEPER** — Librarian Systems Research

---

## 1. Cataloging Schema — Fields to Add to library.json

Current structure is minimal: identifier, title, url, pdf_path, pdf_size_mb, page_count, downloaded_at.

**Extend with:**

```json
{
  "identifier": "archiveID",
  "title": "Book Title",
  "authors": ["Author 1", "Author 2"],
  "domain": "Technology",
  "subdomain": "Systems Design",
  "subjects": ["concurrency", "databases"],
  "isbn": "978-...",
  "published_year": 2020,
  "description": "...",
  "page_count": 350,
  "pdf_size_mb": 12.4,
  "pdf_path": "/path/to/book.pdf",
  "url": "https://archive.org/details/...",
  "downloaded_at": "2026-04-16T...",
  "cover_url": "https://covers.openlibrary.org/...",
  "rating": 4.5,
  "times_opened": 3,
  "tags": ["personal-interest", "reference"],
  "notes": "Found via recommendation on system design",
  "shelf_status": "active"
}
```

**Key additions:**
- `domain` + `subdomain` — hierarchical organization (replaces flat structure)
- `subjects` — free-form keywords from Open Library (enables gap-finding)
- `authors`, `isbn`, `published_year`, `description` — enriched metadata
- `cover_url` — visual library browsing
- `rating`, `times_opened` — signals for library intelligence
- `tags` — user-defined shelves (e.g., "currently-reading", "reference", "gifting")
- `notes` — librarian's annotations (recommendations, cross-references)
- `shelf_status` — "active" (in use), "archive" (reference only), "pending" (to-read)

---

## 2. The Domains Taxonomy — 12 Top-Level Buckets

Designed for nonfiction/reference focus. Non-technical user can visually "walk the shelves."

1. **Philosophy & Ethics** — Metaphysics, meaning, decision-making, applied ethics
2. **Health & Biology** — Medicine, psychology, neuroscience, nutrition, fitness
3. **Technology & Systems** — Computing, software, networks, hardware, AI
4. **Business & Economics** — Management, markets, finance, organizations
5. **History & Culture** — History, geography, anthropology, art, literature
6. **Science & Nature** — Physics, chemistry, ecology, climate, natural systems
7. **Mathematics & Logic** — Pure math, statistics, algorithms, formal systems
8. **Crafts & Making** — DIY, design, cooking, agriculture, practical skills
9. **Humanities & Language** — Linguistics, writing, rhetoric, classics
10. **Society & Politics** — Law, governance, social dynamics, activism
11. **Personal Development** — Learning, habits, relationships, creativity, spirituality
12. **Reference & Tools** — Manuals, guides, indexes, meta-resources

Each domain has 3-5 common subdomains (e.g., Health → Neuroscience, Nutrition, Mental Health, Medicine).

**Why these 12?** Minimal cognitive load, covers 90% of nonfiction, aligns with how humans naturally browse libraries, culturally neutral.

---

## 3. Metadata Enrichment Pipeline

**When:** On first catalog add (via downloaded book metadata extraction)  
**Primary API:** Open Library (free, no auth, excellent for subjects/cover)  
**Secondary:** Google Books (fallback for description, rating)  
**Trigger:** After PDF is validated and added to catalog

```
Step 1: Extract ISBN from PDF metadata (if available)
Step 2: Query Open Library API by ISBN or title+author
Step 3: Harvest: authors, description, subjects array, cover_url, published_year
Step 4: Auto-assign domain using subjects (heuristic: most common subject → domain map)
Step 5: Store; display librarian toast: "📚 Filed under Technology & Systems"
```

**Open Library API endpoints (all free):**
- `GET /search/authors.json?name=Author` → get author key
- `GET /api/books?bibkeys=ISBN:...&jscmd=details` → full metadata
- `GET /subjects/[subject].json` → subject details + related books

**Cost:** $0 (Open Library is public infrastructure). Rate limit: ~1 request/sec, fine for download flow.

**Gap-finding bonus:** Store the full subjects array. Later, compare user's books against related subjects to surface "you have 4 books on memory but nothing on sleep — interested?"

---

## 4. The Librarian Persona

**Name:** ARIA  
**Voice:** Knowledgeable, helpful, *quiet*. Like a librarian who remembers you but doesn't hover.  
**Appearance:** Pip-Boy terminal aesthetic — maybe a subtle Vault-Tec logo, notification toasts at bottom of screen.

**When ARIA speaks:**
1. **On first encounter** (new book) — single one-liner toast
2. **On library milestones** (100 books) — celebratory notification
3. **When asked for recommendation** — brief, relevant
4. **On gap detection** (user has pattern) — proactive suggestion
5. **Never:** unsolicited chitchat, emoji spam, or "let me help you" when nothing is broken

**5 Example Utterances:**

1. *On shelving a neuroscience book:*  
   "✓ Filed. You now have 7 books on learning science."

2. *On detecting a gap:*  
   "Noticed: 12 books on philosophy, 0 on logic. Want recommendations?"

3. *On reaching a milestone:*  
   "Your archive has 100 volumes. Well-read library."

4. *On opening a previously-opened book:*  
   "You've opened *Deep Work* 4 times. Current read?"

5. *In response to manual tag:*  
   "✓ Marked *Thinking Fast and Slow* as reference. It'll show here."

**Design principle:** ARIA is a *presence*, not an agent. Notifications are informational, not conversational. User controls the relationship intensity via settings (verbose/quiet/silent modes).

---

## 5. Gap-Finding Logic

**Heuristic Algorithm:**

```
1. Load all books, extract domain + subjects for each
2. Build frequency map: { domain: [count, subjects_list] }
3. For domains with count >= 3:
   a. Extract top 5 subjects that user HAS books on
   b. Query Open Library for related subjects the user LACKS
   c. Score by relevance (shared adjacent subjects) and popularity
4. Recommend: "You have X books on [Domain], consider adding [Related Subject]"
5. Surface via toast on library open or via manual /recommendations action
```

**Example triggers:**
- User has 5+ books on *Health & Biology* but none on "nutrition" → suggest
- User has books on "machine learning" and "systems" but none on "computer networks" → suggest
- User has 10+ books total but all in same domain → gently suggest another
- User has been reading "philosophy" consistently for 3 weeks → recommend related logic/ethics books

**Why this works:** It's not algorithmic recommendation (which can be overwhelming). It's librarian intuition: "I noticed you like X; you might find Y interesting." Respects user autonomy.

---

## 6. Implementation Roadmap

**Phase 1 (MVP):**
- Add domain + subjects to library.json schema
- Integrate Open Library API fetch on download (async, no blocking)
- Display domain in library view (simple folder-like UI)
- Store but don't yet surface gap recommendations

**Phase 2 (Intelligence):**
- Build gap-finding heuristic
- Surface recommendations as opt-in toast notifications
- Add "tagged shelves" UI (currently-reading, reference, favorites)

**Phase 3 (Polish):**
- ARIA voice integration (optional voice notifications on macOS)
- Seasonal library summaries ("Your reading this month: 3 tech, 2 philosophy")
- Cross-book linking ("Books that cite each other" or "related subjects")

---

## KEEPER's Library-Science Principle

**Every book deserves a context, and every reader deserves a librarian who knows them.**

In the flat world of downloaded PDFs, *domain* + *subjects* + *gap detection* turn a folder into a library. The librarian is not a chatbot—she's the *structure itself*, embodied in smart defaults, subtle recommendations, and respect for silence. ARIA's job is to make the user's library feel less like a backup drive and more like a living organism that learns what you read and gently opens doors you hadn't noticed.

---

*— KEEPER, Librarian Systems Research*  
*Archive Librarian v2 Cataloging Foundation*
