---
name: add-subpage
description: Add a new HTML companion page to the Korean Cheat Sheet site (sister to grammar-cheatsheet.html, exercises.html, flashcards.html). Sets up the shared aesthetic, wires up the three-place cross-link pattern, and updates CLAUDE.md. Use when the user asks to "add a new page", "create a companion page", or "add a [topic] page" to this site.
---

# Add a subpage

Adds a new single-file HTML page that lives alongside the existing pages and follows the site's vermillion seal / hanji paper aesthetic.

## When to use

When the user wants a new page on the site that's a sibling to:
- `grammar-cheatsheet.html` (reference)
- `exercises.html` (drills)
- `flashcards.html` (cards)

Don't use this for one-off changes to existing pages.

## Process

### 1. Get scope

If the user hasn't already given them, briefly clarify:
- Page purpose & audience (one sentence)
- Filename (default: descriptive-name.html)
- Korean title for the hero
- Rough content shape (numbered sections? cards? a single tool?)

Don't dispatch agents for this step.

### 2. Read the existing skeleton

Before writing, read:
- `CLAUDE.md` — full project conventions
- `grammar-cheatsheet.html` lines 1–200 — head + CSS root + body + .ko + layout
- `flashcards.html` if you need a single-column reference
- `exercises.html` if you need a sectioned-content reference

### 3. Create the new HTML file

The file MUST contain (in order):

- `<!doctype html>`, `<head>` with `charset`, `viewport`, `title` in the `English · 한국어` form, `description`, font preconnects, single Google Fonts `<link>`
- `<style>`:
  - `:root` with light-mode CSS vars (lifted verbatim from grammar-cheatsheet.html)
  - `@media (prefers-color-scheme: dark) { :root { ... } }` dark override
  - `body` (Newsreader serif), `body::before` (hanji noise SVG filter)
  - `.ko` (Gowun Batang)
  - `.en` (small italic muted gloss)
  - `.layout` (single column or grid as needed)
  - `header.title` (eyebrow row, h1 with display rows, lede with ko-title)
  - `.callout` with the 註 mark
  - Page-specific CSS for new components
  - `footer` with seal
  - `@media (max-width: 880px)` and `@media (max-width: 480px)` mobile rules
  - `::selection { background: var(--vermillion); color: var(--paper); }`
- `<body>` with optional `.progress` thread, `.layout` container, hero, content, footer

Don't:
- Introduce colors outside the CSS variables
- Introduce romanization
- Add a `*.png` line to `.gitignore`
- Inline-style cross-links inside callouts (use the `.callout a` class rule)

### 4. Cross-link from `grammar-cheatsheet.html`

Add the new page in three places (mirror-symmetric pattern):

1. **Hero lede** (around line 760): "Want to drill it? Try the [Practice page](exercises.html), the [Flash Cards](flashcards.html), or the [NEW PAGE](newpage.html)."
2. **A mid-page callout** in a section relevant to the new page's topic
3. **Footer** (last few lines): add a "· [Link](newpage.html)" entry

### 5. Cross-link from sibling pages where natural

Mention the new page in the lede of `exercises.html` and `flashcards.html` if learners on those pages would benefit from discovering it.

### 6. Update `CLAUDE.md`

Under "## Repo topology" → "This repo", add:
```
- `newpage.html` — one-line description.
```

### 7. Smoke test

```bash
python3 -m http.server 8765 --bind 127.0.0.1 &
sleep 1
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8765/newpage.html  # expect 200
pkill -f "http.server 8765"
```

Span-balance check:
```python
import re
src = open('newpage.html').read()
o = len(re.findall(r'<span[^>]*>', src))
c = src.count('</span>')
assert o == c, f'{o}/{c}'
```

If the page has inline JS, also run `node --check` on the extracted script block.

### 8. Don't ship without asking

The site is public. Confirm before invoking `/ship:ship`.

## Conventions recap

- Korean wrapped in `<span class="ko">…</span>`. **Never** romanize.
- English glosses in tables use `<span class="en">…</span>` (`display: block`, italic, muted).
- Sample sentences wrapped in `<span class="ex">…</span>` (block, italic — see `flashcards.html` and the `.ex` rule).
- Section headers use `<span class="num">NN</span>` for the seal-stamp number.
- Fonts: Fraunces (display), Newsreader (body serif), Gowun Batang (Korean), IBM Plex Sans (UI), JetBrains Mono (code/IPA). One `<link>` from Google Fonts.
- Mobile rules at 880px (layout collapse) and 480px (font-size shrink).

## Common pitfalls

- Forgetting one of the three cross-link places — leaves the new page orphaned.
- Using `<table>` without the `display: block; overflow-x: auto` mobile rule — overflows on phones.
- `display: flex` on a content container that has mixed text + inline `<span>` — each text node becomes its own flex item. Wrap in `<p>` or use `display: block`.
- Adding inline `style=""` attributes — use class-based CSS so styles stay maintainable.
