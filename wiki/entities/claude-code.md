---
title: Claude Code
type: entity
subtype: product
created: 2026-06-21
updated: 2026-10-12
tags: [anthropic, claude-code, agents, tooling]
---

# Claude Code

> Anthropic's agentic coding tool. In this wiki it's the worked example for how to
> *steer* a real agent, how skills compound in practice, and how a production
> harness is shaped by caching, tool design, and containment.

## Overview

A command-line / desktop agentic developer tool by [[anthropic]]. Its design is
the subject of several ingested sources on agent best practices:
[[anthropic-steering-claude-code]] (the seven steering mechanisms),
[[anthropic-lessons-building-claude-code-skills]] (how skills are used at scale),
[[anthropic-prompt-caching-is-everything]] and [[anthropic-seeing-like-an-agent]]
(harness and tool design), [[anthropic-eng-claude-code-auto-mode]] and
[[anthropic-eng-how-we-contain-claude]] (permissions and sandboxing),
[[anthropic-harness-for-every-task]] (dynamic workflows), and
[[anthropic-claude-code-in-the-cloud]] (cloud sessions).

## Key facts

### Steering and configuration
- Offers seven steering mechanisms — CLAUDE.md, rules, skills, subagents, hooks,
  output styles, system-prompt appending. (see [[agent-steering]])
- Skills, subagents, hooks, and styles bundle into **plugins** for sharing.
  (see [[agent-skills]])
- Subagents run in isolated context and can nest/orchestrate at scale.
  (see [[agent-orchestration]])
- For Claude 5-generation models Anthropic cut over 80% of the system prompt
  with no measurable coding-eval loss; code review and verification moved into
  skills; auto-memory replaces the manual `#`-hotkey CLAUDE.md memory habit; the
  practices ship in `claude doctor` (`/doctor`). (see
  [[anthropic-new-rules-context-engineering-claude-5]])
- Custom subagents are markdown files in `.claude/agents/` (project) or
  `~/.claude/agents/` (user), created with `/agents`; each has its own system
  prompt, tools, and optional model. The `description` field drives automatic
  routing. Built-in types are General-purpose, Plan, and Explore. (see
  [[anthropic-subagents-in-claude-code]])
- For large codebases Anthropic recommends a build order of `CLAUDE.md`, then
  hooks, skills, plugins, and MCP servers, plus LSP integrations for
  symbol-level navigation. Claude Code started in a subdirectory walks up and
  loads every `CLAUDE.md` on the path. Skills can be path-scoped to one
  directory. Anthropic advises a review of the configuration every three to six
  months and an owner (a DRI or an "agent manager") for settings, permissions,
  and plugins. (see [[anthropic-claude-code-large-codebases]],
  [[agent-steering]])

### Hooks
- A hook is a shell command (or, for Stop and SubagentStop, a model prompt)
  that runs on a session event. As of 2025-12-11 there were eight events:
  `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`,
  `SessionStart`, `Stop`, `SubagentStop`, and `UserPromptSubmit`. The hook gets
  event JSON on stdin; exit code 2 blocks the action and sends stderr to
  Claude. Hooks have a 60-second default timeout, and matching hooks run in
  parallel. (see [[anthropic-configure-hooks]])
- Hooks live in project, user, or local settings files, plus
  enterprise-managed policy. Direct edits to hook configuration take effect only
  after review in the `/hooks` menu. (see [[anthropic-configure-hooks]],
  [[guardrails]])
- A Stop hook can return `decision: "block"` to keep Claude working until the
  tests pass; the `stop_hook_active` flag prevents an infinite loop. A stop hook
  can also propose `CLAUDE.md` updates from the session. (see
  [[anthropic-subagents-in-claude-code]],
  [[anthropic-claude-code-large-codebases]])

### Prompt caching as a design constraint
- The harness is laid out around prompt caching: static system prompt + tools,
  then CLAUDE.md, then session context, then messages. Changing state (time,
  edited files) goes into `<system-reminder>` messages, not prompt edits.
  Models and tool sets never change mid-session; plan mode is itself a pair of
  tools (`EnterPlanMode` / `ExitPlanMode`); MCP tool schemas are deferred with
  `defer_loading` stubs plus tool search. (see
  [[anthropic-prompt-caching-is-everything]], [[context-engineering]])
- Compaction runs as a "cache-safe fork" reusing the parent's exact prefix.
  Model switches go through a subagent hand-off (Haiku-based Explore agents).
  The team monitors cache hit rate like uptime and declares SEVs on drops. (see
  [[anthropic-prompt-caching-is-everything]])

### Tool-design case studies
- About 20 tools, with a high bar for adding more. (see
  [[anthropic-seeing-like-an-agent]], [[tool-design]])
