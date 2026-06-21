---
title: "Anthropic: Building Effective Agents"
type: source
created: 2026-06-21
updated: 2026-06-21
author: Erik Schluntz, Barry Zhang (Anthropic)
date: 2024-12
source_url: https://www.anthropic.com/engineering/building-effective-agents
source_path: raw/anthropic-building-effective-agents.md
tags: [agents, best-practices, anthropic, workflows]
---

# Anthropic: Building Effective Agents

> Anthropic's engineering field guide on when and how to build agentic systems,
> drawn from working with dozens of teams across industries. Its central advice:
> find the simplest solution possible, and add complexity only when it clearly
> improves outcomes.

## Summary

The piece argues that the most successful implementations use **simple,
composable patterns** rather than complex frameworks. It draws a sharp line
between **workflows** (LLMs and tools orchestrated through predefined code paths)
and **agents** (LLMs that dynamically direct their own processes and tool use) —
both are "agentic systems," but they suit different problems. See
[[agents-vs-workflows]].

## Key points

- **Start simple.** Many applications need only a single well-crafted LLM call
  with retrieval and in-context examples. Don't reach for an agent when a prompt
  will do. See [[agent-design-principles]].
- **Five composable workflow patterns** cover most needs before you need a true
  agent: prompt chaining, routing, parallelization, orchestrator-workers, and
  evaluator-optimizer. See [[workflow-patterns]].
- **Agents** are for open-ended problems where you can't predict the number of
  steps. They need environmental ground truth (tool results, code execution) and
  should run in trusted environments with stopping conditions / guardrails.
- **Three core principles:** simplicity, transparency (show the planning steps),
  and a well-crafted **Agent-Computer Interface (ACI)**. See [[tool-design]].
- **Frameworks** (LangGraph, etc.) ease the start but add abstraction that can
  hide the underlying prompts and behavior — understand the code beneath.

## Concepts

[[agents-vs-workflows]], [[workflow-patterns]], [[tool-design]],
[[agent-orchestration]], [[agent-design-principles]]

## Entities

[[anthropic]]

## Notable claims & data

- "Consistently, the most successful implementations use simple, composable
  patterns rather than complex frameworks." Aligns with OpenAI's
  maximize-a-single-agent-first advice (see [[openai-practical-guide-to-building-agents]]).
- The orchestrator-workers pattern is preferred over parallelization when
  subtasks can't be predicted in advance — a distinction OpenAI's manager
  pattern echoes (see [[agent-orchestration]]).

## Connections

Strong agreement with [[openai-practical-guide-to-building-agents]] on
start-simple, tool quality, and incremental complexity. The two are compared in
[[agent-building-best-practices-anthropic-vs-openai]].
