---
title: "Anthropic: How and When to Use Subagents in Claude Code"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com articles), no named author
date: 2026-04-07
source_url: https://claude.com/resources/articles/subagents-in-claude-code
source_path: raw/anthropic-subagents-in-claude-code.md
tags: [claude-code, subagents, context-engineering, hooks, skills, best-practices]
---

# Anthropic: How and When to Use Subagents in Claude Code

> A practical guide to Claude Code subagents: what they are, the signals that
> call for one, the four ways to direct them, and when not to use them.

## Summary

Anthropic (2026-04-07) presents subagents as the fix for context bloat in long
[[claude-code]] sessions: an isolated Claude instance with its own context
window that does a side task and returns only the result. Subagents start
fresh, can run in parallel, and can carry different permissions. Built-in types
are General-purpose, Plan, and Explore (fast, read-only). The post lists five
signals for delegation, four ways to direct delegation (conversation, custom
subagents, CLAUDE.md policy, skills, hooks), and five cases where subagents hurt.
Its closing advice: start conversational and automate only the patterns that
repeat. Not model-specific. See [[agent-orchestration]], [[context-engineering]].

## Key points

- **Signals to delegate:** research that reads dozens of files; independent
  subtasks; a need for a fresh, unbiased reviewer; verification before commit
  (overfitting to tests, missed edge cases); phased pipelines. Heuristic: 10+
  files or 3+ independent pieces.
- **Custom subagents** are markdown files in `.claude/agents/` (project) or
  `~/.claude/agents/` (user), each with its own system prompt, tools, and
  optional model; create with `/agents`. The `description` field drives
  automatic routing, so it should state trigger conditions, not only
  capability. See [[agent-skills]] for the same description-routing idea.
- **Escalation ladder for steering:** conversational request → CLAUDE.md policy
  (always loaded) → skill (`.claude/skills/`, loaded on demand) → hook (most
  automated). See [[agent-steering]].
- **Stop-hook verification loop:** a Stop hook runs tests and returns
  `decision: "block"` with a `reason` so Claude keeps working; a
  `stop_hook_active` guard prevents infinite loops. See [[guardrails]].
- **When not to use subagents:** sequential dependent work; edits to the same
  file; small tasks; a sprawling specialist roster (makes auto-routing less
  reliable; a handful is typical); agents that must talk to each other
  (subagents report only to the main thread; agent teams are the heavier peer
  option).
- Controls: `Ctrl+B` backgrounds a running subagent; `/tasks` lists background
  work; `/clear` resets context but discards history, unlike a fresh subagent.

## Entities

[[anthropic]], [[claude-code]], [[claude]]

## Concepts

[[agent-orchestration]], [[context-engineering]], [[agent-steering]],
[[agent-skills]], [[guardrails]], [[multi-agent-economics]]

## Notable claims & data

- No measured results. The 10-files / 3-pieces threshold is a stated rule of
  thumb, not a benchmark.

## Connections

- Narrower companion to [[anthropic-steering-claude-code]], which covers all
  seven steering mechanisms.
- The orchestrator-subagent pattern in
  [[anthropic-multi-agent-coordination-patterns]] uses Claude Code subagents as
  its example; "agent teams" there is the peer-communication alternative.
- Writer/reviewer separation matches [[anthropic-eng-claude-code-best-practices]].
- Hook mechanics in more depth: [[anthropic-configure-hooks]].
