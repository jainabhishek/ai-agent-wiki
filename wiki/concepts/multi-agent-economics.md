---
title: Multi-Agent Economics
type: concept
created: 2026-07-21
updated: 2026-10-12
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

### Three designs for mixing models

1. **Frontier planner, cheaper workers.** The frontier model decomposes the
   work and cheaper models execute the packets. (see
   [[anthropic-eng-multi-agent-research-system]],
   [[cursor-agent-swarm-model-economics]]) Block reports that frontier tokens
   concentrate in upfront planning, with no quality drop as work shifts to Opus
   or Sonnet workers. (see [[anthropic-block-orchestrates-fable]])
2. **One model, no planner.** The C compiler run used no routing; the lever was
   verifier quality. (see [[anthropic-eng-building-c-compiler]])
3. **Cheap executor, frontier advisor.** The cheaper model runs the whole loop
   and owns tools and output. It consults the frontier model only at decisions
   it cannot resolve, and the advisor returns a plan, a correction, or a stop
   signal. There is no decomposition or worker pool, so frontier tokens are
   spent only on escalations. Anthropic frames this as the inverse of
   orchestrator-worker. (see [[anthropic-advisor-strategy]],
   [[anthropic-choosing-claude-model]], [[agent-orchestration]])

### Model per pipeline stage

Guidance and case studies converge on matching model strength to the cost of an
error at each stage, not to the size of the task:

- **Strongest model where errors propagate or the path is unknown.** Balyasny
  reports that it runs planning and analysis on its strongest model because
  mistakes there flow into every downstream deliverable. Cursor reports that it
  routes by uncertainty: a cheaper model when the path from A to B is known, the
  strongest model when B is unknown. (see [[anthropic-balyasny-evaluates-fable-5]],
  [[anthropic-cursor-evaluates-models]])
- **Cheaper model where a check fully covers the output.** Anthropic's
  modernization guidance puts a cheaper model on mechanical work that the
  machine-checkable certificate verifies, and stronger models on hard
  transformations and adversarial review. (see [[anthropic-ai-code-modernization]])
- **Cheaper model only where a misread is cheap to spot.** Anthropic's Claude
  Code cost guidance gives cheaper models lookups and log reading, never code
  edits,
  because the main model pays for any detour a misread causes. (see
  [[anthropic-what-a-task-costs-opus-5-5]], [[anthropic-claude-code-session-cost]])
- **Reported stage splits (self-reported case studies).** Kepler reports a
  frontier model for decomposition and plans and a cheaper model for
  constrained high-throughput stages. Caylent reports a small model for
  high-volume parsing and a mid-tier model for synthesis. Wondr Health reports
  separate models for coaching, escalation detection, and the eval judge.
  CodeRabbit reports three tiers (orchestration, step sequencing, narrow
  distillation) chosen by eval results on cost and latency. ABC Legal reports a
  mid-tier default, a small model for volume, and a frontier model for deep
  reasoning, with a model swap as a one-line config change. (see
  [[anthropic-kepler-verifiable-ai]], [[claude-customer-caylent]],
  [[claude-customer-wondr-health]], [[anthropic-coderabbit-agent-orchestration]],
  [[anthropic-abc-legal-managed-agents]])

## Evidence

- **Token multipliers depend on the baseline.** Anthropic's research system used
  about 15x the tokens of *chat*. Anthropic's multi-agent guide says multi-agent
  systems typically use 3–10x the tokens of a *single agent* on the same task.
  Anthropic's Claude Code cost guidance, citing the costs docs, says agent teams
  in plan mode use about 7x the tokens of a *standard Claude Code session*. The
  three figures use different baselines and are not comparable. (see
  [[anthropic-eng-multi-agent-research-system]],
  [[anthropic-building-multi-agent-systems]],
  [[anthropic-what-a-task-costs-opus-5-5]])
- In a role-split experiment (planner, implementer, tester, reviewer), Anthropic
  found that subagents spent more tokens on coordination than on work. (see
  [[anthropic-building-multi-agent-systems]])
- Anthropic's advisor benchmarks report higher scores at lower cost per task for
  a cheap executor plus a frontier advisor than for the executor alone. The
  figures use earlier model generations, and the headline coding comparison is
  confounded by different thinking and prompt settings. (see
  [[anthropic-advisor-strategy]])
- Anthropic's research system used about 15× the tokens of chat while beating a
  single-agent baseline by 90.2% on breadth-first research; token usage explained
  roughly 80% of performance variance. (see
  [[anthropic-eng-multi-agent-research-system]])
- Cursor found that workers consumed at least 69% of tokens and more than 90% in
  most SQLite runs. Similar-quality configurations differed greatly in cost, and
  a planner that used fewer of its own tokens still caused a more expensive run
  through higher worker consumption. (see
  [[cursor-agent-swarm-model-economics]])
- Anthropic's planner / generator / evaluator harness built a retro game maker
  in about 6 h for about $200; a solo run of the same model took 20 min and $9.
  The harness cost over 20x more, but only the harness run produced a working
  core play feature. A later browser-DAW build cost $124.70 over about 4 h; the
  first build round alone was $71.08, while each QA round cost $3–4. (see
  [[anthropic-eng-harness-design-long-running-apps]])
- Claude Code dynamic workflows show the token scale of a per-task multi-agent
  harness: a `review-changes` run used 14 agents and 482k tokens in 6m 12s; a
  `deep-research` run used 22 agents and 1.1M tokens in 11m 3s. Anthropic
  positions them for complex, high-value tasks, not routine coding, and suggests
  setting token caps in the prompt. (see [[anthropic-harness-for-every-task]])
- Parallel isolated cloud sessions consume plan limits in parallel (5 sessions ≈
  5x the rate) and can duplicate discovery work, because sessions do not know
  about each other. (see [[anthropic-claude-code-in-the-cloud]])

