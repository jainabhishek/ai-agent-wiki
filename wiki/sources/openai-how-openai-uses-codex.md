---
title: "OpenAI: How OpenAI uses Codex"
type: source
created: 2026-10-12
updated: 2026-10-12
author: OpenAI
date: 2026-01-14
source_url: https://openai.com/business/guides-and-resources/how-openai-uses-codex/
source_path: raw/openai-how-openai-uses-codex.md
tags: [openai, codex, case-study, coding-agents, best-practices]
---

# OpenAI: How OpenAI uses Codex

> OpenAI's internal case study (byline Jan 14, 2026) of how its own engineering
> teams use Codex: seven use cases and six working habits. The results are
> self-reported anecdotes from engineers.

## Summary

OpenAI published this page about itself. It draws on interviews with OpenAI
engineers and on internal usage data, but it gives no usage figures. The page
still describes Codex as "in research preview" and uses the Ask mode / Code mode
split. Its content therefore likely predates the January 2026 byline (the 2025
cloud Codex). Read the habits as advice for the cloud task-queue Codex of that
time. All results are short engineer anecdotes and are self-reported.

The seven use cases are code understanding, refactoring and migrations,
performance optimization, test coverage, development velocity, staying in flow,
and exploration. See [[openai-codex]].

## Key points (transferable lessons)

- **Plan first, then code.** For large changes, get a plan in Ask mode and feed
  it to Code mode. OpenAI sizes good tasks at about **one hour** of human work or
  **a few hundred lines** of code, and expects that size to grow. See
  [[workflow-patterns]].
- **Fix the environment, not only the prompt.** A startup script, environment
  variables, and internet access "significantly" cut the error rate. Correct
  recurring build errors in the environment configuration. See
  [[agent-harness]].
- **Prompt like a GitHub issue.** Give file paths, component names, diffs, doc
  snippets, and "do it the way [module X] does". See [[agent-instructions]].
- **`AGENTS.md` for persistent context.** Record naming conventions, business
  logic, known quirks, and dependencies that the code does not reveal.
- **Task queue as a backlog.** Send off tangents and drive-by fixes as background
  tasks, then review the PRs later. The point is to stay in flow, not to finish a
  whole PR in one pass.
- **Best-of-N.** Generate several candidates in parallel, then pick one or
  combine parts of several. See [[agent-orchestration]].
- **Bug-class sweeps.** After a fix, ask where the same bug pattern appears
  elsewhere and spin follow-up tasks. Overnight runs against low-coverage
  modules yield test PRs.

## Notable claims & data (self-reported)

- One engineer merged 4 PRs during a day of meetings. Another shipped 3–4
  low-priority fixes that would have stayed in the backlog.
- One anecdote: 5 minutes of prompting saved 30 minutes of work on a performance
  issue.
- One anecdote: a legacy `getUserById()` migration across the codebase took
  minutes instead of hours.

## Entities

[[openai]], [[openai-codex]]

## Concepts

[[agent-instructions]], [[agent-harness]], [[workflow-patterns]],
[[agent-orchestration]]

## Connections

The internal-use counterpart to [[openai-codex-as-a-platform]] and
[[openai-automating-repetitive-work-codex]]. The later
[[openai-codex-maxxing-long-running-work]] moves from one-hour tasks to durable,
multi-day threads. Compare Anthropic's internal-use accounts in
[[anthropic-running-ai-native-engineering-org]].
