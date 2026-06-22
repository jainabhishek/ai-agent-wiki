---
title: Obsidian Graph Analysis
type: synthesis
created: 2026-06-22
updated: 2026-06-22
tags: [graph, obsidian, wiki-health, synthesis]
---

# Obsidian Graph Analysis

> Query answer for: "check the Obsidian graph and explain."

## Answer

The meaningful graph is the `wiki/` subgraph, not the whole repository. Within
`wiki/`, the graph is healthy: 35 pages form one connected component, with 408
unique directed wikilinks, 130 reciprocal link pairs, no unresolved internal
wikilinks, and no wiki-only inbound orphans.

The graph is currently centered on **agent-building doctrine**, not on products.
The strongest hubs are [[anthropic]], [[agent-design-principles]],
[[agent-orchestration]], [[tool-design]], [[agent-harness]], and
[[context-engineering]]. This matches the wiki's stated scope: effective LLM
agent design, tools, orchestration, context, harnesses, and guardrails (see
[[overview]]).

## What the clusters mean

- **Source cluster:** the 12 source summaries feed claims into concepts and
  entities. Most sources are Anthropic primary or blog sources, so [[anthropic]]
  is the graph's strongest entity hub.
- **Concept backbone:** [[agent-design-principles]], [[agent-orchestration]],
  [[tool-design]], [[agent-harness]], and [[context-engineering]] are the main
  connective tissue. They bind source evidence to reusable doctrine.
- **Entity cluster:** [[claude]], [[claude-code]], [[claude-agent-sdk]], and
  [[claude-managed-agents]] form the Anthropic product/platform side of the
  graph, while [[openai]] and [[openai-agents-sdk]] anchor the smaller OpenAI
  comparison side.
- **Synthesis layer:** [[agent-building-best-practices-anthropic-vs-openai]]
  acts like a dense cross-linking bridge across entities, concepts, and core
  sources.

## Top internal hubs

| Page | Inbound wiki links | Interpretation |
|------|--------------------|----------------|
| [[anthropic]] | 32 | Dominant source/vendor anchor |
| [[agent-design-principles]] | 24 | Core doctrine page |
| [[agent-orchestration]] | 24 | Central architecture page |
| [[tool-design]] | 22 | High-leverage implementation surface |
| [[agent-harness]] | 19 | Runtime/session architecture hub |
| [[context-engineering]] | 18 | Cross-cutting memory/context hub |
| [[claude]] | 15 | Model-family anchor for Anthropic examples |
| [[guardrails]] | 14 | Safety/control layer |
| [[harnessing-claudes-intelligence]] | 14 | Recurring source for harness/context guidance |
| [[openai]] | 14 | Secondary vendor anchor |

## Full-vault graph caveats

Obsidian may show more noise than the wiki-only graph because the repository
also contains root docs, templates, and raw source files. In particular:

- `index.md` and `log.md` are navigation/bookkeeping pages, so they become
  artificial high-outbound hubs in the full graph.
- `raw/` contains markdown files with the same basenames as several
  `wiki/sources/` pages. If raw files are included in Obsidian's graph, source
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

- Consider creating an MCP concept page later; [[overview]] already names it as
  an open gap.
- Add non-Anthropic sources if the goal is a more balanced graph. The current
  topology reflects the source base: Anthropic is much more densely represented
  than OpenAI.

## Sources & pages drawn on

- [[overview]]
- [[agent-building-best-practices-anthropic-vs-openai]]
- [[anthropic]], [[openai]], [[claude]], [[claude-code]], [[claude-agent-sdk]],
  [[claude-managed-agents]], [[openai-agents-sdk]]
- [[agent-design-principles]], [[agent-orchestration]], [[tool-design]],
  [[agent-harness]], [[context-engineering]], [[guardrails]],
  [[agent-skills]], [[agent-steering]], [[agent-evals]]
