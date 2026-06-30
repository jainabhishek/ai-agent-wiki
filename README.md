# ai-agent-wiki

A knowledge base on **building effective AI agents** — architecture choices,
tools, orchestration, context engineering, harness design, and guardrails —
synthesized from primary guidance by Anthropic and OpenAI, plus Anthropic's
engineering blog posts on harness, skills, steering, and context.

It's maintained by an LLM agent ([Claude Code](https://www.anthropic.com/claude-code),
via [`CLAUDE.md`](CLAUDE.md)) and meant to be **read by both humans and other
agents** — point an agent at this repo and it can cite settled answers instead
of re-deriving them from scratch.

This repo is **two things at once**: a live knowledge base on building AI
agents, and a reusable scaffold you can fork empty to grow your own wiki on any
topic (see [Start your own](#start-your-own)).

## What's inside

The corpus is **12 source summaries · 7 entities · 13 concepts · 1 synthesis**,
covering how to design, build, and safely deploy LLM agents.

- Start at [`wiki/overview.md`](wiki/overview.md) for the full thesis, or
  [`index.md`](index.md) for the catalog of every page.

**The thesis in one line:** the labs strongly agree on a few load-bearing
principles — *don't build an agent unless you need one*, *start simple and add
complexity only when evals justify it*, *tools are the highest-leverage surface*,
*instructions must be unambiguous*, *safety is layered*, and *engineer the
context and harness, then prune them*. They differ mainly in emphasis.

### What a page looks like

Pages are dense, cross-linked (`[[wikilinks]]`), and cite their sources inline.
Excerpt from [`wiki/concepts/agents-vs-workflows.md`](wiki/concepts/agents-vs-workflows.md):

```markdown
[[anthropic]] frames a spectrum of agentic systems:
- Workflows — LLMs and tools orchestrated through predefined code paths.
  Predictable and consistent; best for well-defined tasks.
  (see [[anthropic-building-effective-agents]])
- Agents — LLMs dynamically direct their own processes and tool usage,
  controlling how they accomplish a task.
  (see [[anthropic-building-effective-agents]])
```

## Using this wiki

### As a human

- Open the folder as an [Obsidian](https://obsidian.md) vault, start at
  [`wiki/overview.md`](wiki/overview.md), and follow wikilinks / the graph view.
- Ask the maintaining agent a question (*"what do my sources say about
  multi-agent orchestration?"*) — it answers with citations and, if the answer
  is durable, files it into `wiki/synthesis/` for next time.

### As an agent

- Read [`CLAUDE.md`](CLAUDE.md) first — it's the schema and operating contract
  for this wiki.
- Read [`index.md`](index.md) to find candidate pages before reading anything
  else; run `tools/search.py "<query>"` for what isn't obvious from the index.
- Prefer citing an existing `wiki/` page over re-deriving an answer from
  `raw/` — the synthesis and cross-references already exist.
- If you're building an agent yourself, the principles in
  [`wiki/overview.md`](wiki/overview.md) and [`wiki/concepts/`](wiki/concepts/)
  are a reasonable starting checklist: scope, tool design, orchestration,
  context engineering, guardrails.

```
python3 tools/search.py "your query"     # ranked results across wiki/
python3 tools/search.py --orphans        # pages with no inbound links
python3 tools/search.py --list           # every page with its title
```

Pure stdlib — no install step.

## How it's maintained

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
3. Browse the result in Obsidian — follow the wikilinks and the graph view.
4. Ask questions: *"what do my sources say about X?"* — good answers get filed
   into the wiki automatically.
5. Occasionally: *"lint the wiki"*.

## Start your own

Fork this repo and clear the content, keeping the machinery:

```
git clone https://github.com/jainabhishek/ai-agent-wiki.git my-wiki
cd my-wiki
rm -rf raw/* wiki/sources/* wiki/entities/* wiki/concepts/* wiki/synthesis/*
: > log.md                                # reset the timeline
```

Keep `CLAUDE.md` (the schema), `templates/`, and `tools/`. Edit
`wiki/overview.md` and `index.md` to describe your new topic, then start
ingesting. The agent reads `CLAUDE.md` every session and follows it.

## License & sources

The **scaffold** — `CLAUDE.md`, `templates/`, `tools/`, and this README — is
released under the [MIT License](LICENSE-scaffold.md); fork and adapt it freely.

The **`raw/` directory contains third-party articles** (e.g. from Anthropic and
OpenAI) reproduced for personal research. Copyright remains with their
respective authors; they are **not** covered by the MIT License and are not
redistributed for any other use. Everything under `wiki/` is LLM-generated
summary and synthesis that cites those sources.

---

**Inspiration:** the ingest/query/lint pattern and the `raw/` → `wiki/` →
`CLAUDE.md` layering follow Andrej Karpathy's
[LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
gist: instead of RAG-style retrieval that re-derives knowledge on every query,
the LLM incrementally builds and maintains a persistent, interlinked markdown
wiki between you and your raw sources, so cross-references and synthesis
already exist by the time you ask.
