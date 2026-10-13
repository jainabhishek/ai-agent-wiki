---
title: "OpenAI (Eng): Inside OpenAI's in-house data agent"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Bonnie Xu, Aravind Suresh, Emma Tang (OpenAI)
date: 2026-01-29
source_url: https://openai.com/index/inside-our-in-house-data-agent/
source_path: raw/openai-in-house-data-agent.md
tags: [openai, case-study, data-agent, text-to-sql, context-engineering, memory, evals, rag]
---

# OpenAI (Eng): Inside OpenAI's in-house data agent

> Case study, published by OpenAI about its own internal-only analytics agent.
> All results are self-reported. Its value is the six-layer context design and
> the SQL eval method.

## Summary

OpenAI built an internal data agent on **GPT-5.2** (post dated 2026-01-29) for
a platform with 3.5k+ internal users, 600+ PB, and 70k datasets. The hard
problems were picking the right table among look-alikes and avoiding silent
SQL errors (many-to-many joins, filter pushdown, nulls). The agent runs in
Slack, a web UI, IDEs, Codex CLI (via MCP), and internal ChatGPT (via an MCP
connector). It checks its own intermediate results (for example zero rows from
a bad join) and retries. See [[context-engineering]].

## Key points

- **Six context layers:** (1) table usage — schema, lineage, historical
  queries; (2) human annotations from domain experts; (3) **Codex enrichment**
  — Codex reads the pipeline code that builds each table to infer uniqueness,
  freshness, scope, and look-alike differences; (4) institutional knowledge
  from Slack, Docs, and Notion, retrieved with permissions; (5) memory; (6)
  live warehouse and platform queries when context is missing or stale.
- **Offline pipeline + RAG.** A daily job merges layers 1–3 into one
  normalized form and embeds it; at query time the agent retrieves only
  relevant context rather than scanning metadata.
- **Memory for non-obvious corrections.** After a correction the agent offers
  to save it; memories are global or personal and user-editable.
- **Evals with golden SQL.** Each curated question has a hand-written golden
  query. The eval runs the generated SQL and compares both the SQL and the
  result data (tolerating syntax differences and extra columns) through the
  Evals API grader. Evals run in development and as production canaries. See
  [[agent-evals]].
- **Pass-through permissions.** Users can query only tables they already have
  access to; answers show assumptions, steps, and links to raw results. See
  [[guardrails]].
- **Lessons:** fewer, non-overlapping tools improved reliability
  ([[tool-design]]); goal-level guidance beat prescriptive prompting
  ([[agent-instructions]]); a table's meaning lives in the code that produces
  it.
- **Workflows** package recurring analyses (weekly reports, table
  validations) as reusable instruction sets, similar to [[agent-skills]].

## Connections

- Direct counterparts on the Anthropic side:
  [[anthropic-self-service-data-analytics]] and
  [[anthropic-claude-tag-analytics-in-slack]].
- "Less is more" on tools agrees with the consolidation advice in
  [[anthropic-eng-writing-tools-for-agents]]; compare "guide the goal, not the
  path" with [[harnessing-claudes-intelligence]].
- Using a coding agent to enrich metadata from source code parallels
  [[openai-harness-engineering]] ("if the agent cannot see it, it does not
  exist").
