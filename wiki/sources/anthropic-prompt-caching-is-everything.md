---
title: "Anthropic: Lessons from Building Claude Code — Prompt Caching Is Everything"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Thariq Shihipar (Anthropic, Claude Code team)
date: 2026-04-30
source_url: https://claude.dev/blog/lessons-from-building-claude-code-prompt-caching-is-everything/
source_path: raw/anthropic-prompt-caching-is-everything.md
tags: [prompt-caching, claude-code, harness, context-engineering, compaction, tool-design]
---

# Anthropic: Lessons from Building Claude Code — Prompt Caching Is Everything

> A Claude Code engineer's account of how the [[claude-code]] harness is laid
> out around prompt caching: prefix ordering, state changes as messages,
> stable tools and models, deferred tool loading, and cache-safe compaction.

## Summary

The post argues that prompt caching is what makes long-running agent products
economically viable, and that the [[agent-harness]] must be designed around it
from day one. Caching is a prefix match up to each `cache_control`
breakpoint, so any change early in the request invalidates everything after
it. Claude Code orders content static-first (system prompt and tools, then
CLAUDE.md, then session context, then messages), sends changing state as
`<system-reminder>` messages instead of prompt edits, never swaps models or
tool sets mid-session, models plan mode as tools (`EnterPlanMode` /
`ExitPlanMode`), and defers MCP tool schemas with `defer_loading` stubs plus
tool search. Compaction is done as a "cache-safe fork" that reuses the
parent's exact prefix. The team monitors cache hit rate like uptime and treats
drops as incidents (SEVs). Source date: 2026-04-30 byline. (raw §§ all)

## Key points

- **Prefix order:** static system prompt + tools (global) → CLAUDE.md
  (project) → session context (session) → conversation. Past breakages: a
  detailed timestamp in the system prompt, non-deterministic tool ordering,
  editing the Agent tool's list of callable agents. (raw: Lay out your prompt)
- **Updates as messages:** stale facts (time, edited files) go into the next
  user message or tool result inside `<system-reminder>`. (raw: Use messages)
- **No model switches mid-session:** caches are per model; at 100k tokens an
  Opus→Haiku switch costs more than staying. Use a subagent with a hand-off
  message instead (Claude Code's Haiku-based Explore agents). (raw: Don't
  change models)
- **No tool add/remove mid-session:** tools are in the prefix. Plan mode keeps
  all tools and is itself a pair of tools, so the model can enter plan mode
  autonomously without a cache break. (raw: Never add or remove tools)
- **Defer, don't remove:** `defer_loading: true` name-only stubs in fixed
  order; full schemas load on selection via tool search (also an API tool).
  See [[tool-design]].
- **Cache-safe forking for compaction:** reuse the parent's system prompt,
  contexts, tools, and messages, then append the compaction instruction as a
  new user message; reserve a "compaction buffer" for the instruction and the
  summary output. A naive separate summarizer call pays full uncached price
  for the whole conversation. See [[context-engineering]].
- **Lessons (5):** prefix match; messages over prompt edits; stable tools and
  models; monitor hit rate like uptime; forks (compaction, summarization,
  skill execution) must share the parent prefix.

## Entities

[[anthropic]], [[claude-code]], [[claude]]

## Concepts

[[context-engineering]], [[agent-harness]], [[tool-design]],
[[agent-orchestration]], [[agent-design-principles]]

## Notable claims & data

- A cache hit is priced at one tenth of the uncached input price; the example
  compaction summary is about 20k tokens. (raw: cache-safe forking, figure)
- A few percentage points of cache miss rate change cost and latency
  materially; Claude Code declares SEVs on hit-rate drops. (raw: Lessons)
- High hit rates are what allow more generous subscription rate limits.
- Confirms and expands the "design for cache hits" principle already in
  [[context-engineering]] and [[agent-design-principles]] (sourced there to
  [[harnessing-claudes-intelligence]]); no contradiction found.

## Connections

Companion to [[anthropic-seeing-like-an-agent]] (same author; that post
explains plan-mode tools and why ExitPlanTool exists). Grounds the caching
advice in [[harnessing-claudes-intelligence]] and the compaction strategy in
[[anthropic-eng-context-engineering]]. Deferred tool loading relates to
[[anthropic-eng-advanced-tool-use]]. Contrast with OpenAI's server-side
compaction in [[openai-shell-skills-compaction]].
