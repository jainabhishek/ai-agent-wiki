---
title: OpenAI
type: entity
subtype: org
created: 2026-06-21
updated: 2026-10-12
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
- Offers three agent runtimes: the [[openai-agents-api]] (OpenAI runs the loop),
  the [[openai-agents-sdk]] (your app runs it), and the Responses API (you build
  it). (see [[openai-agents-api-guide]])
- Shut down the Assistants API on 2026-08-26 and pointed users to the Responses
  and Conversations APIs. (see [[openai-agents-api-guide]])
- Current model lineup as of 2026-10-12: GPT-6 Astra, GPT-6.1 Sol, and GPT-6
  Luna. Prompting guidance for the family is in the GPT-6 Astra guide. (see
  [[openai-prompting-gpt-6-astra]])
- Open-sources the [[openai-codex]] harness and positions it as an embeddable
  agent runtime. (see [[openai-codex-as-a-platform]])
- Most 2026 guidance on skills, `AGENTS.md`, and long-running agents is written
  against Codex. (see [[openai-shell-skills-compaction]],
  [[openai-testing-agent-skills-with-evals]],
  [[openai-skills-for-oss-maintenance]])
- Ships Secure MCP Tunnel so its products can reach private MCP servers. (see
  [[openai-private-mcp-servers]], [[model-context-protocol]])

## Relationships

- Industry counterpart to [[anthropic]]; agent guidance largely agrees — see
  [[agent-building-best-practices-anthropic-vs-openai]].
- Ships the [[openai-agents-sdk]] referenced throughout its guide.
- Builds [[openai-codex]] and the [[openai-agents-api]].

## Appears in

- [[openai-practical-guide-to-building-agents]]
- [[openai-prompt-guidance-gpt-5-6]] (legacy)
- [[openai-prompting-gpt-6-astra]]
- [[openai-rethinking-skills-prompts-gpt-6-astra]]
- [[openai-agents-api-guide]]
- [[openai-codex-as-a-platform]]
- [[openai-automating-repetitive-work-codex]]
- [[openai-one-year-of-responses]]
- [[openai-shell-skills-compaction]]
- [[openai-testing-agent-skills-with-evals]]
- [[openai-skills-for-oss-maintenance]]
- [[openai-private-mcp-servers]]

## Contradictions / open questions

- [[openai-prompt-guidance-gpt-5-6]] (Aug 2026) records OpenAI describing Sol,
  Terra, and Luna as durable capability tiers. The GPT-6 lineup (Sep 2026) has
  no Terra and adds Astra. (see [[openai-prompting-gpt-6-astra]])
- GPT-6 Sol was released on 2026-09-22 but is absent from the current model
  picker; the Astra guide mentions it only as a model to migrate from. (see
  [[openai-prompting-gpt-6-astra]])
