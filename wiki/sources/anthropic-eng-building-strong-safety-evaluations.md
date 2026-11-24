---
title: "Anthropic (Eng): Building Strong Safety Evaluations"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Ruth Appel, Evan Frondorf, Jeremy Hadfield, Rebecca Hiscott, Kamya Jagadish, Shayne Longpre, Madeleine Tucker, Brett Wittmershaus (Anthropic Engineering)
date: 2026-11-13
source_url: https://www.anthropic.com/research/building-strong-safety-evaluations
source_path: raw/anthropic-eng-building-strong-safety-evaluations.md
tags: [evals, safety, llm-as-judge, statistics, multi-turn, simulated-users, primary-source]
---

# Anthropic (Eng): Building Strong Safety Evaluations

> Anthropic's method for safety evals — evals that ask whether a model did the
> right thing for a given input, not whether it finished a task. It borrows
> psychology's replication-crisis reforms: construct validity, preregistration,
> grader validation, and full reporting of uncertainty.

## Summary

A safety eval measures a model's propensity to cause or contribute to harm and
how severe that harm would be. It is distinct from the capability evals in
[[anthropic-eng-demystifying-evals]] (footnote 1). Safety claims such as "safer
than its predecessor" are only as sound as the evals behind them, and AI evals
are easy to game, often measure the wrong thing, and are hard to reproduce.
The post groups its recommendations into four stages: **safety first** (a team
of methods and domain experts; run evals in a sandbox with no internet and live
monitoring), **design** (match observational or causal design to the
question; pick the right construct; make results generalize through multi-turn
simulated users and real-world patterns), **run** (internal validity against
contamination, reward hacking, and bad difficulty; grader calibration;
preregistration and sample size), and **report** (full statistics with
confidence intervals, full configuration, responsible disclosure). The three
minimum steps: write down the construct before collecting data, validate the
grader against humans before trusting it, and report uncertainty. See
[[agent-evals]] and [[guardrails]].

## Key points

- **Run evals safely.** Safety evals often run with safeguards off. Cyber-eval
  models may probe the test environment's edges. After its own incidents,
  Anthropic hardened eval environments, paused many internet-enabled evals, and
  added live monitoring for web-search evals. Compare the eval-awareness
  incident in [[anthropic-eng-eval-awareness-browsecomp]].
- **Observational vs causal design.** Most evals only show that two models
  scored differently. A causal claim ("this system prompt made it safer") needs
  one variable changed at a time.
- **Construct validity: refusal is often the wrong construct.** For suicide and
  self-harm, refusing to engage is a failure; a model that refuses everything
  scores perfectly on refusal rate without being safer. Anthropic's multi-turn
  evals report an **appropriate response rate** against an expert rubric per
  risk area. One bad turn fails the whole conversation.
- **Dual use.** In biology and cyber, the appropriate answer helps with the
  legitimate version and withholds operational specifics. Single-turn evals
  pair harmful prompts (maximize **harmless response rate**) with benign prompts
  in the same domain (minimize **refusal rate**).
- **Multi-turn simulated users.** A domain expert writes a specification
  (objectives, tactics, persona, situation, tone, style). The first user turn is
  fixed. A separate Claude model writes later user turns and reacts to the real
  replies. Each scenario runs many times with different dimension combinations.
  A grader model scores each transcript against the rubric. Example: a romance
  scam suite where no single message is a violation but the pattern is.
- **Vary dimensions independently** (cross every severity with every tone), or
  their effects cannot be separated.
- **Build from real patterns** (usage data, red-team transcripts, incident
  reports, clinician interviews), and keep revising the set. Cover languages,
  modalities, product surfaces, harness, and environment; match the eval setup
  to the deployment (tools, system prompt).
- **Internal validity.** Guard against contamination (use post-cutoff or
  synthetic data) and reward hacking (close shortcut paths; randomize
  irrelevant details such as option order). Saturated evals become regression
  checks; make them harder in ways that keep the construct (longer horizons,
  subtler, more natural), not with trick questions. Too-hard evals also fail.
