---
title: "Anthropic: How Block orchestrates Claude Fable across thousands of pull requests"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Anthropic (claude.com articles); interview with Bradley Axen (Block)
date: 2026-10-08
source_url: https://claude.com/resources/articles/how-block-orchestrates-claude-fable-across-thousands-of-pull-requests
source_path: raw/anthropic-block-orchestrates-fable.md
tags: [case-study, multi-agent, orchestration, model-routing, code-migration, guardrails]
---

# Anthropic: How Block orchestrates Claude Fable across thousands of pull requests

> Customer interview: a frontier model plans company-wide code migrations and
> directs dozens of cheaper worker models, while merges and deploys stay behind
> a two-human approval gate.

## Summary

Published by Anthropic on claude.com (2026-10-08) as an interview with Bradley
Axen, Head of AI Capabilities at Block; claims are self-reported. Block uses
**Claude Fable 5** as orchestrator for migrations of hundreds to thousands of
PRs: a human engineer steers, Fable designs data models, API specs, and
algorithms, and it directs up to dozens of Opus or Sonnet workers that edit
files and run tests. Axen reports frontier tokens concentrate in upfront
planning with no quality drop as work shifts to workers. The setup runs on Buzz,
Block's open-source workspace for humans and agents. Findings are tied to the
Fable 5 / Opus 5 generation as of October 2026.

## Key points

- **Frontier planner, cheap workers.** Model orchestration is the first case
  Axen has seen where "always use the frontier model" is not the answer.
- **Model × effort grid.** Block benchmarks each use case on every model at every
  effort level; effort levels behave like different models, not a linear dial.
  It is building an auto-selector to set defaults per task.
- **Hard gates for irreversible actions.** Merges to main, production deploys,
  and feature flags need security checks plus two human approvers.
- **Secure by default:** remote workstations, network allowlists, and cheap
  out-of-loop checks (regex, small classifiers) built into work interfaces.
- **Permit low-risk actions** (opening PRs, code review, log and analytics
  queries) and rely on model-level safeguards there; Block benchmarks whether
  Claude refuses to bypass dual approval.
- **Recurring maintenance agents** sweep a ~1M-line codebase daily or weekly
  for cleanup.
- **System-level context.** Capture individuals' skills and knowledge centrally
  so every agent run gets it.

## Notable claims & data

- A single migration may merge about a thousand Fable-orchestrated PRs.
- Engineers may work with ~45 concurrent agents; single-conversation tools do
  not scale to that.

## Concepts

[[human-agent-teams]]

## Connections

[[anthropic]], [[claude]], [[claude-code]]. Concepts: [[agent-orchestration]],
[[multi-agent-economics]], [[guardrails]], [[prompt-tuning-axes]],
[[agent-skills]]. Related: [[cursor-agent-swarm-model-economics]] (planner and
worker token split), [[anthropic-advisor-strategy]] (the inverse: cheap executor
escalates), [[anthropic-choosing-claude-model]],
[[anthropic-slack-human-agent-teams]], [[anthropic-ai-code-modernization]],
[[anthropic-prompting-claude-fable-5]].
