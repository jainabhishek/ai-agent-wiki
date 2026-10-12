---
title: Workflow Patterns
type: concept
created: 2026-06-21
updated: 2026-10-12
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
   A coarse-grained form: parallel isolated cloud sessions, one VM and branch
   per task, merged afterwards. Isolated sessions do not know about each other,
   so split work along file boundaries, merge in a sensible order, and expect
   duplicate problem reports. (see [[anthropic-claude-code-in-the-cloud]])

4. **Orchestrator-workers** — a central LLM dynamically breaks a task into
   subtasks, delegates to worker LLMs, and synthesizes results. Preferred over
   parallelization when subtasks **can't be predicted in advance**. This is the
   workflow analogue of OpenAI's **manager pattern** (see [[agent-orchestration]]).
   Cursor's coding case study adds two constraints: the orchestrator should own
   shared design decisions, and delegated leaves should not independently decide
   the same question. Because workers carry most execution volume, routing and
   decomposition determine total cost. (see
   [[cursor-agent-swarm-model-economics]], [[multi-agent-economics]])

5. **Evaluator-optimizer** — one LLM generates, another evaluates and gives
   feedback in a loop. Best with clear evaluation criteria and where iterative
   refinement measurably helps. Analogous to Anthropic's evaluator–optimizer and
   OpenAI's guardrail/eval loops.
   **Sprint contract:** in Anthropic's planner / generator / evaluator harness
   for multi-hour app builds, the generator and evaluator agree before each
   sprint on what "done" means and how it will be tested, and communicate
   through files. The evaluator fails the sprint if any criterion is under its
   hard threshold. A separate skeptical evaluator was more tractable than a
   self-critical generator. With a later model, sprints were dropped and the
   evaluator moved to a single end pass — the contract is scaffolding to remove
   when the model no longer needs it. (see
   [[anthropic-eng-harness-design-long-running-apps]], [[agent-harness]])

## Dynamic-workflow patterns (Claude Code)

[[anthropic-harness-for-every-task]] names six composable patterns that
[[claude-code]] uses when it writes a task-specific multi-agent harness at run
time. The post lists them by name only; the descriptions and the mapping to
the five patterns below are this wiki's reading, not the post's:

| Dynamic-workflow pattern | What it does | Relation to the five |
|---|---|---|
| **Classify-and-act** | a classifier agent sorts inputs, then a handler acts per class (also used for model routing) | Routing |
| **Fan-out-and-synthesize** | one subagent per unit or claim, results merged | Parallelization (sectioning) when units are known; orchestrator-workers when the orchestrator decides them |
| **Adversarial verification** | a separate agent checks work against a rubric | Evaluator half of evaluator-optimizer, run by a distinct agent to counter self-preferential bias |
| **Generate-and-filter** | produce many candidates, keep those that pass a check | Parallelization (voting) plus an evaluator as a filter |
| **Tournament** | N approaches judged pairwise | Voting with pairwise judging instead of consensus |
| **Loop until done** | repeat until an explicit stop condition holds | Evaluator-optimizer loop or a gated chain, with a hard completion check |

The post motivates splitting work across focused subagents with three failures
of a single plan-and-execute context: agentic laziness (stopping early), self-
preferential bias, and goal drift after compaction. It also composes a
**quarantine** chain: read-only reader agents summarize untrusted input into
structured output, and a separate privileged actor acts only on the summaries
(see [[guardrails]]). Costs are higher, so these suit complex, high-value tasks
(see [[multi-agent-economics]]).

## Composed examples

- **Sequential specialists with refinement loops** — Hexagon runs four
  specialized agents in sequence with refinement loops: prompt chaining plus
  evaluator-optimizer. (see [[openai-one-year-of-responses]])
- **Plan, approve, execute, document** — Codex writes a plan into a Runme
  notebook, waits for human approval, then executes and records decisions; the
  finished notebook is context for the next run. A chain with a human gate.
  (see [[openai-automating-repetitive-work-codex]])

## Why it matters

These patterns are the "composable, simple" middle ground that
[[agent-design-principles]] urges you to exhaust before building a true agent
([[agents-vs-workflows]]). They're predictable, debuggable, and cheap.

## Related concepts

- [[agents-vs-workflows]], [[agent-orchestration]], [[agent-design-principles]],
  [[agent-evals]], [[multi-agent-economics]], [[agent-harness]]

## Key entities

- [[anthropic]], [[claude-code]], [[openai]], [[openai-codex]]

## Appears in

- [[anthropic-building-effective-agents]]
- [[cursor-agent-swarm-model-economics]]
- [[anthropic-harness-for-every-task]]
- [[anthropic-eng-harness-design-long-running-apps]]
- [[anthropic-claude-code-in-the-cloud]]
- [[openai-one-year-of-responses]]
- [[openai-automating-repetitive-work-codex]]

## Contradictions / open questions

- OpenAI doesn't enumerate these workflow patterns by name but its
  single-agent-loop + prompt-templates advice and manager/handoff patterns cover
  much of the same ground. (see [[agent-orchestration]])
