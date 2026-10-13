---
title: "Anthropic: How JetBrains evaluates and deploys Claude Fable 5"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com articles)
date: 2026-08-13
source_url: https://claude.com/resources/articles/how-jetbrains-evaluates-and-deploys-claude-fable-5
source_path: raw/anthropic-jetbrains-evaluates-fable-5.md
tags: [case-study, evals, model-selection, private-evals, cost-per-task, security, data-retention]
---

# Anthropic: How JetBrains evaluates and deploys Claude Fable 5

> Customer interview (case study) on how JetBrains evaluates frontier models on
> private repositories and when it chooses Claude Fable 5 over Opus.

## Summary

Published by [[anthropic]] on 2026-08-13 as an interview with Vladislav
Tankov (JetBrains CTO, Agent Systems). All results are self-reported by
JetBrains on its own private eval suite. The benchmark figures compare Claude
Fable 5 with Claude Opus 4.8 as of August 2026; readers should check whether
they still hold for current models. The transferable method: evaluate on
private repositories to detect benchmark-tuned models, and rank models by cost
per task, not price per token.

## Key points

- **Private-repo evals.** JetBrains runs large eval sets on private
  repositories, including its monorepo, to check whether public benchmark
  scores hold on real work. See [[agent-evals]].
- **Three leaderboards:** best quality, best cost per task, fastest model.
- **Cost per task over price per token.** Fable 5 is pricier per token but
  cheaper per task in some cases, mostly complex long-running work.
- **Reported numbers (Fable 5 vs Opus 4.8, Aug 2026):** Python pass rate 44.3%
  vs 28.2%; 18 tasks won vs 2 lost head-to-head; about 22% fewer steps; higher
  test-pass rate when code ran; on Java, Fable 5 skipped unhelpful outside
  resource fetches that Opus 4.8 kept attempting.
- **Model roles.** Opus as the dependable workhorse; Fable 5 for hard
  reasoning and long-running experiments, such as spec-to-app builds and
  near-black-box ports between runtimes or languages. The agent can write the
  spec from an existing app.
- **Safety posture.** JetBrains builds its safety net in the infrastructure and
  [[agent-harness]], not in the model. It uses Fable 5 for white-box security
  testing of its own products. It accepts limited data retention for
  classifier review of serious flagged cases, though it would prefer zero
  retention. See [[guardrails]].

## Connections

- Same "measure on your own work" stance as
  [[anthropic-eng-demystifying-evals]] and [[anthropic-choosing-claude-model]].
- Sibling evaluation case studies: [[anthropic-cursor-evaluates-models]],
  [[anthropic-balyasny-evaluates-fable-5]].
- Entities: [[anthropic]], [[claude]].
