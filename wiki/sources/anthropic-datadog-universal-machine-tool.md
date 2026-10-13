---
title: "Anthropic: How Datadog Built a Universal Machine Tool for Claude Code"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Michael Segner (Anthropic)
date: 2026-07-21
source_url: https://claude.com/resources/articles/how-datadog-built-a-universal-machine-tool-for-claude-code
source_path: raw/anthropic-datadog-universal-machine-tool.md
tags: [case-study, verification, formal-methods, specifications, claude-code, datadog]
---

# Anthropic: How Datadog Built a Universal Machine Tool for Claude Code

> Customer case study: Datadog's Temper kernel has agents emit verified
> specifications instead of application code, moving effort from generation to
> verification.

## Summary

Published by Anthropic on claude.com (2026-07-21) from a Datadog session; claims
are Datadog's own and self-reported. Datadog says all its engineers use AI coding
tools for production code, with [[claude-code]] driving at least two-thirds.
Sesh Nalla (VP engineering) describes a path through Courier (hand-built queue,
2024), BitsEvolve (evolutionary optimization harness, September 2025), and Helix
(Kafka-comparable streaming service built mostly by Claude Code in days, 2x–5x
cheaper in shadowing, but slow to harden). Each exposed a new bottleneck,
ending at verification and at human-designed shipping tools. **Temper** is
the answer: agents write specifications; a deterministic kernel verifies them in
four layers and runs exactly the verified spec, so verified and running
artifacts cannot drift.

## Key points

- **Verification, not generation, is the bottleneck**: invest in closing the gap
  between generated and proven rather than in more throughput.
- **Emit specs for control logic, keep compilation/proof outside the LLM**: the
  kernel plays the role a compiler plays for Rust code. See [[boundary-contracts]].
- **Three contracts per capability**: behavior (states, transitions,
  preconditions, safety properties), data contract (machine-parseable entities and
  actions an agent can discover without docs), authorization (default-deny,
  scoped approval; denials queue as pending decisions a human can approve and
  hot-load). See [[guardrails]], [[tool-design]].
- **Four verification layers**: symbolic reasoning (guards satisfiable,
  invariants inductive), exhaustive state exploration, deterministic simulation
  with seeded fault injection, and ~1,000 randomized property-test sequences with
  shrinking; under a second on a small spec.
- **Make the state machine explicit as data**: a transition table agents can
  read, change, and hot-reload under policy, instead of logic spread across
  routes, services, and jobs.
- **Keep each artifact small enough for one person to understand.**
- In the Helix "dark factory", Temper is the managed-agent control plane, the
  tool-builder layer bridging Git/CI/deploy, and the service control API. See
  [[claude-managed-agents]].

## Entities

[[anthropic]], [[claude-code]], [[claude-managed-agents]]

## Concepts

[[boundary-contracts]], [[guardrails]], [[agent-evals]], [[agent-verification]], [[tool-design]],
[[agent-harness]]

## Notable claims & data

- Protobuf parser refactor in three days; FoundationDB→Postgres metrics control
  rewrite in under three months; Helix functional "in a few days" (Datadog,
  self-reported, 2026-07-21).

## Connections

Same verification-first argument as [[anthropic-ai-code-modernization]] (the
"certificate") and [[anthropic-agentic-coding-ci-test-impact]]; compare the
test-oracle harness in [[anthropic-eng-building-c-compiler]] and OpenAI's
[[openai-harness-engineering]].