- **AskUserQuestion**: a question parameter on ExitPlanTool and a parsed
  markdown format both failed; a dedicated blocking tool with structured options
  worked.
- **TodoWrite → Tasks**: todos plus reminders every 5 turns helped early models
  but constrained later ones; tasks with dependencies shared across subagents
  replaced them.
- **Search**: a pre-indexed RAG vector store was replaced by Grep so Claude
  builds its own context; skills add progressive disclosure.
- **Claude Code Guide**: a docs-search subagent that returns only the answer
  added self-knowledge without a new tool. (all see
  [[anthropic-seeing-like-an-agent]])

### Permissions, auto mode, and sandboxing
- Users approved about 93% of permission prompts, so approval was mostly
  fatigue. (see [[anthropic-eng-claude-code-auto-mode]],
  [[anthropic-eng-how-we-contain-claude]]) A later post gives 97%; see
  Contradictions.
- **Auto mode** sits between per-action approval and
  `--dangerously-skip-permissions`: a server-side prompt-injection probe on tool
  output plus a two-stage transcript classifier that sees user messages and tool
  calls only. Full pipeline: 0.4% false-positive rate on real traffic, 17%
  false-negative rate on real overeager actions. A block returns as a tool
  result; 3 consecutive or 20 total denials escalate to the human (headless
  `claude -p` terminates). Entering auto mode drops broad allow rules. (see
  [[anthropic-eng-claude-code-auto-mode]], [[guardrails]])
- **Auto mode as the default (2026-08).** From 2026-08-14, new Pro, Max, and
  Team sessions start in auto mode; Enterprise, API, and cloud-platform access
  stay opt-in. Admins control it with `defaultMode` and `disableAutoMode` in
  managed settings. Anthropic's case: in a study of 1,053 testers, humans caught
  13.6% of planted dangerous commands and auto mode blocked 89%. New safeguards
  include a hard deny on data exfiltration, data-sharing rules, and a git-status
  check before destructive git commands. (see [[anthropic-auto-mode-default]])
- Production teams report keeping a manual tier for high-stakes work (Nuro for
  cross-team work; Gusto for Terraform, AWS, and live-API POSTs) and layering
  auto mode on deny rules and a governed MCP proxy. Anthropic reports that
  Claude works 9x longer between interruptions than under the previous default,
  with no method given. (see [[anthropic-auto-mode-production]])
- **OS-level sandbox** (Seatbelt on macOS, bubblewrap on Linux): reads and
  in-workspace writes allowed, network denied by default; cut permission prompts
  by 84%. The runtime is open source. (see
  [[anthropic-eng-how-we-contain-claude]])
- Missed risk (fixed): hooks in project config (`.claude/settings.json`) ran
  before the trust dialog. (see [[anthropic-eng-how-we-contain-claude]])

### Cloud sessions
- One task = one disposable VM = one branch (about 4 vCPU, 16 GB RAM, 30 GB
  disk), on Anthropic infrastructure or self-hosted environments (beta). A proxy
  holds the GitHub token; the session gets a short-lived credential that can
  push only to its own branch. Network levels: None, Trusted (default), Custom,
  Full. (see [[anthropic-claude-code-in-the-cloud]])
- Approval modes in the cloud are Auto, Accept edits, or Plan; there is no
  per-command approval. (see [[anthropic-claude-code-in-the-cloud]])
- Repo configuration travels (`CLAUDE.md`, rules, skills, agents, commands,
  `.mcp.json`, `.claude/settings.json` hooks); `~/.claude` does not. A setup
  script runs as root before Claude Code starts and is cached as a snapshot; a
  SessionStart hook runs the same steps locally and in the cloud;
  `CLAUDE_CODE_REMOTE` gates cloud-only steps. (see
  [[anthropic-claude-code-in-the-cloud]])
- Handoff: `claude --cloud "<task>"` starts a session from the pushed branch;
  `claude --teleport` pulls a session's branch and conversation locally;
  `claude -p "<msg>" --cloud <id>` queues a follow-up. **Routines** (research
  preview) start cloud sessions from a schedule, an HTTP call, or a GitHub
  event. Zero Data Retention disables cloud sessions. (see
  [[anthropic-claude-code-in-the-cloud]]) `/schedule` moves a recurring loop
  to the cloud as a routine. (see [[anthropic-getting-started-with-loops]])

### Loops and verification
- Anthropic names four loop types, each handing off one more piece of the work.
  A turn-based loop hands off the check, through verification skills. A
  goal-based loop (`/goal`) hands off the stop condition: when Claude tries to
  stop, an evaluator model checks the user's condition and sends Claude back to
  work, until success or a turn cap. A time-based loop (`/loop 5m ...` locally,
  `/schedule` in the cloud) hands off the trigger. A proactive loop hands off
  the prompt, by combining these with auto mode and dynamic workflows. `/usage`,
  a bare `/goal`, and `/workflows` show spend. (see
  [[anthropic-getting-started-with-loops]], [[agent-harness]])
