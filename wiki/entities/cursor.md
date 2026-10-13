---
title: Cursor
type: entity
subtype: org-product
created: 2026-07-21
updated: 2026-10-12
tags: [cursor, coding-agents, multi-agent, evals, model-selection]
---

# Cursor

> AI coding product and publisher of practitioner research on coding-agent
> harnesses and multi-agent coordination.

## Overview

In this wiki, [[cursor]] contributes a large-scale coding case study rather than
a general agent-building guide. [[cursor-agent-swarm-model-economics]] reports
how its experimental swarm changed after adding task-tree decomposition,
coordination mechanisms, shared memory, and stacked review.
[[anthropic-cursor-evaluates-models]] (2026-07-17) describes how Cursor
evaluates new models.

## Key facts

- Frames planner-worker decomposition as a context-efficiency mechanism, not
  merely a way to run more work in parallel. (see
  [[cursor-agent-swarm-model-economics]])
- Reports model-routing economics at the system level, including how planner
  behavior changes downstream worker consumption. (see
  [[multi-agent-economics]])
- Built specialized version-control and reconciliation infrastructure for an
  experiment operating far beyond normal human Git throughput. (see
  [[cursor-agent-swarm-model-economics]])

### How Cursor evaluates models (self-reported)
- **CursorBench.** Cursor built an in-house benchmark because public scores
  stopped matching how developers received models. It uses real,
  underspecified prompts: one task is a stack trace plus the word "fix";
  another names the wrong module as broken, to test whether the model
  challenges a wrong user assumption. The model must infer intent, find the
  root cause, fix, validate, and report. Cursor reports Claude Fable 5 at 72.9%
  at Max effort (July 2026). (see [[anthropic-cursor-evaluates-models]],
  [[agent-evals]])
- **Read traces when scores look too good.** High scores on ambiguous tasks
  made the team suspect cheating, so it read the reasoning traces before it
  accepted the result. (see [[anthropic-cursor-evaluates-models]])
- **Route by uncertainty.** Cursor uses cheaper models when the path to the
  goal is known and the strongest model when it is not. (see
  [[anthropic-cursor-evaluates-models]], [[multi-agent-economics]])
- OpenAI's long-horizon Codex post quotes Cursor's "Scaling agents" post as
  saying OpenAI models drift less on extended autonomous work; this is a
  vendor-quoted third-party claim. (see [[openai-run-long-horizon-tasks-codex]])

## Appears in

- [[cursor-agent-swarm-model-economics]]
- [[anthropic-cursor-evaluates-models]]
- [[openai-run-long-horizon-tasks-codex]]

## Contradictions / open questions

- Cursor's SQLite experiment is not yet replicated across tasks or ordinary Git
  workflows; the generality of its coordination mechanisms remains open.
- CursorBench is in-house, and the evaluation results come through an Anthropic
  customer profile, not from Cursor directly. They are not independently
  verified. (see [[anthropic-cursor-evaluates-models]])
