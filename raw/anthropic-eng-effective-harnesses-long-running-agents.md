# Effective harnesses for long-running agents — Anthropic Engineering (raw capture)

> Source: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
> Publisher: Anthropic Engineering
> Captured: 2026-06-21 via WebFetch (condensed).

## What a harness is

The structural framework that lets an agent maintain coherence across multiple
context windows — here, the Claude Agent SDK plus prompting strategies and
environmental scaffolding.

## Core architecture: two-agent pattern

- **Initializer agent** (first session only): sets up environment structure;
  creates a feature-requirement file (~200+ specs); inits a git repo; generates
  `init.sh` for the dev server; produces `claude-progress.txt` for handoffs.
- **Coding agent** (subsequent sessions): single-feature incremental work; verify
  environment before new work; update progress docs and git commits; validate via
  end-to-end testing.

## Critical failure modes → solutions

| Problem | Root cause | Solution |
|---|---|---|
| Premature completion | Declares victory early | Structured feature list marking incomplete tasks as "failing" |
| Half-implemented features | Too much per session | Work on one feature at a time |
| Undocumented progress | Context gaps between sessions | Git commits + progress file at session end |
| Incomplete verification | Code-level testing only | Browser automation (Puppeteer MCP) for end-to-end validation |

## Context management — session startup sequence

1. `pwd` to verify working directory.
2. Read git logs + progress files for context.
3. Select highest-priority incomplete feature.
4. Basic functionality test via `init.sh`.
5. Only then implement.
Reduces token waste re-establishing context; catches inherited bugs early.

## Progress & state tracking

- Feature list as **structured JSON** (agents only modify the "passes" field;
  explicit instructions prevent deletion/alteration that could mask bugs).
- Git commit messages describe incremental change; `claude-progress.txt` logs
  across sessions; enables rollback.

## Verification

"Claude mostly did well at verifying features end-to-end once explicitly prompted
to use browser automation tools and do all testing as a human user would."
Requires explicit instruction to test like a human user, not just unit/API tests.

## Recommended patterns

1. Different prompt for first vs continuation sessions.
2. Structured JSON (not Markdown) for specs — models less likely to modify
   inappropriately.
3. Mandatory end-to-end testing before marking complete.
4. Git integration for state recovery / audit.
5. Feature atomicity — discrete, completable units per session.

## Open questions

Whether a single generalist agent beats multi-agent with specialized roles
(testing/QA/cleanup); generalization beyond web development unexplored.
