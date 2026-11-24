---
title: Obsidian Graph Analysis
type: synthesis
created: 2026-06-22
updated: 2026-11-24
tags: [graph, obsidian, wiki-health, synthesis]
---

# Obsidian Graph Analysis

> Query answer for: "check the Obsidian graph and explain." First filed
> 2026-06-22. Refreshed 2026-10-12 and 2026-10-13, and again on 2026-11-24
> after the Oct–Nov 2026 ingest (20 sources) and the GPT-6.2 legacy pass.

## Answer (refreshed 2026-11-24)

The meaningful graph is still the `wiki/` subgraph, not the whole repository.
Within `wiki/`, the graph stays healthy: one connected component, no broken
links, and no page without an inbound link.

| Measure | 2026-06-22 | 2026-08-06 | 2026-10-12 (first ingests) | 2026-10-12 (full sweep) | 2026-10-13 (after splits) | 2026-11-24 |
|---------|-----------:|-----------:|-----------:|-----------:|-----------:|-----------:|
| Pages | 35 | 44 | 83 | 179 | 184 | 204 |
| Source pages | 12 | 17 | 53 | 147 | 148 | 168 |
| Concept / entity pages | — | 16 / 8 | 17 / 10 | 19 / 10 | 23 / 10 | 23 / 10 |
| Unique directed wikilinks | 408 | 516 | 1,364 | 3,184 | 3,367 | 3,830 |
| Reciprocal link pairs | 130 | 154 | 445 | 1,042 | 1,080 | 1,192 |
| Connected components | 1 | 1 | 1 | 1 | 1 | 1 |
| Unresolved internal wikilinks | 0 | 0 | 0 | 0 | 0 | 0 |
| Pages with no inbound link from `wiki/` | 0 | 1 | 0 | 0 | 0 | 0 |
| Source pages marked legacy | 0 | 0 | 4 | 4 | 4 | 8 |

**How the figures are computed.** A script reads every `.md` file under
`wiki/` and collects the double-bracket wikilinks. It ignores aliases and
heading anchors, and it drops self-links and duplicates. It then counts the
links, the reciprocal pairs, and the connected components, treating each link as
undirected for the component count. The figures include this page's own links.
The 2026-10-13 column was rerun on 2026-11-24 from commit `33759f8`, so its hub
counts below are exact. The June figures come from the original analysis (its
log entry says 407 links; this page said 408).

Since 2026-10-13 the link count grew by 463, about 23 per new source page.
That is close to the wiki's average of 19 outbound links per page, so the new
pages are as connected as the old ones.

## What changed since 2026-10-13

- **The concept backbone kept growing.** The ingest put most new claims on
  [[guardrails]] (+16 inbound links), [[agent-harness]] (+14),
  [[human-agent-teams]] (+13), [[agent-evals]] (+10), and
  [[agent-verification]] (+8). [[guardrails]] is now the second-largest hub,
  after [[anthropic]].
- **The four split pages from 2026-10-13 took hold.** [[human-agent-teams]]
  grew from 23 to 36 inbound links, [[agent-verification]] from 22 to 30, and
  [[agent-identity-and-access]] from 19 to 27. [[tool-placement]] stayed at 14:
  no new source was about where tools run.
- **Legacy pages doubled, and they stay linked.** Eight source pages are now
  legacy (Fable 5, Fable 5.1, Opus 5, Sonnet 5, GPT-5.6, and three GPT-6 Astra
  pages). They keep 6–18 inbound links each, because concept pages cite them
  next to their replacements. This is by design: the schema keeps legacy claims
  instead of deleting them.
- **The vendor ratio did not change.** The source base is now 110 Anthropic
  pages and 15 Anthropic customer stories, against 42 OpenAI pages and 1 Cursor
  page: still about 3 to 1. [[openai]] grew from 60 to 67 inbound links, and
  [[openai-codex]] from 51 to 58.
- **The synthesis layer lags.** [[agent-building-best-practices-anthropic-vs-openai]]
  still has 8 inbound links and no update since 2026-10-12. The new sources add
  architecture points that both vendors share (OS-level sandboxes for coding
  agents, monitors for always-on agents), which that page does not yet compare.

## What the clusters mean

- **Source cluster:** 168 source summaries feed claims into concepts and
  entities. A model-scoped sub-cluster (25 pages with a `models:` field, 8
  of them legacy) feeds mainly [[prompt-tuning-axes]], [[claude]], and
  [[openai]].
- **Concept backbone:** [[guardrails]], [[context-engineering]],
  [[agent-harness]], [[agent-orchestration]], [[agent-evals]], and
  [[tool-design]] bind source evidence to reusable doctrine.
- **Entity cluster:** [[claude]], [[claude-code]], [[claude-agent-sdk]], and
  [[claude-managed-agents]] form the Anthropic product side; [[openai]],
  [[openai-agents-sdk]], [[openai-agents-api]], and [[openai-codex]] form the
  OpenAI side.
- **Synthesis layer:** [[agent-building-best-practices-anthropic-vs-openai]]
  bridges the two vendor sides. It compares architecture only.

