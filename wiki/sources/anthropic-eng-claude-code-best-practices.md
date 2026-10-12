---
title: "Anthropic (Eng): Claude Code — Best Practices for Agentic Coding"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Boris Cherny (Anthropic Engineering)
date: 2025-04-18
source_url: https://www.anthropic.com/engineering/claude-code-best-practices
source_path: raw/anthropic-eng-claude-code-best-practices.md
tags: [claude-code, best-practices, claude-md, workflows, multi-agent, headless, primary-source]
---

# Anthropic (Eng): Claude Code — Best Practices for Agentic Coding

> The April 2025 field guide to Claude Code: CLAUDE.md setup, tool allowlists,
> explore-plan-code and TDD workflows, headless fan-out, and multi-Claude
> patterns. Many of its specific mechanisms have since been replaced.

## Summary

**Dates.** The post byline says "Published Apr 18, 2025", with no "updated"
date (Wayback Machine snapshot of 2025-06-02). As of 2026-10-12 the original URL
returns HTTP 308 to the docs page `code.claude.com/docs/en/best-practices`,
whose metadata gives `dateModified` 2026-10-06. This page uses the 2025-04-18
date and summarizes the original post. The raw capture also records how the
successor docs page differs.

The original post presents Claude Code as a low-level, unopinionated tool and
gives starting-point patterns in six groups. (1) Setup: CLAUDE.md files at root,
parent, child, and home locations; tune them like prompts; curate the tool
allowlist; install `gh`. (2) Tools: bash tools, MCP via `.mcp.json`, and custom
slash commands in `.claude/commands/`. (3) Workflows: explore-plan-code-commit,
test-first iteration, screenshot iteration, "Safe YOLO mode" in an offline
container, codebase Q&A, git and GitHub tasks, notebooks. (4) Workflow tips:
specific prompts, images, URLs, early course correction, `/clear`, Markdown
checklists. (5) Headless mode (`claude -p`) for CI and triage. (6) Multi-Claude
patterns: writer and reviewer instances, multiple checkouts, git worktrees, and
headless fan-out. See [[claude-code]] and [[context-engineering]].

## Key points

- **Clear iteration target.** Claude performs best with a target to iterate
  against: tests, a visual mock, or expected output (TDD and screenshot loops).
- **Research and plan before coding.** Without explicit explore and plan steps,
  Claude tends to jump straight to code. Subagents early in a task preserve
  context.
- **Thinking keywords (superseded).** "think" < "think hard" < "think harder" <
  "ultrathink" mapped to increasing thinking budgets.
- **CLAUDE.md is a prompt.** Iterate on it; the `#` key appends instructions;
  emphasis words ("IMPORTANT", "YOU MUST") improve adherence.
- **Separate contexts help review.** One Claude writes and another reviews; this
  often beats a single instance doing both.
- **Headless fan-out.** Generate a task list, loop `claude -p` with
  `--allowedTools`, demand an `OK`/`FAIL` return string, and refine on a few
  runs first.
- **Checklists as scratchpads** for large multi-step jobs such as migrations or
  lint backlogs.

## Entities

[[anthropic]], [[claude-code]], [[claude]]

## Concepts

[[context-engineering]], [[agent-steering]], [[agent-instructions]],
[[agent-skills]], [[agent-orchestration]], [[guardrails]], [[agent-evals]],
[[model-context-protocol]]

## Notable claims & data

- Many Anthropic engineers use Claude for 90%+ of their git interactions.
- Codebase Q&A became Anthropic's core onboarding workflow.
- Screenshot iteration: output typically improves a lot after 2–3 iterations.
- Superseded mechanisms, compared with the 2026-10-06 docs page and later
  posts:
  - The `think`…`ultrathink` keyword ladder. The docs page drops it. Current
    models use adaptive thinking and `effort` (see
    [[anthropic-prompting-claude-sonnet-5]]).
  - The `#` key that writes CLAUDE.md memory. Auto-memory replaces it
    ([[anthropic-new-rules-context-engineering-claude-5]]).
  - Custom slash commands in `.claude/commands/` (`/project:` prefix).
    Skills in `.claude/skills/` replace them, with
    `disable-model-invocation: true` for manual workflows.
  - Safe YOLO mode (`--dangerously-skip-permissions` in an offline container).
    `/sandbox` ([[anthropic-eng-claude-code-sandboxing]]) and auto mode replace
    it. Auto mode is the default starting mode from v2.1.283.
  - Emphasis on many lines. The docs page says to emphasize one line only.
  - "Headless mode does not persist". `claude -p` now creates a resumable
    session unless `--no-session-persistence` is set.
  - `--json` and `--mcp-debug` flags. The docs page uses
    `--output-format json`.
  - Manual 3–4 checkouts. The docs page offers the desktop app, cloud
    sessions, agent view, agent teams, and `/batch` (5–30 worktree subagents).
- Practices that survive into the docs page: explore before coding (now plan
  mode), specificity tables (same `HotDogWidget.php` example), `/clear` between
  tasks, the writer/reviewer split, and headless fan-out.

## Connections

- **Versus [[anthropic-steering-claude-code]] (June 2026).** This post treats
  CLAUDE.md as the main store for commands, conventions, and "other information
  you want Claude to remember". The steering post splits that job across seven
  mechanisms: CLAUDE.md under ~200 lines, path-scoped rules, skills, hooks,
  subagents, output styles, and appended prompts. Procedures move out of
  CLAUDE.md into skills, and "never do X" rules move into hooks.
- **Versus [[anthropic-new-rules-context-engineering-claude-5]].** That post
  names manual CLAUDE.md memory and repeated emphasis as superseded habits for
  Claude 5-generation models. CLAUDE.md is now a brief purpose plus codebase
  gotchas, and auto-memory handles remembering.
- The writer and reviewer split anticipates the evaluator separation in
  [[anthropic-eng-harness-design-long-running-apps]] and the verifier patterns in
  [[anthropic-harness-for-every-task]].
- The verify-first framing of the successor docs page matches the "verification
  loop" emphasis in [[anthropic-eng-effective-harnesses-long-running-agents]].
- Headless fan-out is an early, manual form of the orchestration patterns in
  [[agent-orchestration]].
