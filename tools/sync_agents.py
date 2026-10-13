#!/usr/bin/env python3
"""Regenerate AGENTS.md from CLAUDE.md.

AGENTS.md is the same schema for agents that read that file name. This script
copies CLAUDE.md, swaps the file name, and replaces the sync note so the copy
says where it comes from. Pure stdlib. Run from the repo root:

    python3 tools/sync_agents.py          # write AGENTS.md
    python3 tools/sync_agents.py --check  # exit 1 if AGENTS.md is stale
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "CLAUDE.md"
DST = ROOT / "AGENTS.md"
NOTE = re.compile(r"<!-- sync-note -->.*?<!-- /sync-note -->", re.S)
GENERATED = (
    "<!-- sync-note -->\n"
    "   Generated from `CLAUDE.md` by `tools/sync_agents.py`. Do not edit this\n"
    "   file directly; edit `CLAUDE.md` and rerun the script.\n"
    "   <!-- /sync-note -->"
)


def render() -> str:
    text = SRC.read_text()
    if not NOTE.search(text):
        sys.exit("CLAUDE.md has no <!-- sync-note --> block; refusing to guess.")
    text = NOTE.sub(lambda _: "@@SYNC_NOTE@@", text, count=1)
    text = text.replace("CLAUDE.md", "AGENTS.md")
    return text.replace("@@SYNC_NOTE@@", GENERATED)


def main() -> None:
    want = render()
    if "--check" in sys.argv[1:]:
        have = DST.read_text() if DST.exists() else ""
        if have != want:
            sys.exit("AGENTS.md is out of date; run python3 tools/sync_agents.py")
        print("AGENTS.md is in sync with CLAUDE.md")
        return
    DST.write_text(want)
    print(f"wrote {DST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