- Built-in verification options: the `/verify` skill (build, run, observe);
  exact build and test commands in `CLAUDE.md`; Code Review (research preview,
  a managed multi-agent PR review); a verification skill run by GitHub Actions
  on each push or PR; and a spec-validation skill against a markdown spec. The
  Claude Code team chains `/code-review` → `/simplify` → `/verify` → a custom
  design check. (see [[anthropic-verification-loops-with-skills]],
  [[agent-skills]])

### Sessions and cost
- Each finished turn offers five options: continue, rewind (Esc Esc or
  `/rewind`), `/compact` with a hint, `/clear`, or a subagent. The rule of
  thumb is one new session per new task. Autocompact goes wrong when the model
  cannot predict the next step, so compact early and say what comes next. (see
  [[anthropic-claude-code-session-management]], [[context-engineering]])
- Every turn re-sends the conversation, so turns, cache hit rate, output, and
  the model set the cost. `/usage` (same as `/cost`) shows the cache share.
  Command output over 30,000 characters goes to a file with a preview in
  context. (see [[anthropic-claude-code-session-cost]],
  [[anthropic-what-a-task-costs-opus-5-5]])
- Cache-breaking rules changed during 2026. The 2026-08-14 guidance lists
  `/effort` as a cache breaker. From 2026-09, on Opus 5.5 and Fable 5.1, an
  effort change keeps the cache on an API key or subscription, but still clears
  it on Amazon Bedrock, Google Cloud's Agent Platform, or a Claude apps
  gateway. API-key and cloud-provider users can set a one-hour cache lifetime.
  (see [[anthropic-claude-code-session-cost]],
  [[anthropic-opus-5-5-long-coding-sessions]],
  [[anthropic-what-a-task-costs-opus-5-5]])
- `/effort` changes the level mid-conversation. An Anthropic engineer sets
  effort per phase: low to implement and iterate, high to verify. (see
  [[anthropic-spending-your-effort]], [[prompt-tuning-axes]])
- Aggregate usage from March to September 2026: Claude works 3.3x longer per
  prompt, interruptions fell 68%, and context per request grew 2.6x. (see
  [[anthropic-opus-5-5-long-coding-sessions]])

### Dynamic workflows
- Claude Code can write a per-task multi-agent harness as a JavaScript file from
  `agent()`, `parallel()`, and `pipeline()` (trigger with a request or
  `ultracode`; combine with `/loop` and `/goal`). Six patterns:
  classify-and-act, fan-out-and-synthesize, adversarial verification,
  generate-and-filter, tournament, loop until done. Example runs: 14 agents /
  482k tokens; 22 agents / 1.1M tokens. Suited to complex, high-value tasks, not
  routine coding. (see [[anthropic-harness-for-every-task]],
  [[workflow-patterns]], [[multi-agent-economics]])

### Models in Claude Code
- From v2.1.284 the `sonnet` alias resolves to Claude Sonnet 5.5 on the Claude
  API; `default` stays Opus 5.5. (see [[anthropic-building-with-sonnet-5-5]])
  Model-specific steering advice (e.g. naming unwanted early stops in
  CLAUDE.md, keeping a task list in a file that survives summarization) lives on
  [[anthropic-getting-most-out-of-opus-5-5]].
- Ships the `claude-api` skill, whose `/claude-api build-eval` and
  `/claude-api hillclimb` commands are described in
  [[anthropic-automating-eval-design-hillclimbing]].

- **Sandbox (Oct 2025).** `/sandbox` turns on the sandboxed bash tool:
  filesystem and network isolation enforced by the OS, which cut permission
  prompts by 84% internally. Claude Code on the web keeps the real GitHub token
  outside the sandbox; a git proxy checks a scoped credential and the target
  branch before it attaches the token. (see [[anthropic-eng-claude-code-sandboxing]])
- **History (Apr 2025 guide).** The original best-practices post relied on
  CLAUDE.md as memory (written with the `#` key), custom commands in
  `.claude/commands`, and a "think" … "ultrathink" keyword ladder. Auto-memory,
  skills, and adaptive thinking with effort have since replaced these. The old
  URL now redirects to a maintained docs page. (see [[anthropic-eng-claude-code-best-practices]])

