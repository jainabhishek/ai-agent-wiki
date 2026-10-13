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

## Escalation ladder and build order

- **Steering ladder.** Escalate only as far as needed: a conversational request,
  then a `CLAUDE.md` policy (always loaded), then a skill (loaded on demand), then
  a hook (most automated). Start conversational and automate only the patterns
  that repeat (see [[anthropic-subagents-in-claude-code]]).
- **Build order.** For large codebases, build the extension points in order:
  `CLAUDE.md`, then hooks, then skills, then plugins, then MCP servers. A common
  mistake is building MCP connections before the basics work (see
  [[anthropic-claude-code-large-codebases]], [[model-context-protocol]]).
- **Advisory vs deterministic layers.** A skill makes compliance likely; a hook
  is the deterministic layer behind it, and a policy that must always hold needs
  both. Keep build hooks fast and file-scoped; put human-approval hooks at
  deploy gates, not in the build, or a person sits on the critical path of every
  parallel session (see [[anthropic-ai-native-sdlc-playbook]], [[guardrails]]).

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
- **Put exact build and test commands in `CLAUDE.md`,** so the agent verifies
  against the real toolchain (see [[anthropic-verification-loops-with-skills]]).
- **Put the continue/stop policy for long runs in CLAUDE.md** — which early stops
  you want (blocked on the user, before destructive actions) and which you do not.
  The stop patterns are model-specific; see the scoped example in
  [[anthropic-getting-most-out-of-opus-5-5]]. In OpenAI's Codex run of about 25 hours,
  lint, typecheck, tests, and build ran after each milestone, and failures were
  repaired before the next one (see [[openai-run-long-horizon-tasks-codex]]).
- **Mid-run steering** is a further "when": corrections sent while a run is in
  progress, keeping completed work. (see [[openai-prompting-gpt-6-astra]],
  [[anthropic-getting-most-out-of-opus-5-5]]) Where harness text and user messages
  may go mid-turn is per-model; see [[anthropic-prompting-claude-sonnet-5-5]].
  OpenAI's GPT-6 guide adds that on its API, steering updates are queued and do
  not cancel running tools or undo completed actions (see
  [[openai-practical-guide-building-with-gpt-6]], scoped to GPT-6 models). In
  Codex, a queued instruction can correct, add context, approve, or chain the
  next action, e.g. "once this is done, open a PR" (see
  [[openai-codex-maxxing-long-running-work]]).
- **Set reasoning effort per phase, not per session.** One Anthropic author's
  loop: an interview about the spec, implementation and review at a lower
  effort, then verification at a higher effort. The same source reports that
  without a user in the loop, higher effort stands in for a clarifying question.
  Levels and per-model behavior live on the scoped source page (see
  [[anthropic-spending-your-effort]], [[prompt-tuning-axes]]).
- **AGENTS.md is the Codex counterpart** of CLAUDE.md; short if/then rules there
  can make specific skills mandatory. (see [[openai-skills-for-oss-maintenance]],
  [[agent-instructions]]) Keep it short and use it as a table of contents into a
  `docs/` system of record (see [[openai-harness-engineering]]). The Sora
  Android team reports many `AGENTS.md` files plus a user-level
  `~/.codex/AGENTS.md` that maps local repositories (see
  [[openai-sora-android-with-codex]]).
- **Prefer deterministic hooks over "never do this" prose** — a PreToolUse hook
  can inspect and deny a tool call (exit 2). The deterministic complement to
  [[guardrails]]; Claude Code auto mode is the model-based counterpart (a
  classifier judges each action). (see [[anthropic-eng-claude-code-auto-mode]])
  Lint and format by hook is more consistent than by instruction (see
  [[anthropic-claude-code-large-codebases]]). Case reports agree: Greptile uses
  hooks to guarantee that every file in a PR is examined (see
  [[claude-customer-greptile]]); Outtake reports that in long runs prompt rules
  are eventually ignored, so it moved must-always steps into the harness (see
  [[anthropic-outtake-cyber-investigator]], [[agent-harness]]).
- **Hooks can inject context, not only block.** `SessionStart` stdout becomes
  context, and `UserPromptSubmit` stdout is added with the prompt, e.g. git
  status or sprint notes (see [[anthropic-configure-hooks]]). A start hook can
  load team or module context, and a stop hook can propose `CLAUDE.md` updates
  from the session (see [[anthropic-claude-code-large-codebases]]). Twilio
  reports that a plain learnings file failed within four sessions; hooks that
  write suggestions to a file Claude reads replaced it (see
  [[claude-customer-twilio]]).
