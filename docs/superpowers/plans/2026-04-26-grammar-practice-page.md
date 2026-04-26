# Grammar Practice Subpage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `exercises.html` to the Korean Grammar Cheat Sheet repo — a static practice page with ~195 click-to-reveal exercises across 22 grammar sections, deployed via the same GitHub Pages flow.

**Architecture:** Single-file static HTML, no build step. CSS lifted verbatim from `grammar-cheatsheet.html` plus a small new ruleset for exercise cards. Reveal uses native `<details>/<summary>` — no JavaScript for state. The two scripts that ship with the cheat sheet (progress thread + scroll-spy) are reused as-is. Section IDs (`s0`…`s23`) mirror the cheat sheet so anchors line up.

**Tech Stack:** HTML5, CSS3, vanilla JS for the progress/scroll-spy only. Google Fonts via single `<link>`. Playwright MCP for mobile audit.

---

## File map

| Path | Action | Responsibility |
|---|---|---|
| `exercises.html` | **create** | The new practice page. |
| `grammar-cheatsheet.html` | **modify** | Add three cross-links (hero sentence, callout near §21, footer link). |
| `index.html` | **unchanged** | Still redirects to cheat sheet. |
| `docs/superpowers/specs/2026-04-26-grammar-practice-page-design.md` | reference | The approved design spec. |

The reading-guide sister repo is **not** edited.

## Spec / topic source

The 22 sections to cover, their topics, and example sentences live in `grammar-cheatsheet.html`. **Read the relevant section before authoring its exercises** — vocabulary, particles, and example verbs should match what the cheat sheet has already taught. Do not introduce vocabulary the cheat sheet hasn't surfaced unless it's an obvious common word (학교, 책, 친구, 먹다, 가다, etc.).

## Vocabulary palette (use these by default)

To keep the practice page readable and consistent with the cheat sheet, prefer common high-frequency words across all exercises:

- Nouns: 학교, 집, 책, 물, 친구, 사람, 학생, 선생님, 가게, 영화, 커피, 밥, 한국어, 시간, 오늘, 내일, 어제
- Action verbs: 가다, 오다, 보다, 먹다, 마시다, 읽다, 쓰다, 자다, 듣다, 말하다, 사다, 만나다, 공부하다, 일하다
- Descriptive verbs: 좋다, 나쁘다, 크다, 작다, 예쁘다, 비싸다, 싸다, 맵다, 춥다, 덥다, 쉽다, 어렵다
- Particles: 은/는, 이/가, 을/를, 에, 에서, 와/과/하고, 의, 도, 만, 부터, 까지, 로/으로

If a section requires specific vocabulary (counters, irregulars, etc.), follow the cheat sheet's choices.

---

## Task 1: Scaffold `exercises.html` with lifted CSS and page chrome

**Files:**
- Create: `exercises.html`

- [ ] **Step 1: Read the cheat sheet's `<head>`, root CSS, body open, progress thread, and footer/scripts**

Open `grammar-cheatsheet.html` and read these line ranges (copy-paste targets):
- Lines 1–11: doctype, head meta, font `<link>`
- Lines 13–707: the entire `<style>` block (CSS variables, body, fonts, headings, callouts, tables, pre, etc., responsive rules)
- Line 711: progress thread div
- Lines 713–717, 745–746: `.layout` / `<aside>` / `<main>` wrapper structure
- Lines 1378–1381: footer
- Lines 1386–1427: progress + scroll-spy scripts

You are going to lift them all verbatim into `exercises.html`. Do not modify the existing CSS in this task.

- [ ] **Step 2: Create `exercises.html` with lifted chrome**

Create `exercises.html` as a complete, valid HTML document with:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Korean Grammar Practice · 연습</title>
<meta name="description" content="A practice companion to the Korean Grammar Cheat Sheet — drill particles, conjugation, connectors, and sentence patterns with click-to-reveal answers.">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..900,0..100,0..1;1,9..144,300..900,0..100,0..1&family=Newsreader:ital,opsz,wght@0,6..72,300..700;1,6..72,300..700&family=Gowun+Batang:wght@400;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
/* === BEGIN lifted from grammar-cheatsheet.html lines 13–707 === */
/* … paste the entire style block verbatim … */
/* === END lifted === */

/* === BEGIN exercises-only additions (filled in Task 2) === */
/* … */
/* === END exercises-only additions === */
</style>
</head>
<body>

<div class="progress" aria-hidden="true"><span></span></div>

<div class="layout">

<aside aria-label="Table of contents">
  <!-- TOC filled in Task 3 -->
</aside>

<main>

<header class="title">
  <!-- Hero filled in Task 3 -->
</header>

<!-- Exercise sections inserted in Tasks 4–8 -->

<footer>
  <!-- Footer filled in Task 3 -->
</footer>

</main>
</div>

<script>
  /* === BEGIN lifted from grammar-cheatsheet.html lines 1386–1427 === */
  /* progress thread + scroll-spy, paste verbatim */
  /* === END lifted === */
</script>

</body>
</html>
```

The literal lifted block markers are temporary — once you paste the real CSS and JS, remove the `BEGIN/END` comments. Leave only the marker pair around the exercises-only CSS region (Task 2 fills it).

- [ ] **Step 3: Verify the file parses and serves**

Run from the repo root:

```bash
python3 -m http.server 8765 --bind 127.0.0.1 &
sleep 1
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8765/exercises.html
kill %1
```

Expected: `200`. The page should render with paper background, vermillion progress thread, empty TOC, empty hero, empty body, and a footer placeholder. Open in a browser to eyeball.

- [ ] **Step 4: Commit**

```bash
git add exercises.html
git commit -m "scaffold exercises.html with lifted cheat-sheet chrome

Lift CSS, progress thread, scroll-spy, layout structure verbatim from
grammar-cheatsheet.html. Empty TOC/hero/sections/footer to be filled in
subsequent tasks.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: Add exercise-card CSS

