---
title: "Anthropic: Claude models explained — choosing the best model for your use case"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com articles) — Michael Segner
date: 2026-07-24
source_url: https://claude.com/resources/articles/claude-models-explained-choosing-the-best-model-for-your-use-case
source_path: raw/anthropic-choosing-claude-model.md
tags: [model-selection, cost-per-task, effort, evals, advisor-strategy]
---

# Anthropic: Claude models explained — choosing the best model for your use case

> Anthropic's model-selection guidance: start with the most intelligent
> generally available model and tune effort. Judge by cost per task and your
> own evals.

## Summary

[[anthropic]]'s guide of 2026-07-24 describes the Claude model classes as of
that date. The classes are Mythos/Fable, Opus, Sonnet, and Haiku. Mythos and
Fable are one underlying model in two packages: Mythos for trusted dual-use
cyber and bio work, and Fable with added public-use safeguards. Both require
limited data retention. The default advice is "start smart". You begin with
the most capable generally available model, then lower effort or step down a
class for latency or cost. The post gives two reasons. First, a smarter model
often costs less per task because it needs fewer turns and less thinking.
Second, a small model hides whether a failure comes from the model or from the
setup. The class lineup, access rules (Mythos only under Project Glasswing),
and the advisor figure belong to mid-2026 models. Re-check them against the
current [[claude]] lineup.

## Key points

- **Two directions.** The default is to start at the top and step down. The
  docs also describe starting cheap and moving up until the quality bar is met.
- **Classes differ by difficulty ceiling, not domain.** No class specializes
  in finance or science. Four selection questions: task difficulty, latency
  needs, access constraints, and unit economics.
- **Effort is a second dial.** A higher class at lower effort can be more
  efficient than a smaller model.
- **Opus vs Fable rule:** use Fable where evals show Opus struggling.
  Otherwise Opus's speed and price may win. Larger models are said to show
  more "wisdom, creativity, and writing" at similar benchmark scores.
- **Advisor strategy** (see [[anthropic-advisor-strategy]],
  [[agent-orchestration]]). A cheap executor consults a smarter model only
  when needed. Reported figure (July 2026): on SWE-bench Pro, Sonnet 5 with a
  Fable 5 advisor scores within 10% of Fable 5 at 63% of the price.
- **Benchmarks saturate at the top.** Teams choose between frontier models by
  running real workloads or custom evals built from hard production tasks.
  See [[agent-evals]].

## Connections

- Same cost-per-task argument as [[anthropic-jetbrains-evaluates-fable-5]] and
  the model-sweep section of [[anthropic-anatomy-of-commerce-agents]].
- Per-model prompting guidance is in the model-scoped pages, for example
  [[anthropic-prompting-claude-fable-5-1]] and
  [[anthropic-prompting-claude-opus-5-5]].
- Eval practice: [[anthropic-eng-demystifying-evals]].
