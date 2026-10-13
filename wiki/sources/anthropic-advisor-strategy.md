---
title: "Anthropic: The advisor strategy"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com articles)
date: 2026-04-09
source_url: https://claude.com/resources/articles/the-advisor-strategy
source_path: raw/anthropic-advisor-strategy.md
tags: [multi-agent, model-routing, cost, advisor-tool, claude-platform, api]
---

# Anthropic: The advisor strategy

> Product announcement for the Claude Platform advisor tool: a cheaper executor
> model runs the whole agent loop and escalates hard decisions to a frontier
> advisor model inside the same API request.

## Summary

Anthropic (claude.com articles, 2026-04-09, no byline) describes the "advisor
strategy": Sonnet or Haiku executes the task end to end, and consults Opus only
when it reaches a decision it cannot resolve. The advisor reads the shared
context and returns a plan, a correction, or a stop signal. It never calls tools
and never writes user-facing output. Anthropic frames this as the inverse of the
orchestrator-worker pattern: the small model drives, and there is no
decomposition, worker pool, or orchestration code. The post announces the
server-side **advisor tool** (beta) that implements the hand-off inside one
`/v1/messages` call.

All benchmark numbers are Anthropic's own and use **Sonnet 4.6 and Haiku 4.5 as
executors with Opus 4.6 as advisor**, as of April 2026. Those models predate the
5-series; whether the gains hold for current models is not stated. The customer
quotes (Bolt, Genspark, Eve Legal) are self-reported.

## Key points

- **Pattern.** Executor owns tools, iteration, and output; advisor gives guidance
  only. Frontier tokens are spent only on escalations.
- **API.** Tool type `advisor_20260301`, fields `name`, `model`, `max_uses`.
  Beta header `anthropic-beta: advisor-tool-2026-03-01`. The executor decides
  when to call; the platform routes curated context to the advisor and returns
  the plan in the same request.
- **Cost model.** Each model's tokens bill at its own rate. Advisor output is
  typically 400–700 text tokens per consultation. `max_uses` caps calls per
  request; advisor usage is reported separately in the `usage` block.
- **Evaluation advice.** Run the existing eval suite on three configurations:
  executor solo, executor + advisor, and advisor model solo.

## Entities

[[anthropic]], [[claude]]

## Concepts

[[multi-agent-economics]], [[agent-orchestration]], [[tool-design]],
[[agent-evals]]

## Notable claims & data

- SWE-bench Multilingual: Sonnet 4.6 + Opus 4.6 advisor scored +2.7 points over
  Sonnet 4.6 solo, at 11.9% lower cost per task. **Confound:** per the footnote,
  the solo run used adaptive thinking while the advisor run had thinking off and
  a suggested coding system prompt, so the cost and score deltas are not a pure
  advisor effect.
- BrowseComp: Haiku 4.5 + advisor 41.2% vs 19.7% solo; 29% below Sonnet 4.6 solo
  in score at 85% lower cost per task. 1,266 problems, one attempt each.
- Terminal-Bench 2.0: Sonnet + advisor scored higher at lower cost than Sonnet
  solo (no figure given). 89 tasks, 5 attempts each.
- Eve Legal (self-reported): Haiku 4.5 consulting Opus 4.6 matched frontier
  quality on structured document extraction at 5x lower cost.

## Connections

- Adds a third design to the open question in [[multi-agent-economics]]: besides
  frontier-planner-plus-cheap-workers ([[anthropic-eng-multi-agent-research-system]],
  [[cursor-agent-swarm-model-economics]]) and no-planner runs
  ([[anthropic-eng-building-c-compiler]]), a cheap executor can escalate upward.
- Contrasts with [[anthropic-block-orchestrates-fable]], where the frontier model
  orchestrates and cheaper models do the edits.
- Genspark's quote links to [[claude-customer-genspark]]. Model-choice framing in
  [[anthropic-choosing-claude-model]]; single-vs-multi-agent decision in
  [[anthropic-building-multi-agent-systems]].
