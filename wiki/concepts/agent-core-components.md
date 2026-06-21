---
title: Agent Core Components
type: concept
created: 2026-06-21
updated: 2026-06-21
tags: [agents, architecture, model, tools, instructions]
---

# Agent Core Components

> [[openai]]'s decomposition of an agent into three foundational parts: **Model,
> Tools, Instructions.** (see [[openai-practical-guide-to-building-agents]])

## Definition

| Component | Role |
|-----------|------|
| **Model** | The LLM powering the agent's reasoning and decision-making. |
| **Tools** | External functions / APIs the agent uses to take action. |
| **Instructions** | Explicit guidelines and guardrails defining behavior. |

## The components in depth

- **Model** — different tasks warrant different models (task complexity vs.
  latency vs. cost). Prototype with the most capable model, then down-size where
  evals allow. See the eval loop in [[agent-design-principles]].
- **Tools** — three types (data, action, orchestration), each standardized and
  documented. Detailed in [[tool-design]].
- **Instructions** — high-quality instructions are especially critical for
  agents; derive them from existing SOPs and make every step a clear action.
  Detailed in [[agent-instructions]].

## Why it matters

This is the minimal mental model for what you actually build. [[anthropic]]'s
framing differs in emphasis (it foregrounds the **Agent-Computer Interface** and
the agent loop with environmental feedback) but covers the same surface: a model
that plans, tools to act, and instructions/guardrails to stay on task. (see
[[anthropic-building-effective-agents]])

## Related concepts

- [[tool-design]], [[agent-instructions]], [[agent-orchestration]],
  [[agent-design-principles]]

## Key entities

- [[openai]], [[openai-agents-sdk]]

## Appears in

- [[openai-practical-guide-to-building-agents]]

## Contradictions / open questions

- _None recorded._
