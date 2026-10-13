---
title: "OpenAI: Supercharging Codex with JetBrains MCP at Skyscanner"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Jack Waller (Software Engineer, Skyscanner) — guest post on the OpenAI Developers blog
date: 2026-01-11
source_url: https://developers.openai.com/blog/skyscanner-codex-jetbrains-mcp
source_path: raw/openai-skyscanner-codex-jetbrains-mcp.md
tags: [openai, codex, mcp, ide, feedback-loops, case-study]
---

# OpenAI: Supercharging Codex with JetBrains MCP at Skyscanner

> A practitioner report: connecting the Codex CLI to JetBrains IDEs through MCP
> gives the agent IDE inspections and run configurations as a fast feedback
> loop.

## Summary

Jack Waller, a Skyscanner engineer, wrote this guest post. He connected the
[[openai-codex]] CLI to JetBrains IDEs through the JetBrains
[[model-context-protocol]] server. Two tools matter most. `get_file_problems`
returns IntelliJ inspection errors and warnings with locations.
`execute_run_configuration` runs predefined test, lint, and format
configurations and returns exit codes and output. In his example, Codex wrote
`new NotFound("dummy error")` against the Databricks Java SDK, which has no
such constructor. Codex caught the error with `get_file_problems` right away,
instead of after a test run. The author's `AGENTS.md` tells Codex to check
problems, format, and lint after every edit. All results are qualitative and
self-reported. The post names no model.

## Key points

- **The IDE as a feedback tool.** The agent uses the same compile and inspect
  loop that humans use. See [[tool-placement]].
- **Shorter loop.** Without MCP the loop has five steps: generate, work out how
  to run tests, run them (possibly with user approval), parse the failure, fix.
  With MCP it has three: generate, ask for file problems, fix the reported
  error. This saves time and context. See [[context-engineering]].
- **Reuse existing run configurations.** The agent no longer has to discover
  how to run tests, format, or lint. The author says Codex "no longer
  stumbles" on these steps.
- **Post-edit checks in `AGENTS.md`.** After each edit: use the JetBrains MCP if
  present, then run format, then run lint. See [[agent-instructions]].
- **Reported benefits:** faster feedback loops, fewer back-and-forth prompts,
  more first-try passes, and better fit with existing workflows.

## Entities

[[openai-codex]], [[openai]]

## Concepts

[[model-context-protocol]], [[tool-design]], [[tool-placement]], [[agent-harness]],
[[agent-instructions]], [[context-engineering]]

## Notable claims & data

- No metrics given. The evidence is one anecdote (the `NotFound` constructor)
  plus the author's observations.

## Connections

- Same principle as running tests and linters as verification in
  [[openai-run-long-horizon-tasks-codex]] and
  [[anthropic-eng-claude-code-best-practices]] (give the agent a way to check
  its own work).
- MCP as the way to reach environment tools: [[openai-private-mcp-servers]],
  [[anthropic-eng-code-execution-with-mcp]].
