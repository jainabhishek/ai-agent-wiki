---
title: Agent Evals
type: concept
created: 2026-06-21
updated: 2026-06-21
tags: [evals, measurement, agents, best-practices]
---

# Agent Evals

> Evaluation is the feedback loop that makes every other best practice
> actionable: you can't "start simple and add complexity only when it helps"
> without a way to measure *help*. Both labs treat evals as foundational.

## Why evals come first

- [[openai]]'s model-selection loop is eval-driven: baseline with the best model,
  then down-size while evals still pass. (see [[agent-core-components]],
  [[agent-design-principles]])
- [[anthropic]] frames optimization of prompts, tools, and harnesses as
  eval-gated — add complexity only when it demonstrably improves outcomes.

## What to measure (beyond accuracy)

From [[anthropic-eng-writing-tools-for-agents]]: collect **runtime, tool-call
counts, token consumption, and error rates**, not just task success. These reveal
behavioral inefficiency that an accuracy-only score hides.

## Why agent evals are hard

[[anthropic-eng-demystifying-evals]]: in multi-turn agent runs "mistakes can
propagate and compound," and capable models find unintended-but-valid solutions
that brittle graders wrongly fail. Single-turn (prompt→response→grade) is easy;
multi-turn (tools + mutating state) is the real challenge.

## Three grader types

| Grader | Strengths | Weaknesses |
|--------|-----------|------------|
| **Code-based** (string match, pass/fail, static analysis, tool-call/outcome checks) | fast, cheap, objective, reproducible | brittle to valid variation |
| **Model-based** (LLM-as-judge: rubrics, NL assertions, pairwise) | nuance, open-ended tasks | non-deterministic; needs calibration |
| **Human** (SME, crowdsource, A/B) | gold standard | expensive, slow |

## How to build eval sets

- **Start small and real** — 20–50 tasks drawn from real failures and
  user-reported issues, not a perfect dataset.
- **Task quality** — two experts independently agree on pass/fail; passable by a
  competent agent; success criteria clear from the description; a **reference
  solution** proves solvability.
- **Balance** — test where a behavior *should* and *shouldn't* occur.
- Run **programmatically** in simple agentic loops; isolate environments and
  **reset between trials** (shared state causes correlated failures).
- **Verify like a human user** for end-to-end tasks (e.g. browser automation), not
  just unit/API checks — often needs *explicit* prompting. (see
  [[anthropic-eng-effective-harnesses-long-running-agents]])

## What to measure

- Beyond accuracy: **runtime, tool-call counts, token consumption, error rates**.
- **pass@k** (≥1 success in k attempts) vs **pass^k** (all k succeed) — they
  diverge sharply ("by k=10 ... pass@k → 100% while pass^k → 0%"); pick the one
  matching whether you need *ever* vs *always* succeed.
- Hierarchy: **task** → **trials** → **graders** (scoring transcripts or outcomes).

## LLM-as-judge

Calibrate against human experts; use **structured per-dimension rubrics**, not
holistic scores; give escape routes ("return Unknown"); validate grader accuracy
first. Pitfall: **vague rubrics** → inconsistent judgments.

## Pitfalls

- **Brittle grading** — grade "what the agent produced, not the path it took."
- **Task ambiguity** — Opus 4.5 went 42%→95% on CORE-Bench after fixing rigid
  grading and ambiguous specs (an eval bug, not a model bug).
- **Saturation** — 100% pass rate = no signal; target weaknesses.

## Eval with the agent in the loop

A recurring Anthropic move: paste eval **transcripts** back into the model to
diagnose failures and auto-optimize tools and prompts — an applied
evaluator–optimizer ([[workflow-patterns]]). Layer methods (**Swiss-cheese
model**): automated evals + production monitoring + A/B + user feedback +
transcript sampling + human studies.

## Eval recipes by agent type

- **Coding:** unit-test pass/fail + quality rubrics + static analysis.
- **Conversational:** state verification + transcript constraints + tone rubrics.
- **Research:** groundedness + coverage + source quality.
- **Computer use:** DOM/screenshot + backend state inspection.

## Related concepts

- [[agent-design-principles]], [[tool-design]], [[agent-harness]],
  [[workflow-patterns]], [[agent-core-components]]

## Key entities

- [[anthropic]], [[openai]]

## Appears in

- [[anthropic-eng-demystifying-evals]]
- [[anthropic-eng-writing-tools-for-agents]]
- [[anthropic-eng-effective-harnesses-long-running-agents]]

## Contradictions / open questions

- _None recorded. Primary source ([[anthropic-eng-demystifying-evals]]) now
  ingested._
