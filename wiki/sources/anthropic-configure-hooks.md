---
title: "Anthropic: How to Configure Claude Code Hooks"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com articles)
date: 2025-12-11
source_url: https://claude.com/resources/articles/how-to-configure-hooks
source_path: raw/anthropic-configure-hooks.md
tags: [claude-code, hooks, configuration, guardrails, automation]
---

# Anthropic: How to Configure Claude Code Hooks

> A how-to on Claude Code hooks as of December 2025: the eight hook events, the
> settings-file locations, matcher syntax, the stdin/exit-code contract, and how
> to debug hooks safely.

## Summary

Anthropic article (2025-12-11) for experienced [[claude-code]] users. A hook is a
user-defined shell command (or, in the Stop/SubagentStop examples, a model
prompt) that runs on a session event, receives event JSON on stdin, and answers
through exit codes, stdout, and optional JSON. Hooks solve three problems:
removing repeated manual steps (formatting, approvals), enforcing project rules
every time, and injecting dynamic context (git status, sprint notes). The hook
list and fields describe Claude Code as of the article date; check current
documentation for later events or changed fields.

## Key points

- **Eight events (as of 2025-12-11)**: `PreToolUse` (before a tool runs; can
  approve, block, ask, or modify input), `PermissionRequest` (before a
  permission dialog; allow, deny, or ask), `PostToolUse` (after success; e.g.
  formatter), `PreCompact` (matcher `auto` or `manual`; back up transcript),
  `SessionStart` (stdout becomes context), `Stop` (decide whether the task is
  done), `SubagentStop` (same for subagents created via the Task tool),
  `UserPromptSubmit` (stdout added to context with the prompt).
- **Locations**: `.claude/settings.json` (project, shared),
  `~/.claude/settings.json` (user), `.claude/settings.local.json` (local,
  uncommitted); enterprise-managed policy settings also exist.
- **Matchers** apply only to PreToolUse, PostToolUse, PermissionRequest; exact
  name, `A|B` alternation, `*` or empty for all; case-sensitive; argument
  patterns such as `Bash(npm test*)`; MCP tools as `mcp__<server>__.*`.
- **Contract**: stdin fields `session_id`, `transcript_path`, `cwd`,
  `permission_mode`, `hook_event_name` (+ `tool_name`, `tool_input` for tool
  hooks). Exit 0 = success; exit 2 = block, stderr goes to Claude; other codes =
  non-blocking error. JSON fields `decision`, `reason`, `continue`,
  `updatedInput`.
- **Execution**: env vars `CLAUDE_PROJECT_DIR`, `CLAUDE_CODE_REMOTE`,
  `CLAUDE_ENV_FILE`; 60-second default timeout per hook; matching hooks run in
  parallel; identical commands deduplicated.
- **Security**: hooks run with the user's permissions; direct edits to hook
  config require review in the `/hooks` menu before they take effect; validate
  stdin, quote variables, use absolute paths, avoid `.env`/credential files.
- **Debugging**: every hook gets `transcript_path` (JSONL session log); wrap hook
  commands in a logging script to record why a hook allowed or blocked.
- **Start small**: one hook for a real friction point; a PostToolUse formatter is
  the suggested first hook.

## Entities

[[anthropic]], [[claude-code]]

## Concepts

[[agent-steering]], [[guardrails]], [[context-engineering]]

## Notable claims & data

- The article states project-level settings take precedence over user-level.
- The PostToolUse example uses an env var `$CLAUDE_TOOL_INPUT_FILE_PATH`, and the
  Stop section says `"continue": true` makes Claude keep working. Neither was
  checked against the current hooks reference during capture; treat as the
  article's claims (2025-12-11), not verified contract.

## Connections

The deterministic-hook role is also described in
[[anthropic-steering-claude-code]] and [[anthropic-eng-claude-code-auto-mode]];
hooks as approval gates and build guardrails are developed further in
[[anthropic-ai-native-sdlc-playbook]]; self-improving stop/start hooks appear in
[[anthropic-claude-code-large-codebases]].
