---
title: "Anthropic (Eng): Demystifying Evals for AI Agents"
type: source
created: 2026-06-21
updated: 2026-06-21
author: Anthropic Engineering
date: 2025
source_url: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
source_path: raw/anthropic-eng-demystifying-evals.md
tags: [evals, measurement, agents, best-practices, primary-source]
---

# Anthropic (Eng): Demystifying Evals for AI Agents

> The primary-source playbook for evaluating agents: grader types, building real
> eval sets, the pass@k vs pass^k distinction, and the pitfalls that make evals
> lie. The foundation for [[agent-evals]].

## Summary

Agent evals are hard because **mistakes propagate and compound** across turns and
models find unintended-but-valid solutions. Use three grader types
(code / model / human), start with 20–50 tasks from real failures, measure with
non-determinism in mind, and treat eval suites like production code. Deepens
[[agent-evals]].

## Key points

- **Grader taxonomy:** code-based (fast/objective/brittle), model-based
  (LLM-as-judge; nuanced/non-deterministic), human (gold standard/slow).
- **Build real, small, balanced sets:** two experts agree; reference solution
  proves solvability; test both should- and shouldn't-occur cases.
- **pass@k vs pass^k:** diverge sharply as k grows — pick the metric that matches
  whether you need *ever* succeed vs *always* succeed.
- **Grade outcomes, not the path** — don't enforce tool sequences.
- **Pitfalls:** vague rubrics, task ambiguity (Opus 4.5: 42%→95% after fixes),
  shared state across trials, eval saturation.
- **Swiss-cheese model:** layer automated evals + monitoring + A/B + feedback +
  transcript sampling + human studies.

## Concepts

[[agent-evals]], [[agent-design-principles]], [[tool-design]], [[agent-harness]]

## Entities

[[anthropic]], [[claude]]

## Notable claims & data

- "By k=10, [pass@k and pass^k] tell opposite stories." Non-determinism is
  central to agent measurement.
- Ambiguous specs + brittle grading understate capability — an eval-quality bug,
  not a model bug. Reinforces "grade what was produced."

## Connections

The measurement backbone under [[agent-design-principles]] (eval-gated
complexity) and the tool/harness eval advice in
[[anthropic-eng-writing-tools-for-agents]] and
[[anthropic-eng-effective-harnesses-long-running-agents]].