**Files:**
- Modify: `exercises.html` (the `exercises-only additions` region in the `<style>` block)

- [ ] **Step 1: Insert exercise-card styles**

Replace the `BEGIN/END exercises-only additions` block with this CSS, exactly:

```css
  /* Exercise card */
  .ex {
    background: var(--paper-soft);
    border: 1px solid var(--rule-soft);
    border-left: 3px solid var(--vermillion);
    border-radius: 2px;
    padding: 14px 18px 16px;
    margin: 18px 0;
    box-shadow: var(--shadow-soft);
  }

  .ex-head {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 8px;
  }

  .ex-num {
    font-family: 'JetBrains Mono', ui-monospace, Menlo, monospace;
    font-size: 0.78em;
    color: var(--ink-faint);
    letter-spacing: 0.02em;
  }

  .ex-type {
    font-family: 'IBM Plex Sans', system-ui, sans-serif;
    font-size: 0.68em;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--celadon);
  }

  .ex-prompt {
    font-family: 'Newsreader', 'Iowan Old Style', Charter, Georgia, serif;
    font-size: 1.0em;
    line-height: 1.55;
    color: var(--ink);
  }

  .ex-prompt .en {
    display: block;
    font-style: italic;
    color: var(--ink-faint);
    font-size: 0.92em;
    margin-top: 2px;
  }

  .ex-prompt ul.ex-choices {
    margin: 8px 0 4px;
    padding-left: 1.2em;
    list-style: none;
  }
  .ex-prompt ul.ex-choices li {
    padding: 1px 0;
    font-family: 'Gowun Batang', 'Newsreader', serif;
  }
  .ex-prompt ul.ex-choices li::before {
    content: "○ ";
    color: var(--ink-faint);
    margin-right: 4px;
  }

  details.ex-answer {
    margin-top: 10px;
  }
  details.ex-answer summary {
    display: inline-block;
    cursor: pointer;
    background: var(--vermillion);
    color: var(--paper);
    font-family: 'Gowun Batang', 'Newsreader', serif;
    font-size: 0.86em;
    padding: 3px 10px 4px;
    border-radius: 2px;
    box-shadow: var(--shadow-stamp);
    user-select: none;
    list-style: none;
    transition: background-color 120ms ease;
  }
  details.ex-answer summary::-webkit-details-marker { display: none; }
  details.ex-answer summary:hover { background: var(--vermillion-deep); }
  details.ex-answer[open] summary {
    background: var(--vermillion-deep);
    opacity: 0.85;
  }

  .ex-solution {
    margin-top: 10px;
    padding: 10px 14px;
    background: var(--paper);
    border-left: 2px solid var(--vermillion);
    font-family: 'Newsreader', serif;
    line-height: 1.6;
  }
  .ex-solution .ko { font-family: 'Gowun Batang', 'Newsreader', serif; }
  .ex-solution .en {
    font-style: italic;
    color: var(--ink-soft);
  }

  /* Section lede points back at the cheat sheet */
  .section-lede {
    color: var(--ink-soft);
    font-style: italic;
    margin: 4px 0 18px;
  }
  .section-lede a {
    color: var(--vermillion);
    text-decoration: none;
    border-bottom: 1px solid var(--rule);
  }
  .section-lede a:hover { border-bottom-color: var(--vermillion); }

  /* Mobile */
  @media (max-width: 880px) {
    .ex { padding: 12px 14px 14px; margin: 14px 0; }
    .ex-head { gap: 10px; }
    details.ex-answer summary { padding: 4px 12px 5px; }
  }
  @media (max-width: 480px) {
    .ex { padding: 10px 12px 12px; }
    .ex-prompt { font-size: 0.96em; }
  }

  /* Print: de-style the 답 tab; the JS in Task 3 force-opens all <details> on beforeprint */
  @media print {
    details.ex-answer summary,
    details.ex-answer[open] summary {
      background: transparent;
      color: var(--ink);
      box-shadow: none;
      padding: 0;
    }
    details.ex-answer summary::after { content: " (answer):"; color: var(--ink-faint); }
  }
```

Forcing `<details>` open in print is done in JavaScript (Task 3 Step 4), since the open state is a DOM property and not reliably toggled by CSS alone.

- [ ] **Step 2: Verify CSS parses and applies**

Reload `http://127.0.0.1:8765/exercises.html`. The page should still render (no broken styles). Run a quick HTML/CSS sanity check:

```bash
python3 -c "
import re, sys
html = open('exercises.html').read()
# Brace balance in style block
style = re.search(r'<style>(.*?)</style>', html, re.S).group(1)
opens = style.count('{'); closes = style.count('}')
print(f'braces: {opens} open / {closes} close')
sys.exit(0 if opens == closes else 1)
"
```

Expected: matched braces, exit 0.

- [ ] **Step 3: Commit**

```bash
git add exercises.html
git commit -m "add exercise-card CSS to exercises.html

Cards, type label, vermillion 답 reveal tab, solution panel, mobile
breakpoints, print stylesheet.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: Hero, TOC, footer, scroll-spy aside, print-open script

**Files:**
- Modify: `exercises.html`

- [ ] **Step 1: Replace the `<aside>` TOC with the practice TOC**

Inside `<aside aria-label="Table of contents">`, replace the empty placeholder with:

```html
  <div class="toc-label">Practice</div>
  <div class="toc-rule"></div>
  <ol>
    <li><a href="#s0">Foundations · <span class="ko">기초</span></a></li>
    <li><a href="#s1">Word Order — SOV</a></li>
    <li><a href="#s2">Particles <span class="ko">조사</span></a></li>
    <li><a href="#s3">Copula <span class="ko">이다 / 아니다</span></a></li>
    <li><a href="#s4">Verb / Adjective Stems</a></li>
    <li><a href="#s5">Speech Levels</a></li>
    <li><a href="#s6">Present Tense</a></li>
    <li><a href="#s7">Past Tense</a></li>
    <li><a href="#s8">Future / Probability</a></li>
    <li><a href="#s9">Negation</a></li>
    <li><a href="#s10">Honorifics</a></li>
    <li><a href="#s11">Connectors</a></li>
    <li><a href="#s12">Modifiers</a></li>
    <li><a href="#s13">Nominalization</a></li>
    <li><a href="#s14">Sentence-Final Patterns</a></li>
    <li><a href="#s15">Quoting &amp; Reported Speech</a></li>
    <li><a href="#s16">Numbers &amp; Counters</a></li>
    <li><a href="#s18">Question Words</a></li>
    <li><a href="#s19">Causative &amp; Passive</a></li>
    <li><a href="#s20">Irregular Verb Stems</a></li>
    <li><a href="#s21">Build a Sentence</a></li>
    <li><a href="#s23">Identify Endings</a></li>
  </ol>
