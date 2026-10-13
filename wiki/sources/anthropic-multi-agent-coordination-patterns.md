---
title: "Anthropic: Multi-Agent Coordination Patterns"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Cara Phillips (Anthropic, claude.com articles)
date: 2026-04-10
source_url: https://claude.com/resources/articles/multi-agent-coordination-patterns
source_path: raw/anthropic-multi-agent-coordination-patterns.md
tags: [multi-agent, orchestration, coordination, patterns, best-practices]
---

# Anthropic: Multi-Agent Coordination Patterns

> A catalog of five multi-agent coordination patterns, each with its mechanism,
> best fit, and failure modes, plus pairwise rules for choosing between them.

## Summary

Cara Phillips (Anthropic, 2026-04-10) describes five ways to coordinate
agents: **generator-verifier**, **orchestrator-subagent**, **agent teams**,
**message bus**, and **shared state**. The choice depends on four axes: how long
a worker keeps its context, how predictable the workflow is, whether agents need
each other's findings, and whether work flows as events or accumulates as
knowledge. The recommendation is to start with orchestrator-subagent (widest
coverage, least overhead) and move to another pattern only when a specific need
appears. Production systems often combine patterns. Not model-specific. See
[[agent-orchestration]].

## Key points

- **Generator-verifier.** Generator drafts; verifier accepts or rejects against
  explicit criteria and returns feedback; loop until accepted or an iteration
  cap. Failure modes: a vague verifier rubber-stamps; loops oscillate. Mitigate
  with a cap plus a fallback (human escalation, or best attempt with caveats).
  The Anthropic name for [[workflow-patterns]]' evaluator-optimizer.
- **Orchestrator-subagent.** Lead plans, delegates bounded subtasks, and
  synthesizes. Fits clear decomposition with low interdependence. Failure modes:
  the orchestrator is an information bottleneck; sequential dispatch adds tokens
  without speed.
- **Agent teams.** A coordinator spawns persistent workers that claim tasks from
  a shared queue and keep context across assignments (subagents end after one
  task). Fits independent long-running work such as a per-service migration.
  Failure modes: no sharing of intermediate findings; hard completion detection
  when durations vary; conflicting edits on shared resources.
- **Message bus.** Agents publish and subscribe; a router delivers by topic; new
  agents join without rewiring. Fits event-driven pipelines (security alert
  triage). Failure modes: hard tracing; silent drops or misroutes; an LLM router
  adds its own errors.
- **Shared state.** No coordinator; agents read and write a persistent store.
  No single point of failure. Failure modes: duplicate or contradictory work and
  reactive loops. Locking, versioning, and partitioning fix write conflicts;
  loops need explicit termination (time budget, no new findings over N cycles,
  or a judge agent).
- **Pairwise choice rules.** Short focused subtasks → orchestrator-subagent;
  sustained context → agent teams. Fixed sequence → orchestrator; emergent,
  event-driven flow (orchestrator conditionals multiplying) → message bus.
  Partitioned work → agent teams; findings flowing between agents → shared
  state. Stage pipeline → bus; accumulating knowledge → shared state.

## Entities

[[anthropic]], [[claude-code]]

## Concepts

[[agent-orchestration]], [[workflow-patterns]], [[multi-agent-economics]],
[[agent-evals]], [[agent-verification]], [[agent-design-principles]]

## Notable claims & data

- No benchmark numbers; the article is a design taxonomy. The cited example of
  orchestrator-subagent is [[claude-code]] subagents.
- The message bus and shared state patterns are new to the wiki; existing pages
  cover manager/handoff (OpenAI) and orchestrator-worker (Anthropic) shapes.

## Connections

- Extends the OpenAI manager vs. handoff split in
  [[openai-practical-guide-to-building-agents]] with three more patterns.
- Orchestrator-subagent in production: [[anthropic-eng-multi-agent-research-system]].
- Shared state with no orchestrator in practice: the 16-agent compiler in
  [[anthropic-eng-building-c-compiler]].
- Generator-verifier in a long-running harness:
  [[anthropic-eng-harness-design-long-running-apps]].
- Companion Claude Code guide: [[anthropic-subagents-in-claude-code]]; related
  Anthropic guidance: [[anthropic-building-multi-agent-systems]].
