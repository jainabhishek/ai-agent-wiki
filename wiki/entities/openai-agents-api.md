---
title: OpenAI Agents API
type: entity
subtype: product
created: 2026-10-12
updated: 2026-10-12
tags: [openai, api, agents, managed-agents, harness]
---

# OpenAI Agents API

> OpenAI's hosted agent runtime: OpenAI runs the [[openai-codex]] harness loop,
> the session state, and optionally the sandbox. Public beta since 2026-09-10.

## Overview

The Agents API is the managed option in OpenAI's three-way runtime choice. With
the Agents API, OpenAI runs the agent loop and stores state. With the
[[openai-agents-sdk]], your application runs the loop. With the Responses API,
you build the loop yourself. OpenAI rates the integration effort of the three as
low, medium, and high. (see [[openai-agents-api-guide]])

It is OpenAI's counterpart to [[claude-managed-agents]]. Both products host the
harness for the developer, keep the session outside the model's context window,
and let the developer choose where the sandbox runs. (see
[[openai-agents-api-guide]], [[anthropic-eng-scaling-managed-agents]])

## Key facts

- Entered public beta on 2026-09-10. It runs the managed Codex harness, with
  durable sessions, MCP server connections, and OpenAI-hosted or self-connected
  sandboxes. (see [[openai-agents-api-guide]])
- Four core concepts: Agent, Environment, Session, and Events/items. (see
  [[openai-agents-api-guide]])
- `environment.type` is `none`, `openai_hosted`, or `self_hosted`. With
  `self_hosted`, your own executor runs the commands. (see
  [[openai-agents-api-guide]])
- Agent configuration includes `multi_agent` (`enabled`,
  `max_concurrent_subagents`) and `capability_directories` for skills. (see
  [[openai-agents-api-guide]])
- Sessions start with `POST /v1/agents/sessions` and the header
  `OpenAI-Beta: agents=v1`. Progress arrives by streaming or webhooks. (see
  [[openai-agents-api-guide]])
- Data residency is US only. Zero Data Retention is not available, even with a
  self-hosted sandbox. (see [[openai-agents-api-guide]])
- Computer use was added on 2026-09-29. It runs in an OpenAI-hosted browser.
  Approval of a website origin does not confirm each action, and only the main
  agent can request browser sign-in. (see [[openai-agents-api-guide]])
- AWS Bedrock Managed Agents is built on the Agents API. (see
  [[openai-agents-api-guide]])

## Relationships

- Built by [[openai]]; runs the [[openai-codex]] harness.
- Managed alternative to the [[openai-agents-sdk]]. (see
  [[openai-agents-api-guide]])
- Architectural counterpart to [[claude-managed-agents]]; compared in
  [[agent-building-best-practices-anthropic-vs-openai]].

## Appears in

- [[openai-agents-api-guide]]
- [[openai-codex-as-a-platform]]

## Contradictions / open questions

- _None recorded._
