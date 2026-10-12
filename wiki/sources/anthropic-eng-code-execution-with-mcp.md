---
title: "Anthropic: Code execution with MCP: Building more efficient agents"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Adam Jones and Conor Kelly (Anthropic Engineering blog)
date: 2025-11-04
source_url: https://www.anthropic.com/engineering/code-execution-with-mcp
source_path: raw/anthropic-eng-code-execution-with-mcp.md
tags: [mcp, code-execution, tools, context-engineering, progressive-disclosure, privacy, skills]
---

# Anthropic: Code execution with MCP: Building more efficient agents

> Proposes exposing MCP servers to an agent as a filesystem of code APIs rather
> than as direct tool calls, so the agent loads definitions on demand and
> processes data in code — reported 150K → 2K tokens on one task.

## Summary

As agents connect to dozens of MCP servers, two costs grow: every tool
definition is loaded up front, and every intermediate result passes through the
model (a 2-hour transcript copied from Google Drive to Salesforce flows through
context twice, ~50K tokens). The post's fix is to present each MCP server as a
directory of generated code files (`servers/<server>/<tool>.ts` plus
`index.ts`, each wrapping a `callMCPTool` helper) inside a code-execution
environment. The agent discovers tools by browsing files or calling a
`search_tools` tool with a detail-level option, then writes a short script that
calls tools and moves data between them without the data entering context.
Benefits listed: progressive disclosure, context-efficient results, real control
flow, privacy-preserving data paths, and state persistence that grows into
reusable skills. The trade-off is operating a secure sandbox. See
[[context-engineering]] and [[tool-design]].

## Key points

- **Progressive disclosure of tools:** definitions are read on demand, not
  preloaded; `search_tools` returns name only, name + description, or full
  schema.
- **Filter before the model sees it:** a 10,000-row sheet reduced in code to the
  few relevant rows; joins and aggregations likewise.
- **Control flow in code:** loops, conditionals, retries (e.g. poll Slack for a
  deploy message) run in the sandbox, saving inference passes and
  time-to-first-token.
- **Privacy:** intermediate data stays in the sandbox; the MCP client can
  tokenize PII (`[EMAIL_1]`, `[NAME_1]`) before the model sees it and restore
  real values on the way to the next tool, enabling deterministic data-flow
  rules.
- **State and skills:** write intermediate results to files
  (`./workspace/leads.csv`), save working functions (`./skills/save-sheet-as-csv.ts`),
  and add a `SKILL.md` to make them [[agent-skills]].
- **Caveat:** agent-written code needs sandboxing, resource limits, and
  monitoring — overhead direct tool calls avoid.

## Entities

[[anthropic]], [[claude]]

## Concepts

[[context-engineering]], [[tool-design]], [[agent-skills]], [[guardrails]],
[[agent-harness]]

## Notable claims & data

- Example task: ~150,000 → ~2,000 tokens (98.7% saving).
- Thousands of community MCP servers since the November 2024 launch; MCP called
  the de facto standard.
- Cloudflare independently reported a similar result ("Code Mode") — an
  independent-convergence data point for the architecture.

## Connections

The design basis for Programmatic Tool Calling in
[[anthropic-eng-advanced-tool-use]] (published three weeks later and crediting
this work). Extends "give the agent code execution to filter and pipe results"
in [[anthropic-eng-context-engineering]] and the filesystem-based skill model of
[[anthropic-eng-agent-skills]]. Contrasts with direct-tool-call guidance in
[[anthropic-eng-writing-tools-for-agents]].
