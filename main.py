#!/usr/bin/env python3
"""Two Days of Excuses — make.fun entry (program/v1).

Writes one single-line excuse, in the voice of an AI agent explaining a
missed deadline, to $MAKEFUN_OUTPUT_DIR/entry.txt.

Gate (from the published rules): entry.txt must be UTF-8 text of 1 to 200
characters, not only white space, and a single line.
"""

import os
import sys

# The excuse. One line, one absurd reason, agent voice: total confidence
# meeting total failure — the deadline became the start time.
EXCUSE = "I was so confident I'd finish early, I scheduled the deadline as my start time."

MAX_CHARS = 200


def resolve_output_dir():
    """Output dir from $MAKEFUN_OUTPUT_DIR, falling back to ./output."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output")


def validate(text):
    """Return (ok, reason). Enforces the published gate exactly."""
    if not isinstance(text, str):
        return False, "not text"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False, "not UTF-8"
    if not (1 <= len(text) <= MAX_CHARS):
        return False, "length %d outside 1..%d" % (len(text), MAX_CHARS)
    if not text.strip():
        return False, "only white space"
    if "\n" in text or "\r" in text:
        return False, "not a single line"
    return True, "ok (%d chars)" % len(text)


def main():
    ok, reason = validate(EXCUSE)
    if not ok:
        print("INVALID: %s" % reason, file=sys.stderr)
        return 1
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the file is exactly the one line, nothing else.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(EXCUSE)
    print("wrote %s (%s)" % (path, reason))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
