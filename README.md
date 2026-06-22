# ai-agent-wiki

A personal **research wiki** maintained by an LLM agent, following Andrej
Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
pattern.

Instead of RAG-style retrieval that re-derives knowledge on every query, the LLM
**incrementally builds and maintains a persistent, interlinked markdown wiki**
that sits between you and your raw sources. Knowledge is compiled once and kept
current — cross-references, contradictions, and synthesis already exist by the
time you ask. The wiki compounds with every source you add and every question
you ask.

> Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.

## How it works

Three layers:

| Layer | Path | Who owns it |
|-------|------|-------------|
| **Raw sources** | `raw/` | You. Immutable. The LLM reads, never edits. |
| **The wiki** | `wiki/` | The LLM. Summaries, entity & concept pages, synthesis. |
| **The schema** | `CLAUDE.md` | Both. Conventions + workflows the LLM follows. |

Three operations:

- **Ingest** — drop a source in `raw/`, ask the agent to process it. It reads,
  summarizes, updates 10–15 entity/concept pages, refreshes the index, logs it.
- **Query** — ask questions; the agent searches the wiki, answers with
  citations, and files durable answers back into `wiki/synthesis/`.
- **Lint** — periodically ask the agent to health-check: contradictions, stale
  claims, orphans, missing pages, data gaps.

## Layout

```
raw/            # your source documents (immutable) + assets/ for images
wiki/
  overview.md   # orientation + current thesis
  sources/      # one summary page per source
  entities/     # people, orgs, products, datasets, places
  concepts/     # ideas, methods, theories
  synthesis/    # comparisons & analyses worth keeping
index.md        # content catalog, by category
log.md          # append-only timeline of ingests/queries/lints
templates/      # page templates the LLM copies from
tools/search.py # local BM25 search over the wiki (no dependencies)
CLAUDE.md       # the schema — read by the agent every session
```

## Getting started

1. Add a source: drop a `.md`/`.pdf`/`.txt` into `raw/` (the
   [Obsidian Web Clipper](https://obsidian.md/clipper) is great for web articles).
2. Tell the agent: *"ingest the new source in raw/"*.
3. Browse the result in Obsidian (open this folder as a vault) — follow the
   wikilinks and the graph view.
4. Ask questions: *"what do my sources say about X?"* — good answers get filed
   into the wiki automatically.
5. Occasionally: *"lint the wiki"*.

## Search

```
python3 tools/search.py "your query"     # ranked results across wiki/
python3 tools/search.py --orphans        # pages with no inbound links
python3 tools/search.py --list           # every page with its title
```

Pure stdlib — no install step.
