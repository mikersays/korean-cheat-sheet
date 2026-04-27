#!/usr/bin/env python3
"""Merge flash-card chunk files into the target array in flashcards.html.

Default behavior is **append** — the existing deck is preserved and new chunks
are added after it. Use --replace for a destructive rebuild.

Usage:
  merge_chunks.py [--replace] {grammar|vocab} <chunk_glob_or_files...>

Examples:
  # Append new vocab chunks to the existing deck
  merge_chunks.py vocab /tmp/_vocab_chunk_*.js

  # Destructive rebuild of the grammar deck
  merge_chunks.py --replace grammar /tmp/_fc_chunk_*.js
"""
import sys, re, glob, subprocess
from pathlib import Path

VAR_NAMES = {"grammar": "grammarCards", "vocab": "vocabCards"}
KEY_NAMES = {"grammar": "section", "vocab": "pos"}
DEFAULT_TARGET = Path("flashcards.html")


def fail(msg, code=1):
    print(f"FAIL: {msg}")
    sys.exit(code)


def main():
    args = sys.argv[1:]
    replace = False
    if args and args[0] == "--replace":
        replace = True
        args = args[1:]
    if len(args) < 2:
        print(__doc__)
        sys.exit(2)
    deck = args[0]
    if deck not in VAR_NAMES:
        fail(f"deck must be one of {list(VAR_NAMES)}, got: {deck}")

    var_name = VAR_NAMES[deck]
    key_name = KEY_NAMES[deck]

    # Expand globs
    paths = []
    for arg in args[1:]:
        if any(c in arg for c in "*?["):
            paths.extend(sorted(glob.glob(arg)))
        else:
            paths.append(arg)
    if not paths:
        fail("no chunk files matched")

    print(f"merging {len(paths)} chunk(s) into {var_name} ({'replace' if replace else 'append'} mode)")

    # Read & strip each chunk
    chunks_inner = []
    for p in paths:
        s = Path(p).read_text().strip()
        if not (s.startswith("[") and s.endswith("]")):
            fail(f"{p} is not a bare JS array literal (must open `[` and close `]`)")
        inner = s[1:-1].strip().rstrip(",").rstrip()
        chunks_inner.append(inner)
        print(f"  read {p} ({len(inner)} chars)")

    # In append mode, prepend the existing array's inner content
    target = DEFAULT_TARGET
    if not target.exists():
        fail(f"{target} not found in cwd")
    html = target.read_text()
    pattern = re.compile(rf"  const {var_name} = \[(.*?)\n  \];", re.DOTALL)
    matches = pattern.findall(html)
    if len(matches) != 1:
        fail(f"expected exactly 1 `const {var_name} = [...]` block in {target}, found {len(matches)}")

    if not replace:
        existing_inner = matches[0].strip().rstrip(",").rstrip()
        if existing_inner:
            chunks_inner = [existing_inner] + chunks_inner
            print(f"  prepending existing {existing_inner.count('{ ' + key_name + ':')} cards from {var_name}")

    merged_inner = ",\n\n".join(chunks_inner)

    # Re-indent to 4-space
    out_lines = []
    for line in merged_inner.split("\n"):
        stripped = line.lstrip()
        if stripped == "":
            out_lines.append("")
        else:
            out_lines.append("    " + stripped)

    new_block = f"  const {var_name} = [\n" + "\n".join(out_lines) + "\n  ];"

    # Validate
    tmp_path = Path(f"/tmp/_merged_{deck}.js")
    tmp_path.write_text(new_block)
    r = subprocess.run(["node", "--check", str(tmp_path)], capture_output=True, text=True)
    if r.returncode != 0:
        fail(f"merged JS does not parse:\n{r.stderr}")
    card_count = new_block.count(f"{{ {key_name}:")
    print(f"  merged JS validates ({card_count} cards total)")

    # Splice into flashcards.html
    new_html = pattern.sub(lambda m: new_block, html, count=1)
    target.write_text(new_html)
    print(f"  replaced {var_name} array in {target}")
    print("DONE")


if __name__ == "__main__":
    main()
