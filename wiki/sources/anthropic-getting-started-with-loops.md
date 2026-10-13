---
title: "Anthropic: Loop engineering — getting started with loops"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com articles) — Delba de Oliveira, Michael Segner
date: 2026-06-30
source_url: https://claude.com/resources/articles/getting-started-with-loops
source_path: raw/anthropic-getting-started-with-loops.md
tags: [agent-loop, claude-code, verification, stop-conditions, scheduling, token-usage]
---

# Anthropic: Loop engineering — getting started with loops

> The Claude Code team's taxonomy of agent loops: turn-based, goal-based,
> time-based, and proactive. Each type is defined by its trigger, its stop
> condition, and the primitive that runs it.

## Summary

The Claude Code team defines a loop as an agent repeating cycles of work until
a stop condition is met. Each loop type hands off one more piece of the work
to [[claude-code]]. A turn-based loop hands off the check, through
verification skills. A goal-based loop hands off the stop condition, through
`/goal`. A time-based loop hands off the trigger, through `/loop` and
`/schedule`. A proactive loop hands off the prompt itself, by composing those
primitives with auto mode and dynamic workflows. The authors advise starting
with the simplest loop. Quality comes from the system around the loop:
verification, a clean codebase, and a second-agent review. Cost control comes
from clear stop criteria, the right model, and pilots. Published 2026-06-30.
`/schedule` and dynamic workflows were in research preview at that date.

## Key points

- **Turn-based loop.** Each prompt runs the agentic loop: gather, act, check,
  respond. Encode your manual checks as a `SKILL.md` with tools that let
  Claude see and measure the result. The example `verify-frontend-change`
  has four steps: start the dev server, click the change with before/after
  screenshots, require zero new console errors, and audit Core Web Vitals
  through the Chrome DevTools MCP. On any failure, Claude reruns from step 1.
  See [[agent-skills]].
- **Goal-based loop (`/goal`).** When Claude tries to stop, an evaluator model
  checks the user's condition and sends Claude back to work. The loop ends at
  success or at a turn cap. Deterministic criteria, such as tests passed or a
  score threshold, work best. Example: Lighthouse ≥ 90, stop after 5 tries.
- **Time-based loop.** `/loop 5m ...` re-runs a prompt on the local machine.
  `/schedule` moves the loop to the cloud as a routine. This loop suits
  recurring work and polling of external systems, such as PR reviews and CI.
- **Proactive loop.** The trigger is an event or schedule, with no human in
  real time. Route routine work to small models and judgment calls to the
  most capable model. Example: an hourly triage of `#project-feedback`, where
  each fix gets three parallel worktree solutions and an adversarial judge.
  See [[agent-orchestration]] and [[workflow-patterns]].
- **Quality.** Use a second agent with fresh context for code review. When a
  result misses the standard, fix the system, not only that one result.
- **Token control.** Small tasks need no loop. Pilot dynamic workflows before
  large runs, because they can spawn hundreds of agents. Use scripts for
  deterministic steps. Match the routine interval to how often the watched
  system changes. `/usage`, a bare `/goal`, and `/workflows` show spend. The
  post names model and effort choice among the biggest cost levers.

## Connections

- The loop is the same gather, act, verify cycle as in
  [[anthropic-building-agents-claude-agent-sdk]].
- Verification depth: [[anthropic-verification-loops-with-skills]]. Mechanism
  choice: [[anthropic-steering-claude-code]]. Dynamic workflows:
  [[anthropic-harness-for-every-task]]. Review loops:
  [[anthropic-securing-ai-native-sdlc]].
- Loops that run unattended depend on auto mode (see
  [[anthropic-eng-claude-code-auto-mode]], [[guardrails]]).
