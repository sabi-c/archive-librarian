# SCOUT Research: RISO Aesthetic Polish & Transitions

## Top 6 References

### 1. **Things 3** — The Gold Standard for Editorial Polish
- **URL**: [culturedcode.com/things/features](https://culturedcode.com/things/features)
- **What they do**: Custom animation toolkit with fluid, purposeful transitions. Opening a task expands it like an unfolding white piece of paper. Smooth navigation between views without jarring shifts.
- **Why it works**: Each gesture invokes deeply satisfying animations; smooth gestures maintain spatial continuity. Animation serves the metaphor (document unfolding), not distraction.
- **What to steal**: Build a custom animation system, not generic fades. Metaphor-driven transitions (paper, cards, layers) feel more intentional than abstract dissolves.
- **What to skip**: Don't animate every state change—only the meaningful interactions.

### 2. **Apple Books Page-Turn Transitions** — Print Metaphor in Motion
- **URL**: [iOS 16.4 introduces page turn animations](https://goodereader.com/blog/e-book-news/ios-16-4-introduces-page-turn-animations-to-apple-books)
- **What they do**: Three transition modes: curl (physical page fold), slide (minimal), and none. Users choose their metaphor.
- **Why it works**: The curl animation creates tactile satisfaction—viewers feel the page turning under their fingers, evoking a real book.
- **What to steal**: Physical metaphors resonate. The curl, while mechanical-sounding, is actually deeply human. Archive Librarian's pages could "unfold" rather than "fade."
- **What to skip**: Avoid page-flip for every transition—it's too heavy-handed for rapid navigation. Reserve it for major section breaks.

### 3. **Linear Dashboard** — Minimalist Editorial Precision
- **URL**: [linear.app/now/how-we-redesigned-the-linear-ui](https://linear.app/now/how-we-redesigned-the-linear-ui)
- **What they do**: Custom design system (Orbiter) with modular components. Transitions are *invisible*—"If most people don't immediately notice what changed, that's probably a good sign."
- **Why it works**: Micro-refinements over flashy motion. Focus on consistency, readable fonts, breathing room. State changes happen naturally within the existing layout.
- **What to steal**: Subtlety is the move. A 100ms opacity+scale combo on screen entry beats any 1-second animation. Transitions should feel like state change, not showmanship.
- **What to skip**: Avoid cascading animations or long entrance sequences.

### 4. **Ink Transition Effect (CSS)** — Print Bleeding & Reveal
- **URL**: [CodyHouse Ink Transition Effect](https://codyhouse.co/gem/ink-transition-effect/)
- **What they do**: Ink bleeds across the screen using PNG sprite sequences and CSS steps(). Simulates wet ink spreading, revealing new content beneath.
- **Why it works**: Ties directly to print aesthetics—ink is the physical medium. The staggered reveal (via steps) mimics how ink settles on paper.
- **What to steal**: **This is the Archive Librarian win.** Replace hard reloads with an ink-bleed effect. Use halftone color separation (cyan/magenta/yellow) animating in sequence, each layer offsetting slightly—print plate registration in real-time.
- **What to skip**: Don't overuse it; reserve for major navigation (switching screens), not every dialog.

### 5. **RISO Print Simulator (Risotto Studio)** — Authentic Visual Feedback
- **URL**: [risottostudio.com/pages/print-simulator-ink-shift](https://risottostudio.com/pages/print-simulator-ink-shift)
- **What they do**: Real-time preview of RISO separations (color layers), showing how ink misalignment and bleed affect the final print.
- **Why it works**: Users *see* the imperfection. Misregistration isn't a bug—it's the aesthetic. The UI itself becomes tactile.
- **What to steal**: Add *visible* color separation to the transition itself. Show cyan, then magenta, then yellow layers sliding into place with intentional offset. Let imperfection be the feature.
- **What to skip**: Avoid perfectly registered, smooth separations. The charm is in the misalignment.

### 6. **Spectrolite App** — RISO Color Separation Workflow
- **URL**: [spectrolite.app](https://spectrolite.app/how-to/resources/software-recs)
- **What they do**: Free Mac app for preparing artwork for RISO printing. Auto-separates images into color layers with layer-by-layer control.
- **Why it works**: Makes the technical process visible and interactive. Each color layer is a *choice*, not an algorithm output.
- **What to steal**: The mental model of "layers" is crucial. Archive Librarian's screens could transition by revealing color layers one by one, just like RISO prep.
- **What to skip**: Don't hide the process; the process *is* the aesthetic.

---

## Transition Recommendation

**Use a "RISO Ink Develop" effect instead of page-flip or fade.**

Here's the specific move:

1. **Screen A is visible** (all layers: cyan, magenta, yellow, black halftone dots).
2. **User triggers navigation**. The canvas "resets"—all content fades to deep blue background (the paper color).
3. **Ink develop sequence** (120ms total):
   - **+0ms**: Cyan layer enters, bleeding slightly right and down (1px offset, ease-out).
   - **+40ms**: Magenta layer enters, offset left and down, slightly higher opacity.
   - **+80ms**: Yellow layer enters, offset right, slight delay.
   - **+100ms**: Black halftone dots fade in sharp.

**Why this works**:
- It's *fast* (not precious). Doesn't feel like you're waiting.
- It's *iconic* to Archive Librarian's aesthetic—viewers immediately recognize "print happening."
- It's *unique*. Fade is generic. Page-flip is mechanical. Ink develop is editorial + tactile.
- It *allows imperfection*: 1px misalignment is a feature, not a glitch.

**Implementation**: Use CSS keyframe animations or a lightweight JS library (Framer Motion, Gsap). Animate on a single `<canvas>` overlay during screen swap, or use SVG paths to clip content layers.

---

## Microinteraction Patterns — What's Shipping in 2026

### 1. **Subtle Scale + Opacity** (Vercel, Linear)
- On focus/hover: scale 1.0 → 1.02 + opacity shift. 150ms ease-out. No translation—keeps layout stable.
- **Rule**: Never use `transition: all`. Only animate `opacity` and `transform`.

### 2. **Staggered Layer Reveal** (RISO simulation, Apple Books)
- Multiple elements enter with staggered delays (40-80ms apart). Creates flow without feeling busy.
- **Rule**: Each layer should complete before the next starts, not overlap.

### 3. **Cross-Dissolve with Hold** (Editorial design)
- Fade out current, hold black for 60ms, fade in new content. Gives viewers mental reset point.
- **Rule**: The "hold" is crucial—it signals a new context.

### 4. **Ink Bleed / Gradient Mask** (Print aesthetic)
- Content is masked with a gradient or feathered edge, bleeding slightly into adjacent pixels. CSS `mask-image` or canvas.
- **Rule**: Imperfection is the point. 1-2px bleed is perfect.

### 5. **Halftone Dot Density Shift** (Risotto, RISO aesthetic)
- As state changes, dot density increases/decreases (simulating ink pressure). Optical illusion of "darkening" or "lightening" the screen.
- **Rule**: Use SVG or canvas to modulate dot size/spacing during transitions.

---

## What's NOT in the Wild — Your Opportunity

**Gap 1: Apps that transition using RISO layer separation in real-time.**
- Every RISO tool we found is *static preview* (you see the separation, but it doesn't animate).
- **Archive Librarian can own this**: Animated color-separation transitions are novel.

**Gap 2: Halftone dot animati during state change.**
- Halftone is aesthetic; halftone *motion* is rare.
- **Steal this**: Modulate dot density/size during screen entry to create an "ink pressure" effect.

**Gap 3: Print metaphor applied to navigation, not just aesthetics.**
- Things 3 uses paper unfolding. Apple Books uses page-turn. But no app chains multiple *print plates* together to create a sequence of transitions.
- **Your move**: Make each screen a separate "print plate," and navigation is the act of registering them on top of each other.

**Gap 4: Tactile feedback via color separation imperfection.**
- Most apps hide misalignment. Spectrolite *shows* it, but it's static.
- **Archive Librarian can**: Celebrate 1-2px misregistration as a feature. Let the misalignment subtly animate—it adds life.

---

## Bonus Finding: The Weird Thing SCOUT Wasn't Asked About

**Risotto Studio has a free **"Print Simulator"** web tool ([risottostudio.com/pages/print-simulator-simple](https://risottostudio.com/pages/print-simulator-simple)) that lets you upload an image and watch it RISO-separate in real-time in your browser.**

You can drag sliders to adjust color intensity and *watch the halftone pattern shift*. It's hypnotic. The interaction model is: *feel the medium*. Archive Librarian could steal this exact UX pattern for settings or color customization—don't just let users pick a color, let them *watch the ink layer adjust* while they decide.

Also: **RizzCraft (True Grit Texture Supply)** is the production tool for RISO effects in 2026, and it works across Photoshop, Procreate, Clip Studio Paint, and Affinity. If you ever need to generate on-brand test assets, this is the ecosystem to build into.

---

**— SCOUT**

---

## Reference URLs

- [Things 3 – Cultured Code](https://culturedcode.com/things/features)
- [Apple Books iOS 16.4 Page Turn Animations](https://goodereader.com/blog/e-book-news/ios-16-4-introduces-page-turn-animations-to-apple-books)
- [Linear UI Design Refresh](https://linear.app/now/how-we-redesigned-the-linear-ui)
- [CodyHouse Ink Transition Effect](https://codyhouse.co/gem/ink-transition-effect/)
- [Risotto Studio Print Simulator](https://risottostudio.com/pages/print-simulator-ink-shift)
- [Spectrolite – RISO App](https://spectrolite.app/how-to/resources/software-recs)
- [Vercel Design Guidelines](https://vercel.com/design/guidelines)
- [RizzCraft RISO Effects System](https://www.truegrittexturesupply.com/products/rizzcraft)
- [Halftone/Neo-Print Trends 2026](https://artcoastdesign.com/blog/halftone-textures-neo-print-trend-2026)