```

§17, §22, §24 are intentionally omitted — they don't drill.

- [ ] **Step 2: Replace the `<header class="title">` with the hero**

```html
  <div class="eyebrow-row">
    <span class="dot"></span>
    <span>Practice · 한국어 · 22 Sections</span>
    <span class="rule"></span>
  </div>
  <h1>
    <span class="display-row">Korean Grammar</span>
    <span class="display-row muted">Practice,</span>
    <span class="display-row"><span class="ko-title">연습</span></span>
  </h1>
  <p class="lede">A click-to-reveal drill set built on the <a href="grammar-cheatsheet.html">Korean Grammar Cheat Sheet</a>. Read a prompt, work it out, then tap <span class="ko">답</span> to check. Can't read Hangul yet? Start with the <a href="https://mikersays.github.io/hangeul-reading-guide/">Hangul Reading Guide</a>.</p>
```

- [ ] **Step 3: Replace the `<footer>` with the practice footer**

```html
  <span><span class="seal">韓</span> &nbsp; Korean Grammar Practice · companion to the <a href="grammar-cheatsheet.html">Cheat Sheet</a> · prerequisite: <a href="https://mikersays.github.io/hangeul-reading-guide/">Hangul Reading Guide</a></span>
  <span>한국어 연습</span>
```

- [ ] **Step 4: Add print-open script to the existing `<script>` block**

After the scroll-spy IIFE (still inside the same `<script>` element), append:

```js
  // Print: force every <details> open so the page is a usable worksheet
  (function() {
    if (!window.matchMedia) return;
    const mql = window.matchMedia('print');
    const setAll = (open) => {
      document.querySelectorAll('details.ex-answer').forEach(d => { d.open = open; });
    };
    let restoreState = null;
    window.addEventListener('beforeprint', () => {
      restoreState = Array.from(document.querySelectorAll('details.ex-answer')).map(d => d.open);
      setAll(true);
    });
    window.addEventListener('afterprint', () => {
      if (!restoreState) return;
      document.querySelectorAll('details.ex-answer').forEach((d, i) => { d.open = !!restoreState[i]; });
      restoreState = null;
    });
  })();
```

- [ ] **Step 5: Verify TOC, hero, and footer render**

Reload `http://127.0.0.1:8765/exercises.html`. Confirm:
- Sidebar lists 22 entries.
- Hero shows "Korean Grammar Practice, 연습" with the bilingual link line.
- Footer shows the seal and the two cross-links.

- [ ] **Step 6: Commit**

```bash
git add exercises.html
git commit -m "add hero, TOC, footer, print-open script to exercises.html

22-entry TOC mirrors cheat-sheet section IDs (s0..s23, omitting 17/22/24).
Hero links back to cheat sheet and reading guide. Print handler force-opens
all <details> for worksheet mode.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: Author content for §00–§05

**Files:**
- Modify: `exercises.html` (insert sections inside `<main>`, after `<header class="title">` and before `<footer>`)

**Counts (must hit):** s0=4, s1=6, s2=15, s3=6, s4=6, s5=6 → **43 exercises**

- [ ] **Step 1: Read the corresponding cheat-sheet sections for vocabulary alignment**

Read `grammar-cheatsheet.html` lines 764–946 — that's §00 Foundations through §05 Speech Levels. Your prompts should reuse the example verbs and patterns the cheat sheet has already taught.

- [ ] **Step 2: Add the §00 Foundations section**

Insert after `<header class="title">`:

```html
<!-- 0 -->
<section id="s0">
  <h2><span class="num">00</span> Foundations · <span class="ko">기초</span></h2>
  <p class="section-lede">Cushion vowels and 받침 — does the syllable end in a consonant? → <a href="grammar-cheatsheet.html#s0">read the rule</a>.</p>

  <div class="ex" id="ex-0-1">
    <div class="ex-head"><span class="ex-num">0.1</span><span class="ex-type">identify</span></div>
    <div class="ex-prompt">Does <span class="ko">학교</span> end in a 받침?</div>
    <details class="ex-answer"><summary aria-label="Reveal answer">답</summary>
      <div class="ex-solution">No — <span class="ko">교</span> ends in a vowel (<span class="ko">ㅛ</span>). The block has no final consonant.</div>
    </details>
  </div>

  <div class="ex" id="ex-0-2">
    <div class="ex-head"><span class="ex-num">0.2</span><span class="ex-type">identify</span></div>
    <div class="ex-prompt">Does <span class="ko">책</span> end in a 받침?</div>
    <details class="ex-answer"><summary aria-label="Reveal answer">답</summary>
      <div class="ex-solution">Yes — <span class="ko">ㄱ</span> is the 받침 of <span class="ko">책</span>.</div>
    </details>
  </div>

  <div class="ex" id="ex-0-3">
    <div class="ex-head"><span class="ex-num">0.3</span><span class="ex-type">choose</span></div>
    <div class="ex-prompt">Pick the correct cushion-vowel form: <span class="ko">먹 + (으)면</span> →
      <ul class="ex-choices"><li>먹면</li><li>먹으면</li><li>머그면</li></ul>
    </div>
    <details class="ex-answer"><summary aria-label="Reveal answer">답</summary>
      <div class="ex-solution"><span class="ko">먹으면</span> — the stem ends in a consonant (받침 <span class="ko">ㄱ</span>), so insert <span class="ko">으</span>.</div>
    </details>
  </div>

  <div class="ex" id="ex-0-4">
    <div class="ex-head"><span class="ex-num">0.4</span><span class="ex-type">choose</span></div>
    <div class="ex-prompt">Pick the correct cushion-vowel form: <span class="ko">가 + (으)면</span> →
      <ul class="ex-choices"><li>가면</li><li>가으면</li></ul>
    </div>
    <details class="ex-answer"><summary aria-label="Reveal answer">답</summary>
      <div class="ex-solution"><span class="ko">가면</span> — the stem ends in a vowel, so the cushion <span class="ko">으</span> is dropped.</div>
    </details>
  </div>
