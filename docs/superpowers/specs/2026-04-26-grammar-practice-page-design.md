# Grammar Practice Subpage — Design

**Date:** 2026-04-26
**Repo:** mikersays/korean-cheat-sheet
**Status:** Approved (pending user review of this written spec)

## Goal

Add a static practice subpage to the Korean Grammar Cheat Sheet site, deployed via the same GitHub Pages flow, that gives a learner ~195 exercises across the grammar topics taught in `grammar-cheatsheet.html`. Each exercise hides its answer behind a click-to-reveal control so a learner can think first, then check.

## Constraints (inherited from CLAUDE.md)

- Static HTML, no build step, deploys on push to `main`.
- Vermillion / hanji / seal aesthetic with the existing CSS variables — no new colors.
- Fonts: Fraunces, Newsreader, Gowun Batang, IBM Plex Sans, JetBrains Mono — single `<link>` to Google Fonts.
- No romanization, anywhere. Korean examples may be paired with `.en` glosses or `(English)` parentheticals.
- Mobile invariants at 880px / 480px (Korean `keep-all`, `pre-wrap`, scrollable tables) must hold.
- Cross-link the new page in three places per the existing mirror-symmetric pattern.

## File layout

| Path | Purpose |
|---|---|
| `exercises.html` | New file at repo root. Sibling of `grammar-cheatsheet.html`. |
| `index.html` | Unchanged — keeps redirecting to `grammar-cheatsheet.html`. |
| `grammar-cheatsheet.html` | Edited in three places to cross-link the new page. |

`hangeul-reading-guide` (sister repo) is **not** edited. Exercises are post-cheat-sheet, not post-reading-guide.

## Page structure (`exercises.html`)

A single page mirroring the cheat sheet's structure: progress thread, hero, anchored TOC, then numbered sections, then footer.

### Hero
- `<h1>` *Korean Grammar Practice · <span class="ko">연습</span>*
- One-paragraph lede explaining the page is a companion drill set for the cheat sheet, with links back to `grammar-cheatsheet.html` and `https://mikersays.github.io/hangeul-reading-guide/`.

### TOC
Anchored `<nav>` listing each section, same pattern and styling as the cheat sheet's TOC. Section IDs match the cheat sheet (`s0`, `s1`, … `s23`) so a reader can compare grammar reference and drills side-by-side and cross-jump cleanly.

### Sections (22 of them)

Covered: §00, §01–§16, §18–§21, §23. Skipped: §17 Pronouns, §22 Decision Tree, §24 Study Tips. (25 cheat-sheet sections − 3 skipped = 22.)

Each section contains:
1. `<h2><span class="num">NN</span> Title</h2>` — vermillion seal-stamp number, same as cheat sheet.
2. One-line `lede` reminding the rule, ending with `→ <a href="grammar-cheatsheet.html#sN">read the rule</a>`.
3. 6–15 exercise cards mixing the eight exercise types defined below.

Volume target per section (rough; the implementation plan will fix exact counts):

| Section | Count | Section | Count |
|---|---|---|---|
| s0 Foundations | 4 | s11 Connectors | 10 |
| s1 Word Order | 6 | s12 Modifiers | 10 |
| s2 Particles | 15 | s13 Nominalization | 8 |
| s3 Copula | 6 | s14 Sentence-Final | 12 |
| s4 Stems | 6 | s15 Quoting | 8 |
| s5 Speech Levels | 6 | s16 Numbers/Counters | 10 |
| s6 Present | 12 | s18 Question Words | 8 |
| s7 Past | 10 | s19 Caus./Pass. | 8 |
| s8 Future/Probability | 8 | s20 Irregular Stems | 12 |
| s9 Negation | 8 | s21 Build a Sentence | 8 |
| s10 Honorifics | 8 | s23 Identify Endings | 12 |

**Total: ~195 exercises.**

### Footer
Mirrors the cheat sheet's footer: 韓 seal, project name, links to cheat sheet and reading guide.

## Exercise card

One markup pattern, eight prompt types. Reveal uses native `<details>/<summary>` — no JS.

```html
<div class="ex" id="ex-2-7">
  <div class="ex-head">
    <span class="ex-num">2.7</span>
    <span class="ex-type">particle</span>
  </div>
  <div class="ex-prompt">
    Fill in the blank: <span class="ko">저는 학교___ 가요.</span>
    <span class="en">(I'm going to school.)</span>
  </div>
  <details class="ex-answer">
    <summary>답</summary>
    <div class="ex-solution">
      <span class="ko">에</span> — <span class="en">destination/location particle, attaches to <span class="ko">학교</span></span>.
    </div>
  </details>
</div>
```

### The eight exercise types

