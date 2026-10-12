# Quantifying infrastructure noise in agentic coding evals — Anthropic (Engineering blog) (raw capture)

> Source: https://www.anthropic.com/engineering/infrastructure-noise
> Publisher: Anthropic (Engineering blog) · Date: 2026-02-05
> Captured: 2026-10-12 via WebFetch (condensed).

Author: Gian Segato. Contributors: Nicholas Carlini, Jeremy Hadfield, Mike Merrill, Alex Shaw.

## Introduction (untitled)

- The infrastructure setup alone can move agentic coding benchmark scores
  (SWE-bench, Terminal-Bench) by several points — sometimes more than the gap
  between top models on a leaderboard.
- Internal result: the most- and least-resourced Terminal-Bench 2.0 setups
  differed by 6 percentage points (p < 0.01).
- In agentic evals the model works inside a full environment, so the runtime
  shapes how it solves the task. Resource budgets and time limits are part of
  the test, not neutral plumbing.

## How we got here

- Anthropic ran Terminal-Bench 2.0 on a Google Kubernetes Engine (GKE) cluster.
  Scores did not match the official leaderboard; up to 6% of tasks failed from
  pod errors mostly unrelated to the task itself.
- Cause: enforcement. Per-task resource specs were applied as both a guaranteed
  floor and a hard kill ceiling. The leaderboard's sandboxing provider allows
  temporary over-allocation, which avoids spurious kills.
- Experiment: six resource configurations, from strict 1x enforcement to
  uncapped; model, harness, and task set held constant.
- Infra error rate fell at every step: 5.8% at 1x → 0.5% uncapped. The 1x→3x
  drop was significant (p < 0.001).
- Scores from 1x through 3x stayed within noise (p = 0.40); tasks that crashed
  at 1x mostly would have failed anyway.
- Above ~3x, success rose faster than infra errors fell. Uncapped gave +6 points
  over 1x (p < 0.01), enabling strategies such as large dependency installs and
  memory-heavy test runs. `rstan-to-pystan` and `compile-compcert` gained
  notably from more memory.

## How this affects measurement

- Up to ~3x: extra resources mostly fix reliability (transient spikes). The
  eval becomes more stable, not easier.
- Above ~3x: extra resources let the agent solve problems it otherwise could
  not. The limit then changes *what* the benchmark measures.
- Tight limits reward lean, efficient strategies; generous limits reward agents
  that exploit heavy resources. Example `bn-fit-modify`: installing the full
  Python data-science stack works with generous memory but runs out under tight
  limits; a standard-library-only approach avoids the problem. Models default to
  different strategies, so the configuration decides which ones succeed.
- The direction replicated across Anthropic models (magnitude varied); likely
  similar for non-Claude models but not rigorously tested.
- SWE-bench check: 227 problems × 10 samples, RAM up to 5x baseline. Score rose
  monotonically with RAM but only +1.54 points at 5x vs 1x — expected, since
  these tasks are less resource-intensive.

## Other sources of variance

- Time limits matter in some configurations.
- Also: cluster health, hardware specs, concurrency, egress bandwidth.
- Anecdotally, pass rates varied with time of day, likely from API latency under
  changing traffic and incidents.
- Model providers can shield their own eval infra with dedicated hardware;
  external evaluators usually cannot.
- Recommendation: run public coding evals at multiple times and on multiple days
  to average out noise.

## What we recommend

- Ideal: identical hardware for both the scaffold and the inference stack —
  often impractical.
- Container runtimes separate a guaranteed allocation from a kill threshold.
  Evals should specify **both values per task**, not one pinned value; a single
  value leaves no headroom for transient spikes.
- Calibrate the gap so the floor-run and ceiling-run scores fall within noise of
  each other.
- Terminal-Bench 2.0: a 3x ceiling cut infra errors 5.8% → 2.1% (p < 0.001)
  while the score lift stayed within noise (p = 0.40).
- The right multiplier is benchmark-specific and should be reported.

## Why we care

- Benchmark scores increasingly drive decisions, but setup and reporting often
  lack rigor; a small lead may reflect capability, hardware, or timing.
- Resource configuration should be a first-class experimental variable, like
  prompt format or sampling temperature.
- Benchmark maintainers should publish recommended specs and the enforcement
  method.
- Until resource methodology is standardized, treat leaderboard differences
  under 3 points with skepticism unless the configuration is documented and
  matched.
- Terminal-Bench numbers: spread across moderate configurations just under 2
  points; binomial confidence intervals already span 1–2 points; extremes
  reached 6 points.

## Acknowledgements

Contributor credits (listed above) and a careers link.
