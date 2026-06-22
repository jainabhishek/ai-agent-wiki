---
title: "Anthropic (Eng): Effective Harnesses for Long-Running Agents"
type: source
created: 2026-06-21
updated: 2026-06-21
author: Anthropic Engineering
date: 2025
source_url: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
source_path: raw/anthropic-eng-effective-harnesses-long-running-agents.md
tags: [harness, agents, long-running, verification, primary-source]
---

# Anthropic (Eng): Effective Harnesses for Long-Running Agents

> A concrete case study of a harness that keeps an agent coherent across many
> context windows: a two-agent (initializer + coding) pattern with structured
> state, git, and end-to-end verification. Deepens [[agent-harness]].

## Summary

A harness is the scaffolding that maintains coherence across context windows. The
study pairs an **initializer agent** (one-time environment + spec + progress
setup) with a **coding agent** (single-feature incremental sessions), and shows
the failure modes that emerge without structure. (see [[agent-harness]],
[[context-engineering]])

## Key points

- **Two-agent pattern:** different prompts for first vs continuation sessions.
- **Failure modes → fixes:** premature completion → feature list marking
  incomplete as "failing"; over-reach → one feature per session; lost progress →
  git commits + `claude-progress.txt`; weak verification → browser automation
  (Puppeteer MCP) end-to-end.
- **Startup sequence:** `pwd` → read git log + progress → pick top incomplete
  feature → smoke-test via `init.sh` → implement. Saves re-establishing context.
- **State as structured JSON** (agents only flip the "passes" field) — models are
  less likely to inappropriately edit JSON than Markdown.
- **Verify like a human user**, not just unit/API tests — but only reliably once
  *explicitly* prompted to.

## Concepts

[[agent-harness]], [[context-engineering]], [[agent-orchestration]],
[[agent-evals]], [[agent-design-principles]]

## Entities

[[anthropic]], [[claude]], [[claude-agent-sdk]]

## Notable claims & data

- Verification is a prompting problem as much as a capability one: explicit
  "test as a human would" instruction was the unlock. Feeds [[agent-evals]].
- Open question: does a single generalist agent beat specialized
  testing/QA/cleanup agents? Ties to [[agent-orchestration]] multi-agent tradeoffs.

## Connections

The applied counterpart to [[anthropic-eng-context-engineering]] long-horizon
techniques and the principle-level [[harnessing-claudes-intelligence]] /
[[anthropic-evolution-of-agentic-surfaces]]. Built on the [[claude-agent-sdk]].
