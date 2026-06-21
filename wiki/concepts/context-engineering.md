---
title: Context Engineering
type: concept
created: 2026-06-21
updated: 2026-06-21
tags: [context, memory, caching, agents, best-practices]
---

# Context Engineering

> Managing what goes into (and stays out of) the model's context window — load the
> right information at the right time, let the agent prune and persist context
> itself, and structure prompts for cache efficiency. A through-line across the
> ingested Anthropic sources.

## Core practices

**Load on demand, not all at once (progressive disclosure).**
Use [[agent-skills]] whose bodies load only when invoked; path-scope rules; keep
CLAUDE.md lean. (see [[agent-steering]], [[anthropic-steering-claude-code]])

**Let the agent manage its own context.**
- Give code execution so the agent **orchestrates actions** and filters/pipes tool
  results without pushing them all through context.
- Use **context editing** to remove stale information.
- Use **subagents** for isolated work whose intermediate results don't return.
(see [[harnessing-claudes-intelligence]], [[agent-orchestration]])

**Let the agent persist context.**
Append-only logs, memory folders, compaction, and strategic summarization let the
agent choose what to remember across sessions — rather than relying solely on
retrieval/RAG infrastructure. The **session** (append-only event log) in
[[claude-managed-agents]] is the durable form of this. (see [[agent-harness]])

**Design for cache hits.**
Order static content first, send updates as messages, don't switch models
mid-session, keep tools stable, and manage cache breakpoints. (see
[[harnessing-claudes-intelligence]])

## Why it matters

Context is the scarce resource in long-running agents. Good context engineering is
what lets a single agent scale (see [[agent-orchestration]]) and is the mechanism
behind "let Claude manage context" — a key part of [[agent-design-principles]].
It also connects back to the LLM-wiki idea this repo is built on: a persistent,
curated artifact beats re-retrieving raw context every turn.

## Related concepts

- [[agent-skills]], [[agent-steering]], [[agent-harness]], [[agent-orchestration]],
  [[agent-design-principles]]

## Key entities

- [[anthropic]], [[claude]], [[claude-managed-agents]]

## Appears in

- [[harnessing-claudes-intelligence]]
- [[anthropic-steering-claude-code]]
- [[anthropic-evolution-of-agentic-surfaces]]

## Contradictions / open questions

- Anthropic has a dedicated "context engineering" engineering post (seen in
  search, not yet ingested) that would deepen this page.