Each labeled with `<span class="ex-type">…</span>`:

| Label | Use |
|---|---|
| `particle` | Fill-in-the-blank particle (§2 et al.) |
| `conjugate` | Given stem + level + tense, write the form (§6, §7, §8, §10, §20) |
| `transform` | Make this past / honorific / negative / question (§7, §9, §10, §18) |
| `read` | Korean → English comprehension (any) |
| `write` | English → Korean production (any, harder) |
| `identify` | "Which ending is this and what does it mean?" (§14, §23) |
| `choose` | Multiple choice — picker rendered as a small list, answer revealed (any) |
| `build` | Assemble a sentence from given pieces (§21) |

For `choose`, the choices render in the prompt; the `<summary>` reveals the correct option plus a one-line why.

## CSS additions

All additions live in the same `<style>` block as the lifted cheat-sheet CSS. New rules:

- `.ex` — card with paper-soft background, hairline rule, slight padding. Bottom margin of one rhythmic unit.
- `.ex-head` — flex row holding number and type label.
- `.ex-num` — JetBrains Mono, ink-faint, like a marginalia number.
- `.ex-type` — IBM Plex Sans, uppercase, celadon, letter-spaced, small.
- `.ex-prompt` — Newsreader body. Inline `.ko` keeps Gowun Batang, `.en` keeps muted italic.
- `details.ex-answer summary` — styled as a small vermillion tab containing the text `답` ("answer"): vermillion background, paper text, rounded edges, `cursor: pointer`. Hides the default disclosure triangle (`list-style: none; ::-webkit-details-marker { display: none; }`).
- `details.ex-answer[open] summary` — slightly muted to signal "revealed."
- `.ex-solution` — same paper-soft inset, indented, with a vermillion left rule (echoing `<pre>` blocks).
- `@media print { details.ex-answer { ... } details.ex-answer[open] { ... } }` — opens all answers when printing so the page is usable as a printable worksheet.

Mobile rules at the existing breakpoints reduce padding and keep `.ko` `keep-all`. No new motifs.

## Cross-linking edits to `grammar-cheatsheet.html`

Three new touches following the existing mirror-symmetric pattern:

1. **Hero lede** — append a sentence pointing to `exercises.html` ("Want to drill? See the **Practice** page.").
2. **Mid-page callout** — a new `.callout` near §21 *Building a Sentence* nudging the learner to drill the recipe in the practice page.
3. **Footer** — add a Practice link alongside the existing reading-guide link.

Reading guide repo is **not** edited.

## Mobile / responsive

Verified at 360 / 414 / 768 via Playwright MCP before the work is called done. Specifically check:

- Exercise cards don't overflow horizontally.
- `<summary>` tap target is at least 44×44 (iOS HIG) and remains tappable when nested in a card.
- Korean inside `.ex-prompt` does not break mid-word.
- The TOC links scroll smoothly to each section.

## Accessibility

- Native `<details>` is keyboard-accessible by default; preserve that (no `tabindex` or JS overrides).
- `<summary>` text is "답" — pair it with `aria-label="Reveal answer"` for screen readers, since "답" alone is opaque outside Korean context.
- Color contrast for vermillion on paper meets WCAG AA at the existing values; new `.ex-type` celadon must also be checked.
- Do not rely on color alone — the `<summary>` includes the 답 text so the affordance reads even without color.

## What's intentionally out of scope

- Scoring, streaks, localStorage state — would force JS, breaks the "scroll" feel.
- Randomization or shuffling — same reason.
- Audio playback of Korean prompts.
- A separate index page or per-section pages.
- Editing the reading guide repo.

If any of these are wanted later, they are additive and can land in a follow-up.

## Acceptance criteria

1. `exercises.html` exists at repo root and renders with the same aesthetic as `grammar-cheatsheet.html`.
2. ~195 exercises across 22 sections, with the type mix described.
3. Native `<details>` reveal works without JavaScript.
4. Three cross-links land in `grammar-cheatsheet.html` (hero, callout near §21, footer).
5. No romanization anywhere.
6. Mobile audit at 360 / 414 / 768 passes — no overflow, Korean stays whole, tap targets adequate.
7. Print stylesheet opens all answers.
8. Page deploys cleanly via GitHub Pages on push to `main`.

## Implementation strategy note

Given the volume (~185 exercises), drafting all the exercise content in a single conversation turn risks parallel-write conflicts (per CLAUDE.md). The implementation plan should either:

- generate exercises in serial section-by-section edits, or
- if parallelizing, have each subagent emit `_content_partN.html` with `=== sN ===` markers, then a small integration step merges them into `exercises.html`. Temp files cleaned up afterward.

The implementation plan (next step, via writing-plans) will pick one and detail it.
