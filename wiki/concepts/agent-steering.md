---
title: Agent Steering & Configuration
type: concept
created: 2026-06-21
updated: 2026-06-21
tags: [steering, configuration, agents, claude-code, best-practices]
---

# Agent Steering & Configuration

> How you instruct an agent — and the discipline of choosing the *right
> mechanism* based on when instructions load, whether they persist, and how much
> authority they carry. Drawn from [[anthropic-steering-claude-code]] using
> [[claude-code]] as the worked example.

## The seven mechanisms (Claude Code)

| Mechanism | Loads | Persists | Use for |
|-----------|-------|----------|---------|
| **CLAUDE.md** | start (root) / on-demand (subdir) | yes | overview, conventions, build commands (<200 lines) |
| **Rules** | start / on file touch | yes | constraints, path-scoped via `paths:` |
| **Skills** | desc at start, body on invoke | re-injected on compaction | repeatable procedures → [[agent-skills]] |
| **Subagents** | on invoke | summary only | isolated side tasks → [[agent-orchestration]] |
| **Hooks** | lifecycle events | n/a | deterministic automation; deny tool calls |
| **Output styles** | system prompt | never compacted | role changes (high authority, sparse) |
| **System-prompt append** | invocation | cached | coding standards, domain knowledge |

## Best practices

- **Match the mechanism to the job.** Procedures → skills; constraints → rules;
  must-happen-deterministically → hooks; isolated exploration → subagents.
- **Path-scope constraints** (`paths:` frontmatter) so unrelated work stays clean
  and tokens aren't wasted.
- **Keep CLAUDE.md lean** (<200 lines); move procedures to skills, preferences to
  user-level files.
- **Prefer deterministic hooks over "never do this" prose** — a PreToolUse hook
  can inspect and deny a tool call (exit 2). The deterministic complement to
  [[guardrails]].
- **Use output styles sparingly** — they override default guidance on scope,
  security, and testing.

## Why it matters

Steering is applied [[context-engineering]]: the goal is the right instructions at
the right moment, not all instructions all the time. This is the Anthropic-side
analogue to OpenAI's [[agent-instructions]] guidance.

## Related concepts

- [[agent-skills]], [[context-engineering]], [[agent-instructions]],
  [[agent-orchestration]], [[guardrails]]

## Key entities

- [[anthropic]], [[claude-code]]

## Appears in

- [[anthropic-steering-claude-code]]
- [[anthropic-lessons-building-claude-code-skills]]

## Contradictions / open questions

- _None recorded._
