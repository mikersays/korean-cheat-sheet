# Numbers Flash Cards — Design

**Date:** 2026-04-28
**Scope:** Add comprehensive coverage of Korean numbers, counters, and number-usage patterns to `flashcards.html`.

## Goal

Make Numbers a first-class category in the flash-cards site. Cover both the raw vocabulary (numerals + counters) and the usage rules (which system, sound changes, common patterns).

## Current state

- Cheat sheet `grammar-cheatsheet.html:1184` has §16 "Numbers & Counters" — a concise reference page.
- Flash cards `flashcards.html` has 18 existing `s16` grammar cards covering system selection, attributive shifts, basic counters, time/dates/money.
- No top-level "Numbers" category in the vocab tab.

## Architecture

Approach A: numbers spans both decks.

**Vocab tab** — new `number` POS with 9 subcats. Numerals and counter vocabulary live here. Picked up by the existing primary POS dropdown and secondary subcat dropdown.

**Grammar tab** — expand the existing `s16` deck. Usage rules, sound changes, idioms.

This matches the existing tab philosophy (vocab = "what's the word", grammar = "how do I use it") and keeps numbers visible as a top-level filter.

## Taxonomy changes (`flashcards.html` JS)

Three dicts get extended. Existing entries unchanged.

```js
// posTitles — add one entry
number: { en: 'Number', ko: '수사' }

// subcatTitles — add 7 new keys (time and money already exist; reuse them)
sino:     { en: 'Sino-Korean', ko: '한자어 수' }
native:   { en: 'Native',      ko: '고유어 수' }
counters: { en: 'Counters',    ko: '단위' }
dates:    { en: 'Dates',       ko: '날짜' }
age:      { en: 'Age',         ko: '나이' }
ordinals: { en: 'Ordinals',    ko: '서수' }
math:     { en: 'Math',        ko: '계산' }

// posSubcats — add the new POS with its subcat order
number: ['sino', 'native', 'counters', 'time', 'dates', 'money', 'age', 'ordinals', 'math']
```

## Card targets

**Vocab — `number` POS, ~96 cards total:**

| Subcat     | Target | Coverage |
|------------|-------:|----------|
| `sino`     | 15 | 일–십, 백/천/만/억, 영/공, big-number reading, sound changes (십육→[심뉵], 십일→[시빌]) |
| `native`   | 15 | 하나–열, 11–19 compound forms, tens 스물–아흔, attributive shifts (한/두/세/네/스무), upper bound at 99 |
| `counters` | 25 | 개·명·분(honorific)·사람·마리·권·잔·병·장·대·살·시·시간·번·층·호·호선·인분·송이·켤레·그루·점 — each with what it counts and which system |
| `time`     | 10 | 시 (native) + 분 (sino) + 초, 오전/오후, 반/정각, 시간 duration, 몇 시 |
| `dates`    | 10 | 월 1–12 incl. 유월/시월 irregulars, 일, 요일, 년, 오늘/어제/내일 with calendar |
| `money`    | 5  | 원, 만/십만/백만, 얼마, price reading |
| `age`      | 5  | 살 vs 세 vs 연세, 몇 살이세요, 한국 나이 vs 만 나이 |
| `ordinals` | 6  | 첫째/둘째 (native), 제1/제2 (sino prefix), 첫 번째 vs 처음, 마지막 |
| `math`     | 5  | 더하기/빼기/곱하기/나누기, 분의 (fractions), 점 (decimal), 퍼센트 |

Phone numbers fold into `sino` (just sino with 공 = 0).

**Grammar — `s16` expansion, ~25 new cards on top of the existing 18:**

- Which-system drills (dates, money, floors, bus numbers, ages, hours, minutes, phone)
- Sound-change rules (십육 [심뉵], 십일 [시빌], 유월·시월 month irregulars)
- 몇 + counter pattern
- Big-number grouping (만/억 boundaries when reading aloud)
- 부터 / 까지 with numbers (range expressions)
- Approximate numbers (-쯤, -정도, 약)
- Half/quarter (반)
- Common pitfalls (마리 only for animals; 분 vs 명 vs 사람; 잔 vs 컵)

**Grand total: ~120 new cards.**

## Card schema and conventions

Per the existing `add-flashcards` skill — no deviations.

**Vocab card:**
```js
{ pos: "number", subcat: "<subcat>", front: "<task>", back: "<answer>" }
```

**Grammar card:**
```js
{ section: "s16", type: "<type>", front: "<task>", back: "<answer>" }
```

Front-text directives: `Translate to English:` · `Translate to Korean:` · `Distinguish:` · `Choose:` · `Conjugate:` · `Identify:` · `Recall:`.

Korean always wrapped in `<span class="ko">…</span>`. Sample sentences in the back wrapped in `<span class="ex">…</span>`. **No romanization** anywhere. For sound-change cards, show the surface pronunciation in Hangul-in-brackets (e.g. 십육 → [심뉵]) — that's the reading-guide convention; it is not romanization.

## Subagent split

5 parallel general-purpose agents, per the `add-flashcards` skill workflow:

| Agent | Deck    | Subcats / scope                                    | Target | Output                  |
|-------|---------|----------------------------------------------------|-------:|-------------------------|
| A     | vocab   | `sino` + `native`                                  | 30     | `/tmp/_vocab_chunk_A.js` |
| B     | vocab   | `counters`                                         | 25     | `/tmp/_vocab_chunk_B.js` |
| C     | vocab   | `time` + `dates`                                   | 20     | `/tmp/_vocab_chunk_C.js` |
| D     | vocab   | `money` + `age` + `ordinals` + `math`              | 21     | `/tmp/_vocab_chunk_D.js` |
| E     | grammar | `s16` expansion (usage rules, sound changes, etc.) | 25     | `/tmp/_fc_chunk_E.js`    |

Each agent runs in the background, writes a bare JS array literal, self-validates with `node --check`, and reports done.

## Validation, merge, smoke test

Per the `add-flashcards` skill:

1. `python3 .claude/skills/add-flashcards/scripts/validate_chunk.py <chunk>` for each
2. Three taxonomy edits applied to `flashcards.html` (posTitles, subcatTitles, posSubcats)
3. Append-merge: `merge_chunks.py vocab /tmp/_vocab_chunk_*.js` + `merge_chunks.py grammar /tmp/_fc_chunk_E.js`
4. Inline-JS check + HTTP 200 smoke test
5. If Playwright MCP available: load `/flashcards.html`, switch to vocab tab, pick `Number → Counters`, flip 5 cards, navigate
6. Clean up `/tmp/_*.js`

## Out of scope

- No changes to the cheat sheet §16 itself. The grammar deck cards complement the existing prose, they don't replace it.
- No changes to `exercises.html`. Exercises mirror cheat-sheet sections, and §16 already exists there if it has exercises; numbers vocabulary doesn't need its own exercise page.
- No new section IDs. `number` is a POS, not a cheat-sheet section.
- Cross-linking pattern unchanged (numbers isn't a sister-repo concern).

## Acceptance

- `flashcards.html` parses cleanly (Node `--check` on inline JS).
- Local server returns 200 for `/flashcards.html`.
- Vocab tab shows "Number" in the primary dropdown; selecting it shows 9 subcats in the secondary.
- `Number → Counters` filter shows ~25 counter cards; flip + nav works.
- Grammar tab `s16` filter shows ~43 cards (18 existing + 25 new).
- No romanization anywhere in card content.
