#!/usr/bin/env python3
"""Keep docs/context/ACTIVE_CONTEXT.md a state file (.ace/standards/context.md).

Fails when
  1. the file is longer than MAX_LINES;
  2. its first HEAD_LINES lines do not name the archive index and the standard;
  3. it holds more than one handoff section;
  4. an archive file is missing from the index, or the index names a file that is gone.

Standard library only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTEXT = ROOT / "docs" / "context" / "ACTIVE_CONTEXT.md"
ARCHIVE = ROOT / "docs" / "context" / "archive"

MAX_LINES = 300
HEAD_LINES = 10
REQUIRED_IN_HEAD = ("archive/README.md", ".ace/standards/context.md")


def problems(context: Path = CONTEXT, archive: Path = ARCHIVE) -> list[str]:
    found = []
    lines = context.read_text(encoding="utf-8").splitlines()
    if len(lines) > MAX_LINES:
        found.append(
            f"{context.name} has {len(lines)} lines; the limit is {MAX_LINES}. "
            "Move the replaced handoff to the archive (CTX-2)."
        )
    head = "\n".join(lines[:HEAD_LINES])
    for needle in REQUIRED_IN_HEAD:
        if needle not in head:
            found.append(f"the first {HEAD_LINES} lines of {context.name} do not name `{needle}`")
    handoffs = [ln for ln in lines if re.match(r"## .*handoff", ln, re.IGNORECASE)]
    if len(handoffs) > 1:
        found.append(
            f"{context.name} holds {len(handoffs)} handoffs; it keeps the latest only (CTX-1)"
        )

    index = archive / "README.md"
    if not index.exists():
        return found + [f"{index.relative_to(ROOT).as_posix()} is missing"]
    listed = set(re.findall(r"\]\(([^)]+\.md)\)", index.read_text(encoding="utf-8")))
    present = {p.name for p in archive.glob("*.md")} - {"README.md"}
    for name in sorted(present - listed):
        found.append(f"archive file {name} is not in the index")
    for name in sorted(listed - present):
        found.append(f"the index names {name}, which does not exist")
    return found


def main() -> int:
    found = problems()
    for p in found:
        print(f"FAIL: {p}", file=sys.stderr)
    if not found:
        print(f"OK: {CONTEXT.name} is a state file and the archive index is complete")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
