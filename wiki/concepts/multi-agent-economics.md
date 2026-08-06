---
title: Multi-Agent Economics
type: concept
created: 2026-07-21
updated: 2026-07-21
tags: [multi-agent, economics, routing, tokens, evals]
---

# Multi-Agent Economics

> Optimize the cost of a successful agent system, not the price or token count
> of any one model call.

## Role-aware economics

Orchestrator-worker systems concentrate ambiguity in a small number of planning
decisions and volume in worker execution. A frontier model can be economical as
a planner when it turns uncertainty into explicit work packets that less
expensive models can execute. The planner is still an upstream cost multiplier:
poor decomposition creates duplicate work, retries, conflicts, and excess worker
tokens. (see [[anthropic-eng-multi-agent-research-system]],
[[cursor-agent-swarm-model-economics]], [[agent-orchestration]],
[[workflow-patterns]])

## Evidence

- Anthropic's research system used about 15× the tokens of chat while beating a
  single-agent baseline by 90.2% on breadth-first research; token usage explained
  roughly 80% of performance variance. (see
  [[anthropic-eng-multi-agent-research-system]])
- Cursor found that workers consumed at least 69% of tokens and more than 90% in
  most SQLite runs. Similar-quality configurations differed greatly in cost, and
  a planner that used fewer of its own tokens still caused a more expensive run
  through higher worker consumption. (see
  [[cursor-agent-swarm-model-economics]])

## Evaluation rule

Compare configurations on **cost per accepted outcome**. Include planner,
worker, reviewer, retry, and cache usage plus wall time, conflicts, code churn,
human correction, and end-to-end success. A cheaper call is not an improvement
if it moves cost downstream or lowers reliability. (see [[agent-evals]])

## Practical implications

- Use frontier intelligence for decomposition, shared design decisions, hard
  trade-offs, and review only when evals justify it.
- Route bounded, high-volume leaves to the least expensive model that still
  passes their acceptance criteria.
- Cap fan-out and stop when marginal coverage no longer earns its token and
  coordination cost.
- Re-evaluate the entire harness when models change; prompts and scaffolding
  optimized for one model may be inefficient or unstable for another. (see
  [[agent-harness]])

## Related concepts

- [[agent-orchestration]], [[workflow-patterns]], [[agent-harness]],
  [[context-engineering]], [[agent-evals]], [[agent-design-principles]]

## Appears in

- [[anthropic-eng-multi-agent-research-system]]
- [[cursor-agent-swarm-model-economics]]

## Contradictions / open questions

- Published results use different tasks, harnesses, and accounting methods;
  cross-study model or price comparisons are not valid without a shared eval.
