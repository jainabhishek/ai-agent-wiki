---
title: Claude Agent SDK
type: entity
subtype: product
created: 2026-06-21
updated: 2026-06-21
tags: [anthropic, sdk, agents, harness]
---

# Claude Agent SDK

> Anthropic's agent SDK (2025): a tuned agent **harness** — the middle stage
> between hand-rolled loops and fully managed agents.

## Overview

In the evolution traced by [[anthropic-evolution-of-agentic-surfaces]], the Agent
SDK provided a tuned harness over raw "tokens in, tokens out," but left deployment
complexity (sandboxing, sessions, secrets) to the developer — the gap later
closed by [[claude-managed-agents]]. The Anthropic counterpart to the
[[openai-agents-sdk]].

## Key facts

- A tuned **agent harness** rather than just an API. (see [[agent-harness]])
- Superseded for production deployment concerns by [[claude-managed-agents]],
  which decouples reasoning from execution.

## Relationships

- Built by [[anthropic]]; predecessor surface to [[claude-managed-agents]];
  analogous to [[openai-agents-sdk]].

## Appears in

- [[anthropic-evolution-of-agentic-surfaces]]
- [[anthropic-eng-effective-harnesses-long-running-agents]]
- [[anthropic-eng-agent-skills]]

## Contradictions / open questions

- The harness case study ([[anthropic-eng-effective-harnesses-long-running-agents]])
  builds *on* the SDK but doesn't document the SDK itself — the Agent SDK docs
  remain a candidate for a dedicated source.
