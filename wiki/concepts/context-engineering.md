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

## Definition & why it matters

[[anthropic-eng-context-engineering]] defines it as "curating and maintaining the
optimal set of tokens (information) during LLM inference" — the evolution beyond
prompt engineering, spanning system instructions, tools, external data, and
message history. It matters because of **context rot**: "as the number of tokens
in the context window increases, the model's ability to accurately recall
information from that context decreases" (n² attention + sparse training on long
sequences). Treat context as **finite and precious**. Governing maxim: **find the
smallest set of high-signal tokens that maximize the likelihood of your desired
outcome.**

## System-prompt altitude

Aim between **brittle** (hardcoded if-else in the prompt) and **vague** (overly
general). Organize into sections (XML tags / Markdown headers); start minimal with
your best model and add only to fix identified failures; "minimal does not
necessarily mean short." Closely related to [[agent-steering]] and
[[agent-instructions]].

## Retrieval: just-in-time vs pre-loading

- **Just-in-time** — hold lightweight identifiers (paths, queries, URLs) and load
  at runtime; metadata (folders, names, timestamps) guides behavior; progressive
  disclosure. e.g. Claude Code uses `head`/`tail` instead of loading whole files.
- **Pre-loading** (embeddings) — faster but risks staleness/indexing complexity.
- **Hybrid (recommended)** — some upfront, the rest explored autonomously.
This is the same "persistent curated artifact > re-retrieve raw context" intuition
behind the LLM-wiki idea this repo implements.

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

## The three long-horizon techniques

For work exceeding a single context window ([[anthropic-eng-context-engineering]]):
1. **Compaction** — summarize near the limit and reinitialize; preserve decisions,
   open bugs, key details; discard redundant tool outputs. Tune recall-first, then
   precision. Clearing old tool-call results is the lightest touch.
2. **Structured note-taking (agentic memory)** — persist notes outside context and
   reload on demand (e.g. the file-based memory tool; Claude playing Pokémon
   tracking objectives/maps across resets).
3. **Sub-agent architectures** — sub-agents explore with large context and return
   ~1–2k-token summaries to a focused coordinator. See [[agent-orchestration]].

Selection: compaction for heavy back-and-forth; note-taking for milestone-based
iterative work; multi-agent for complex parallel research.

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
  [[agent-design-principles]], [[tool-design]], [[agent-instructions]]

## Key entities

- [[anthropic]], [[claude]], [[claude-managed-agents]], [[claude-code]]

## Appears in

- [[anthropic-eng-context-engineering]]
- [[harnessing-claudes-intelligence]]
- [[anthropic-steering-claude-code]]
- [[anthropic-evolution-of-agentic-surfaces]]

## Contradictions / open questions

- _Primary source now ingested ([[anthropic-eng-context-engineering]]). Remaining
  depth would come from the memory-tool and compaction feature docs._
