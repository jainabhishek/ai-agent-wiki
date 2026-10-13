---
title: "Anthropic: Building multi-agent systems — when and how to use them"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Cara Phillips (Anthropic, claude.com articles)
date: 2026-01-23
source_url: https://claude.com/resources/articles/building-multi-agent-systems-when-and-how-to-use-them
source_path: raw/anthropic-building-multi-agent-systems.md
tags: [multi-agent, orchestration, subagents, context-engineering, verification, decomposition]
---

# Anthropic: Building multi-agent systems — when and how to use them

> Anthropic's decision guide for the orchestrator-subagent pattern: start with
> one agent, go multi-agent only for context protection, parallelism, or
> specialization, and decompose by context boundary rather than by work type.

## Summary

Published by Anthropic on claude.com (2026-01-23, Cara Phillips), first in a
series on multi-agent systems. It defines a multi-agent system as several LLM
instances with separate contexts, coordinated by code, and covers only the
orchestrator-subagent pattern. Its central claim: multi-agent systems are often
built where a single agent would do better, and typically cost 3–10x the tokens
of a single agent for the same task. Three situations justify them: context
pollution, parallelizable work, and specialization. The guide's main design rule
is **context-centric decomposition**: split work where context can truly be
isolated, not by type of work. It recommends a **verification subagent** as a
pattern that works across domains, and names the "early victory problem" as its
main failure mode. Examples use `claude-sonnet-4-5`; the guide names Opus 4.5 as
an orchestrator able to check subagent work itself. Thresholds are stated as
guidelines that will move as models improve.

## Key points

- **Single agent first.** Each extra agent adds a failure point and a prompt to
  maintain. Teams that split plan/execute/review/iterate lost context at each
  hand-off and spent more tokens coordinating than working.
- **Context protection.** Isolate a subtask when it produces >1,000 tokens that
  are mostly irrelevant to the main task, has clear extraction criteria, or is a
  lookup that needs filtering. Example: an order-lookup subagent returns 50–100
  tokens instead of 2,000+.
- **Parallelization** buys thoroughness, not speed: total compute rises and the
  whole run often takes longer than a single agent.
- **Specialization signals.** Tool count (often 20+), tools spanning unrelated
  domains, or new tools degrading old tasks. Conflicting personas and heavy
  domain context are other reasons. Cost: routing errors and prompt upkeep.
- **Before going multi-agent for tools,** try on-demand tool discovery (Tool
  Search Tool, up to 85% fewer tokens). For context limits, compaction now
  extends single-agent horizons.
- **Decompose by context.** Good boundaries: independent research paths,
  components with a clean API contract, blackbox verification. Bad boundaries:
  sequential phases of one piece of work, tightly coupled components, shared
  state. Splitting by role produces a "telephone game."
- **Verification subagent.** Give the verifier the artifact, success criteria,
  and tools, not the build history. Retry loop feeds verifier issues back to the
  implementer (`max_attempts=3` in the example).
- **Early victory problem.** Verifiers declare success after one or two tests.
  Fix with concrete criteria, edge cases, negative tests, and explicit "run the
  complete suite" instructions.

## Entities

[[anthropic]], [[claude]], [[claude-managed-agents]]

## Concepts

[[agent-orchestration]], [[multi-agent-economics]], [[context-engineering]],
[[agents-vs-workflows]], [[tool-design]], [[agent-evals]], [[agent-verification]],
[[agent-design-principles]]

## Notable claims & data

- Multi-agent: typically 3–10x tokens of single-agent for equivalent tasks
  (Anthropic testing). Compare ~15x chat tokens in
  [[anthropic-eng-multi-agent-research-system]] (different baseline).
- In a role-split experiment (planner, implementer, tester, reviewer), subagents
  used more tokens on coordination than on work.
- 40+ tools across three platforms caused selection errors; splitting into
  specialists of 8–10 tools each resolved them (illustrative example).
- **Tension:** "thoroughness, not speed" and "often longer overall" vs the
  research-system report that parallelism cut research time up to 90%. The
  research-system figure compares parallel with sequential subagents; this guide
  compares multi-agent with single-agent. See [[agent-orchestration]].

## Connections

- The series' next post: [[anthropic-multi-agent-coordination-patterns]].
- Builds on [[anthropic-building-effective-agents]] (single-agent patterns),
  [[anthropic-eng-context-engineering]], and
  [[anthropic-eng-multi-agent-research-system]].
- Tool Search Tool claim: [[anthropic-eng-advanced-tool-use]].
- Related: [[anthropic-subagents-in-claude-code]], [[anthropic-advisor-strategy]]
  (escalation instead of decomposition), [[anthropic-verification-loops-with-skills]].
