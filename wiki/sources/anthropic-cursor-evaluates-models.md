---
title: "Anthropic: How Cursor knew Claude Fable 5 was ready for the hardest 1% of problems"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com articles); subject Nate Schmidt (Cursor)
date: 2026-07-17
source_url: https://claude.com/resources/articles/working-at-the-frontier-cursor
source_path: raw/anthropic-cursor-evaluates-models.md
tags: [case-study, agent-evals, model-selection, underspecified-prompts, model-routing, coding-agents]
---

# Anthropic: How Cursor knew Claude Fable 5 was ready for the hardest 1% of problems

> Interview case study: Cursor's in-house benchmark of underspecified real
> prompts, trace reading to rule out cheating, and routing by task uncertainty.

## Summary

Anthropic published this profile on claude.com on 2026-07-17. Results are
self-reported by [[cursor]] via Anthropic and are not independently verified.
The model findings compare Claude Fable 5 with an unversioned "Claude Opus" as
of July 2026. Cursor built CursorBench because public benchmark scores stopped
matching how developers received models. Fable 5 scored 72.9% at Max effort,
which the article calls a new high.

## Key points

- **Benchmark the messy prompt.** CursorBench uses real, underspecified prompts.
  One task is a stack trace plus the word "fix". Another names the wrong module
  as broken, to test whether the model challenges a wrong user assumption. The
  model must infer intent, find the root cause, fix, validate, and report. See
  [[agent-evals]].
- **Read traces when scores look too good.** High scores on ambiguous tasks made
  the team suspect cheating, so they read the reasoning traces. They report real
  wins with fewer operations. Related to eval-awareness concerns in
  [[anthropic-eng-eval-awareness-browsecomp]].
- **Open-ended long-horizon probe.** In a space-flight simulator with a
  one-line prompt, Fable 5 first flew a telemetry orbit and then landed in a
  couple of hours. Claude Opus had failed after 12+ hours. Schmidt calls this
  global versus local reasoning. This is one anecdote, not a benchmark.
- **Route by uncertainty, not by task size.** Use cheaper models when the path
  from A to B is known; use the strongest model when B is unknown. Pair it with
  lighter models for routine work. See [[multi-agent-economics]].
- **Agent as coordination aid.** An agent reads a teammate's recent commits and
  flags conflicts before Schmidt edits shared code.

## Connections

Sibling interviews: [[anthropic-balyasny-evaluates-fable-5]],
[[anthropic-jetbrains-evaluates-fable-5]]. Cursor's swarm research:
[[cursor-agent-swarm-model-economics]]. Model guidance:
[[anthropic-prompting-claude-fable-5]]. Entities: [[cursor]], [[anthropic]],
[[claude]].
