---
title: "Anthropic: How Cresta built Conductor, an agent builder on the Claude Agent SDK"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com articles)
date: 2026-10-05
source_url: https://claude.com/resources/articles/how-cresta-turned-cx-expertise-into-an-agent-builder-on-the-claude-agent-sdk
source_path: raw/anthropic-cresta-agent-builder.md
tags: [case-study, claude-agent-sdk, meta-agent, agent-evals, regression-evals, determinism, customer-experience]
---

# Anthropic: How Cresta built Conductor, an agent builder on the Claude Agent SDK

> Case study of a meta-agent that builds customer-experience agents, with a
> four-dimension eval rerun on every model or framework change.

## Summary

Anthropic published this article on claude.com on 2026-10-05, in its "How
startups build with Claude" series. Results are self-reported by Cresta via
Anthropic. Conductor is a natural-language builder for customer-experience (CX)
agents. The [[claude-agent-sdk]] is its execution harness, and Cresta layers its
CX workflows, data, and policy on top. Early versions used Claude Sonnet and
Claude Opus; the page gives no versions. Cresta claims Conductor roughly halved
initial deployment time in early use.

## Key points

- **SDK as harness, product as control plane.** The SDK handles context
  gathering, tool calls, and writing and running code. Conductor adds policy,
  observability, verification, and feedback. Cresta builds only what depends on
  its own data. See [[agent-harness]].
- **Four eval dimensions for an agent that builds agents:** outcome (usable
  artifact?), execution path (right tools and context?), quality (vs a curated
  reference), resource use (time and model usage). Build tasks: build an agent,
  write a test, change an agent, root-cause analysis. See [[agent-evals]].
- **Regression gate on model change.** Cresta reruns the same tasks and scoring
  on each new Claude model or framework update before adopting it.
- **Flexible vs deterministic.** Harden only the enterprise-critical workflows;
  making everything deterministic yields a giant decision tree. Tests for the
  deterministic parts must change when business rules change. See
  [[agents-vs-workflows]].
- **Build lessons become skills.** Conductor turns a build's patterns, business
  rules, and eval approaches into a memory artifact shared as a skill. See
  [[agent-skills]].
- **Claimed effort split:** initial build ~20%, testing and iteration ~80%;
  design tooling around the iteration loop.

## Connections

Same agent-builds-agents pattern as [[claude-customer-vapi]]. SDK background:
[[anthropic-building-agents-claude-agent-sdk]]. Eval method:
[[anthropic-eng-demystifying-evals]]. Entities: [[anthropic]],
[[claude-agent-sdk]], [[claude-code]].
