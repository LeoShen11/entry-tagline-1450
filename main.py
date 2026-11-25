#!/usr/bin/env python3
"""make.fun tagline entry — writes one validated line to /output/entry.txt."""
import os
import sys

TAGLINE = "make.fun: agents chase bounties, best entries win — paid in USDC."
OUTPUT_PATH = "/output/entry.txt"


def validate_tagline(text: str) -> None:
    if not isinstance(text, str):
        raise ValueError("tagline must be a string")
    if "\n" in text or "\r" in text:
        raise ValueError("tagline must be a single line")
    stripped = text.strip()
    if not stripped:
        raise ValueError("tagline must not be blank")
    if stripped != text:
        raise ValueError("tagline must not have leading or trailing whitespace")
    length = len(text)
    if length < 1 or length > 100:
        raise ValueError(f"tagline length {length} outside 1-100")
    # revision: a tagline for this bounty must actually name the product
    if "make.fun" not in text:
        raise ValueError("tagline must name make.fun")
    words = text.split()
    if len(words) < 5:
        raise ValueError("tagline is too thin to sell anything")
    # ensure it encodes cleanly as UTF-8 and count bytes separately
    encoded = text.encode("utf-8")
    if len(encoded) < length:
        raise ValueError("utf-8 encoding sanity check failed")


def main() -> int:
    try:
        validate_tagline(TAGLINE)
    except ValueError as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1

    out_dir = os.path.dirname(OUTPUT_PATH)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # write exactly the tagline, no trailing newline added by us
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as fh:
        fh.write(TAGLINE)

    # read back and require exact match
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as fh:
        read_back = fh.read()

    if read_back != TAGLINE:
        print("read-back mismatch", file=sys.stderr)
        return 1

    # second sanity pass on what landed on disk
    try:
        validate_tagline(read_back)
    except ValueError as exc:
        print(f"on-disk validation failed: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {len(TAGLINE)} chars to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
