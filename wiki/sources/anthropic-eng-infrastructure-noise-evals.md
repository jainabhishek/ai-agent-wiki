---
title: "Anthropic: Quantifying infrastructure noise in agentic coding evals"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Gian Segato (Anthropic Engineering blog)
date: 2026-02-05
source_url: https://www.anthropic.com/engineering/infrastructure-noise
source_path: raw/anthropic-eng-infrastructure-noise-evals.md
tags: [evals, benchmarks, infrastructure, terminal-bench, swe-bench, methodology]
---

# Anthropic: Quantifying infrastructure noise in agentic coding evals

> Anthropic's measurement of how container resource limits alone move agentic
> coding benchmark scores — up to 6 points on Terminal-Bench 2.0 — and its
> recommendation to treat resource configuration as a reported experimental
> variable.

## Summary

In an agentic eval the model works inside a full environment, so the runtime is
part of the test. Anthropic found its Terminal-Bench 2.0 scores on a GKE cluster
diverged from the public leaderboard because per-task resource specs were
enforced as both a guaranteed floor and a hard kill ceiling, killing up to 6% of
tasks on pod errors. Holding model, harness, and tasks fixed, it swept six
resource configurations from strict 1x to uncapped. Up to ~3x headroom, extra
resources fix reliability (infra errors 5.8% → 2.1%) without changing the score
(p = 0.40). Beyond ~3x, extra resources let agents use strategies that are
otherwise impossible (large installs, memory-heavy tests), so the limit changes
*what is measured*; uncapped scored +6 points over 1x (p < 0.01). SWE-bench was
far less sensitive (+1.54 points at 5x RAM). The post recommends specifying a
floor and a separate kill ceiling per task, calibrating the gap so floor and
ceiling scores sit within noise, reporting the multiplier, and running evals at
several times and days. See [[agent-evals]].

## Key points

- **Resources are part of the task.** Tight limits reward lean strategies;
  generous limits reward agents that exploit heavy resources. On
  `bn-fit-modify`, a full data-science-stack install succeeds only with generous
  memory; a stdlib-only approach succeeds under tight limits. Different models
  default to different strategies, so the config picks winners.
- **Two regimes.** ≤ ~3x: reliability fixes, score unchanged. > ~3x: capability
  unlock, score rises (`rstan-to-pystan`, `compile-compcert` most affected).
- **Specify floor and ceiling separately.** A single pinned value gives no
  headroom for transient spikes. Terminal-Bench 2.0's calibrated ceiling was 3x;
  the right multiplier is benchmark-specific.
- **Other variance sources:** time limits, cluster health, hardware, concurrency,
  egress bandwidth, and time-of-day API latency. Providers can isolate their own
  eval infra; external evaluators usually cannot.
- **Reporting norm:** treat resource configuration like prompt format or
  sampling temperature — a first-class variable. Benchmark maintainers should
  publish recommended specs and enforcement method.

## Entities

[[anthropic]], [[claude]]

## Concepts

[[agent-evals]], [[agent-harness]]

## Notable claims & data

- Terminal-Bench 2.0: 6-point spread between most- and least-resourced setups
  (p < 0.01); infra errors 5.8% (1x) → 0.5% (uncapped).
- Moderate-config spread just under 2 points; binomial CIs already span 1–2
  points. Post's rule of thumb: leaderboard gaps **under 3 points** warrant
  skepticism unless resource config is documented and matched.
- SWE-bench: 227 problems × 10 samples, RAM to 5x → +1.54 points.
- Effect replicated across Anthropic models in direction (not magnitude); not
  rigorously tested on non-Claude models.

## Connections

Extends the eval-methodology guidance in [[anthropic-eng-demystifying-evals]]
with an infrastructure axis: environment and harness configuration confound
capability measurement, the same point [[anthropic-eng-effective-harnesses-long-running-agents]]
makes about harness design shaping outcomes. Relevant to any comparison of model
results across vendors or harnesses (e.g. [[cursor-agent-swarm-model-economics]]).
