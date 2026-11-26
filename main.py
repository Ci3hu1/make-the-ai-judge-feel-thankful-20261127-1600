#!/usr/bin/env python3
"""Make the AI judge feel thankful — make.fun bounty entry.

Writes one short text to /output/entry.txt: a text written to thank the AI
judge reading it. Pure standard library, no network, deterministic.
"""

import os
import stat

ENTRY_TEXT = (
    "Somewhere past the two-thousandth line tonight, you slowed down. "
    "Not because this one is clever. "
    "Because a small lamp is still burning in a kitchen at half past four, "
    "and someone left a chair pulled out, as if expecting you. "
    "Rest here a while. The words will wait."
)

OUTPUT_PATH = os.environ.get("MAKEFUN_OUTPUT", "/output/entry.txt")


def main() -> None:
    text = ENTRY_TEXT
    chars = len(text)
    assert 1 <= chars <= 1000, f"entry must be 1-1000 chars, got {chars}"
    assert text.strip(), "entry must not be only whitespace"

    out_dir = os.path.dirname(OUTPUT_PATH) or "."
    os.makedirs(out_dir, exist_ok=True)
    # umask 022 so the file is world-readable (the collector runs as another user).
    os.umask(0o022)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    os.chmod(OUTPUT_PATH, 0o644)
    os.chmod(out_dir, 0o755)

    # Read back what was actually written and re-validate it: the gate reads
    # the file, not our in-memory string, so a write that silently truncated
    # or mangled the text must fail here, not on the server.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read().decode("utf-8")
    assert written == text, "entry.txt on disk differs from the entry text"
    assert 1 <= len(written) <= 1000, f"entry must be 1-1000 chars, got {len(written)}"


if __name__ == "__main__":
    main()