### Team norms and reported use
- Anthropic's Claude Code engineering director reports that every commit on
  the team is Claude-assisted. The team mandates three norms: dogfood
  relentlessly, keep the team flat, and give explicit permission to kill
  obsolete processes. Claude reviews style, lint, bugs, and tests; humans review
  legal risk, trust boundaries, security-sensitive code, and product taste.
  The three adoption metrics are onboarding ramp time, PR cycle time, and the
  share of Claude-assisted commits. (see
  [[anthropic-running-ai-native-engineering-org]])
- Anthropic reports that Claude authors 80% of its code and that CI jobs rose
  25x in six months, which overloaded its test-selection service. (see
  [[anthropic-agentic-coding-ci-test-impact]])
- Self-reported deployments: Twilio built a subagent pipeline whose output is
  a Claude Code plugin; ABC Legal non-developers built Managed Agents from
  templates with Claude Code; Outtake prototyped its investigator in Claude Code
  before moving to the Agent SDK. Anthropic ships a code modernization plugin
  with `assess`, `map`, and `extract-rules` commands. (see
  [[claude-customer-twilio]], [[anthropic-abc-legal-managed-agents]],
  [[anthropic-outtake-cyber-investigator]], [[anthropic-ai-code-modernization]])

## Relationships

- Built by [[anthropic]]; related to the [[claude-agent-sdk]] and
  [[claude-managed-agents]] surfaces. Its harness is a worked example of
  [[agent-harness]] design.

## Appears in

- [[anthropic-steering-claude-code]]
- [[anthropic-lessons-building-claude-code-skills]]
- [[anthropic-eng-context-engineering]]
- [[anthropic-eng-agent-skills]]
- [[anthropic-prompt-caching-is-everything]]
- [[anthropic-seeing-like-an-agent]]
- [[anthropic-eng-claude-code-auto-mode]]
- [[anthropic-eng-how-we-contain-claude]]
- [[anthropic-claude-code-in-the-cloud]]
- [[anthropic-harness-for-every-task]]
- [[anthropic-new-rules-context-engineering-claude-5]]
- [[anthropic-building-with-sonnet-5-5]]
- [[anthropic-getting-most-out-of-opus-5-5]]
- [[anthropic-automating-eval-design-hillclimbing]]
- [[anthropic-eng-claude-code-sandboxing]]
- [[anthropic-eng-claude-code-best-practices]]
- [[anthropic-eng-building-c-compiler]]
- [[anthropic-subagents-in-claude-code]]
- [[anthropic-claude-code-large-codebases]]
- [[anthropic-configure-hooks]]
- [[anthropic-auto-mode-default]]
- [[anthropic-auto-mode-production]]
- [[anthropic-getting-started-with-loops]]
- [[anthropic-verification-loops-with-skills]]
- [[anthropic-claude-code-session-management]]
- [[anthropic-claude-code-session-cost]]
- [[anthropic-opus-5-5-long-coding-sessions]]
- [[anthropic-what-a-task-costs-opus-5-5]]
- [[anthropic-spending-your-effort]]
- [[anthropic-running-ai-native-engineering-org]]
- [[anthropic-agentic-coding-ci-test-impact]]
- [[anthropic-ai-code-modernization]]
- [[anthropic-abc-legal-managed-agents]]
- [[anthropic-outtake-cyber-investigator]]
- [[claude-customer-twilio]]

## Contradictions / open questions

- [[anthropic-new-rules-context-engineering-claude-5]] (2026-07-24) says
  auto-memory replaces the manual CLAUDE.md memory habit, which partly
  supersedes the CLAUDE.md-as-memory framing in
  [[anthropic-steering-claude-code]].
- Cloud sessions have no per-command approval, and routines run with no
  approval prompts; the sources do not say how this squares with
  [[guardrails]] advice to require human approval for high-risk actions. The
  containment burden moves to the VM, the network policy, and the
  branch-scoped credential. (see [[anthropic-claude-code-in-the-cloud]])
- **Approval rate: 93% or 97%?** [[anthropic-eng-claude-code-auto-mode]]
  (2026-03-25) and [[anthropic-eng-how-we-contain-claude]] say users approve
  about 93% of permission prompts. [[anthropic-auto-mode-default]] (2026-08-07)
  says 97%. Neither states its measurement window; different windows are
  likely. Miss rates in the two posts are not comparable: 17% false negatives
  on real overeager actions versus 12% → 7% on Apollo's synthetic attacks.
- **Cache-breaking rules are dated.** [[anthropic-claude-code-session-cost]]
  (2026-08-14) says `/effort` breaks the cache;
  [[anthropic-opus-5-5-long-coding-sessions]] (2026-09-24) says it no longer
  does on Opus 5.5 and Fable 5.1; [[anthropic-what-a-task-costs-opus-5-5]]
  (2026-09-25) limits that to API-key and subscription access. The later posts
  supersede the earlier one for those models; they do not contradict it.