## Top internal hubs (2026-11-24)

| Page | Inbound wiki links | 2026-10-13 | June | Interpretation |
|------|-------------------:|-----------:|-----:|----------------|
| [[anthropic]] | 152 | 139 | 32 | Dominant source and vendor anchor |
| [[guardrails]] | 131 | 115 | 14 | Safety layer: sandboxes, approvals, monitors |
| [[context-engineering]] | 117 | 109 | 18 | Context, caching, cost, and sessions |
| [[agent-harness]] | 114 | 100 | 19 | Runtime and loop mechanics |
| [[claude]] | 109 | 97 | 15 | Model family; current vs. legacy lineup |
| [[claude-code]] | 106 | 96 | — | Anthropic's main worked example |
| [[agent-orchestration]] | 101 | 94 | 24 | Multi-agent patterns |
| [[agent-evals]] | 99 | 89 | — | Evals and eval integrity |
| [[tool-design]] | 91 | 87 | 22 | Tool interfaces and scaling |
| [[agent-skills]] | 77 | 72 | — | Skill types, architecture, and maintenance |
| [[openai]] | 67 | 60 | 14 | Secondary vendor anchor |
| [[openai-codex]] | 58 | 51 | — | OpenAI's harness and coding agent |

"—" means the page was not in June's top ten.

## Full-vault graph caveats

Obsidian may show more noise than the wiki-only graph, because the repository
also contains root docs, templates, and raw source files:

- `index.md` and `log.md` are navigation and bookkeeping pages, so they become
  artificial high-outbound hubs in the full graph.
- `raw/` contains markdown files with the same basenames as `wiki/sources/`
  pages (165 of 168 as of 2026-11-24). If raw files are included in Obsidian's
  graph, source nodes can look duplicated or ambiguous.
- `templates/` used to contain placeholder wikilinks such as `source-a` and
  `concept-b`. They are now plain placeholder text, so they no longer create
  fake graph nodes.

## Bottom-right disconnected component

The disconnected component at the bottom right of the earlier Obsidian graph was
template and schema noise, not a research cluster. It was made from:

- `templates/source.md`, `templates/entity.md`, `templates/concept.md`, and
  `templates/synthesis.md`;
- placeholder wikilinks that were embedded in those templates, such as `source-a`,
  `source-b`, `source-name`, `entity-a`, `entity-b`, `concept-a`, `concept-b`,
  `concept-c`, `related-concept`, `other-entity`, and `other-source`;
- schema and root docs that reused the same example wikilinks, such as
  `CLAUDE.md` and local agent-instruction files visible to Obsidian.

Those nodes floated separately because they were examples for future pages, not
links to real pages in `wiki/`. The nearby isolated node
`anthropic-harnessing-claudes-intelligence` is the raw capture at
`raw/anthropic-harnessing-claudes-intelligence.md`; the connected, summarized
wiki page is [[harnessing-claudes-intelligence]].

After cleanup, the full-vault graph has no unresolved placeholder wikilinks. The
remaining disconnected nodes are single files, not fake clusters: root and
schema docs, templates, README, and the isolated raw capture.

For the clearest graph view, filter the graph to `path:wiki/`. For a cleaner
concept map, hide `wiki/sources/` and focus on `wiki/concepts/`,
`wiki/entities/`, and `wiki/synthesis/`.

## What to do next

- **Refresh the vendor comparison.**
  [[agent-building-best-practices-anthropic-vs-openai]] has not changed since
  2026-10-12. The Oct–Nov sources show both vendors converging on OS-level
  sandboxes with domain-filtering proxies ([[openai-inside-the-codex-sandbox]],
  [[anthropic-eng-claude-code-sandboxing]]) and on layered monitors for
  persistent agents ([[openai-securing-persistent-agents-openclaw]],
  [[anthropic-building-always-on-agents]]).
- **Add non-Anthropic sources** if the goal is a more balanced graph. Anthropic
  sources still outnumber OpenAI ones about 3 to 1, and no other lab is
  represented except [[cursor]].
- **Watch [[guardrails]] for size.** At 131 inbound links it carries the most
  claims of any concept page. The 2026-10-13 split moved identity out; a later
  split could move monitoring and observability out.
- ~~Create an MCP concept page.~~ Done 2026-10-12: [[model-context-protocol]].
- ~~Split concept pages that hold two topics.~~ Done 2026-10-13.

## Sources & pages drawn on

- [[overview]]
- [[agent-building-best-practices-anthropic-vs-openai]]
- [[anthropic]], [[openai]], [[claude]], [[claude-code]], [[claude-agent-sdk]],
  [[claude-managed-agents]], [[openai-agents-sdk]]
- [[agent-design-principles]], [[agent-orchestration]], [[tool-design]],
  [[agent-harness]], [[context-engineering]], [[guardrails]],
  [[agent-skills]], [[agent-steering]], [[agent-evals]],
  [[model-context-protocol]], [[prompt-tuning-axes]], [[human-agent-teams]],
  [[agent-verification]], [[agent-identity-and-access]], [[tool-placement]]
- [[openai-agents-api]], [[openai-codex]], [[cursor]]