</section>
```

**Important:** every `<summary>` in every exercise card across this whole page must include `aria-label="Reveal answer"` — the literal text "답" is opaque to screen readers without it. Use this exact `<details><summary aria-label="Reveal answer">답</summary>…</details>` shape throughout Tasks 4–8.
```

- [ ] **Step 3: Add the §01 Word Order section**

Topics to cover (one exercise each; pick 6 of these):
1. Reorder English subject/object/verb into Korean SOV.
2. Identify the verb position in a Korean sentence.
3. Spot the wrong-order sentence in a multiple-choice list.
4. Translate "I read a book" with correct SOV.
5. Translate "The student studies Korean" with correct SOV.
6. Identify which word in a Korean sentence carries the action.

Use the same `<div class="ex">` template as Step 2. IDs: `ex-1-1` through `ex-1-6`. `ex-num` `1.1`–`1.6`. Mix `transform`, `write`, `read`, `identify` types.

Full template for one exercise (replicate, varying content):

```html
  <div class="ex" id="ex-1-1">
    <div class="ex-head"><span class="ex-num">1.1</span><span class="ex-type">write</span></div>
    <div class="ex-prompt">Translate to Korean (SOV order): "I eat a book" — <em>(silly on purpose; just check word order)</em>
      <span class="en">Use 저는, 책을, 먹어요.</span>
    </div>
    <details class="ex-answer"><summary aria-label="Reveal answer">답</summary>
      <div class="ex-solution"><span class="ko">저는 책을 먹어요.</span> — Subject + Object + Verb. Verb always last.</div>
    </details>
  </div>
```

Wrap the section in `<section id="s1"><h2><span class="num">01</span> Word Order — SOV</h2><p class="section-lede">Subject — object — verb. Verb always last. → <a href="grammar-cheatsheet.html#s1">read the rule</a>.</p>…</section>`.

- [ ] **Step 4: Add the §02 Particles section (15 exercises)**

This is the biggest section. Cover all of these particles, mixing types:

| Particle | Cheat-sheet rule |
|---|---|
| 은/는 | topic, contrast |
| 이/가 | subject, new info |
| 을/를 | direct object |
| 에 | destination, time, location with stative verb |
| 에서 | location with action verb, source |
| 와/과/하고 | "and / with" |
| 의 | possessive |
| 도 | "also, too" |
| 만 | "only" |
| 부터 | "from" (time/sequence) |
| 까지 | "until / up to" |
| 로/으로 | direction, means |

