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
  [[anthropic-eng-how-we-contain-claude]])
- **Auto mode** sits between per-action approval and
  `--dangerously-skip-permissions`: a server-side prompt-injection probe on tool
  output plus a two-stage transcript classifier that sees user messages and tool
  calls only. Full pipeline: 0.4% false-positive rate on real traffic, 17%
  false-negative rate on real overeager actions. A block returns as a tool
  result; 3 consecutive or 20 total denials escalate to the human (headless
  `claude -p` terminates). Entering auto mode drops broad allow rules. (see
  [[anthropic-eng-claude-code-auto-mode]], [[guardrails]])
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
  [[anthropic-claude-code-in-the-cloud]])

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
