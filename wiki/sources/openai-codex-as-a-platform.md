---
title: "OpenAI: Codex as a platform — build on the open agent harness"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Nicolas Bonamy, Derrick Choi (OpenAI)
date: 2026-08-19
source_url: https://developers.openai.com/blog/codex-as-a-platform
source_path: raw/openai-codex-as-a-platform.md
tags: [openai, codex, agent-harness, app-server, sdk, mcp, human-in-the-loop]
---

# OpenAI: Codex as a platform — build on the open agent harness

> OpenAI Developers blog post that presents the open-source Codex harness as a
> reusable agent runtime to embed in domain-specific applications.

## Summary

The post separates the **harness** from the products built on it. The
open-source [[openai-codex]] harness powers the Codex App, CLI, and IDE
extension. It manages conversation state, streaming, tool use, sandbox and
approval policies, and work across turns. OpenAI recommends that teams start
from this harness instead of building a new runtime. The host application owns
the interface, the context and tools (including application-owned MCP
servers), and the operational boundaries. See [[agent-harness]].

Date: the page byline says Aug 19, 2026. A "2026-07-07" string in the page HTML
is the slug of a linked GitHub changelog post, not the publication date.

## Key points

- **The agent loop is the reusable part.** A harness covers task understanding,
  context over time, tool calls, progress, failure handling, human approval, and
  returning a result. See [[agent-core-components]].
- **Harness design changes results.** On ARC-AGI-3, retained reasoning plus
  context compaction raised GPT-5.6 Sol from 13.3% to 38.3%, with six times
  fewer output tokens.
- **Three integration layers:**
  - `codex exec` for scripts, CI jobs, and one-off background tasks with
    structured output;
  - the Codex SDK for application code that starts, resumes, or streams tasks;
  - **Codex app-server** when the agent is part of the product. The app-server
    client protocol supports threads, turns, events, interrupts, tools, and
    approval requests.
- **What the host application controls:** the UI, the context and tools
  exposed, where the agent runs, file and tool access, which actions need
  approval, how work is observed, and how results return to the system of
  record. See [[guardrails]].
- **Open versus managed.** The CLI, app-server, and SDK are open source. Model
  access and managed services are separate.
- **Relay sample.** An ops dashboard with application-owned MCP tools. The user
  starts work by clicking an action (for example **Compare recovery**), not by
  writing a prompt. A shipment rebooking requires human approval.

## Notable claims & data

- ARC-AGI-3: 13.3% → 38.3% for GPT-5.6 Sol from harness settings alone; output
  tokens cut sixfold.
- Thrive Holdings and Crete tax-preparation pilot: 7,000 returns, preparation
  time cut by about a third.
- Other adopters named: GitHub and JetBrains (IDE integration), Cisco (Codex
  SDK in App Builder inside Cisco Cloud Control).

## Entities

[[openai]], [[openai-codex]]

## Concepts

[[agent-harness]], [[agent-core-components]], [[guardrails]], [[tool-design]],
[[context-engineering]]

## Connections

[[openai-agents-api-guide]] is the managed, OpenAI-hosted form of the same
Codex harness. The harness/product split parallels [[claude-agent-sdk]] and
[[claude-managed-agents]] on the Anthropic side, and the "harness design moves
benchmark results" claim supports [[agent-harness]]. A worked internal example
is [[openai-automating-repetitive-work-codex]].

## Contradictions / open questions

- _None recorded._ The ARC-AGI-3 figure is cited from a separate OpenAI post
  that was not ingested.
