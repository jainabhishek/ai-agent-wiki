---
title: Obsidian Graph Analysis
type: synthesis
created: 2026-06-22
updated: 2026-10-12
tags: [graph, obsidian, wiki-health, synthesis]
---

# Obsidian Graph Analysis

> Query answer for: "check the Obsidian graph and explain." First filed
> 2026-06-22; figures refreshed 2026-10-12 after the 30-source ingest, the six-post
> backlog ingest, and the full claude.com / openai.com sweep (94 sources).

## Answer (refreshed 2026-10-12)

The meaningful graph is still the `wiki/` subgraph, not the whole repository.
Within `wiki/`, the graph is healthy and has more than doubled since June:

| Measure | 2026-06-22 | 2026-08-06 (`main`) | 2026-10-12 (first ingests) | 2026-10-12 (full sweep) |
|---------|-----------:|--------------------:|-----------:|-----------:|
| Pages | 35 | 44 | 83 | 179 |
| Source pages | 12 | 17 | 53 | 147 |
| Concept / entity pages | — | 16 / 8 | 17 / 10 | 19 / 10 |
| Unique directed wikilinks | 408 | 516 | 1,364 | 3,184 |
| Reciprocal link pairs | 130 | 154 | 445 | 1,042 |
| Connected components | 1 | 1 | 1 | 1 |
| Unresolved internal wikilinks | 0 | 0 | 0 | 0 |
| Pages with no inbound link from `wiki/` | 0 | 1 | 0 | 0 |

How the 2026-10-12 figures were computed: a script reads every `.md` file under
`wiki/`, collects double-bracket wikilinks (ignoring aliases and heading anchors), drops
self-links and duplicates, and counts the rest. The figures include this page's
own links. The June figures come from the
original analysis (its log entry says 407 links; this page said 408). The August
column reruns the same script on `main`. The one August page without a `wiki/`
inbound link was [[boundary-contracts]], linked then only from `index.md`; it is
now linked from [[model-context-protocol]].

The graph is still centered on **agent-building doctrine**. The concept backbone
([[context-engineering]], [[agent-harness]], [[tool-design]], [[guardrails]],
[[agent-orchestration]]) now carries more links than any page except
[[anthropic]].

## What changed since June

- **The concept backbone thickened.** [[context-engineering]] and
  [[agent-harness]] grew from 18–19 inbound links to 53–55, and [[guardrails]]
  from 14 to 49. The 2026-10-12 ingest put most of its new claims on these pages.
- **The OpenAI side is no longer a thin satellite.** [[openai]] grew from 14 to
  32 inbound links, and two new entities joined it: [[openai-codex]] (25) and
  [[openai-agents-api]] (13). After the full sweep the source base is 97
  Anthropic source pages and 15 Anthropic-published customer stories,
  against 34 OpenAI and 1 Cursor: still about 3 to 1.
- **Legacy pages stay well linked.** The four legacy prompting pages keep 5–12
  inbound links each, because concept pages cite them next to their
  replacements. This is intended: the schema keeps legacy claims rather than
  deleting them.
- **MCP has a home.** [[model-context-protocol]], the gap this page named in
  June, now exists and links the tool, context, and guardrails clusters.

## What the clusters mean

- **Source cluster:** 147 source summaries feed claims into concepts and
  entities. A model-scoped sub-cluster (12 prompting pages, 4 of them legacy)
  feeds mainly [[prompt-tuning-axes]], [[claude]], and [[openai]].
- **Concept backbone:** [[context-engineering]], [[agent-harness]],
  [[tool-design]], [[guardrails]], [[agent-orchestration]], and
  [[agent-design-principles]] bind source evidence to reusable doctrine.
- **Entity cluster:** [[claude]], [[claude-code]], [[claude-agent-sdk]], and
  [[claude-managed-agents]] form the Anthropic product side; [[openai]],
  [[openai-agents-sdk]], [[openai-agents-api]], and [[openai-codex]] form the
  OpenAI side.
- **Synthesis layer:** [[agent-building-best-practices-anthropic-vs-openai]]
  bridges the two vendor sides; its 2026-10-12 update compares architecture
  only.

## Top internal hubs (2026-10-12, after the full sweep)

