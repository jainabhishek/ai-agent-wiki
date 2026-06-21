---
title: Overview
type: overview
created: 2026-06-21
updated: 2026-06-21
tags: [meta, agents]
---

# Overview

A research wiki on **building effective LLM agents**, synthesized from primary
guidance published by frontier labs.

## Scope

How to design, build, and safely deploy LLM agents — the architecture choices,
tooling, orchestration, and guardrails. Currently grounded in the two canonical
practitioner guides from [[anthropic]] and [[openai]]; expandable to other labs,
frameworks, and case studies.

## Current thesis

Across independent guidance, the labs **strongly agree** on a few load-bearing
principles (see [[agent-design-principles]] and the full comparison in
[[agent-building-best-practices-anthropic-vs-openai]]):

1. **Don't build an agent unless you need one.** Most tasks are better served by a
   workflow or a single LLM call. ([[agents-vs-workflows]])
2. **Start with the simplest design and add complexity only when evals show it
   helps.** Maximize a single agent before going multi-agent.
   ([[agent-orchestration]])
3. **Tools are the highest-leverage surface.** Invest in clear, documented,
   well-tested tools; clarity beats count. ([[tool-design]])
4. **Instructions must be unambiguous**, derived from real procedures.
   ([[agent-instructions]])
5. **Safety is layered** — guardrails plus human-in-the-loop for high-risk or
   repeatedly-failing actions. ([[guardrails]])

They differ mainly in emphasis: Anthropic is deeper on **composable workflow
patterns** ([[workflow-patterns]]); OpenAI is deeper on **production guardrails**
and a crisp **Model/Tools/Instructions** component model ([[agent-core-components]]).

## Key entities

- [[anthropic]] — *Building Effective Agents*
- [[openai]] — *A Practical Guide to Building Agents*; [[openai-agents-sdk]]

## Key concepts

- [[agents-vs-workflows]] · [[agent-design-principles]] · [[agent-core-components]]
  · [[tool-design]] · [[workflow-patterns]] · [[agent-orchestration]] ·
  [[agent-instructions]] · [[guardrails]]

## Open questions

- Ingest Anthropic's companion engineering pieces (context engineering, writing
  tools for agents, long-running harnesses) to balance the safety/tooling depth.
- Add other perspectives (Google, LangChain, academic) to test how universal
  these "best practices" really are.
