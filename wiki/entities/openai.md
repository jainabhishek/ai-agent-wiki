---
title: OpenAI
type: entity
subtype: org
created: 2026-06-21
updated: 2026-06-21
tags: [openai, agents]
---

# OpenAI

> AI research and deployment company; maker of the GPT models and the
> [[openai-agents-sdk]], and publisher of "A Practical Guide to Building Agents."

## Overview

In this wiki, OpenAI is the source of [[openai-practical-guide-to-building-agents]],
which defines agents as systems that independently accomplish tasks, and lays out
three design foundations (model, tools, instructions), orchestration patterns,
and a layered guardrails model.

## Key facts

- Defines an agent's three core components as **Model, Tools, Instructions**.
  (see [[agent-core-components]])
- Recommends **maximizing a single agent first**, moving to multi-agent only when
  needed. (see [[agent-orchestration]])
- Treats **guardrails** as a first-class, layered defense, with optimistic
  execution in the SDK. (see [[guardrails]])

## Relationships

- Industry counterpart to [[anthropic]]; agent guidance largely agrees — see
  [[agent-building-best-practices-anthropic-vs-openai]].
- Ships the [[openai-agents-sdk]] referenced throughout its guide.

## Appears in

- [[openai-practical-guide-to-building-agents]]

## Contradictions / open questions

- _None recorded._
