---
title: "Anthropic: Introducing advanced tool use on the Claude Developer Platform"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Bin Wu et al. (Anthropic Engineering blog)
date: 2025-11-24
source_url: https://www.anthropic.com/engineering/advanced-tool-use
source_path: raw/anthropic-eng-advanced-tool-use.md
tags: [tools, tool-use, mcp, context-engineering, code-execution, claude-api, beta]
---

# Anthropic: Introducing advanced tool use on the Claude Developer Platform

> Launch post for three beta API features — Tool Search Tool, Programmatic Tool
> Calling, and Tool Use Examples — each aimed at one bottleneck of agents with
> large tool libraries: definition bloat, intermediate-result bloat, and
> parameter errors.

## Summary

The post argues that agents need access to hundreds or thousands of tools
without loading every definition into context (a five-server MCP setup already
costs ~55K tokens; Anthropic has seen 134K). It ships three features behind beta
header `advanced-tool-use-2025-11-20`:

1. **Tool Search Tool** — tools marked `defer_loading: true` are sent to the API
   but kept out of the initial context; Claude searches (regex, BM25, or a
   custom search such as embeddings) and only matching definitions load. ~85%
   fewer definition tokens; prompt caching is preserved.
2. **Programmatic Tool Calling** — tools opted in via `allowed_callers` become
   Python functions inside `code_execution_20250825`; Claude writes code that
   calls them, filters results, and returns only the final output. One code
   block replaces many inference passes.
3. **Tool Use Examples** — an `input_examples` array of concrete sample calls in
   the tool definition teaches formats, conventions, and parameter correlations
   that JSON Schema cannot express.

Best-practice framing: layer features by bottleneck rather than enabling all.
See [[tool-design]] and [[context-engineering]].

## Key points

- **Selection by bottleneck:** definition bloat → Tool Search; large
  intermediate results → Programmatic Tool Calling; parameter errors → Tool Use
  Examples.
- **Tool Search when:** definitions > ~10K tokens, 10+ tools, multiple MCP
  servers, or selection-accuracy problems. Keep the 3–5 most-used tools always
  loaded; whole MCP servers can be deferred via `mcp_toolset`. Names and
  descriptions must be search-friendly (`search_customer_orders`, not
  `query_db_orders`).
- **Programmatic Tool Calling when:** 3+ dependent calls, large datasets where
  only aggregates matter, parallel fan-out. Not when Claude must reason over
  every intermediate result. Document return formats precisely; opt in only
  parallel-safe / idempotent tools. Code-issued calls carry a `caller` field;
  only `code_execution_tool_result` enters context.
- **Tool Use Examples when:** nested structures, many optional params,
  domain conventions, near-duplicate tools (`create_ticket` vs
  `create_incident`). Use 1–5 realistic examples spanning minimal, partial, and
  full calls.

## Entities

[[anthropic]], [[claude]]

## Concepts

[[tool-design]], [[context-engineering]], [[agent-harness]],
[[agent-core-components]]

## Notable claims & data

Figures are Anthropic's own. Named models: Opus 4 and Opus 4.5 (Tool Search
accuracy only); the sample request uses `claude-sonnet-4-5-20250929`; other
figures name no model.

- Tool Search: ~77K → ~8.7K definition tokens for 50+ tools (−85%); MCP-eval
  accuracy Opus 4 49% → 74%, Opus 4.5 79.5% → 88.1%.
- Programmatic Tool Calling: avg tokens 43,588 → 27,297 (−37%) on complex
  research tasks; internal knowledge retrieval 25.6% → 28.5%; "GIA" benchmarks
  (as written) 46.5% → 51.2%; budget example ~200KB raw → ~1KB returned.
- Tool Use Examples: complex-parameter accuracy 72% → 90%.
- **Tension with later guidance:** [[anthropic-new-rules-context-engineering-claude-5]]
  (Jul 2026) reports that for Claude 5-generation models, tool usage examples
  narrow exploration and recommends designing expressive interfaces instead.

## Connections

Productizes the code-as-tool-orchestration idea of
[[anthropic-eng-code-execution-with-mcp]] (credited, along with LLMVM and
Cloudflare's Code Mode). Extends the tool-writing guidance in
[[anthropic-eng-writing-tools-for-agents]] and the just-in-time loading of
[[anthropic-eng-context-engineering]]. Deferred tool loading reappears as
`ToolSearch` inside [[claude-code]] per [[anthropic-new-rules-context-engineering-claude-5]].
