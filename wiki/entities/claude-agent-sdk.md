---
title: Claude Agent SDK
type: entity
subtype: product
created: 2026-06-21
updated: 2026-10-12
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
- Provides automatic compaction: once Opus 4.5 removed "context anxiety", the
  long-running app harness dropped context resets for one continuous session
  with SDK compaction. (see [[anthropic-eng-harness-design-long-running-apps]])
- A **static** harness: the SDK and `claude -p` must stay generic, whereas
  Claude Code's dynamic workflows write a harness tailored to each task. (see
  [[anthropic-harness-for-every-task]])
- Claude Code's dedicated tools are callable from the SDK (the AskUserQuestion
  tool's composability was one reason to prefer a tool over a prompt format).
  (see [[anthropic-seeing-like-an-agent]])
- The `sonnet` alias resolves to Claude Sonnet 5.5 from Claude Code v2.1.284
  and Agent SDK for TypeScript v0.3.284 or later. (see
  [[anthropic-building-with-sonnet-5-5]])

## Relationships

- Built by [[anthropic]]; predecessor surface to [[claude-managed-agents]];
  analogous to [[openai-agents-sdk]]. The harness/product split parallels the
  open [[openai-codex]] harness and its SDK. (see [[openai-codex-as-a-platform]])

## Appears in

- [[anthropic-evolution-of-agentic-surfaces]]
- [[anthropic-eng-effective-harnesses-long-running-agents]]
- [[anthropic-eng-agent-skills]]
- [[anthropic-eng-harness-design-long-running-apps]]
- [[anthropic-harness-for-every-task]]
- [[anthropic-seeing-like-an-agent]]
- [[anthropic-building-with-sonnet-5-5]]
- [[openai-codex-as-a-platform]]

## Contradictions / open questions

- The harness case study ([[anthropic-eng-effective-harnesses-long-running-agents]])
  builds *on* the SDK but doesn't document the SDK itself — the Agent SDK docs
  remain a candidate for a dedicated source.
