---
title: "Anthropic: Building agents with the Claude Agent SDK"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Anthropic (claude.com articles) — Thariq Shihipar
date: 2025-09-29
source_url: https://claude.com/resources/articles/building-agents-with-the-claude-agent-sdk
source_path: raw/anthropic-building-agents-claude-agent-sdk.md
tags: [agents, claude-agent-sdk, agent-loop, harness, verification, context-engineering]
---

# Anthropic: Building agents with the Claude Agent SDK

> The launch post that renamed the Claude Code SDK to the Claude Agent SDK. It
> frames agent design as a loop: gather context, take action, verify work,
> repeat.

## Summary

Published 2025-09-29, this is the oldest source in the wiki. [[anthropic]]
renamed the Claude Code SDK to the [[claude-agent-sdk]]. The reason: the
harness behind [[claude-code]] now powered almost all of Anthropic's major
agent loops, including non-coding work. The core design principle is "give
your agents a computer": bash plus file tools let an agent work like a person.
The post organizes agent capabilities around the loop **gather context → take
action → verify work → repeat**, using an email agent as the example. Later
wiki sources update some details. For example, compaction and subagent
practices have since evolved.

## Key points

- **Gather context.** Agentic search over the file system (`grep`, `tail`)
  comes first. Folder structure is itself context engineering. Semantic search
  is faster but less accurate, harder to maintain, and less transparent. The
  post says to add semantic search only when needed. Subagents give
  parallelism and isolated context, and return only relevant excerpts.
  Compaction summarizes as the context limit nears. See
  [[context-engineering]].
- **Take action.** Tools are the primary actions because they are prominent
  in context. Bash and scripts handle flexible work. Code generation is the
  preferred output for complex, reliable operations: claude.ai file creation
  writes Python to build Office files. MCP gives ready-made integrations. See
  [[tool-design]] and [[model-context-protocol]].
- **Verify work.** Three methods, in order of robustness:
  1. Rules-based feedback, such as linting. TypeScript plus lint beats plain
     JavaScript because it gives more feedback layers.
  2. Visual feedback from screenshots, for example through a Playwright MCP
     server.
  3. LLM-as-judge, described as "not a very robust method" with latency cost.
  See [[agent-verification]].
- **Improve by reading failures.** Missing information means the search APIs
  need restructuring. Repeated failures need a formal rule in the tools.
  Errors the agent cannot fix need better tools. Variance across features
  needs a test set built from customer usage.
- Use cases named: finance, personal assistant, customer support, and deep
  research agents.

## Connections

- Successor framing to [[anthropic-building-effective-agents]]. The same loop
  appears in [[anthropic-getting-started-with-loops]] ("the agentic loop").
- The tool advice points to [[anthropic-eng-writing-tools-for-agents]].
  Compaction is developed further in [[anthropic-eng-context-engineering]].
- The managed successor surface is [[claude-managed-agents]] (see
  [[anthropic-evolution-of-agentic-surfaces]]).
