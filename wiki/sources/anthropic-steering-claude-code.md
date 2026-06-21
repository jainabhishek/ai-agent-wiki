---
title: "Anthropic: Steering Claude Code"
type: source
created: 2026-06-21
updated: 2026-06-21
author: Anthropic (Claude blog)
date: 2026-06-18
source_url: https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more
source_path: raw/anthropic-steering-claude-code.md
tags: [agents, claude-code, configuration, skills, hooks, best-practices]
---

# Anthropic: Steering Claude Code

> A practical taxonomy of the seven mechanisms for instructing an agentic coding
> tool — and when to reach for each. The throughline: match the mechanism to
> *when instructions load, whether they persist, and how much authority they
> carry.*

## Summary

[[claude-code]] exposes seven steering mechanisms: **CLAUDE.md files, rules,
skills, subagents, hooks, output styles, and system-prompt appending.** Choosing
correctly is a context-engineering decision — load the right instructions at the
right time without wasting tokens. See [[agent-steering]] and [[context-engineering]].

## Key points

- **CLAUDE.md** (<200 lines): project overview/conventions; root persists,
  subdir loads on demand. Push procedures into [[agent-skills]], constraints into
  rules.
- **Rules**: path-scoped (`paths:`) constraints — load only when relevant.
- **Skills**: names/descriptions load at start; body on invocation; re-injected
  up to a token budget on compaction.
- **Subagents**: isolated context; only summaries return — see
  [[agent-orchestration]].
- **Hooks**: deterministic lifecycle automation; a PreToolUse hook can deny a
  tool call (exit 2). The deterministic complement to [[guardrails]].
- **Output styles / system-prompt append**: high-authority system-prompt edits;
  use sparingly.

## Concepts

[[agent-steering]], [[agent-skills]], [[context-engineering]],
[[agent-orchestration]], [[agent-design-principles]]

## Entities

[[anthropic]], [[claude-code]]

## Notable claims & data

- Subagents nest up to five levels and can orchestrate tens-to-hundreds of
  background agents; plans/intermediate results live in script variables, not
  context. (see [[agent-orchestration]])
- Bundles of skills/subagents/hooks/styles ship as **plugins**.

## Connections

Concrete instance of the principles in [[harnessing-claudes-intelligence]] ("let
Claude manage context") and a counterpart to OpenAI's instruction/guardrail
advice in [[openai-practical-guide-to-building-agents]].
