# Korean Cheat Sheet — Project Notes

Static GitHub Pages site teaching Korean grammar. Has a sister repo that teaches reading Hangul, and the two are designed to be maintained together.

## Repo topology

- **This repo** — `mikersays/korean-cheat-sheet` → https://mikersays.github.io/korean-cheat-sheet/
  - `grammar-cheatsheet.html` — the whole site (CSS + content in one file)
  - `index.html` — meta-refresh redirect
  - `grammar-cheatsheet.md` — earlier markdown source, kept for reference; **HTML is the source of truth**
- **Sister repo** — `mikersays/hangeul-reading-guide` → https://mikersays.github.io/hangeul-reading-guide/
  - Local path: `../hangeul-reading-guide/`
  - Same single-HTML-file layout, same CSS lifted from this repo
  - Teaches Hangul reading as a prerequisite to the cheat sheet
  - **When changing shared CSS, update both files.** They were lifted from a single source and have drifted only by intentional additions.

Both Pages sites: branch `main`, path `/`, build_type `legacy`. No build step — push and it's live in ~30s.

## Aesthetic — non-negotiable

Vermillion seal / hanji paper aesthetic. CSS variables in `:root` (and dark mode override) define the whole palette: `--paper`, `--ink`, `--vermillion`, `--celadon`, etc. **Don't introduce new colors outside the variables.**

Fonts: Fraunces (display), Newsreader (body serif), Gowun Batang (Korean), IBM Plex Sans (UI/labels), JetBrains Mono (code/IPA). All from Google Fonts via the single `<link>`.

Section headers use a vermillion seal-stamp number (`<span class="num">NN</span>`) rotated -2°. Callouts use a 註 mark in the corner. Pre blocks have a vermillion left rule. Don't add competing visual motifs.

## Markup classes (shared across both files)

- `.ko` — inline Korean text (Gowun Batang, `word-break: keep-all`)
- `.en` — small italic muted English gloss below Korean in table cells (`display: block`)
- `.ipa` — IPA pronunciation badge, monospace celadon, `[bracketed]` (sister repo only currently — promote here if needed)
- `.callout` — vermillion sidenote with 註 mark; use `.callout a` (which has a class-level rule) — **never inline-style** cross-links
- `<pre><code>` — example sentence blocks with the vermillion margin rule
- `<table>` — standard; tables become `display: block; overflow-x: auto` at ≤880px
- `ol.tree` — decision-tree numbered steps with seal-stamp markers
- `.endings` — two-column quick reference (used in §23)

Sister repo also has: `.jamo-grid` / `.jamo-cell`, `.walk` / `.step`, `.diagram` (inline SVG). Don't add those here unless a section needs them.

## Translation/pronunciation policy

- **No romanization.** Anywhere. Both repos.
- The cheat sheet uses inline `(English)` parenthetical glosses inside `<pre>` blocks and small `.en` glosses below Korean examples in table cells.
- The reading guide uses IPA in `[brackets]` via `.ipa`, never romanization.
- Korean example sentences should always have an English meaning gloss; pure conjugation/morphology demonstrations don't need one.

## Mobile invariants (verified at 360 / 414 / 768)

These rules in the `≤880px` media query exist for specific reasons — don't relax them without re-running a Playwright audit:

- `pre { white-space: pre-wrap; word-break: keep-all; overflow-wrap: anywhere; }` — Korean syllables stay intact, English wraps. Without `keep-all` Korean breaks mid-word.
- `table { display: block; overflow-x: auto; white-space: nowrap; } table td, table th { white-space: normal; }` — wide tables become independently scrollable; cells still wrap.
- At ≤480px: smaller `pre` and `table` font, `.ipa { white-space: normal; }` so dense IPA-heavy tables (like the reading guide drill list) fit.

## Cross-linking pattern

Each site links the other in **three places** (mirror-symmetric):

1. **Hero lede** — first paragraph
2. **A mid-page callout** — §0 Foundations here; closing graduation callout after §20 in the reading guide
3. **Footer**

If you add a new prerequisite or sequel, follow the same three-place pattern.

## Local dev

- `python3 -m http.server 8765 --bind 127.0.0.1` from this repo
- `python3 -m http.server 8766 --bind 127.0.0.1` from the reading-guide repo (different port so both can run)
- Mobile audits via Playwright MCP — viewports 360 / 414 / 768. Screenshots go to `playwright-screenshots/` (gitignored). The Playwright MCP also writes to `.playwright-mcp/` and sometimes `audit/` — both gitignored.

## Things to avoid

- **Don't broad-ignore `*.png`** in `.gitignore` — scope to specific Playwright dirs so future legitimate image assets aren't silently ignored.
- **Don't dispatch parallel subagents writing to the same file.** Have each agent emit content with `=== sN ===` markers to its own `_content_partN.html`, then a small integration script merges them. Always clean up the temp content files after merging.
- **Don't amend pushed commits** — create a new commit. Both repos are public.
- **Don't introduce romanization** even casually in comments or examples. The "no romanization" stance is a feature.