- **Codex rules and managed configuration.** Codex rules are Starlark
  `prefix_rule` entries that allow named read-only commands outside the sandbox
  and can block or gate dangerous ones — a deterministic layer like PreToolUse
  hooks. Managed configs (cloud requirements, macOS managed preferences, local
  requirement files) set one posture across the desktop app, CLI, and IDE
  extension, and users cannot override the requirements (see
  [[openai-running-codex-safely]], [[openai-codex]]).
- **Repo-owned workflow policy.** OpenAI's Symphony spec keeps a `WORKFLOW.md` in
  the repo with YAML config and the per-issue prompt template; changes reload
  live, and templates render strictly (see
  [[openai-symphony-codex-orchestration]], [[agent-orchestration]]).
- **Steering surfaces for humans.** One Anthropic author asks for throwaway
  single-file HTML editors (a triage board, a config form) that end with a "copy
  as JSON/prompt/diff" button feeding the result back to Claude Code (see
  [[anthropic-unreasonable-effectiveness-of-html]], personal opinion).

## Closing the loop: config as a maintained artifact

- **Write discovered bug classes back.** Each bug class found in review goes
  back into `CLAUDE.md` or org-wide skills (see
  [[anthropic-securing-ai-native-sdlc]]). A mistake made twice goes into
  `CLAUDE.md` (see [[anthropic-ai-native-sdlc-playbook]]). Anthropic's CI on-call
  agent appends each resolved incident to a lessons file it reads at the start
  of each run, and recurring patterns move into the skill (see
  [[anthropic-ai-ci-cd-on-call]], [[agent-memory]]). Spotify reports encoding
  quality in skills and `CLAUDE.md` to go faster without losing quality (see
  [[claude-customer-spotify-boris-office-hours]]).
- **Evals as CI for configuration.** Run 20–50 real tasks on a schedule and on any
  change to `CLAUDE.md`, skills, or hooks; gate configuration changes on the pass
  rate (see [[anthropic-ai-native-sdlc-playbook]], [[agent-evals]]).
- **Review configuration every three to six months** and after major model
  releases. Configuration decays: a rule forcing single-file refactors hampered a
  newer model, and a hook became redundant when Claude Code added the feature
  natively. Name an owner (a DRI) for settings, permissions, plugins, and
  `CLAUDE.md` conventions (see [[anthropic-claude-code-large-codebases]],
  [[agent-instructions]]).
- **Use output styles sparingly** — they override default guidance on scope,
  security, and testing.

## Why it matters

Steering is applied [[context-engineering]]: the goal is the right instructions at
the right moment, not all instructions all the time. This is the Anthropic-side
analogue to OpenAI's [[agent-instructions]] guidance.

## Related concepts

- [[agent-skills]], [[context-engineering]], [[agent-instructions]],
  [[agent-orchestration]], [[guardrails]], [[agent-harness]],
  [[agent-evals]], [[agent-memory]], [[model-context-protocol]],
  [[prompt-tuning-axes]]

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
- [[anthropic-subagents-in-claude-code]]
- [[anthropic-claude-code-large-codebases]]
- [[anthropic-ai-native-sdlc-playbook]]
- [[anthropic-securing-ai-native-sdlc]]
- [[anthropic-configure-hooks]]
- [[anthropic-verification-loops-with-skills]]
- [[anthropic-ai-ci-cd-on-call]]
- [[anthropic-spending-your-effort]]
- [[anthropic-outtake-cyber-investigator]]
- [[anthropic-unreasonable-effectiveness-of-html]]
- [[claude-customer-greptile]]
- [[claude-customer-twilio]]
- [[claude-customer-spotify-boris-office-hours]]
- [[openai-run-long-horizon-tasks-codex]]
- [[openai-practical-guide-building-with-gpt-6]]
- [[openai-codex-maxxing-long-running-work]]
- [[openai-harness-engineering]]
- [[openai-sora-android-with-codex]]
- [[openai-running-codex-safely]]
- [[openai-symphony-codex-orchestration]]

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
- **Soft tension on `CLAUDE.md` length (recorded 2026-10-12).**
  [[anthropic-steering-claude-code]] (2026-06-18) says under 200 lines;
  [[anthropic-ai-native-sdlc-playbook]] (2026-08-21) says keep it under a page;
  [[anthropic-new-rules-context-engineering-claude-5]] (2026-07-24) says purpose
  plus gotchas only. On the OpenAI side, [[openai-harness-engineering]]
  (2026-02-11) uses a ~100-line `AGENTS.md` as a table of contents. All point
  the same way (short, pointers out), but the stated limits differ. Open which
  limit, if any, is measured rather than a rule of thumb.
