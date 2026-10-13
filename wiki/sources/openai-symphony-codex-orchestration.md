---
title: "OpenAI (Eng): Symphony — An Open-Source Spec for Codex Orchestration"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Alex Kotliarskyi, Victor Zhu, Zach Brock (OpenAI)
date: 2026-04-27
source_url: https://openai.com/index/open-source-codex-orchestration-symphony/
source_path: raw/openai-symphony-codex-orchestration.md
tags: [orchestration, codex, coding-agent, issue-tracker, long-running-agents, harness, spec]
---

# OpenAI (Eng): Symphony — An Open-Source Spec for Codex Orchestration

> OpenAI Engineering post (byline 2026-04-27) introducing Symphony, a
> language-agnostic `SPEC.md` for a daemon that turns an issue tracker into the
> control plane for coding agents: every open ticket gets an agent in its own
> workspace.

## Summary

The team behind OpenAI's no-human-written-code repository (see
[[openai-harness-engineering]]) found that the next bottleneck was human
attention: engineers could run three to five interactive [[openai-codex]]
sessions before context switching cut productivity. Symphony replaces session
supervision with ticket-level delegation. A long-running service polls Linear,
creates a deterministic workspace per active issue, and runs a Codex
app-server session there until the issue leaves an active state. Humans review
results at handoff states such as `Human Review`. OpenAI reports, as a
self-reported internal figure, a 500% increase in landed PRs for some teams in
the first three weeks.

The repository is mainly a written spec, with an Elixir reference
implementation that Codex wrote in one shot from the spec. OpenAI says it will
not maintain Symphony as a product and asks readers to point their own coding
agent at the spec. Date note: the byline is 2026-04-27, but embedded social
posts about the release date from 2026-03-06, so the repository predates the
post.

## Key points

- **Work, not sessions, is the unit.** One issue can yield several PRs across
  repos or no code at all. Agents decompose large work into a task DAG with
  blockers; only unblocked tasks dispatch, so parallelism follows dependencies.
  Agents also file follow-up issues for out-of-scope findings.
- **Deterministic scheduler, goal-directed agent.** The orchestrator is
  ordinary code: one authoritative in-memory state, claim states (`Unclaimed`,
  `Claimed`, `Running`, `RetryQueued`, `Released`), reconciliation before each
  dispatch, exponential backoff, and stall detection. But treating agents as
  "rigid nodes in a state machine" failed. The team moved to giving agents
  objectives plus tools (`gh` CLI, CI-log skills) instead of strict
  transitions.
- **Policy lives in the repo.** `WORKFLOW.md` holds YAML config and the
  per-issue prompt template. It encodes the team's previously implicit human
  workflow, and changes reload live. Templates render strictly: unknown
  variables fail the attempt.
- **The orchestrator reads, the agent writes.** Symphony only reads the
  tracker. Ticket transitions, comments, and PR links are agent tool calls.
- **Failures become harness improvements.** Misses led to guardrails and skills
  rather than hand patches: end-to-end tests, Chrome DevTools app driving, and
  QA smoke tests.
- **Safety invariants are path-based.** The agent runs only with
  `cwd == workspace_path`, inside the workspace root, with sanitized keys.
  Approval and sandbox posture is left to each implementation. The spec's
  example high-trust policy auto-approves commands and file edits and treats
  any user-input request as a hard failure, so no run stalls.
- **Credentials stay with the orchestrator.** The `linear_graphql` dynamic tool
  runs GraphQL with Symphony's own auth. The Linear token never reaches the
  agent's process or containers, and no Linear MCP is needed.
- **The spec doubles as a test.** Codex implemented the spec in TypeScript, Go,
  Rust, Java, and Python to find ambiguities.

## Entities

[[openai]], [[openai-codex]]

## Concepts

[[agent-orchestration]], [[agent-harness]], [[guardrails]],
[[agents-vs-workflows]], [[agent-steering]], [[workflow-patterns]]

## Notable claims & data

- 3–5 concurrent interactive sessions per engineer before productivity drops
  (OpenAI internal observation).
- +500% landed PRs on some teams in three weeks; over 15K GitHub stars by
  April 23 (self-reported).
- Spec defaults: poll 30 s, 10 concurrent agents, 20 turns per worker, 1 h turn
  timeout, 5 min stall timeout, failure backoff
  `min(10000 * 2^(attempt-1), 300000)` ms.
- Not every task fits: ambiguous or judgment-heavy work stays in interactive
  sessions.

## Connections

- **Follows [[openai-harness-engineering]]**, which built the agent-friendly
  repo that Symphony orchestrates. It runs on the app-server integration layer
  described in [[openai-codex-as-a-platform]] and
  [[openai-codex-app-server-harness]].
- **Human attention as the bottleneck** converges with
  [[anthropic-building-effective-human-agent-teams]] and with
  [[openai-sora-android-with-codex]], where parallel sessions moved the
  bottleneck to review and decisions.
- **Credentials kept out of the agent** matches the "credentials never enter the
  sandbox" pattern in [[guardrails]], for example the git proxy in
  [[anthropic-eng-claude-code-sandboxing]].
- **Objectives over strict transitions** echoes the agent-versus-workflow
  distinction in [[agents-vs-workflows]]. The orchestration layer stays a
  deterministic workflow, and the agent inside each ticket is autonomous.
- Compare the git-and-lock-file coordination without an orchestrator in
  [[anthropic-eng-building-c-compiler]], and Claude Code cloud sessions with
  one VM and branch per task in [[anthropic-claude-code-in-the-cloud]].
- The Tax AI loop in [[openai-self-improving-tax-agents-codex]] cites Symphony
  as a basis.
