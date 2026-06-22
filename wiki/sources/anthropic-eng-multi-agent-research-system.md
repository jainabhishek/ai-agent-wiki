---
title: "Anthropic (Eng): How We Built Our Multi-Agent Research System"
type: source
created: 2026-06-21
updated: 2026-06-21
author: Anthropic Engineering
date: 2025
source_url: https://www.anthropic.com/engineering/multi-agent-research-system
source_path: raw/anthropic-eng-multi-agent-research-system.md
tags: [multi-agent, orchestration, research, evals, primary-source]
---

# Anthropic (Eng): How We Built Our Multi-Agent Research System

> The primary source on orchestrator-worker multi-agent design — including the
> blunt economics (≈15× tokens) and the striking finding that **token usage alone
> explains ~80% of performance variance.** Deepens [[agent-orchestration]].

## Summary

A **lead agent** plans and spawns parallel **subagents**, each with its own
context window, then synthesizes their findings. Multi-agent beat single-agent
Opus 4 by **90.2%** on breadth-first research, but costs ~15× chat tokens and
fails on shared-context/coordination-heavy work like most coding. (see
[[agent-orchestration]])

## Key points

- **Orchestrator-worker**: lead decomposes → 3–5 subagents explore in parallel
  (3+ parallel tool calls each) → lead synthesizes; cut research time up to 90%.
- **Token usage explains ~80% of variance** (BrowseComp) — the win is separate
  context windows, not architecture per se. Reinforces [[context-engineering]].
- **Multi-agent ≠ default**: ~4× tokens (single agent) / ~15× (multi) vs chat;
  avoid when context must be shared. (see [[agents-vs-workflows]])
- **Prompt principles**: explicit delegation, effort-scaling by complexity,
  rigorous tool interfaces, self-improvement, broad→narrow search, extended
  thinking; "instill good heuristics rather than rigid rules."
- **Eval**: ~20-query small samples early; LLM-as-judge with a multi-dimension
  rubric; human checks for hallucinations/source bias. (see [[agent-evals]])

## Concepts

[[agent-orchestration]], [[context-engineering]], [[agents-vs-workflows]],
[[agent-evals]], [[tool-design]], [[agent-design-principles]]

## Entities

[[anthropic]], [[claude]]

## Notable claims & data

- "A multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4
  subagents outperformed single-agent Claude Opus 4 by 90.2%."
- Production lessons: resume-from-failure state, full production tracing for
  non-determinism, **rainbow deployments**, synchronous-subagent bottleneck. "The
  last mile often becomes most of the journey." (see [[agent-harness]])

## Connections

The concrete realization of the sub-agent technique in
[[anthropic-eng-context-engineering]] and the manager/orchestrator-workers
patterns in [[agent-orchestration]] and [[workflow-patterns]].
