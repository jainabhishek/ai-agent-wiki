---
title: Agent Orchestration
type: concept
created: 2026-06-21
updated: 2026-06-21
tags: [orchestration, multi-agent, single-agent, patterns]
---

# Agent Orchestration

> How to structure execution once you've chosen an agent: the run loop, when to
> stay single-agent, and the two multi-agent patterns. Both guides agree:
> **maximize a single agent first.** (see [[openai-practical-guide-to-building-agents]],
> [[agent-design-principles]])

## The agent run loop

Every orchestration needs a **run** — a loop that lets the agent operate until an
**exit condition**: a final-output tool, a structured output of a given type, an
error, or a maximum number of turns. In the [[openai-agents-sdk]], `Runner.run()`
loops the LLM until a final-output tool fires or the model replies with no tool
calls. (see [[openai-practical-guide-to-building-agents]])

[[anthropic]]'s agents work the same way: plan → act via tools → observe
environmental ground truth → repeat, with stopping conditions and guardrails.
(see [[anthropic-building-effective-agents]])

In production, the loop is realized as a durable **session** — an append-only log
of every model call, tool call, and result — with the harness (brain) separated
from the execution sandbox (hands). See [[agent-harness]] and
[[anthropic-evolution-of-agentic-surfaces]].

## Single-agent systems

A single agent handles many tasks by **incrementally adding tools**, keeping
evaluation and maintenance simple. To manage complexity without splitting:
use a single flexible **prompt template** with policy variables rather than many
bespoke prompts. (see [[openai-practical-guide-to-building-agents]])

**When to split into multiple agents:**
- **Complex logic** — prompts full of if-then-else branches that don't scale.
- **Tool overload** — driven by tool *overlap*, not count (see [[tool-design]]).

**Subagents** are a lightweight form of multi-agent: they run in an isolated
context window and return only a final summary, keeping the main thread clean.
Use them for deep search, log analysis, or audits whose intermediate results you
won't reference again; they can nest several levels and orchestrate many
background agents, with plans/results held in script variables rather than
context. (see [[anthropic-steering-claude-code]], [[context-engineering]])

## Multi-agent patterns (OpenAI)

- **Manager (agents as tools)** — a central manager LLM delegates to specialized
  agents via tool calls and synthesizes results. Best when one agent should keep
  control and user contact. Mirrors Anthropic's **orchestrator-workers**
  ([[workflow-patterns]]).
- **Decentralized (handoffs)** — peer agents transfer execution to one another; a
  handoff is a one-way tool call that passes conversation state. Best for triage
  and when a specialist should fully take over.

Both can be modeled as graphs (agents = nodes; edges = tool calls or handoffs).
The guiding principle across patterns: keep components **flexible, composable,
and driven by clear prompts.**

## Declarative vs. code-first

OpenAI contrasts **declarative graph** frameworks (define every branch/loop
upfront) with the [[openai-agents-sdk]]'s **code-first** approach (express logic
with normal programming constructs). Echoes Anthropic's caution about framework
abstraction in [[agent-design-principles]].

## Related concepts

- [[workflow-patterns]], [[agent-core-components]], [[tool-design]],
  [[agent-design-principles]], [[guardrails]], [[agent-harness]],
  [[context-engineering]]

## Key entities

- [[openai]], [[openai-agents-sdk]], [[anthropic]], [[claude-code]],
  [[claude-managed-agents]]

## Appears in

- [[openai-practical-guide-to-building-agents]]
- [[anthropic-building-effective-agents]]
- [[anthropic-steering-claude-code]]
- [[anthropic-evolution-of-agentic-surfaces]]

## Contradictions / open questions

- _None — the manager pattern and orchestrator-workers describe the same shape
  from the agent and workflow vocabularies respectively._
