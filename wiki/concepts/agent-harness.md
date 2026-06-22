---
title: Agent Harness
type: concept
created: 2026-06-21
updated: 2026-06-21
tags: [harness, architecture, agents, sessions, best-practices]
---

# Agent Harness

> The harness is the scaffolding around the model — the loop, tool wiring, context
> management, and execution environment that turn a model into an agent. Two
> ingested Anthropic sources argue the harness must **co-evolve with the model**
> and should stay as thin as the model allows.

## Definition

The code that calls the model, manages its context, executes its tool calls, and
decides when a run ends. Historically hand-rolled ("tokens in, tokens out"), then
tuned in SDKs ([[claude-agent-sdk]], [[openai-agents-sdk]]), then partly delegated
to managed platforms ([[claude-managed-agents]]). (see
[[anthropic-evolution-of-agentic-surfaces]])

## Brain–hands separation

A durable production pattern: run the **harness (brain)** separately from the
**sandbox (hands)** where code/tools execute, connected by a **session** — an
append-only log of every model call, tool call, and result. Yields parallel
spin-up latency wins, credential isolation (vaults outside the sandbox), and
resumable, auditable runs. This is the concrete form of the run-loop / exit-
condition idea in [[agent-orchestration]] and the persistence idea in
[[context-engineering]].

## Harness–model co-evolution

The central best practice: **re-test your harness assumptions with every model
upgrade, and delete scaffolding the model has outgrown.**
- Example: Sonnet 4.5 "context anxiety" (rushing near the context limit) led teams
  to add context resets; Opus 4.5 removed the behavior, making those resets pure
  overhead. (see [[anthropic-evolution-of-agentic-surfaces]])
- The general rule from [[harnessing-claudes-intelligence]]: "Assumptions about
  what Claude can't do need to be re-tested with each step change in its
  capability." Prefer general-purpose tools and let the model do more
  ([[tool-design]], [[agent-design-principles]]).

**Implication:** delegate harness tuning to the platform/SDK where you can, and
spend your effort on domain expertise, tools, and context — not on maintaining a
custom loop.

## Concrete long-running patterns

From the case study in [[anthropic-eng-effective-harnesses-long-running-agents]]:
- **Two-agent pattern** — a one-time **initializer** (environment, spec file, git,
  progress file) and a per-session **coding agent** doing one feature at a time.
- **Structured JSON state** the agent only partially edits (flip a "passes" field)
  — models inappropriately edit Markdown more readily than JSON.
- **Session startup sequence** — `pwd` → read git log + progress → pick top
  incomplete feature → smoke-test → implement, to avoid re-establishing context.
- **Verify like a human user** (e.g. browser automation), but only reliably once
  *explicitly* prompted. See [[agent-evals]].
- **Failure modes to design against:** premature completion, half-finished
  features, undocumented progress, code-only (non-end-to-end) verification.

## Related concepts

- [[agent-orchestration]], [[context-engineering]], [[agent-design-principles]],
  [[tool-design]], [[agent-core-components]], [[agent-evals]]

## Key entities

- [[anthropic]], [[claude]], [[claude-agent-sdk]], [[claude-managed-agents]]

## Appears in

- [[anthropic-evolution-of-agentic-surfaces]]
- [[harnessing-claudes-intelligence]]
- [[anthropic-eng-effective-harnesses-long-running-agents]]
- [[anthropic-eng-context-engineering]]

## Contradictions / open questions

- _None — strongly consistent with the start-simple / prune-complexity theme._
