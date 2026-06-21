---
title: Claude Code
type: entity
subtype: product
created: 2026-06-21
updated: 2026-06-21
tags: [anthropic, claude-code, agents, tooling]
---

# Claude Code

> Anthropic's agentic coding tool. In this wiki it's the worked example for how to
> *steer* a real agent and how skills compound in practice.

## Overview

A command-line / desktop agentic developer tool by [[anthropic]]. Its design is
the subject of two ingested sources on agent best practices:
[[anthropic-steering-claude-code]] (the seven steering mechanisms) and
[[anthropic-lessons-building-claude-code-skills]] (how skills are used at scale).

## Key facts

- Offers seven steering mechanisms — CLAUDE.md, rules, skills, subagents, hooks,
  output styles, system-prompt appending. (see [[agent-steering]])
- Skills, subagents, hooks, and styles bundle into **plugins** for sharing.
  (see [[agent-skills]])
- Subagents run in isolated context and can nest/orchestrate at scale.
  (see [[agent-orchestration]])

## Relationships

- Built by [[anthropic]]; related to the [[claude-agent-sdk]] and
  [[claude-managed-agents]] surfaces.

## Appears in

- [[anthropic-steering-claude-code]]
- [[anthropic-lessons-building-claude-code-skills]]

## Contradictions / open questions

- _None recorded._
