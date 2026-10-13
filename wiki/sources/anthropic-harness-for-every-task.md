---
title: "Anthropic: A harness for every task: dynamic workflows in Claude Code"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Thariq Shihipar and Sid Bidasaria (Anthropic, claude.dev blog)
date: 2026-06-02
source_url: https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/
source_path: raw/anthropic-harness-for-every-task.md
tags: [claude-code, workflows, multi-agent, orchestration, subagents, verification, harness]
---

# Anthropic: A harness for every task: dynamic workflows in Claude Code

> Introduces dynamic workflows: Claude Code writes a task-specific multi-agent
> harness as a JavaScript file, built from `agent()`, `parallel()`, and
> `pipeline()`, plus six composable patterns and when the extra tokens are
> worth it.

## Summary

A dynamic workflow is a JavaScript file that [[claude-code]] writes per request
to orchestrate subagents. Three primitives: `agent(prompt, opts)` (options
`schema`, `model`, `isolation` = worktree/remote, `agentType`), `parallel()`,
and `pipeline()`. The motivation is three failure modes of a single context
that both plans and executes — **agentic laziness** (stopping at 35 of 50
items), **self-preferential bias** (grading its own work), and **goal drift**
(losing requirements after compaction) — which separate focused subagents
counter. Static harnesses (Claude Agent SDK, `claude -p`) must be generic; a
dynamic one is tailored to the task. The post was written when Claude Opus 4.8
was current and says that model made per-task harness writing viable. Workflows
reproduce Anthropic's earlier hand-built harnesses (Research, security analysis,
agent teams, Code Review) and cost more tokens, so they suit complex,
high-value tasks. See [[agent-orchestration]] and [[workflow-patterns]].

## Key points

- **Six composable patterns:** classify-and-act; fan-out-and-synthesize;
  adversarial verification (separate agent + rubric); generate-and-filter;
  tournament (N approaches, pairwise judging); loop until done (stop
  condition).
- **Use cases:** migrations (Bun rewritten from Zig to Rust — one subagent per
  unit in a worktree, adversarial review, merge); deep research and deep
  verification (one checker per claim); sorting 1,000+ items via brackets so no
  context holds everything; rule adherence (one verifier per rule + skeptic
  filter) and rule mining into `CLAUDE.md`; root-cause investigation with
  verifiers and refuters; evals; model routing by a classifier agent.
- **Quarantine for untrusted input:** read-only reader agents summarize
  untrusted content into structured output; a separate high-privilege actor
  acts only on the summaries (fix + PR, or escalate).
- **When not to:** routine coding; parallelism and specialization must pay for
  coordination cost, as with multi-agent vs single-agent generally.
- **Operation:** trigger with a request or the word `ultracode`; combine with
  `/loop` (repeat) and `/goal` (hard completion); set token caps in the prompt;
  save runs (`s`) to `~/.claude/workflows` or ship inside a skill folder
  (`SKILL.md` + `*.workflow.js` + `rubric.md`) as a template.

## Entities

[[anthropic]], [[claude-code]], [[claude-agent-sdk]], [[claude]]

## Concepts

[[agent-orchestration]], [[workflow-patterns]], [[agents-vs-workflows]],
[[agent-harness]], [[multi-agent-economics]], [[guardrails]], [[agent-evals]], [[agent-verification]],
[[agent-skills]]

## Notable claims & data

- Panel examples: `review-changes` 14 agents / 482k tokens / 6m 12s;
  `deep-research` 22 agents / 1.1M tokens / 11m 3s.
- Interrupted workflows resume when the session resumes.
- Blurs the [[agents-vs-workflows]] line: the model authors the workflow code at
  run time, so the predefined-code-path property belongs to each run, not to the
  system.

## Connections

Generalizes the orchestrator–worker system of
[[anthropic-eng-multi-agent-research-system]] and the evaluator–optimizer and
parallelization patterns of [[anthropic-building-effective-agents]] into a
user-invoked primitive. The cost caution matches [[multi-agent-economics]] and
[[cursor-agent-swarm-model-economics]]. Verifier agents with rubrics are cited
by [[anthropic-new-rules-context-engineering-claude-5]]. Subagent nesting and
scripted orchestration were previewed in [[anthropic-steering-claude-code]].
The post closes by pointing to Anthropic's post on three harness design
patterns (not linked here; target page ambiguous).
