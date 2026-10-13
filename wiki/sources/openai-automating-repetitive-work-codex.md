---
title: "OpenAI: Automating repetitive work at OpenAI with Codex"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Jeremy Lewi (OpenAI)
date: 2026-08-25
source_url: https://developers.openai.com/blog/automating-repetitive-work-at-openai-with-codex
source_path: raw/openai-automating-repetitive-work-codex.md
tags: [openai, codex, automation, runme, webmcp, human-in-the-loop, context-engineering]
---

# OpenAI: Automating repetitive work at OpenAI with Codex

> A first-person case study: an OpenAI engineer uses Codex with Runme
> notebooks and WebMCP to run model evaluations and to keep a reusable record
> of each run.

## Summary

The author runs recurring operational work, such as model evaluations, through
[[openai-codex]]. He does not write a separate automation per task. Instead he
uses **Runme**, an open-source notebook web app. A Runme notebook holds the goal,
the plan, the commands, the outputs, and the decisions. Codex reads the goal
cell, writes a plan, waits for human approval, then executes and documents.
Each finished notebook becomes context for the next run. See
[[context-engineering]].

## Key points

- **Plan-then-approve loop.** The goal outline tells Codex to review an earlier
  run, write a plan in the notebook, and wait for approval. The human mainly
  chooses between alternatives (which eval system, new or existing
  infrastructure) and nudges when Codex is stuck (for example, exhausted quota).
- **Capture decisions before closing.** Before finishing, the author and Codex
  record why an option was chosen, which approach is now preferred, and what to
  change next time. Dead ends stay in the notebook.
- **Discoverable history.** Notebooks save to Google Drive. Runme writes a
  companion `*.index.md` per notebook, which Drive indexes, so agents can find
  earlier runs.
- **WebMCP instead of a server.** Runme is a static client-side app. It
  registers browser-side tools through WebMCP: read Runme instructions, run
  bounded JavaScript programs over notebook content, and read the docs. A
  traditional MCP server would add infrastructure and change where notebook data
  is handled. See [[tool-placement]].
- **Codex features used:** a persistent goal (long-running work) keeps Codex on
  task. Automatic approval review checks eligible actions without changing the
  existing permission boundaries. See [[guardrails]].
- **Division of labor.** The human decides when a plan is ready and makes
  consequential choices. Codex does the repetitive execution and records more
  detail than the human would.

## Notable claims & data

- The author says the hard problem is lowering the cost of writing things down
  during the work itself; the value of documentation is not in question.
- No quantitative results are given.

## Entities

[[openai]], [[openai-codex]]

## Concepts

[[context-engineering]], [[guardrails]], [[tool-design]], [[tool-placement]], [[agent-harness]],
[[workflow-patterns]]

## Connections

A concrete application of the "build software around the workflow" pattern in
[[openai-codex-as-a-platform]]. The run-document-improve loop resembles the
progress-file pattern in [[anthropic-eng-effective-harnesses-long-running-agents]].

## Contradictions / open questions

- _None recorded._