Suggested distribution (15 cards):
- 5 × `particle` fill-in-the-blank
- 4 × `choose` multiple-choice between two particles
- 3 × `read` (read Korean and explain which particle is doing what)
- 2 × `write` (compose Korean from English with the right particle)
- 1 × `identify` (this sentence is wrong — what's the particle error?)

Section wrapper:
```html
<section id="s2">
  <h2><span class="num">02</span> Particles <span class="ko">조사</span></h2>
  <p class="section-lede">Tiny suffixes that mark each noun's job in the sentence. → <a href="grammar-cheatsheet.html#s2">read the rule</a>.</p>
  <!-- 15 .ex cards, ex-2-1 through ex-2-15 -->
</section>
```

Concrete example cards (use these verbatim as the first three; you author the remaining 12):

```html
  <div class="ex" id="ex-2-1">
    <div class="ex-head"><span class="ex-num">2.1</span><span class="ex-type">particle</span></div>
    <div class="ex-prompt">Fill in the blank: <span class="ko">저___ 학생이에요.</span>
      <span class="en">(I'm a student.)</span>
    </div>
    <details class="ex-answer"><summary aria-label="Reveal answer">답</summary>
      <div class="ex-solution"><span class="ko">는</span> — topic particle. <span class="ko">저</span> ends in a vowel, so 는 not 은.</div>
    </details>
  </div>

  <div class="ex" id="ex-2-2">
    <div class="ex-head"><span class="ex-num">2.2</span><span class="ex-type">choose</span></div>
    <div class="ex-prompt">Which particle? <span class="ko">학교___ 가요.</span>
      <ul class="ex-choices"><li>에</li><li>에서</li></ul>
      <span class="en">(I'm going to school.)</span>
    </div>
    <details class="ex-answer"><summary aria-label="Reveal answer">답</summary>
      <div class="ex-solution"><span class="ko">에</span> — destination with a motion verb. <span class="ko">에서</span> would mark the location <em>where</em> something happens, not the destination.</div>
    </details>
  </div>

  <div class="ex" id="ex-2-3">
    <div class="ex-head"><span class="ex-num">2.3</span><span class="ex-type">particle</span></div>
    <div class="ex-prompt">Fill in the blank: <span class="ko">친구___ 만나요.</span>
      <span class="en">(I'm meeting a friend.)</span>
    </div>
    <details class="ex-answer"><summary aria-label="Reveal answer">답</summary>
      <div class="ex-solution"><span class="ko">를</span> — direct object. <span class="ko">친구</span> ends in a vowel, so 를 not 을.</div>
    </details>
  </div>
```

For the remaining cards, reuse the structure exactly. Solutions must always state *which rule was applied* in one sentence.

- [ ] **Step 5: Add §03 Copula (6), §04 Stems (6), §05 Speech Levels (6)**

Each follows the same pattern: `<section id="sN">` + `<h2>` + `<p class="section-lede">` (linking to `#sN` in the cheat sheet) + 6 `<div class="ex">` cards numbered `N.1`…`N.6`.

§03 Copula topics: 이에요/예요 vs 입니다/입니다, choosing the cushion 이, 이/가 아니에요 negation form.
§04 Stems topics: drop 다 to find the stem, distinguish action vs descriptive verbs from a list, identify if a verb is consonant-final or vowel-final.
§05 Speech Levels topics: convert one sentence between 해요체 / 합니다체 / 해체 (반말); identify the level of a given sentence; pick the right level for a given context (talking to a stranger, writing an email, talking to a close friend).

- [ ] **Step 6: Verify and count**

```bash
grep -c 'class="ex"' exercises.html
```

Expected: 43 (after this task).

```bash
python3 -c "
import re
html = open('exercises.html').read()
# All .ex IDs should be unique and follow ex-N-M pattern
ids = re.findall(r'id=\"(ex-\d+-\d+)\"', html)
assert len(ids) == len(set(ids)), 'duplicate IDs'
print(f'unique exercise IDs: {len(ids)}')
# Section IDs present
for sid in ['s0','s1','s2','s3','s4','s5']:
    assert f'id=\"{sid}\"' in html, f'missing section {sid}'
print('sections s0..s5 present')
"
```

Expected: 43 unique IDs, all six sections present.

- [ ] **Step 7: Visual smoke check**

Reload `http://127.0.0.1:8765/exercises.html`. Click a `답` tab in each of the six sections — answer reveals; click again — answer collapses. No console errors.

- [ ] **Step 8: Commit**

```bash
git add exercises.html
git commit -m "author exercises §00–§05 (foundations through speech levels)

43 click-to-reveal exercises across six sections, mixing particle,
conjugate, transform, read, write, identify, choose types.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: Author content for §06–§10

**Files:**
- Modify: `exercises.html`

**Counts (must hit):** s6=12, s7=10, s8=8, s9=8, s10=8 → **46 exercises**

- [ ] **Step 1: Read cheat-sheet §06–§10 first**

`grammar-cheatsheet.html` lines 947–1027.

- [ ] **Step 2: Add §06 Present Tense (12)**

Topics, distribute roughly evenly:
- Conjugate 가다, 보다, 먹다, 마시다, 자다, 사다, 읽다, 입다 into 해요-form (use `conjugate` type)
- Spot the right vs wrong vowel-harmony choice (아요 vs 어요)
- 하다 contraction → 해요 (give two examples: 공부하다, 일하다)
- 이다 → 이에요/예요 (covered separately if not in §03)

Wrapper:
```html
<section id="s6">
  <h2><span class="num">06</span> Present Tense — <span class="ko">아/어/해요</span></h2>
  <p class="section-lede">Stem + 아/어요, with vowel harmony and contraction. → <a href="grammar-cheatsheet.html#s6">read the rule</a>.</p>
  <!-- 12 cards: ex-6-1 .. ex-6-12 -->
</section>
```

Concrete example (replicate this shape; vary verb and harmony rule):

```html
  <div class="ex" id="ex-6-1">
    <div class="ex-head"><span class="ex-num">6.1</span><span class="ex-type">conjugate</span></div>
    <div class="ex-prompt">Conjugate <span class="ko">먹다</span> in 해요-form, present tense.</div>
    <details class="ex-answer"><summary aria-label="Reveal answer">답</summary>
      <div class="ex-solution"><span class="ko">먹어요</span> — stem <span class="ko">먹</span> has a dark vowel (<span class="ko">ㅓ</span>), so it takes <span class="ko">어요</span>.</div>
    </details>
  </div>
```

- [ ] **Step 3: Add §07 Past Tense (10)**

Topics: 았/었/했어요 conjugation; transform present → past; spot whether a stem takes 았 or 었; convert 하다 verbs to 했어요. Mix `conjugate` and `transform`.

- [ ] **Step 4: Add §08 Future / Probability (8)**

Topics: ~(으)ㄹ 거예요 (future); ~겠어요 (intent / supposition); difference between the two. Use `conjugate` and `read`.

- [ ] **Step 5: Add §09 Negation (8)**

Topics: 안 vs 못; placement of 안 with 하다 verbs (안 공부해요 vs 공부 안 해요); ~지 않다 long-form; 못 capability negation. Mix `transform` and `choose`.

- [ ] **Step 6: Add §10 Honorifics (8)**

Topics: ~(으)시~ insertion; honorific past (~(으)셨어요); special honorific verbs (계시다, 잡수시다, 주무시다); when honorifics apply (subject is socially elevated). Mix `transform`, `identify`, `read`.

- [ ] **Step 7: Verify count**

```bash
grep -c 'class="ex"' exercises.html
```

Expected: 89 cumulative (43 + 46).

- [ ] **Step 8: Commit**

```bash
git add exercises.html
git commit -m "author exercises §06–§10 (tense, future, negation, honorifics)

46 exercises covering present/past conjugation, future and probability,
안/못 negation placement, and honorific insertion.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: Author content for §11–§15

**Files:**
- Modify: `exercises.html`

**Counts (must hit):** s11=10, s12=10, s13=8, s14=12, s15=8 → **48 exercises**

- [ ] **Step 1: Read cheat-sheet §11–§15**

`grammar-cheatsheet.html` lines 1028–1182.

- [ ] **Step 2: Add §11 Connectors (10)**

Topics: ~고 (sequence/listing), ~서/아서/어서 (cause + sequence), ~지만 (but), ~(으)면 (if), ~(으)니까 (because/since), ~는데 (background/contrast), ~(으)러 (in order to). Mix `transform`, `choose`, `identify`.

Wrapper template:
```html
<section id="s11">
  <h2><span class="num">11</span> Connectors (clause linking)</h2>
  <p class="section-lede">Clause-joining endings: 고, 서, 지만, (으)면, (으)니까, 는데, (으)러. → <a href="grammar-cheatsheet.html#s11">read the rule</a>.</p>
  <!-- 10 cards -->
</section>
```

- [ ] **Step 3: Add §12 Modifiers (10)**

Topics: action verb past (~(으)ㄴ 책 = "the book I read"), action verb present (~는 책 = "the book I'm reading"), action verb future (~(으)ㄹ 책 = "the book I will read"), descriptive verb (~(으)ㄴ 예쁜 꽃). Mix `transform` and `choose`.

- [ ] **Step 4: Add §13 Nominalization (8)**

Topics: ~기 vs ~(으)ㅁ (gerund noun); ~는 것 (the act of); when each is preferred. Mix `transform`, `read`, `identify`.

- [ ] **Step 5: Add §14 Sentence-Final Patterns (12)**

This section has many small patterns. Cover at least: ~네요 (notice/realize), ~지요/죠 (confirm), ~군요 (oh-I-see), ~잖아요 (you-know-this), ~(으)ㄴ/는 것 같다 (seems like), ~(으)ㄹ까요? (shall we / I wonder), ~(으)ㄹ게요 (I'll do), ~(으)세요 (polite imperative), ~(으)ㄹ래요? (do you want to), ~아/어 보다 (try doing). Use mostly `identify` and `read`.

- [ ] **Step 6: Add §15 Quoting (8)**

Topics: direct quote (~라고/이라고 했어요), indirect statement (~다고 했어요), indirect question (~냐고 했어요), indirect command (~(으)라고 했어요), indirect proposal (~자고 했어요). Mix `transform` and `read`.

- [ ] **Step 7: Verify count and commit**

```bash
grep -c 'class="ex"' exercises.html
```

Expected: 137 cumulative (43 + 46 + 48).

```bash
git add exercises.html
git commit -m "author exercises §11–§15 (connectors, modifiers, nominalization, finals, quoting)

48 exercises covering clause-joining endings, noun modifier endings,
nominalization choices, common sentence-final patterns, and the four
indirect quote forms.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: Author content for §16, §18, §19

**Files:**
- Modify: `exercises.html`

**Counts (must hit):** s16=10, s18=8, s19=8 → **26 exercises**

§17 Pronouns is intentionally skipped per the spec.

- [ ] **Step 1: Read cheat-sheet §16, §18, §19**

`grammar-cheatsheet.html` lines 1183–1283 (skip §17 lines 1225–1242).

- [ ] **Step 2: Add §16 Numbers & Counters (10)**

Topics:
- Sino-Korean (일, 이, 삼, …) for dates, money, phone numbers, minutes.
- Native Korean (하나, 둘, 셋, …) for ages (when paired with 살), hours (when paired with 시), counted objects (개, 명, 마리, 권).
- Counter agreement: 세 명 (3 people), 네 권 (4 books) — note the special forms 한, 두, 세, 네, 스무.
- Time: 세 시 삼십 분 (3:30) — hours native, minutes Sino.

Mix `choose` (which counter system?), `write` (translate the number+counter), `identify` (correct vs wrong counter pairing).

- [ ] **Step 3: Add §18 Question Words (8)**

Topics: 누구/누가, 무엇/뭐, 어디, 언제, 왜, 어떻게, 얼마, 몇. Each used in a complete question. Mix `write`, `read`, `transform` (statement → question with correct word).

- [ ] **Step 4: Add §19 Causative & Passive (8)**

Topics: causative ~게 하다 (make someone do); morphological passive (~이/히/리/기) on common verbs (보다 → 보이다, 닫다 → 닫히다, 듣다 → 들리다); ~아/어지다 ("become") with descriptive verbs; passive vs active voice swap. Mix `identify`, `transform`, `read`.

- [ ] **Step 5: Verify count and commit**

```bash
grep -c 'class="ex"' exercises.html
```

Expected: 163 cumulative.

```bash
git add exercises.html
git commit -m "author exercises §16, §18, §19 (numbers, questions, voice)

26 exercises covering Sino vs native counter choice, the eight question
words, and causative/passive voice transformations.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 8: Author content for §20, §21, §23

**Files:**
- Modify: `exercises.html`

**Counts (must hit):** s20=12, s21=8, s23=12 → **32 exercises**

- [ ] **Step 1: Read cheat-sheet §20, §21, §23**

`grammar-cheatsheet.html` lines 1284–1366 (skip §22 line 1315–1329).

- [ ] **Step 2: Add §20 Irregular Verb Stems (12)**

Cover each major family at least once:
- ㅂ irregular: 춥다 → 추워요, 쉽다 → 쉬워요, 무겁다 → 무거워요
- ㄷ irregular: 듣다 → 들어요, 걷다 → 걸어요, 묻다 → 물어요
- 르 irregular: 빠르다 → 빨라요, 모르다 → 몰라요, 부르다 → 불러요
- ㅡ irregular: 예쁘다 → 예뻐요, 크다 → 커요, 바쁘다 → 바빠요
- ㅅ irregular: 짓다 → 지어요, 낫다 → 나아요
- ㅎ irregular: 그렇다 → 그래요, 빨갛다 → 빨개요
- 르 vs 러 distinction (이르다 has both — context-dependent)

Heavy on `conjugate` type. One `identify` ("what irregularity is this?") at the end.

- [ ] **Step 3: Add §21 Build a Sentence (8)**

This section is the synthesis drill. Each card gives a target meaning + level + tense and asks the learner to assemble the sentence end-to-end.

Concrete first card to use verbatim:

```html
  <div class="ex" id="ex-21-1">
    <div class="ex-head"><span class="ex-num">21.1</span><span class="ex-type">build</span></div>
    <div class="ex-prompt">Build a sentence:
      <span class="en">"I'm going to school" — 해요체, present tense, with topic marker.</span>
    </div>
    <details class="ex-answer"><summary aria-label="Reveal answer">답</summary>
      <div class="ex-solution"><span class="ko">저는 학교에 가요.</span> — Subject + topic 는 + destination 에 + verb 가다 → 가요.</div>
    </details>
  </div>
```

The remaining 7 should escalate: add object, add past tense, add honorifics, add a connector, add a question word, add a sentence-final pattern. Use `build` type for all.

- [ ] **Step 4: Add §23 Identify Endings (12)**

Show a sentence ending and ask what it signals. Use `identify` type for all 12. Cover from the cheat sheet's "Top 30" list — include at least: ~네요, ~지요, ~군요, ~잖아요, ~거든요, ~(으)ㄴ/는데, ~(으)면서, ~(으)려고, ~(으)면 안 되다, ~아/어야 되다, ~(으)ㄹ 수 있다/없다, ~아/어 보다.

Concrete first card:

```html
  <div class="ex" id="ex-23-1">
    <div class="ex-head"><span class="ex-num">23.1</span><span class="ex-type">identify</span></div>
    <div class="ex-prompt">What does the ending signal? <span class="ko">비가 오네요.</span></div>
    <details class="ex-answer"><summary aria-label="Reveal answer">답</summary>
      <div class="ex-solution"><span class="ko">~네요</span> — speaker noticing/realizing something just now. "Oh, it's raining."</div>
    </details>
  </div>
```

- [ ] **Step 5: Verify the final count**

```bash
grep -c 'class="ex"' exercises.html
```

Expected: 195 cumulative. If it's not exactly 195, adjust the last few cards in §23 up or down to hit it.

```bash
python3 -c "
import re
html = open('exercises.html').read()
ids = re.findall(r'id=\"(ex-\d+-\d+)\"', html)
assert len(ids) == len(set(ids)), 'duplicate IDs found'
section_ids = ['s0','s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12','s13','s14','s15','s16','s18','s19','s20','s21','s23']
for sid in section_ids:
    assert f'id=\"{sid}\"' in html, f'missing section {sid}'
print(f'OK — {len(ids)} unique exercises across {len(section_ids)} sections')
"
```

Expected: `OK — 195 unique exercises across 22 sections`.

- [ ] **Step 6: Commit**

```bash
git add exercises.html
git commit -m "author exercises §20, §21, §23 (irregulars, build, identify endings)

32 exercises completing the practice page: irregular conjugation
families, build-a-sentence synthesis drills, and ending identification.
Total content now 195 exercises across 22 sections.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 9: Cross-link from `grammar-cheatsheet.html`

**Files:**
- Modify: `grammar-cheatsheet.html` (three places)

- [ ] **Step 1: Update the hero lede**

In `grammar-cheatsheet.html` line 760, find:

```html
<p class="lede">A structural reference for building Korean sentences — particles, conjugation, connectors, and the patterns that hold them together. Can't read Hangul yet? Start with the <a href="https://mikersays.github.io/hangeul-reading-guide/">Hangul Reading Guide</a> first.</p>
```

Replace with:

```html
<p class="lede">A structural reference for building Korean sentences — particles, conjugation, connectors, and the patterns that hold them together. Want to drill it? Try the <a href="exercises.html">Practice page</a>. Can't read Hangul yet? Start with the <a href="https://mikersays.github.io/hangeul-reading-guide/">Hangul Reading Guide</a> first.</p>
```

- [ ] **Step 2: Add a callout near §21 *Building a Sentence***

Locate `<section id="s21">` (around line 1303). Inside the section, after the existing content but before the closing `</section>`, append:

```html
  <div class="callout">
    <strong>Ready to drill?</strong> Try the <a href="exercises.html#s21">Build-a-Sentence exercises</a> on the Practice page — 8 progressive prompts that walk you through this recipe.
  </div>
```

If you don't immediately see where the section ends, search for the next `<section id="s22">` line; the callout goes immediately above it (still inside the §21 section).

- [ ] **Step 3: Update the footer**

Find:

```html
<footer>
  <span><span class="seal">韓</span> &nbsp; Korean Grammar Cheat Sheet · prerequisite: <a href="https://mikersays.github.io/hangeul-reading-guide/">Hangul Reading Guide</a></span>
  <span>한국어 문법</span>
</footer>
```

Replace with:

```html
<footer>
  <span><span class="seal">韓</span> &nbsp; Korean Grammar Cheat Sheet · drill it on the <a href="exercises.html">Practice page</a> · prerequisite: <a href="https://mikersays.github.io/hangeul-reading-guide/">Hangul Reading Guide</a></span>
  <span>한국어 문법</span>
</footer>
```

- [ ] **Step 4: Verify all three links resolve**

```bash
grep -n 'exercises.html' grammar-cheatsheet.html
```

Expected: three lines — one in the hero lede area (~line 760), one inside §21, one in the footer.

Reload `http://127.0.0.1:8765/grammar-cheatsheet.html`. Click each new "Practice" link — all three should navigate to `exercises.html` (the third also includes `#s21`).

- [ ] **Step 5: Commit**

```bash
git add grammar-cheatsheet.html
git commit -m "link cheat sheet to new exercises page in three places

Hero lede, callout near §21 build-a-sentence, and footer — same
three-place mirror-symmetric pattern used for the reading guide.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 10: Mobile audit via Playwright

**Files:**
- (none modified unless issues are found)

- [ ] **Step 1: Make sure the local server is running**

```bash
# If not already running:
python3 -m http.server 8765 --bind 127.0.0.1 &
sleep 1
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8765/exercises.html
```

Expected: `200`.

- [ ] **Step 2: Audit at 360×800 (phone)**

Use the Playwright MCP browser tool. Steps:

1. `browser_resize` → 360×800
2. `browser_navigate` → `http://127.0.0.1:8765/exercises.html`
3. `browser_snapshot`
4. Visually verify: no horizontal scrollbar; TOC links to `#s2`, `#s14`, `#s23` all scroll smoothly; tap a 답 in §2 — answer reveals, no overflow.
5. `browser_take_screenshot` → save as `playwright-screenshots/exercises-360.png`.

Specific things to check:
- `.ex` cards do not horizontally overflow.
- Korean inside `<span class="ko">` does not break mid-word (it should `keep-all`).
- Tap target on `summary` — at least 44px tall.
- TOC label, hero, footer all readable.

- [ ] **Step 3: Audit at 414×896 (larger phone)**

Repeat Step 2 at 414×896, screenshot to `playwright-screenshots/exercises-414.png`.

- [ ] **Step 4: Audit at 768×1024 (tablet)**

Repeat at 768×1024, screenshot to `playwright-screenshots/exercises-768.png`.

- [ ] **Step 5: Audit at 1280×800 (desktop)**

Repeat once for desktop layout sanity, screenshot to `playwright-screenshots/exercises-1280.png`. The two-column layout (TOC `<aside>` + `<main>`) should appear here. Confirm scroll-spy highlights the active TOC entry as you scroll.

- [ ] **Step 6: If any issue is found, fix it in `exercises.html`**

Common possibilities and fixes:
- **Horizontal overflow on a long English gloss inside `.en`:** add `overflow-wrap: anywhere` to `.ex-prompt .en` in the `≤480px` media query.
- **Korean breaking mid-word in `.ex-prompt`:** add `word-break: keep-all` to `.ex-prompt .ko` (note: `.ko` already has it, but it must cascade — verify in DevTools).
- **Choices list `ul.ex-choices` indenting too far on mobile:** reduce `padding-left` to `0.8em` inside `≤480px`.
- **Summary tap target too small on mobile:** ensure `padding: 4px 12px 5px` in the `≤880px` block (already there in Task 2 — confirm it stuck).

After any fix, re-run the relevant viewport audit and re-screenshot.

- [ ] **Step 7: Print preview check**

In the browser, open `exercises.html`, hit ⌘P (or Ctrl+P). All `<details>` should be open in the print preview. Cancel.

- [ ] **Step 8: Commit screenshots and any fixes**

```bash
git add exercises.html playwright-screenshots/exercises-*.png 2>/dev/null
# only commit if there are changes
git diff --cached --quiet || git commit -m "mobile audit: exercises.html at 360/414/768/1280

Playwright screenshots and any responsiveness fixes uncovered by the audit.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

Note: per `.gitignore`, `playwright-screenshots/` is gitignored, so the `git add` for those will silently fail — that's expected. Only HTML changes (if any) will be committed.

---

## Task 11: Final verification and push

**Files:**
- (none — release step)

- [ ] **Step 1: Confirm working tree is clean**

```bash
git status
```

Expected: `nothing to commit, working tree clean`.

- [ ] **Step 2: Confirm the spec→implementation link**

```bash
ls docs/superpowers/specs/2026-04-26-grammar-practice-page-design.md
ls docs/superpowers/plans/2026-04-26-grammar-practice-page.md
ls exercises.html
```

All three should exist.

- [ ] **Step 3: Run the final exercise count**

```bash
grep -c 'class="ex"' exercises.html
```

Expected: `195`.

- [ ] **Step 4: Confirm git log shows the expected commits**

```bash
git log --oneline -15
```

Expected (in some order, most recent first): the spec commit, scaffold commit, CSS commit, hero/TOC commit, five content commits (§00–05, §06–10, §11–15, §16/18/19, §20/21/23), cross-link commit, optional mobile-audit commit.

- [ ] **Step 5: Push to origin**

```bash
git push origin main
```

GitHub Pages will rebuild within ~30 seconds. Verify the deploy by visiting:

- `https://mikersays.github.io/korean-cheat-sheet/exercises.html`
- `https://mikersays.github.io/korean-cheat-sheet/grammar-cheatsheet.html` (verify the three new "Practice" links work)

- [ ] **Step 6: Stop the local dev server**

```bash
kill %1 2>/dev/null || true
```

---

## Acceptance criteria (final check)

Tick these off before declaring done:

- [ ] `exercises.html` exists at repo root and renders identically in style to `grammar-cheatsheet.html`.
- [ ] 195 exercises across 22 sections (s0, s1–s16, s18–s21, s23). §17, §22, §24 absent.
- [ ] Each exercise card has: numbered `.ex-num`, type label `.ex-type`, prompt `.ex-prompt`, and a `<details>` containing the answer.
- [ ] Reveal works without JavaScript (test with JS disabled).
- [ ] No romanization anywhere in `exercises.html`.
- [ ] `grammar-cheatsheet.html` has three new links to `exercises.html` (hero, callout near §21, footer).
- [ ] Mobile audit passed at 360/414/768.
- [ ] Print preview opens all answers.
- [ ] Page is live at `https://mikersays.github.io/korean-cheat-sheet/exercises.html`.

---

## Notes for the implementer

- **Don't dispatch parallel subagents writing into `exercises.html`.** CLAUDE.md is explicit about this. If you parallelize content authoring (Tasks 4–8), have each subagent write to `_content_partN.html` with `=== sN ===` markers, then a small integration step concatenates them in order into `exercises.html`. Clean up temp files after.
- **No romanization, ever.** If you catch yourself writing "anyeonghaseyo" anywhere, delete and rewrite with Korean only.
- **Reuse cheat-sheet vocabulary.** A learner reading both pages should not feel they hit a different vocabulary set.
- **Prefer 6 great exercises over 12 padded ones.** The counts above are targets; the spec says "~195," not "exactly 195." If a section feels stretched at 12, drop it to 10 and add 2 to a richer section. The verification grep should still land near 195.
