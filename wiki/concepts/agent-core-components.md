---
title: Agent Core Components
type: concept
created: 2026-06-21
updated: 2026-10-13
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
  documented. Detailed in [[tool-design]]. When the model calls tools from code
  it writes (programmatic tool calling), expose only parallel-safe / idempotent
  tools to that code (see [[anthropic-eng-advanced-tool-use]]).
- **Instructions** — high-quality instructions are especially critical for
  agents; derive them from existing SOPs and make every step a clear action.
  Detailed in [[agent-instructions]].

## Beyond the three: runtime components

Later vendor architectures keep model + tools + instructions but add runtime
parts around them:

- **OpenAI Agents API** — an **Agent** (model, instructions, tools, MCP servers)
  plus an **Environment** (optional sandbox), a **Session** (a durable agent
  instance), and **Events/items** (see [[openai-agents-api-guide]]).
- **Anthropic Managed Agents** — the **session** (append-only event log), the
  **harness** (the loop that calls the model and routes tool calls), and the
  **sandbox** (where code runs), each behind a small interface so any one can
  fail or be replaced (see [[anthropic-eng-scaling-managed-agents]],
  [[claude-managed-agents]]).
- **OpenAI Codex platform** — the agent loop (task understanding, context over
  time, tool calls, progress, failure handling, approval, result) is the reusable
  part; the host application owns the UI, the exposed context and tools, and the
  operational boundaries (see [[openai-codex-as-a-platform]]).

The two vendors converge on the same split: durable session state and the
execution sandbox sit outside the model/tools/instructions core. See
[[agent-harness]].

## Layered architectures: loop, runtime, connectors, skills

Two later vendor posts describe the full agent as layers that can change
independently:

| Anthropic: four layers | OpenAI: five parts |
|------------------------|--------------------|
| **Agent loop** — reasons | **Orchestration** — the Responses API runs the loop |
| **Agent runtime** — runs code on a filesystem | **Actions** (shell) and **runtime context** (container) |
| **MCP servers** — connect to external systems | — |
| **Skills library** — procedural knowledge as files | **Reusable workflow** (skills) |
| — | **Longevity** (compaction) |

Sources: [[anthropic-building-agents-with-skills]] (2026-01-22);
[[openai-responses-api-computer-environment]] (2026-03-11).

- **Convergence.** Both separate the loop from the runtime that executes code,
  and both make skills a layer of their own. They differ in the named layer:
  Anthropic names MCP connectivity, and OpenAI names compaction.
- **Anthropic's argument.** A general agent with bash and a filesystem covers
  many domains, so Anthropic adds skills instead of building a specialized agent
  per domain (see [[anthropic-building-agents-with-skills]], [[agent-skills]]).
- **Who runs the loop depends on the tool type.** In OpenAI's Responses API,
  custom tools hand control back to the client's harness. Hosted tools
  (file search, code interpreter, web search, image generation, MCP, shell)
  run server-side, and the API runs the loop itself (see
  [[openai-why-we-built-responses-api]],
  [[openai-responses-api-computer-environment]], [[tool-design]]).
- **One request carries the components.** Each Codex request to the Responses
  API carries the instructions, the tools (Codex tools, hosted tools, and MCP
  tools), and a list of typed input items (see
  [[openai-unrolling-codex-agent-loop]]).

## Why it matters

This is the minimal mental model for what you actually build. [[anthropic]]'s
framing differs in emphasis (it foregrounds the **Agent-Computer Interface** and
the agent loop with environmental feedback) but covers the same surface: a model
that plans, tools to act, and instructions/guardrails to stay on task. (see
[[anthropic-building-effective-agents]]) Practitioner case studies on OpenAI's
Responses API show the same three components in production (see
[[openai-one-year-of-responses]]).

## Related concepts

- [[tool-design]], [[agent-instructions]], [[agent-orchestration]],
  [[agent-design-principles]], [[agent-harness]]

## Key entities

- [[openai]], [[openai-agents-sdk]], [[claude-managed-agents]]

## Appears in

- [[openai-practical-guide-to-building-agents]]
- [[anthropic-eng-advanced-tool-use]]
- [[anthropic-eng-scaling-managed-agents]]
- [[openai-agents-api-guide]]
- [[openai-codex-as-a-platform]]
- [[openai-one-year-of-responses]]
- [[anthropic-building-agents-with-skills]]
- [[openai-responses-api-computer-environment]]
- [[openai-why-we-built-responses-api]]
- [[openai-unrolling-codex-agent-loop]]
- [[anthropic-building-effective-agents]]

## Contradictions / open questions

- _None recorded._
