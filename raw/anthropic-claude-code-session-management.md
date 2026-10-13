# Using Claude Code: session management and 1M context — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/using-claude-code-session-management-and-1m-context
> Publisher: Anthropic (claude.com articles) · Date: 2026-04-15
> Captured: 2026-10-12 via curl (condensed).

Author: Thariq Shihipar, member of technical staff at Anthropic (Claude Code).
Category: Best practices. Product: Claude Code. Listed reading time 8 min.

## Introduction
- Announces `/usage`, a slash command for understanding Claude Code usage,
  informed by customer conversations.
- Customers vary widely in session habits, especially after the update to 1M
  context: one long session, two in a terminal, a new session per prompt; when
  to compact, rewind, or use subagents. Most of this is context-window
  management.

## A quick primer on context, compaction and context rot
- Context window: everything the model sees — system prompt, conversation, tool
  calls and outputs, files read. Claude Code's window is 1M tokens.
- Context rot: performance degrades as context grows; attention spreads over
  more tokens and old irrelevant content distracts.
- Compaction: near the hard limit, the task is summarized and work continues in
  a new window; users can also trigger it.

## Every turn as a branching point
After Claude finishes a turn, five options:
- Continue — another message in the same session.
- `/rewind` (Esc Esc) — jump back to an earlier message and retry from there.
- `/clear` — new session, usually with a brief distilled from what was learned.
- Compact — summarize and continue on top of the summary.
- Subagents — delegate the next chunk to a clean context and pull back only the
  result.

## When to start a new session
- Rule of thumb: new task, new session.
- 1M context makes longer tasks more reliable (example: a full-stack app from
  scratch), but context rot can occur.
- Related follow-on tasks (docs for a feature just built) may justify staying,
  since a new session would re-read the files, slower and more expensive.

## Rewinding instead of correcting
- Double-Esc or `/rewind` drops all messages after the chosen point.
- Example: Claude reads five files, tries an approach that fails. Instead of
  replying with a correction, rewind to just after the file reads and re-prompt
  with the lesson (don't use approach A because module foo lacks that; go to B).
- "Summarize from here" or `/rewind` can have Claude write a handoff message of
  its learnings, like a note from a future self.

## Compacting vs. launching a fresh session
- `/compact`: model summarizes and replaces history. Lossy, no user writing;
  Claude may include learnings and files thoroughly. Steerable with instructions
  (example: `/compact focus on the auth refactor, drop the test debugging`).
- `/clear`: user writes what matters (task, constraints, key files, ruled-out
  approaches) and starts clean. More work; context is exactly what the user chose.

## What causes a bad autocompact?
- Bad compactions happen when the model cannot predict where the work is going.
  Example: autocompact after a long debugging session, then the next message
  asks to fix a different warning in `bar.ts` that the summary dropped.
- Because of context rot, the model is at its least capable when compacting.
  With 1M context there is more room to `/compact` proactively with a statement
  of what comes next.

## Subagents and fresh context windows
- Good fit when a chunk of work will produce much intermediate output not needed
  later. A subagent spawned via the Agent tool gets a fresh window and returns
  only a final report.
- Anthropic's test: will I need this tool output again, or just the conclusion?
- Claude Code spawns subagents automatically, but you can ask explicitly.
  Examples: verify work against a spec file; read another codebase and summarize
  how it implemented auth, then implement it the same way; write feature docs
  from the git changes.

## Putting it together (decision table)
| Situation | Reach for | Why |
|---|---|---|
| Same task, context still relevant | Continue | Everything is still useful; do not pay to rebuild it |
| Claude went down a wrong path | Rewind (double-Esc) | Keep useful reads, drop the failed attempt, re-prompt with the lesson |
| Mid-task, session bloated with stale debugging/exploration | `/compact <hint>` | Low effort; Claude decides what mattered; steer if needed |
| Genuinely new task | `/clear` | No rot; you control what carries forward |
| Next step makes lots of output where only the conclusion matters (search, verification, docs) | Subagent | Tool noise stays in the child context |
