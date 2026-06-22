# Demystifying evals for AI agents — Anthropic Engineering (raw capture)

> Source: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
> Publisher: Anthropic Engineering
> Captured: 2026-06-21 via WebFetch (condensed).

## Types of evals

- **Single-turn** (prompt → response → grade) vs **multi-turn** (agent acts over
  many turns, calls tools, mutates state — much harder to assess).
- Agent evals differ because "mistakes can propagate and compound"; frontier
  models may find unintended solutions that fail the eval but are real improvements.

## Three grader types

- **Code-based** — string match, pass/fail, static analysis, outcome verification,
  tool-call inspection. Fast, cheap, objective, reproducible; brittle to valid
  variation.
- **Model-based (LLM-as-judge)** — rubrics, NL assertions, pairwise comparison.
  Capture nuance; non-deterministic; need calibration with human judgment.
- **Human** — SME review, crowdsourcing, A/B. Gold standard; expensive and slow.

## Building eval sets

- **Start small and real:** 20–50 simple tasks drawn from real failures; convert
  user-reported issues into test cases.
- **Task quality:** two experts independently agree on pass/fail; passable by a
  competent agent; success criteria clear from the description; a reference
  solution proves solvability.
- **Balance/diversity:** test where a behavior should and shouldn't occur; avoid
  class-imbalanced sets.

## What to measure

- **pass@k** (≥1 success in k) vs **pass^k** (all k succeed) — diverge as k grows;
  "by k=10 ... pass@k approaches 100% while pass^k falls to 0%."
- Hierarchy: **task** (inputs + success criteria) → **trials** (attempts) →
  **graders** (score transcripts or outcomes).

## LLM-as-judge

Calibrate with human experts; use structured per-dimension rubrics, not holistic
scores. Give escape routes ("return Unknown" when info is insufficient). Validate
grader accuracy before use. Pitfall: **vague rubrics** → inconsistent judgments.

## Common pitfalls

- **Brittle grading** — grade "what the agent produced, not the path it took";
  don't enforce specific tool sequences.
- **Task ambiguity** — Opus 4.5 went 42% → 95% on CORE-Bench after fixing rigid
  grading + ambiguous specs.
- **Shared state** — trials must start clean; shared state causes correlated
  failures unrelated to capability.
- **Saturation** — at 100% pass there's no signal; target agent weaknesses.

## Development roadmap

1. Extract test cases from dev practice + production failures.
2. Write unambiguous tasks with reference solutions.
3. Build isolated, stable, resetting environments.
4. Combine deterministic checks with model-based graders.
5. Review transcripts to verify grader fairness.
6. Monitor saturation; rotate hard tasks into capability suites.
Treat eval suites like production code (ownership, expert contribution, iteration).

## Agent-type-specific

- **Coding:** unit-test pass/fail + quality rubrics + static analysis.
- **Conversational:** state verification + transcript constraints + tone rubrics.
- **Research:** groundedness + coverage + source quality.
- **Computer use:** DOM/screenshot + backend state inspection.

## Swiss-cheese model

Layer methods so failures missed by one are caught by another: automated evals
(CI/CD), production monitoring, A/B testing, user feedback, transcript sampling,
systematic human studies.
