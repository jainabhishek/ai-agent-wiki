---
title: "Anthropic: Using Claude Code — Session Management and 1M Context"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Thariq Shihipar (Anthropic)
date: 2026-04-15
source_url: https://claude.com/resources/articles/using-claude-code-session-management-and-1m-context
source_path: raw/anthropic-claude-code-session-management.md
tags: [claude-code, context-engineering, compaction, context-rot, subagents, sessions, best-practices]
---

# Anthropic: Using Claude Code — Session Management and 1M Context

> A decision guide for what to do after each [[claude-code]] turn: continue,
> rewind, clear, compact, or delegate to a subagent. The basis is context rot in
> a 1M-token window.

## Summary

Published 2026-04-15 on claude.com articles by Thariq Shihipar of [[anthropic]]. The
post launched alongside the `/usage` command. It states that Claude Code has a
1M-token context window. The later [[anthropic-claude-code-session-cost]]
(2026-08-14) qualifies this as "if you're on a 1M model". Context rot means
performance degrades as context grows, because attention spreads and old content
distracts. Compaction summarizes the task near the hard limit and continues in a new
window.

Every finished turn is a branching point with five options. The rule of thumb is one
new session per new task. A follow-on task that reuses fresh context, such as docs for
a feature just built, can justify staying in the session.

## Key points

- **Rewind instead of correcting.** When an approach fails after useful file reads,
  rewind (Esc Esc or `/rewind`) to just after the reads and re-prompt with the
  lesson. Do not append a correction on top of the failed attempt. Claude can also
  write a handoff summary of what it learned.
- **Compact versus clear.** `/compact` is lossy and model-written, and it can take a
  steering hint (`/compact focus on ...`). `/clear` with a user-written brief takes
  more work, but the user controls exactly what carries forward.
- **Why autocompact goes bad.** It fails when the model cannot predict where the
  work goes next; for example, a later request references a warning that the
  debugging-focused summary dropped. The model is at its least capable at compaction
  time because of context rot. Compact proactively and say what comes next.
- **Subagents.** Use one when a chunk of work will produce much intermediate output.
  Anthropic's test: will I need this tool output again, or just the conclusion?
  Examples: verify against a spec, study another codebase's auth flow, write docs
  from git changes.
- **Decision table.** Continue: the context is still useful. Rewind: wrong path.
  `/compact <hint>`: mid-task but bloated. `/clear`: new task. Subagent: the output
  is noisy and only the conclusion matters.

## Entities

[[anthropic]], [[claude-code]]

## Concepts

[[context-engineering]], [[agent-orchestration]]

## Notable claims & data

- The post's general claim: the model is weakest when compacting. This supports
  proactive, directed compaction over waiting for autocompact (see
  [[context-engineering]] on compaction).

## Connections

The cost-side companion is [[anthropic-claude-code-session-cost]]. Same author as
[[anthropic-fable-field-guide-unknowns]]. Context rot and compaction theory come
from [[anthropic-eng-context-engineering]]. The subagent guidance matches
[[anthropic-subagents-in-claude-code]] and [[anthropic-steering-claude-code]].
