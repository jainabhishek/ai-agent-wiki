#!/usr/bin/env python3
"""Local search over the wiki — pure stdlib, no dependencies.

Usage:
    python3 tools/search.py "your query"      Ranked BM25 search across wiki/
    python3 tools/search.py --list            List every page with its title
    python3 tools/search.py --orphans         Pages with no inbound [[wikilinks]]
    python3 tools/search.py "q" -n 20         Limit to 20 results

Scope: searches all .md files under wiki/ (run from the repo root).
"""
from __future__ import annotations

import math
import re
import sys
from collections import Counter
from pathlib import Path

WIKI_DIR = Path(__file__).resolve().parent.parent / "wiki"

WORD_RE = re.compile(r"[a-z0-9]+")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)")
FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
TITLE_RE = re.compile(r"^title:\s*(.+)$", re.MULTILINE)

# BM25 parameters
K1 = 1.5
B = 0.75


def tokenize(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def page_title(path: Path, text: str) -> str:
    m = TITLE_RE.search(text)
    if m:
        return m.group(1).strip().strip("\"'")
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def load_pages() -> list[dict]:
    pages = []
    if not WIKI_DIR.exists():
        return pages
    for path in sorted(WIKI_DIR.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        body = FRONTMATTER_RE.sub("", text)
        pages.append(
            {
                "path": path,
                "rel": path.relative_to(WIKI_DIR.parent),
                "slug": path.stem,
                "title": page_title(path, text),
                "tokens": tokenize(body + " " + path.stem.replace("-", " ")),
                "links": {m.strip().lower() for m in WIKILINK_RE.findall(text)},
            }
        )
    return pages


def bm25_search(query: str, pages: list[dict], limit: int) -> list[tuple[float, dict]]:
    q_terms = tokenize(query)
    if not q_terms or not pages:
        return []

    N = len(pages)
    avgdl = sum(len(p["tokens"]) for p in pages) / N
    # document frequency per term
    df = Counter()
    tfs = []
    for p in pages:
        counts = Counter(p["tokens"])
        tfs.append(counts)
        for term in set(q_terms):
            if term in counts:
                df[term] += 1

    scored = []
    for p, counts in zip(pages, tfs):
        dl = len(p["tokens"]) or 1
        score = 0.0
        for term in q_terms:
            if term not in counts:
                continue
            idf = math.log(1 + (N - df[term] + 0.5) / (df[term] + 0.5))
            tf = counts[term]
            denom = tf + K1 * (1 - B + B * dl / avgdl)
            score += idf * (tf * (K1 + 1)) / denom
        # small boost when query terms appear in the slug/title
        slug_title = (p["slug"] + " " + p["title"]).lower()
        for term in q_terms:
            if term in slug_title:
                score += 0.5
        if score > 0:
            scored.append((score, p))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:limit]


def snippet(path: Path, query: str, width: int = 160) -> str:
    text = FRONTMATTER_RE.sub("", path.read_text(encoding="utf-8", errors="replace"))
    flat = re.sub(r"\s+", " ", text).strip()
    q_terms = tokenize(query)
    low = flat.lower()
    pos = -1
    for term in q_terms:
        pos = low.find(term)
        if pos != -1:
            break
    if pos == -1:
        return flat[:width] + ("…" if len(flat) > width else "")
    start = max(0, pos - width // 3)
    end = min(len(flat), start + width)
    return ("…" if start > 0 else "") + flat[start:end] + ("…" if end < len(flat) else "")


def cmd_search(query: str, limit: int) -> int:
    pages = load_pages()
    results = bm25_search(query, pages, limit)
    if not results:
        print(f"No matches for: {query!r}")
        return 0
    for score, p in results:
        print(f"\n[{score:5.2f}] {p['title']}  ({p['rel']})")
        print(f"        {snippet(p['path'], query)}")
    print()
    return 0


def cmd_list() -> int:
    pages = load_pages()
    if not pages:
        print("No pages in wiki/ yet.")
        return 0
    for p in pages:
        print(f"{p['rel']}  —  {p['title']}")
    print(f"\n{len(pages)} page(s).")
    return 0


def cmd_orphans() -> int:
    pages = load_pages()
    if not pages:
        print("No pages in wiki/ yet.")
        return 0
    inbound = set()
    for p in pages:
        inbound |= p["links"]
    orphans = [p for p in pages if p["slug"].lower() not in inbound]
    if not orphans:
        print("No orphan pages — every page has at least one inbound wikilink.")
        return 0
    print("Orphan pages (no inbound [[wikilinks]]):\n")
    for p in orphans:
        print(f"  {p['rel']}  —  {p['title']}")
    print(f"\n{len(orphans)} orphan(s).")
    return 0


def main(argv: list[str]) -> int:
    args = argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if args[0] == "--list":
        return cmd_list()
    if args[0] == "--orphans":
        return cmd_orphans()

    limit = 10
    if "-n" in args:
        i = args.index("-n")
        try:
            limit = int(args[i + 1])
            del args[i : i + 2]
        except (IndexError, ValueError):
            print("error: -n needs a number")
            return 1
    query = " ".join(a for a in args if not a.startswith("-"))
    if not query:
        print("error: empty query")
        return 1
    return cmd_search(query, limit)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
