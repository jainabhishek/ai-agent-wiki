---
title: "Anthropic (Eng): Harness Design for Long-Running Application Development"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Prithvi Rajasekaran (Anthropic Labs)
date: 2026-03-24
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
source_path: raw/anthropic-eng-harness-design-long-running-apps.md
tags: [harness, long-running, multi-agent, evaluator, verification, primary-source]
---

# Anthropic (Eng): Harness Design for Long-Running Application Development

> A planner / generator / evaluator harness for multi-hour autonomous app
> builds, with cost and time data, and a record of which components became
> unnecessary as models improved.

## Summary

The author starts from the two-agent harness (initializer + coding agent) and
names two remaining failures: **context loss** (Sonnet 4.5 "context anxiety";
context resets with handoffs fixed it, compaction alone did not) and
**self-evaluation** (agents praise their own mediocre work). A separate,
skeptical, tunable evaluator was more tractable than a self-critical generator.
The GAN-inspired generator–evaluator loop first targets frontend design with
four gradable criteria, then scales to full-stack apps with a planner,
generator, and evaluator. See [[agent-harness]] and [[agent-orchestration]].

## Key points

- **Make subjective quality gradable.** Criteria: design quality, originality,
  craft, functionality; the first two weighted higher. The evaluator is
  calibrated with few-shot examples and score breakdowns and uses Playwright MCP
  on live pages. Criteria wording visibly steers output style.
- **Planner** expands a 1–4 sentence prompt into a product spec; stays
  high-level to avoid cascading technical errors.
- **Generator** builds one feature per sprint (React, Vite, FastAPI,
  SQLite/PostgreSQL), uses git.
- **Evaluator** clicks through the app with Playwright and checks UI, API, and
  DB state; any criterion under its hard threshold fails the sprint.
- **Sprint contract.** Generator and evaluator agree on "done" and the test
  before each sprint. Agents communicate through files.
- **Every component encodes an assumption** about what the model cannot do;
  remove components one at a time when a new model ships. With Opus 4.6:
  sprints dropped, planner kept (generator under-scoped without it), evaluator
  moved to a single end pass.

## Entities

[[anthropic]], [[claude]], [[claude-agent-sdk]]

## Concepts

[[agent-harness]], [[agent-orchestration]], [[agent-evals]],
[[context-engineering]], [[workflow-patterns]], [[agent-design-principles]],
[[multi-agent-economics]]

## Notable claims & data

- Retro game maker, Opus 4.5: solo run 20 min / $9 with the core play feature
  broken; full harness 6 h / $200 (over 20x) with a 16-feature spec over 10
  sprints and a working play mode. Sprint 3 had 27 criteria.
- Browser DAW, updated harness: about 4 h (table sums to 3 h 50 min), $124.70;
  build round 1 alone 2 h 7 min / $71.08; QA rounds $3–4 each. The builder ran
  coherently for 2+ hours without sprints; QA still found stubbed recording and
  non-movable clips.
- Frontend runs: 5–15 iterations, up to 4 hours; scores rise then plateau.
- Early evaluators approved flawed work; the QA prompt needed several tuning
  rounds.
- The evaluator's value depends on whether the task is beyond what the model
  does reliably alone.

## Connections

- Successor to [[anthropic-eng-effective-harnesses-long-running-agents]]. That
  post: initializer + coding agent, structured JSON feature list,
  `claude-progress.txt`, Puppeteer MCP verification, and an open question about
  generalist vs. specialized QA agents. This post answers part of that
  question: a **separate evaluator agent** beats generator self-checking; it
  adds a planner, sprint contracts, gradable criteria, and cost data. It also
  replaces context resets with continuous compaction once Opus 4.5 removed
  context anxiety.
- The context-anxiety history matches
  [[anthropic-evolution-of-agentic-surfaces]] and
  [[anthropic-eng-scaling-managed-agents]].
- Applies the "start simple" rule of [[anthropic-building-effective-agents]] and
  its evaluator-optimizer pattern ([[workflow-patterns]]).
- The 20x cost for higher quality is a data point for [[multi-agent-economics]].
