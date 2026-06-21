---
title: OpenAI Agents SDK
type: entity
subtype: product
created: 2026-06-21
updated: 2026-06-21
tags: [openai, sdk, agents, tooling]
---

# OpenAI Agents SDK

> OpenAI's code-first library for building agents, used as the reference
> implementation throughout [[openai-practical-guide-to-building-agents]].

## Overview

A library for defining agents (model + tools + instructions), running them in a
loop, composing them, and enforcing guardrails. It favors a **code-first,
non-declarative** approach: developers express workflow logic with familiar
programming constructs rather than pre-defining an entire graph upfront.

## Key facts

- `Runner.run()` drives the **agent run loop**, iterating the LLM until an exit
  condition (final-output tool, a response with no tool calls, error, or max
  turns). (see [[agent-orchestration]])
- Supports **agents-as-tools** (`agent.as_tool(...)`) for the manager pattern and
  **handoffs** for the decentralized pattern. (see [[agent-orchestration]])
- Treats **guardrails** as first-class with **optimistic execution** — the agent
  generates while guardrails run concurrently and raise tripwire exceptions on
  violation. (see [[guardrails]])
- Contrasted with **declarative graph** frameworks, which it argues become
  cumbersome as workflows grow dynamic.

## Relationships

- Built and maintained by [[openai]].

## Appears in

- [[openai-practical-guide-to-building-agents]]

## Contradictions / open questions

- _None recorded._
