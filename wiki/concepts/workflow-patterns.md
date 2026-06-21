---
title: Workflow Patterns
type: concept
created: 2026-06-21
updated: 2026-06-21
tags: [workflows, patterns, anthropic, architecture]
---

# Workflow Patterns

> [[anthropic]]'s five composable building blocks for agentic systems. Reach for
> these before a full agent — most needs are met by one or a combination. (see
> [[anthropic-building-effective-agents]])

## The five patterns

1. **Prompt chaining** — decompose into a fixed sequence of steps; each LLM call
   processes the prior output. Add programmatic **gates** between steps to
   validate progress. Best when a task cleanly decomposes; trades latency for
   accuracy.

2. **Routing** — classify the input and direct it to a specialized follow-up.
   Enables separation of concerns and prompts optimized per category. Best with
   distinct, accurately classifiable categories.

3. **Parallelization** — run work concurrently in two modes:
   - *Sectioning* — split a task into independent subtasks run in parallel.
   - *Voting* — run the same task multiple times for diverse outputs / consensus.
   Good for speed or when multiple perspectives raise confidence.

4. **Orchestrator-workers** — a central LLM dynamically breaks a task into
   subtasks, delegates to worker LLMs, and synthesizes results. Preferred over
   parallelization when subtasks **can't be predicted in advance**. This is the
   workflow analogue of OpenAI's **manager pattern** (see [[agent-orchestration]]).

5. **Evaluator-optimizer** — one LLM generates, another evaluates and gives
   feedback in a loop. Best with clear evaluation criteria and where iterative
   refinement measurably helps. Analogous to Anthropic's evaluator–optimizer and
   OpenAI's guardrail/eval loops.

## Why it matters

These patterns are the "composable, simple" middle ground that
[[agent-design-principles]] urges you to exhaust before building a true agent
([[agents-vs-workflows]]). They're predictable, debuggable, and cheap.

## Related concepts

- [[agents-vs-workflows]], [[agent-orchestration]], [[agent-design-principles]]

## Key entities

- [[anthropic]]

## Appears in

- [[anthropic-building-effective-agents]]

## Contradictions / open questions

- OpenAI doesn't enumerate these workflow patterns by name but its
  single-agent-loop + prompt-templates advice and manager/handoff patterns cover
  much of the same ground. (see [[agent-orchestration]])
