---
title: "Anthropic: Harnessing Claude's Intelligence"
type: source
created: 2026-06-21
updated: 2026-06-21
author: Anthropic (Claude blog)
date: 2026-04-02
source_url: https://claude.com/blog/harnessing-claudes-intelligence
source_path: raw/anthropic-harnessing-claudes-intelligence.md
tags: [agents, harness, context-engineering, tools, best-practices]
---

# Anthropic: Harnessing Claude's Intelligence

> Three patterns for building Claude apps/agents that stay good as the model
> improves — and a recurring instruction to *delete* harness scaffolding the
> model has outgrown.

## Summary

The post's frame is **harness–model co-evolution**: build on durable foundations,
periodically ask what you can stop doing, and set boundaries deliberately. See
[[agent-harness]] and [[context-engineering]].

## Key points

1. **Use what Claude knows** — prefer general-purpose tools (bash, text editor)
   the model keeps getting better at, over bespoke interfaces. Higher-level
   features (programmatic tool calling, skills, memory) compose from these. See
   [[tool-design]].
2. **Ask "what can I stop doing?"** — let Claude orchestrate actions (code
   execution to filter/pipe tool results off the context window), manage context
   (skills, context editing, subagents), and persist context (compaction, memory
   folders, summarization). See [[context-engineering]], [[agent-orchestration]].
3. **Set boundaries carefully** — design for cache hits (static-first ordering,
   stable models/tools, breakpoints); use declarative tools only where security,
   UX, or observability require.

## Concepts

[[agent-harness]], [[context-engineering]], [[tool-design]],
[[agent-orchestration]], [[agent-design-principles]]

## Entities

[[anthropic]], [[claude]]

## Notable claims & data

- "Claude 3.5 Sonnet reached 49% on SWE-bench Verified with only a bash tool and
  a text editor tool" — evidence for the general-purpose-tools thesis.
- "Assumptions about what Claude can't do need to be re-tested with each step
  change in its capability." Prune dead weight (e.g. old context resets).

## Connections

The principle layer beneath [[anthropic-evolution-of-agentic-surfaces]] (harness
co-evolution) and [[anthropic-steering-claude-code]] (context mechanisms).
Extends [[agent-design-principles]] with a "delete scaffolding" corollary.