| Page | Inbound wiki links | June | Interpretation |
|------|-------------------:|-----:|----------------|
| [[anthropic]] | 135 | 32 | Dominant source/vendor anchor |
| [[guardrails]] | 111 | 14 | Safety layer; injection detail moved to [[prompt-injection]] |
| [[context-engineering]] | 107 | 18 | Context, caching, cost, and session hub |
| [[claude]] | 96 | 15 | Model-family anchor; current vs. legacy lineup |
| [[agent-harness]] | 96 | 19 | Runtime, loop mechanics, and cross-vendor convergence |
| [[claude-code]] | 93 | — | Anthropic's main worked example |
| [[agent-orchestration]] | 92 | 24 | Multi-agent patterns and the human review limit |
| [[agent-evals]] | 90 | — | Evals, verification, and eval integrity |
| [[tool-design]] | 85 | 22 | Tool interfaces, scaling, and placement |
| [[agent-skills]] | 70 | — | Skill types, architecture, and maintenance |
| [[openai]] | 55 | 14 | Secondary vendor anchor |
| [[openai-codex]] | 46 | — | OpenAI's harness and coding agent |

"—" means the page was not in June's top ten.

## Full-vault graph caveats

Obsidian may show more noise than the wiki-only graph because the repository
also contains root docs, templates, and raw source files. In particular:

- `index.md` and `log.md` are navigation/bookkeeping pages, so they become
  artificial high-outbound hubs in the full graph.
- `raw/` contains markdown files with the same basenames as `wiki/sources/`
  pages (45 of 47 as of 2026-10-12). If raw files are included in Obsidian's graph, source
  nodes can look duplicated or ambiguous.
- `templates/` used to contain placeholder wikilink examples such as `source-a`
  and `concept-b`; these have been converted to plain placeholder text so they
  no longer create fake graph nodes.

## Bottom-right disconnected component

The disconnected component at the bottom right of the earlier Obsidian graph was
template/schema noise, not a research cluster. It was made from:

- `templates/source.md`, `templates/entity.md`, `templates/concept.md`, and
  `templates/synthesis.md`;
- placeholder wikilinks that were embedded in those templates, such as `source-a`,
  `source-b`, `source-name`, `entity-a`, `entity-b`, `concept-a`, `concept-b`,
  `concept-c`, `related-concept`, `other-entity`, and `other-source`;
- schema/root docs that reused the same example wikilinks, such as `CLAUDE.md`
  and local agent-instruction files visible to Obsidian.

Those nodes floated separately because they were examples for future pages, not
links to real pages in `wiki/`. The nearby isolated node
`anthropic-harnessing-claudes-intelligence` is the raw capture at
`raw/anthropic-harnessing-claudes-intelligence.md`; the connected, summarized
wiki page is [[harnessing-claudes-intelligence]].

After cleanup, the full-vault graph has no unresolved placeholder wikilinks. The
remaining disconnected nodes are singleton files rather than fake clusters:
root/schema docs, templates, README, and the isolated raw capture.

For the clearest graph view, filter the graph to `path:wiki/`. For an even
cleaner concept map, temporarily hide `wiki/sources/` and focus on
`wiki/concepts/`, `wiki/entities/`, and `wiki/synthesis/`.

## What to do next

- ~~Create an MCP concept page.~~ Done 2026-10-12: [[model-context-protocol]].
- Add non-Anthropic sources if the goal is a more balanced graph. OpenAI coverage
  roughly doubled on 2026-10-12, but Anthropic sources still outnumber OpenAI
  ones more than 3 to 1, and no other lab is represented except [[cursor]].
- The five largest concept pages now hold 47–55 inbound links each. If one of
  them starts to cover two topics, split it, as the schema's atomic-pages rule
  requires. [[guardrails]] (environment vs. model layer) is the likeliest
  candidate.

## Sources & pages drawn on

- [[overview]]
- [[agent-building-best-practices-anthropic-vs-openai]]
- [[anthropic]], [[openai]], [[claude]], [[claude-code]], [[claude-agent-sdk]],
  [[claude-managed-agents]], [[openai-agents-sdk]]
- [[agent-design-principles]], [[agent-orchestration]], [[tool-design]],
  [[agent-harness]], [[context-engineering]], [[guardrails]],
  [[agent-skills]], [[agent-steering]], [[agent-evals]],
  [[model-context-protocol]], [[prompt-tuning-axes]]
- [[openai-agents-api]], [[openai-codex]], [[cursor]]