- **One model, no planner, verifier as the lever.** The C compiler run used 16
  agents of one model, about 2,000 sessions over two weeks, about 2B input and
  140M output tokens, and just under $20,000. It had no planner and no model
  routing; the effective lever was verifier and test-harness quality, not
  worker routing. Its dollar figure is not comparable with the Cursor figures
  above, which come from different tasks, models, and accounting. (see [[anthropic-eng-building-c-compiler]])

## Evaluation rule

Compare configurations on **cost per accepted outcome**. Include planner,
worker, reviewer, retry, and cache usage plus wall time, conflicts, code churn,
human correction, and end-to-end success. A cheaper call is not an improvement
if it moves cost downstream or lowers reliability. (see [[agent-evals]])

The same rule applies to a single model choice. Anthropic's model guidance, its
commerce-agent guidance, and its Claude Code cost guidance all measure cost per
completed task, not price per token. A smarter model can cost less per task
because it needs fewer turns, and a retry costs more than the savings from a
smaller model or lower effort. JetBrains reports the same result on its private
evals for complex long-running work. (see [[anthropic-choosing-claude-model]],
[[anthropic-anatomy-of-commerce-agents]], [[anthropic-what-a-task-costs-opus-5-5]],
[[anthropic-jetbrains-evaluates-fable-5]]) To test an advisor design, run the
existing eval suite on three configurations: executor alone, executor with
advisor, and advisor model alone. (see [[anthropic-advisor-strategy]])

## Practical implications

- Use frontier intelligence for decomposition, shared design decisions, hard
  trade-offs, and review only when evals justify it.
- Route bounded, high-volume leaves to the least expensive model that still
  passes their acceptance criteria.
- Start with a single agent. Go multi-agent only for context protection,
  parallelism, or specialization, because each extra agent adds coordination
  tokens. (see [[anthropic-building-multi-agent-systems]],
  [[anthropic-subagents-in-claude-code]])
- Cap fan-out and stop when marginal coverage no longer earns its token and
  coordination cost.
- Give shared-state systems an explicit termination rule: a time budget, no new
  findings over N cycles, or a judge agent. Without a coordinator, reactive
  loops between agents otherwise keep spending. (see
  [[anthropic-multi-agent-coordination-patterns]])
- Before you escalate work to a stronger model, measure the retry rate of the
  cheaper one. A pilot run gives the token cost floor. (see
  [[anthropic-ai-code-modernization]]) When you escalate inside a session,
  switch back at a natural break, because a model switch rewrites the prompt
  cache. (see [[anthropic-what-a-task-costs-opus-5-5]])
- Spend on a separate evaluator only when the task is beyond what the model does
  reliably alone; in the app-build harness, QA rounds were a small share of cost
  compared with build rounds. (see
  [[anthropic-eng-harness-design-long-running-apps]])
- Re-evaluate the entire harness when models change; prompts and scaffolding
  optimized for one model may be inefficient or unstable for another. (see
  [[agent-harness]])

## Related concepts

- [[agent-orchestration]], [[workflow-patterns]], [[agent-harness]],
  [[context-engineering]], [[agent-evals]], [[agent-design-principles]]

## Appears in

- [[anthropic-eng-multi-agent-research-system]]
- [[cursor-agent-swarm-model-economics]]
- [[anthropic-eng-harness-design-long-running-apps]]
- [[anthropic-harness-for-every-task]]
- [[anthropic-claude-code-in-the-cloud]]
- [[anthropic-eng-building-c-compiler]]
- [[anthropic-advisor-strategy]]
- [[anthropic-building-multi-agent-systems]]
- [[anthropic-multi-agent-coordination-patterns]]
- [[anthropic-subagents-in-claude-code]]
- [[anthropic-what-a-task-costs-opus-5-5]]
- [[anthropic-claude-code-session-cost]]
- [[anthropic-choosing-claude-model]]
- [[anthropic-anatomy-of-commerce-agents]]
- [[anthropic-ai-code-modernization]]
- [[anthropic-kepler-verifiable-ai]]
- [[anthropic-block-orchestrates-fable]]
- [[anthropic-balyasny-evaluates-fable-5]]
- [[anthropic-cursor-evaluates-models]]
- [[anthropic-jetbrains-evaluates-fable-5]]
- [[anthropic-coderabbit-agent-orchestration]]
- [[anthropic-abc-legal-managed-agents]]
- [[claude-customer-caylent]]
- [[claude-customer-wondr-health]]

## Contradictions / open questions

- Published results use different tasks, harnesses, and accounting methods;
  cross-study model or price comparisons are not valid without a shared eval.
- The "frontier planner plus cheaper workers" design is not the only one that
  works: the C compiler run had no planner and no routing ([[anthropic-eng-building-c-compiler]]),
  and the advisor design inverts it, with the cheap model in charge
  ([[anthropic-advisor-strategy]], 2026-04-09). Block (2026-10-08) reports that
  frontier-planner orchestration is the first case where "always use the
  frontier model" is not the answer ([[anthropic-block-orchestrates-fable]]).
  No shared eval compares the three designs, so the evidence does not say
  which is cheaper per accepted outcome.
- **Small models for edits.** [[anthropic-what-a-task-costs-opus-5-5]]
  (2026-09-25) says to use Sonnet or Haiku for lookups and log reading, never
  for code edits. The same post notes that Claude Code's `opusplan` alias puts
  edits on Sonnet, which contradicts that advice, and says to measure it first. Several case studies above route execution to cheaper
  models. Whether edits are safe on a cheaper model appears to depend on how
  fully a check covers them (see [[anthropic-ai-code-modernization]]); no
  source tests this directly.
