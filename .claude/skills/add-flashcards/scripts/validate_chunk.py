#!/usr/bin/env python3
"""Validate a single flash-card chunk file.

Checks:
  - Parses as JS (wrapped as `var x = ...;`)
  - Schema field present (type for grammar, pos for vocab)
  - All type/pos values in the allowed set
  - Span tags balanced
  - Fronts start with a directive verb (grammar deck only)
  - Sample-sentence wrappers are well-formed (warn-only)

Usage:
  validate_chunk.py <chunk_file>
"""
import sys, re, subprocess
from pathlib import Path
from collections import Counter

ALLOWED_TYPES = {"recall", "translate", "conjugate", "identify", "choose"}
ALLOWED_POS = {"noun", "verb", "adjective", "adverb", "pronoun", "interjection", "number"}
DIRECTIVES = ("Recall", "Translate", "Conjugate", "Identify", "Choose", "Apply", "Distinguish", "Arrange")


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def warn(msg):
    print(f"WARN: {msg}")


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_chunk.py <chunk_file>")
        sys.exit(2)
    path = Path(sys.argv[1])
    if not path.exists():
        fail(f"file not found: {path}")
    src = path.read_text()

    # 1. Parses
    import tempfile, os
    wrapped = f"var x = {src};"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as tf:
        tf.write(wrapped)
        tmp_js = tf.name
    try:
        r = subprocess.run(["node", "--check", tmp_js], capture_output=True, text=True)
    finally:
        os.unlink(tmp_js)
    if r.returncode != 0:
        fail(f"JS does not parse:\n{r.stderr}")

    # 2. Detect schema
    is_vocab = bool(re.search(r'\{\s*pos\s*:', src))
    is_grammar = bool(re.search(r'\{\s*section\s*:', src))
    if is_vocab and is_grammar:
        fail("chunk mixes grammar and vocab schemas")
    if not (is_vocab or is_grammar):
        fail("cannot detect schema (no `pos:` or `section:` keys)")

    # 3. Type/pos values
    if is_vocab:
        poses = re.findall(r'\{\s*pos:\s*"(\w+)"', src)
        bad = [p for p in poses if p not in ALLOWED_POS]
        print(f"vocab chunk: {len(poses)} cards")
        print(f"  POS distribution: {dict(Counter(poses))}")
        if bad:
            fail(f"invalid POS values: {bad[:5]}")
    else:
        types = re.findall(r'type:\s*"(\w+)"', src)
        sections = re.findall(r'\{\s*section:\s*"(s\d+)"', src)
        bad_t = [t for t in types if t not in ALLOWED_TYPES]
        print(f"grammar chunk: {len(sections)} cards")
        print(f"  type distribution: {dict(Counter(types))}")
        print(f"  sections: {sorted(set(sections), key=lambda s: int(s[1:]))}")
        if bad_t:
            fail(f"invalid type values: {bad_t[:5]}")
        if len(types) != len(sections):
            warn(f"type/section count mismatch: {len(types)} vs {len(sections)} (some cards missing `type`?)")

    # 4. Span balance
    opens = len(re.findall(r"<span[^>]*>", src))
    closes = src.count("</span>")
    print(f"  spans: {opens} open / {closes} close")
    if opens != closes:
        fail(f"span imbalance ({opens} vs {closes})")

    # 5. Directive front (grammar only)
    if is_grammar:
        # Match front: "..." values, accounting for escaped chars inside
        fronts = re.findall(r'front:\s*"((?:[^"\\]|\\.)*)"', src)
        bad_fronts = [f for f in fronts if not f.lstrip().startswith(DIRECTIVES)]
        print(f"  fronts with directive verb: {len(fronts) - len(bad_fronts)} / {len(fronts)}")
        for bf in bad_fronts[:3]:
            print(f"    bad: {bf[:80]}")
        if bad_fronts:
            fail(f"{len(bad_fronts)} fronts missing directive verb")

    # 6. Sample-sentence wrappers (warn-only)
    backs = re.findall(r'back:\s*"((?:[^"\\]|\\.)*)"', src)
    unwrapped_examples = 0
    for b in backs:
        # Find <ko>SENTENCE.</ko> (gloss) NOT inside a class="ex" wrapper
        ex_pattern = re.compile(r'<span class=\\"ko\\">[^<]*[.?!]</span>\s*\([^)]+\)')
        for m in ex_pattern.finditer(b):
            # Check 30 chars before the match for class=\"ex\"
            ctx = b[max(0, m.start() - 40):m.start()]
            if r'class=\"ex\"' not in ctx:
                unwrapped_examples += 1
    if unwrapped_examples:
        warn(f"{unwrapped_examples} sample sentences not wrapped in <span class=\"ex\">…</span>")

    print("ALL OK")


if __name__ == "__main__":
    main()
