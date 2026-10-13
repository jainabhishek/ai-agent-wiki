---
title: "Anthropic: How Anthropic Enables Self-Service Data Analytics with Claude"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Josh Cherry, Clement Peng, Johanne Jiao, Justin Leder, Chen Chang (Anthropic)
date: 2026-06-03
source_url: https://claude.com/resources/articles/how-anthropic-enables-self-service-data-analytics-with-claude
source_path: raw/anthropic-self-service-data-analytics.md
tags: [case-study, data-analytics, agent-skills, evals, semantic-layer, verification, claude-code]
---

# Anthropic: How Anthropic Enables Self-Service Data Analytics with Claude

> Case study: Anthropic's data team describes its agentic analytics stack (governed
> data, sources of truth, skills, and validation) and the evals and ablations that
> shaped it.

## Summary

Published 2026-06-03 on claude.com articles by five members of the [[anthropic]]
Data Science and Data Engineering team, writing about their own internal system. All
numbers are self-reported. Anthropic says that 95% of business analytics queries are
automated via Claude, at about 95% aggregate accuracy. The post's thesis: analytics
is "not software". There is often one correct answer from one correct source, and no
test proves it. Accuracy is therefore a context and verification problem, not a
code-generation problem. Three failure modes cause most errors: concept–entity
ambiguity, data staleness, and retrieval failure. Each layer of the stack targets one
or more of these failure modes.

## Key points (transferable lessons)

- **Shrink ambiguity before retrieval.** Use a small set of canonical, governed
  datasets and deprecate near-duplicates. Enforce them through tooling, CI, and
  mandate. Without enforcement, governance decays.
- **Sources of truth, ranked by trust.** Semantic layer (the agent must try it
  first), then lineage and table ranking, then the query corpus, then business
  context (a company knowledge graph).
- **Skills as procedural knowledge.** A thin knowledge skill routes to about 30
  per-domain reference files (the answer to retrieval failure). A runbook skill
  encodes an analyst's process and ends in adversarial review sub-agents. Reference
  docs carry grain, exclusions, gotchas, and IF/DO NOT routing triggers (see
  [[agent-skills]]).
- **Colocate skills with what they describe.** Skill docs live in the data-model
  repo. A code-review hook flags model changes that do not touch a skill. About 90%
  of data-model PRs now include a skill change. One canonical source syncs to a
  plugin marketplace, to cloud blobs, and to MCP resources.
- **Eval practice** (see [[agent-evals]]):
  - Pin ground truth to snapshots, or grade the query, not the number.
  - Run affected evals in CI.
  - Store every run as warehouse telemetry: skill version, git SHA, model ID,
    per-assertion results, tokens, and wall-clock.
  - Gate each domain's launch on an eval threshold (about 90% at first).
  - Harvest stakeholder corrections as new evals.
- **Ablate one variable at a time** on a fixed eval set (about one hour per run).
  Record null and negative results.
- **Online checks** (see [[guardrails]]): an adversarial review skill, a provenance
  footer (source tier, freshness, owner), data-quality checks, monitoring of
  semantic-layer share and correction language, and a scheduled agent that turns
  corrections into reference-doc PRs.
- **Appendix.** A skill skeleton with a mandatory semantic-layer-first path, a
  pre-rebutted list of excuses for skipping it, a PII rule (return SQL, not
  results), and a mandatory SQL-reviewer sub-agent with no self-certification.

## Notable claims & data (self-reported)

- Without skills, eval accuracy did not exceed 21%. With skills, it is above 95% in
  aggregate and about 99% in some domains.
- Unmaintained skills drifted from about 95% to about 65% offline accuracy within a
  month.
- Grep access to thousands of prior SQL files moved accuracy by less than 1 point.
  The answer was present in about 80% of the misses, and presence did not predict a
  fix. The bottleneck was structure, not access.
- Adversarial review: +6% accuracy, at +32% tokens and +72% latency.
- Things that did not work:
  - An LLM-bootstrapped semantic layer (net-negative against a human-curated one).
  - A cheaper reviewer model (lost most of the gains, with no real speedup).
  - Doc refinement past three net-negative rounds.
- Eval counts show diminishing returns past a few dozen per topic. That ceiling
  drops with each model generation.
- Silent plausible-but-wrong answers remain unsolved. The mitigations are
  provenance, human sign-off on leadership-bound work, and daily KPI checks.

## Connections

The Slack-facing deployment is [[anthropic-claude-tag-analytics-in-slack]]. Skill
design echoes [[anthropic-lessons-building-claude-code-skills]] and
[[anthropic-verification-loops-with-skills]]. The eval method parallels
[[anthropic-eng-demystifying-evals]] and
[[anthropic-automating-eval-design-hillclimbing]]. A data-agent counterpart from
OpenAI is [[openai-in-house-data-agent]].
