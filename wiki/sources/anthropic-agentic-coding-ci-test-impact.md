---
title: "Anthropic: Agentic Coding Is Straining CI — Scaling Test Impact Analysis"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Sachin Malhotra (Anthropic)
date: 2026-09-14
source_url: https://claude.com/resources/articles/agentic-coding-is-straining-ci-heres-how-we-scaled-test-impact-analysis-at-anthropic
source_path: raw/anthropic-agentic-coding-ci-test-impact.md
tags: [case-study, ci, testing, infrastructure, claude-code, scaling]
---

# Anthropic: Agentic Coding Is Straining CI — Scaling Test Impact Analysis

> An Anthropic engineer's account of how agent-driven code volume overloaded the
> internal test-selection service, and why a stateless redesign beat three
> successive patches.

## Summary

Internal case study published by Anthropic on claude.com (2026-09-14); all
numbers are self-reported. Anthropic says its engineers ship 8x as much code per
quarter as in 2021–2025, Claude authors 80% of it, tests grew 10x, and CI jobs
rose 25x in six months. The deterministic test impact analysis (TIA) service — a
**listener** recording results and a **selector** choosing tests per PR — ran as
a single-writer process and fell behind. Three patches (bigger machine, per-package
sharding, daily restarts) lasted 70 days, 29 days, and under a day. The redesign
made listener workers stateless by appending results to a journal in an in-memory
data store, with a separate consumer rolling it into per-test history. It took one
engineer three weeks (estimated a quarter a year earlier). The author's lesson:
plan for the exponential — assume 25x load within two quarters — and note that
redesigns are now cheap because code writing is not the bottleneck. See
[[claude-code]], [[agent-harness]].

## Key points

- **Agents raise CI load in three ways**: more PRs, more tests, and smaller,
  more granular PRs (Claude's preference), with an activity floor raised by
  overnight/weekend agent pushes but still bursty from human approvals.
- **Targeted test selection helps agents self-verify**: agents need a specific
  set of valid tests more than humans, who can judge which failures apply to
  them. Links to the feedback-loop practice in [[anthropic-eng-claude-code-best-practices]].
- **Stale selector data hurts**: 20 minutes of listener lag can mean tens of
  thousands of unapplied test updates — broken tests hit everyone, flaky reds
  block merges, new or fixed tests do not run.
- **Monitoring agent with persistent context**: a long-running internal Claude
  Tag session pinged the author when lag passed 50,000 jobs and kept the history
  of past efforts; Claude repeatedly recommended the overhaul the team later did.
- **Transferable design rules**: keep state out of the process from the start;
  avoid single-instance critical services you cannot measure or canary;
  instrument services as Claude's "eyes and ears" (e.g. CI jobs in = jobs out)
  so it can hill-climb fixes; v0 designs can target 10–20x perceived scale if
  budget allows.

## Entities

[[anthropic]], [[claude-code]], [[claude]]

## Concepts

[[agent-harness]], [[agent-evals]], [[agent-design-principles]]

## Notable claims & data

- 8x code per engineer per quarter; 80% Claude-authored; 10x tests; 25x CI jobs
  in six months; patches lasted 70 / 29 / <1 days; redesign 3 engineer-weeks.
  All self-reported by Anthropic.
- Claude did post-cutover tuning (journal size, worker count) largely
  autonomously.

## Connections

Companion to [[anthropic-ai-ci-cd-on-call]] (Claude Tag on CI on-call) and the
SDLC-level view in [[anthropic-ai-native-sdlc-playbook]] and
[[anthropic-running-ai-native-engineering-org]]. The "verification is the new
bottleneck" theme matches [[anthropic-datadog-universal-machine-tool]].
