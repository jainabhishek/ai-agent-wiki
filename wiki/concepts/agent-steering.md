---
title: Agent Steering & Configuration
type: concept
created: 2026-06-21
updated: 2026-10-12
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

**Portability.** Repo-level mechanisms (`CLAUDE.md`, rules, skills, agents,
commands, `.mcp.json`, `.claude/settings.json` hooks) travel with the repo into
cloud sessions; user-level `~/.claude` does not. Anything a remote run needs,
such as the test command, must live in repo `CLAUDE.md`. (see
[[anthropic-claude-code-in-the-cloud]])

## Best practices

- **Match the mechanism to the job.** Procedures → skills; constraints → rules;
  must-happen-deterministically → hooks; isolated exploration → subagents.
- **Path-scope constraints** (`paths:` frontmatter) so unrelated work stays clean
  and tokens aren't wasted.
- **Keep CLAUDE.md lean** (<200 lines); move procedures to skills, preferences to
  user-level files. For the Claude 5 generation Anthropic narrows it further:
  brief purpose plus codebase gotchas, nothing the agent can discover itself,
  structured as a tree of files rather than a catch-all; auto-memory replaces
  manual memory notes. (see [[anthropic-new-rules-context-engineering-claude-5]])
- **Audit layers for conflicts.** System prompt, CLAUDE.md, skills, and the user
  request can issue conflicting instructions, and the model spends reasoning
  reconciling them. (see [[anthropic-new-rules-context-engineering-claude-5]])
- **Put the continue/stop policy for long runs in CLAUDE.md** — which early stops
  you want (blocked on the user, before destructive actions) and which you do not.
  The stop patterns are model-specific; see the scoped example in
  [[anthropic-getting-most-out-of-opus-5-5]].
- **Mid-run steering** is a further "when": corrections sent while a run is in
  progress, keeping completed work. (see [[openai-prompting-gpt-6-astra]],
  [[anthropic-getting-most-out-of-opus-5-5]]) Where harness text and user messages
  may go mid-turn is per-model; see [[anthropic-prompting-claude-sonnet-5-5]].
- **AGENTS.md is the Codex counterpart** of CLAUDE.md; short if/then rules there
  can make specific skills mandatory. (see [[openai-skills-for-oss-maintenance]],
  [[agent-instructions]])
- **Prefer deterministic hooks over "never do this" prose** — a PreToolUse hook
  can inspect and deny a tool call (exit 2). The deterministic complement to
  [[guardrails]]; Claude Code auto mode is the model-based counterpart (a
  classifier judges each action). (see [[anthropic-eng-claude-code-auto-mode]])
- **Use output styles sparingly** — they override default guidance on scope,
  security, and testing.

## Why it matters

Steering is applied [[context-engineering]]: the goal is the right instructions at
the right moment, not all instructions all the time. This is the Anthropic-side
analogue to OpenAI's [[agent-instructions]] guidance.

## Related concepts

- [[agent-skills]], [[context-engineering]], [[agent-instructions]],
  [[agent-orchestration]], [[guardrails]], [[agent-harness]]

## Key entities

- [[anthropic]], [[claude-code]], [[openai-codex]]

## Appears in

- [[anthropic-steering-claude-code]]
- [[anthropic-lessons-building-claude-code-skills]]
- [[anthropic-new-rules-context-engineering-claude-5]]
- [[anthropic-claude-code-in-the-cloud]]
- [[anthropic-getting-most-out-of-opus-5-5]]
- [[anthropic-eng-claude-code-auto-mode]]
- [[anthropic-eng-how-we-contain-claude]]
- [[openai-prompting-gpt-6-astra]]
- [[openai-skills-for-oss-maintenance]]
- [[anthropic-prompting-claude-sonnet-5-5]]

## Contradictions / open questions

- **CLAUDE.md as memory, partly superseded (recorded 2026-10-12).**
  [[anthropic-new-rules-context-engineering-claude-5]] (2026-07-24) recasts
  "manual CLAUDE.md memory" (the `#`-hotkey habit) as a myth: auto-memory now
  records learnings, and CLAUDE.md should hold only purpose and gotchas. That page
  says this partly supersedes [[anthropic-steering-claude-code]] (2026-06-18).
  The steering source does not itself call CLAUDE.md a memory store; it frames
  CLAUDE.md as overview, conventions, and build commands. The concrete conflict
  is scope: "overview, conventions, build commands" (2026-06-18) vs. "nothing
  discoverable" (2026-07-24). Open: whether the newer rule applies to models
  before the Claude 5 generation, and how auto-memory interacts with the
  mechanisms table above.
- **Steering inputs are an attack surface.** Project config (`.claude/settings.json`
  hooks) once ran before the trust dialog, and persistent memory poisoning via
  cross-session state (memory, CLAUDE.md, scheduled-agent state) is an open
  problem. (see [[anthropic-eng-how-we-contain-claude]], [[guardrails]])
