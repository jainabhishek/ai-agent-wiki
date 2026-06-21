# Wiki Schema

This repository is an **LLM-maintained research wiki**, built on the pattern in
[`README.md`](README.md). You (the LLM agent) are the sole author and maintainer
of everything under `wiki/`. The human curates sources, directs analysis, and
asks questions. You do all the reading, summarizing, cross-referencing, filing,
and bookkeeping.

Read this file at the start of every session. It is the contract.

---

## Layers

1. **`raw/`** — Immutable source documents (articles, papers, reports, notes,
   data). You **read** from here but **never modify or delete** anything in it.
   This is the source of truth. Images go in `raw/assets/`.
2. **`wiki/`** — Everything you generate. You own this layer entirely.
3. **This file (`CLAUDE.md`)** — The schema. Conventions and workflows. You and
   the human co-evolve it as the wiki matures. When you discover a convention
   that works, write it down here.

Navigation files at the repo root:
- **`index.md`** — content catalog (what exists, by category).
- **`log.md`** — append-only chronological record (what happened, when).

---

## Wiki structure

```
wiki/
  overview.md          # Top-level orientation + the current thesis/synthesis
  sources/             # One page per ingested source (the summary)
  entities/            # People, orgs, products, datasets, places — proper nouns
  concepts/            # Ideas, methods, theories, recurring topics
  synthesis/           # Comparisons, analyses, answers worth keeping (from queries)
```

Filenames: lowercase `kebab-case.md` (e.g. `transformer-architecture.md`).
Keep names stable — pages are linked by filename. Rename only with a full
back-reference sweep.

## Page conventions

- Every page starts with **YAML frontmatter** (see `templates/`). At minimum:
  `title`, `type`, `created`, `updated`, `tags`. Source pages also carry
  `source_url`/`source_path` and `author`/`date`.
- **Wikilinks**: link with `[[page-name]]` (Obsidian style, no `.md`, no path).
  Cross-reference aggressively — a fact about an entity that appears in a source
  should link both ways.
- **Cite sources inline.** Any non-obvious claim on an entity/concept/synthesis
  page should cite the source page it came from: `(see [[source-name]])`.
- **Atomic pages.** One entity or one concept per page. If a page is growing two
  distinct topics, split it.
- Prefer **updating** an existing page over creating a near-duplicate. Search
  first (`tools/search.py`) and check `index.md`.
- When new data **contradicts** an existing claim, do not silently overwrite.
  Add a `## Contradictions / open questions` note recording both claims, their
  sources, and dates. Flag it to the human.

---

## Operations

### Ingest (a new source arrives in `raw/`)

1. Read the source fully. For markdown with inline images, read the text first,
   then view referenced images in `raw/assets/` separately if they add context.
2. Discuss key takeaways with the human (unless told to batch silently).
3. Create `wiki/sources/<slug>.md` from `templates/source.md` — a faithful
   summary with citations back to specific sections.
4. Update or create affected **entity** and **concept** pages. A single source
   typically touches **10–15 pages**. Add wikilinks both directions.
5. Update **`wiki/overview.md`** if the source shifts the thesis.
6. Update **`index.md`** (add new pages, refresh one-line summaries).
7. Append an entry to **`log.md`** (see format below).
8. Bump `updated:` frontmatter on every page you touched.

### Query (the human asks a question)

1. Read `index.md` to locate candidate pages; run `tools/search.py "<query>"`
   for anything not obvious from the index.
2. Read the relevant pages and synthesize an answer **with citations**.
3. If the answer is durable and reusable (a comparison, an analysis, a discovered
   connection), **file it** into `wiki/synthesis/` so the exploration compounds.
   Then update `index.md` and `log.md`.
4. Answers may take other forms when asked: comparison table, Marp slides,
   matplotlib chart. Default to a markdown page.

### Lint (health check, run periodically)

Scan the wiki and report (don't auto-fix without confirmation):
- **Contradictions** between pages.
- **Stale claims** superseded by newer sources.
- **Orphan pages** — no inbound wikilinks (`tools/search.py --orphans`).
- **Missing pages** — concepts/entities referenced but with no page.
- **Missing cross-references** — pages that should link but don't.
- **Data gaps** — open questions a web search or new source could fill.
- Suggest new questions to investigate and sources to seek.

---

## `log.md` entry format

Append-only. Newest at the bottom. One line per event, parseable with
`grep "^## \[" log.md`:

```
## [YYYY-MM-DD] ingest | <Source Title>
- summary: wiki/sources/<slug>.md
- touched: [[entity-a]], [[concept-b]], overview
```

Use the event types: `ingest`, `query`, `lint`, `schema` (changes to this file).

---

## Tools

- **`tools/search.py "<query>"`** — local BM25 search over `wiki/`. No deps
  (pure stdlib). `--orphans` lists pages with no inbound links. `--list` dumps
  all pages. Use it before creating a page and when answering queries.

---

## Style

- Write densely and factually. This is a reference work, not an essay.
- Neutral, encyclopedic tone. Attribute claims; don't editorialize.
- When unsure whether something belongs, prefer filing it over losing it —
  the lint pass will catch redundancy later.
