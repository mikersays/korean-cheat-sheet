---
name: add-flashcards
description: Add more flash cards to flashcards.html (either the grammarCards or vocabCards array) using multiple parallel subagents to bulk-generate cards in chunks, then merging them with a helper script. Use when the user asks to "add more flashcards", "add cards for X", "expand the [grammar|vocab] deck", or similar.
---

# Add flash cards

Bulk-adds cards to one of the two decks in `flashcards.html` using parallel subagents.

## When to use

- `grammarCards` array (Grammar tab) — keyed by `section: "sN"` from the grammar cheat sheet
- `vocabCards` array (Vocabulary tab) — keyed by `pos: "noun|verb|adjective|adverb|pronoun|interjection"`

Use 3–6 parallel subagents when adding more than ~30 cards or when coverage spans multiple categories. For ≤30 cards in a single category, just write them inline.

## Process

### 1. Clarify scope

Ask the user briefly (if not specified):
- Which deck? (grammar / vocab)
- What scope? (e.g. "more verbs for cooking", "cards on s11 connectors", "TOPIK II body-part nouns")
- Approximate target count?

Then propose a chunk plan (e.g. "3 agents, ~50 cards each, split by subcategory") and confirm.

### 2. Dispatch parallel subagents

Use the Agent tool with `subagent_type: "general-purpose"` and `run_in_background: true` so you can continue other work while they run.

Each agent prompt MUST include:
- The card schema (see "Card schemas" below)
- Front-text convention (front starts with a directive verb)
- Back format (explanation + sample sentence wrapped in `<span class="ex">…</span>`)
- Korean-wrapping rule (always `<span class="ko">…</span>`, **never** romanize)
- Specific subcategory + target count for that agent
- Output path: `/tmp/_fc_chunk_<LETTER>.js` (grammar) or `/tmp/_vocab_chunk_<LETTER>.js` (vocab)
- File format: a bare JS array literal — opens with `[`, closes with `]`, no preamble, no `const x =`, no trailing comments
- Self-validation: confirm the file parses with `node --check` (wrapped as `var x = ...;`) before reporting done

Each agent owns its own chunk file. Don't have two agents write to the same path.

### 3. Wait for completion notifications

You'll be notified when each background agent finishes. **Don't poll.** Continue with other work in the meantime.

### 4. Validate each chunk

```bash
python3 .claude/skills/add-flashcards/scripts/validate_chunk.py /tmp/_fc_chunk_A.js
```

The validator checks:
- JS parses
- Schema field present (`type` for grammar, `pos` for vocab)
- All `type`/`pos` values in the allowed set
- Span tags balanced
- Fronts start with an allowed directive verb (grammar only)

If a chunk fails, send the agent (via `SendMessage` with the agentId from launch) a fix-up request describing the failure. Don't blindly retry.

### 5. Merge into flashcards.html

Default behavior is **append** — preserves existing cards.

```bash
# Append new chunks to the existing deck
python3 .claude/skills/add-flashcards/scripts/merge_chunks.py grammar /tmp/_fc_chunk_*.js
# or
python3 .claude/skills/add-flashcards/scripts/merge_chunks.py vocab /tmp/_vocab_chunk_*.js
```

For a destructive rebuild (rare):
```bash
python3 .claude/skills/add-flashcards/scripts/merge_chunks.py --replace grammar /tmp/_fc_chunk_*.js
```

The script:
- Reads each chunk
- (Append mode) reads the existing array from flashcards.html and prepends it
- Concatenates into a single array literal
- Validates JS parses
- Replaces the `const grammarCards = [...]` or `const vocabCards = [...]` block in flashcards.html

### 6. Smoke test

```bash
python3 -m http.server 8765 --bind 127.0.0.1 &
sleep 1
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8765/flashcards.html  # expect 200
pkill -f "http.server 8765"
```

Inline JS check:
```bash
python3 -c "
import re, subprocess
src = open('flashcards.html').read()
js = re.search(r'<script>(.*?)</script>', src, re.DOTALL).group(1)
open('/tmp/_check.js','w').write(js)
print(subprocess.run(['node','--check','/tmp/_check.js'], capture_output=True, text=True).returncode)
" && rm /tmp/_check.js
```

If you have a Playwright MCP available, click through 5 cards (flip + arrow nav) before declaring done. Without it, say so.

### 7. Clean up

```bash
rm -f /tmp/_fc_chunk_*.js /tmp/_vocab_chunk_*.js /tmp/_merged_*.js /tmp/_check.js
```

### 8. Don't ship without asking

## Card schemas

### Grammar card

```js
{ section: "sN", type: "<type>", front: "<task>", back: "<answer>" }
```

- `section`: `s0`–`s24`, matches grammar-cheatsheet.html section IDs
- `type`: one of `recall`, `translate`, `conjugate`, `identify`, `choose`
- `front`: starts with the directive verb that matches the type
- `back`: explanation + sample sentence wrapped in `<span class="ex">…</span>`

### Vocab card

```js
{ pos: "<pos>", front: "<task>", back: "<answer>" }
```

- `pos`: one of `noun`, `verb`, `adjective`, `adverb`, `pronoun`, `interjection`
- `front`: typically `"Translate to English: <span class=\"ko\">…</span>"` or `"Translate to Korean: \"…\""`. Some cards use `"Distinguish: …"`, `"Conjugate: …"`, or `"Choose: …"`.
- `back`: translation + sample sentence wrapped in `<span class="ex">…</span>`. For verbs/adjectives, include the polite-present form and any irregular flag (e.g., "ㅂ-irregular") in the back.

## Front-text convention

Every front MUST start with one of these directive verbs:
- `Recall: …` — remember a rule
- `Translate to English: …` / `Translate to Korean: "…"` — produce in the other language
- `Conjugate: …` — apply an ending
- `Identify: …` — name a feature in the given Korean
- `Choose: …` — pick the correct option from alternatives

This is what makes cards self-explanatory. Without the directive, the front is just a label.

## Sample-sentence wrapping

Every example sentence (the kind that should render on a new line in italics) MUST be wrapped:
```
<span class="ex"><span class="ko">SENTENCE.</span> (English gloss.)</span>
```

The `.ex` CSS rule turns this into a block element with italic styling. Skip the wrapper and the example flows inline with the surrounding text — looks bad.

The Korean inside `.ex` will be browser-synth-slanted (Gowun Batang has no real italic). That's intentional and accepted.

## Anti-patterns

- Two agents writing to the same chunk path — content gets overwritten
- Romanizing Korean anywhere
- Adding a new POS or grammar section without updating `posTitles` / `sectionTitles` and the rendering JS in flashcards.html
- Adding cards directly to flashcards.html when scope is large — use the chunk + merge flow so changes are reviewable
- Forgetting the `.ex` wrapper on new example sentences

## Helper scripts

- `scripts/validate_chunk.py <chunk_file>` — validates one chunk file
- `scripts/merge_chunks.py [--replace] {grammar|vocab} <chunk_glob_or_files...>` — appends (or replaces) chunks into flashcards.html
