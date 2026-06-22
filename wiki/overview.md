---
title: Overview
type: overview
created: 2026-06-21
updated: 2026-06-22
tags: [meta, agents]
---

# Overview

A research wiki on **building effective LLM agents**, synthesized from primary
guidance published by frontier labs.

## Scope

How to design, build, and safely deploy LLM agents — the architecture choices,
tooling, orchestration, context engineering, harness design, and guardrails.
Grounded in the canonical practitioner guides from [[anthropic]] and [[openai]],
plus Anthropic's operational blog posts on harness, skills, steering, and context;
expandable to other labs, frameworks, and case studies.

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
6. **Engineer the context and the harness, then prune them.** Load instructions
   on demand, let the agent manage/persist its own context, and delete harness
   scaffolding the model has outgrown. ([[context-engineering]], [[agent-harness]])

They differ mainly in emphasis: Anthropic is deeper on **composable workflow
patterns** ([[workflow-patterns]]), **context engineering**, **harness design**,
and **skills/steering** ([[agent-skills]], [[agent-steering]]); OpenAI is deeper on
**production guardrails** and a crisp **Model/Tools/Instructions** component model
([[agent-core-components]]). Full comparison:
[[agent-building-best-practices-anthropic-vs-openai]].

## Key entities

- [[anthropic]] — *Building Effective Agents* + operational blog posts; maker of
  [[claude]], [[claude-code]], [[claude-agent-sdk]], [[claude-managed-agents]]
- [[openai]] — *A Practical Guide to Building Agents*; [[openai-agents-sdk]]

## Key concepts

- [[agents-vs-workflows]] · [[agent-design-principles]] · [[agent-core-components]]
  · [[tool-design]] · [[workflow-patterns]] · [[agent-orchestration]] ·
  [[agent-instructions]] · [[guardrails]] · [[agent-skills]] · [[agent-steering]] ·
  [[context-engineering]] · [[agent-harness]] · [[agent-evals]]

## Wiki health

- Current graph topology, hubs, and Obsidian filter caveats:
  [[obsidian-graph-analysis]].

## Open questions

- **Done:** the six core Anthropic *engineering* posts are ingested — building
  effective agents, context engineering, writing tools, long-running harnesses,
  demystifying evals ([[agent-evals]]), multi-agent research
  ([[agent-orchestration]]), and Agent Skills ([[agent-skills]]).
- Remaining engineering posts are narrower/tangential (advanced tool use, the
  "think" tool, code execution with MCP, agentic-coding best practices,
  postmortems) — ingest selectively if a specific question needs them. **MCP**
  has no page yet and is a candidate concept.
- Add other perspectives (Google, LangChain, academic) to test how universal
  these "best practices" really are.
- Deepen OpenAI-side harness/context-engineering coverage to match Anthropic's.
