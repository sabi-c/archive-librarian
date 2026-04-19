# Archive Librarian v2.1 — Anti-Slop Design Research

## What "AI Design Slop" Actually Looks Like

The 2026 anti-AI backlash identifies five concrete signatures of AI-generated interfaces:

**Color:** [Purple-to-blue gradients](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website) appear in hero sections and CTA buttons because LLMs trained on SaaS landing pages predict them as statistically "safe." This trained mediocrité dominates every web design corpus scraped through 2024.

**Typography:** [Inter font](https://techbytes.app/posts/escape-ai-slop-frontend-design-guide/) everywhere. Roboto, Open Sans, Lato fill the gaps. These are the defaults Claude and ChatGPT reach for because they're ubiquitous in tutorial data. The absence of character.

**Layout:** [Card-based grids with uniform 16px border radius](https://www.925studios.co/blog/ai-slop-web-design-guide/)—three boxes with icons, predictable stacks, zero compositional tension. Hero text centered below a massive button. Zero asymmetry, zero hierarchy beyond "bold header."

**Iconography:** [Material Symbols and Heroicons](https://fonts.google.com/icons) provide neutral, untraceable visual language. They feel corporate precisely because they're designed to offend no one.

**Motion:** Smooth fades, ease-in-out, timed animations that feel like they came from a Framer template circa 2021. No jank, no character.

**The Root Cause:** [During token sampling, LLMs predict based on statistical patterns](https://techbytes.app/posts/escape-ai-slop-frontend-design-guide/). Safe design choices dominate web training corpora. The model converges toward the median.

---

## Five Anti-Slop Principles (with Sources)

### 1. **Constraint + Provenance Over Safe Defaults**
[Frank Chimero](https://shapeofdesignbook.com/chapters/01-how-and-why/) argues that design gains value as it moves "from hand to hand; context to context." Context shapes character. Archive Librarian isn't a generic SaaS product—it's a macOS app with a specific thesis (riso + vernacular). Commit to one aesthetic vision before writing CSS.

**For AL:** Deep blue + cream + halftone is already constraining. Build everything within that constraint. One typeface family with deliberate weight hierarchy. No gradients outside the halftone texture.

### 2. **Distinctive Typography = Immediate Differentiation**
[The anti-slop research consensus](https://medium.com/@similarfonts/inter-font-alternatives-7-fonts-similar-to-inter-9b886101a810) is clear: avoid Inter, Roboto, Open Sans. Instead, choose fonts with personality—[Playfair Display and Crimson Pro for editorial](https://techbytes.app/posts/escape-ai-slop-frontend-design-guide/), Clash Display or Bricolage Grotesque for contemporary work, JetBrains Mono for code contexts.

**For AL:** AL likely uses system fonts or a safe web font. Switching to a single distinctive serif (e.g., Crimson Pro) for headings and a hardworking sans (e.g., Work Sans) for body text would immediately break the AI slop pattern and signal intent.

### 3. **Asymmetry + Compositional Tension**
[Anti-design rejects symmetry and harmony](https://builtin.com/articles/anti-design), embracing "chaos, clashing colors, irregular layouts, and unconventional typography." This isn't just chaos for chaos's sake—it's reaction against the "everything centered, everything grid-aligned" default. [IndieWeb design](https://indieweb.org/principles) prioritizes UX and character over protocol.

**For AL:** If every section is 8px grid–aligned and centered, it reads as safe. Offset navigation. Place a card outside the grid. Let content breathe asymmetrically. Riso printing tolerates misregistration—embrace digital asymmetry.

### 4. **Color Palette = Specific, Not AI-Predicted**
Instead of purple-to-pink (the AI median), [Impeccable recommends OKLCH color spaces](https://github.com/pbakaus/impeccable) with specific saturation and lightness values. The deep blue + cream palette is already specific. Halftone textures should generate the secondary colors through overlap, not smooth gradients.

**For AL:** Use the riso primary colors as true constants. Secondary colors emerge from halftone overlap simulation (multiply blends in CSS). No smooth gradients between blue and cream—only the halftone texture does blending.

### 5. **Print Discipline in Digital Space**
[Hassan Rahim](https://hassanrahim.com/) and [Bryce Wilner](https://brycewilner.com/) work across print and digital, translating physical constraints into digital character. [Risograph aesthetics](https://outoftheblueprint.org/files/) depend on halftone dots, misregistration, and ink layering—constraints that make each print unique.

**For AL:** Halftone texture isn't ornament; it's the design system. Use halftone patterns to simulate ink overlap. Let some misalignment happen—don't grid-snap every element. Texture is character.

### 6. **No Smooth Animations Unless Justified**
[Impeccable flags ease-in-out as a slop pattern](https://github.com/pbakaus/impeccable). Editorial software (Linear, Framer) uses motion sparingly: focus shifts, state changes, nothing decorative. [Framer](https://www.framer.com) itself avoids motion in UI—it's there for interaction feedback, not delight.

**For AL:** If AL has animations, tie them to interaction (hover, click, scroll). No auto-play, no decorative floating elements. Riso prints don't move. Digital interactions should feel like page turns, not tweens.

### 7. **Vernacular + Handmade Aesthetic**
[The IndieWeb](https://indieweb.org/principles) and [vernacular web revival](https://vernacular.is/) reject polished uniformity. [Anti-design](https://builtin.com/articles/anti-design) embraces irregularity, hand-drawn touches, and "bad 1990s' designs on steroids"—not bad in execution, but bad in breaking expectations. Asymmetry is a feature.

**For AL:** If UI elements have slightly imperfect corners, or text sits off-grid, that's not a bug—it's vernacular. A printed book has spine curl and page warping. Digital can have that intentionality too.

---

## Existing Skill/Rule Packages

Two packages directly address anti-slop for AI-assisted design:

1. **[Impeccable](https://github.com/pbakaus/impeccable)** (10k+ GitHub stars)
   - 20 slash commands for Claude Code / Cursor / Gemini CLI
   - 7 domain-specific references (typography, OKLCH color, spatial design, motion, interaction, responsive, UX writing)
   - Detects 20+ anti-patterns: gradient text, nested cards, low contrast, AI color palettes
   - Catches Material Symbols + Heroicons monoculture

2. **[anti-slop](https://smithery.ai/skills/rand/anti-slop)** (Smithery)
   - Detects slop across text, code, and design
   - Reference files for design-patterns with improvement strategies
   - Python preview/apply modes
   - Install: `npx @smithery/cli@latest skill add rand/anti-slop`

Both are built for Claude Code. Neither is tailored to riso/print aesthetics, but both catch the "AI median" patterns that Archive Librarian should actively avoid.

---

## Map to Archive Librarian

| Principle | Archive Librarian: Keep | Add | Kill |
|-----------|---------|-----|------|
| **Constraint** | Deep blue + cream + halftone thesis | Rigorous design system document | Generic component libraries |
| **Typography** | Current choice (TBD) | One distinctive serif, one hardworking sans | Inter everywhere, system fonts only |
| **Asymmetry** | If present | Deliberate off-grid placement | Rigid 8px grid alignment everywhere |
| **Color** | Riso primaries | Halftone overlap simulation (CSS multiply) | Smooth gradients, purple-pink, HSLA |
| **Print Discipline** | Halftone texture reference | Misregistration tolerance in spacing | Pixel-perfect alignment obsession |
| **Motion** | Sparse, interaction-tied | Focus shifts, state feedback | Decorative animations, floating elements |
| **Vernacular** | If hand-drawn elements exist | Slight imperfection as intentional | Polished uniformity, Material Design pastels |

---

## My Take

Archive Librarian's riso direction is **already anti-slop**. Deep blue + cream + halftone is not a purple gradient. It's specific, constrained, and rooted in print. But anti-slop isn't just "not AI"—it's **active commitment to character over convenience.**

The riso aesthetic succeeds only if every decision (type, spacing, color, motion) reflects the constraint. If AL falls back on Inter, smooth gradients, centered heroes, and Material Symbols, it loses the thesis and becomes "generic macOS app with a riso filter." The difference between "intentional print aesthetic" and "AI slop wearing a riso costume" is whether the constraint is structural (baked into every decision) or decorative (applied at the end).

Recommend: Run AL through [Impeccable](https://github.com/pbakaus/impeccable) before shipping. Use `@impeccable typography`, `@impeccable colors`, `@impeccable layout` as guardrails. Then, add a print-specific constraint: every color must exist in the halftone palette, every typeface decision must reflect the editorial aesthetic, every animation must justify itself functionally. If it doesn't, delete it.

---

## Follow

**SCOUT-2 recommends:** [Hassan Rahim](https://hassanrahim.com/) / [12:01 Studio](https://www.1201.am/). His work moves seamlessly between print (collage, type), objects (woven stools), and digital (video, design). No platform-native defaults. Every medium gets a specific aesthetic. That's the model.

---

## Sources

- [CNN Business: Why 2026 could be the year of anti-AI marketing](https://www.cnn.com/2025/12/16/business/anti-ai-backlash-nightcap)
- [Why Your AI Keeps Building the Same Purple Gradient Website](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website)
- [Tech Bytes: Escape AI Slop: Claude Skills Transform Frontend Design](https://techbytes.app/posts/claude-frontend-design-skills-guide/)
- [Medium: Inter Font Alternatives](https://medium.com/@similarfonts/inter-font-alternatives-7-fonts-similar-to-inter-9b886101a810)
- [Built In: Anti-Design Is Intentionally Loud and Messy](https://builtin.com/articles/anti-design)
- [IndieWeb Principles](https://indieweb.org/principles)
- [Hassan Rahim Portfolio](https://hassanrahim.com/)
- [Bryce Wilner Portfolio](https://brycewilner.com/)
- [GitHub: Impeccable Design Skill](https://github.com/pbakaus/impeccable)
- [Smithery: anti-slop Skill](https://smithery.ai/skills/rand/anti-slop)
- [Frank Chimero: The Shape of Design](https://shapeofdesignbook.com/chapters/01-how-and-why/)
- [RISO Print Guide](https://outoftheblueprint.org/files/)
- [Risograph FAQ](https://risottostudio.com/pages/printing-faq)
- [Vernacular Web](https://vernacular.is/)