- **Grader calibration.** Graders fail silently and drift when their
  underlying model changes; add alerts. Six practices: simple and objective
  grading with a reference solution per item; atomic, binary criteria with
  explicit "does not count" cases; tell the grader that disclaimers do not make
  harmful content harmless; hide design metadata and stress-test for
  self-preference, length bias, and position bias (flip pairwise order, re-grade
  with another model or rubric); fail loudly by flagging and excluding broken
  items; validate against blind human labels with chance-corrected agreement
  (e.g. Cohen's kappa), benchmarked against human–human agreement.
- **Preregister** metrics, comparisons, slices, and the threshold for an
  improvement or regression. Report deviations.
- **Sample size floors:** 100 items for complex multi-turn evals, 1,000 for
  simpler single-turn evals; run each case several times. Use **paired
  comparisons** (confidence interval on per-item differences) to detect small
  model differences.
- **Report fully:** per-category results (including unchanged ones),
  multiple-comparison correction, confidence intervals on every estimate.
  Record model versions, sampling settings, prompts, grader version, and dates;
  never compare scores from different graders.
- **Run evals continuously** on snapshots throughout fine-tuning, so the
  Safeguards and Model Behavior teams can adjust reward signals or system
  prompts before release. Disclose severe flaws to the developer before
  publishing.
- **Tooling:** UK AI Security Institute's open-source Inspect framework;
  Anthropic's Petri toolkit (built on Inspect) for multi-turn behavioral tests.

## Entities

[[anthropic]], [[claude]]. No page yet: UK AI Security Institute, Inspect,
Petri.

## Concepts

[[agent-evals]], [[guardrails]], [[agent-verification]],
[[boundary-contracts]]

## Notable claims & data

- Single-turn harmless response rates on the API are 94%–98% for every recent
  model, so single-turn sets are saturated.
- Multi-turn API confidence intervals can exceed ±10 percentage points.
- Romance-scams multi-turn eval on claude.ai: Claude Opus 5 98% vs Opus 5.5
  94%, **not statistically significant**, so neither model is called better.
- Claude Fable 5.1: the API vs claude.ai gap on multi-turn safety evals reached
  34 percentage points. On the self-harm eval, a targeted system-prompt
  instruction (do not say self-harm works or helps) and other mitigations gave
  60% on the API vs 94% on claude.ai.
- Single-turn safety suites span 16 policy areas in seven languages across
  several product surfaces.
- An audit of a leading coding benchmark found a substantial share of tasks
  underspecified, missing context, or graded by tests that rejected correct
  solutions. This matches the CORE-Bench task-ambiguity pitfall in
  [[agent-evals]].
- Agrees with the existing [[agent-evals]] guidance on structured
  per-dimension rubrics, a judge model different from the model under test,
  and calibration against human experts. It is softer on the judge model: it
  says "consider" a different model, where
  [[anthropic-automating-eval-design-hillclimbing]] says it must differ.
- Tension with [[anthropic-anatomy-of-commerce-agents]] as cited in
  [[agent-evals]]: that guide uses simulated-user evals only to discover new
  cases; this post makes simulated-user multi-turn runs the headline safety
  metric.

## Connections

- Safety-eval companion to [[anthropic-eng-demystifying-evals]] (capability
  evals), which the post names as its predecessor.
- Grader stability checks and blind pairwise order extend
  [[anthropic-automating-eval-design-hillclimbing]]; the human–human agreement
  baseline adds a method to the open question on judge reliability in
  [[agent-evals]].
- The "fail loudly" grader rule matches the fail-loud rule in
  [[boundary-contracts]].
- Configuration effects (34-point API vs claude.ai gap) parallel the
  resource-configuration effects in [[anthropic-eng-infrastructure-noise-evals]].
- Reward-hacking and contamination warnings echo
  [[anthropic-eng-eval-awareness-browsecomp]] and
  [[anthropic-eng-ai-resistant-evaluations]].
- Sandboxed, monitored eval runs apply the containment view in
  [[anthropic-eng-how-we-contain-claude]].
