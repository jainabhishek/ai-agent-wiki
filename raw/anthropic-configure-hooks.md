# Claude Code power user customization: How to configure hooks — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/how-to-configure-hooks
> Publisher: Anthropic (claude.com articles) · Date: 2025-12-11
> Captured: 2026-10-12 via curl (HTML downloaded, text extracted locally; condensed).

No author byline. Category: Best practices. Product: Claude Code. Reading time
14 min. Audience: developers already familiar with Claude Code basics. Note: the
article describes the hook set as of its December 2025 date ("eight hook
types"); later Claude Code releases may differ.

## Introduction
- Friction examples: running Prettier by hand after each write; the same
  permission prompt for `npm test`; pasting the same project context each
  session. Hooks are configurable triggers that fire before or after actions to
  inject logic, scripts, commands.

## What is a hook?
- A custom shell command that runs automatically on a targeted session event
  (e.g. before a file write, on prompt submit). Uses: intercept actions, inject
  context, automate approvals, block operations.
- Configured in settings files as JSON: event names, matchers (filter tools),
  commands. Run locally with the user's permissions; receive event data on stdin;
  respond via exit codes and stdout.

## Why use hooks in Claude Code?
Three problem categories:
1. Eliminate repetitive manual steps (PostToolUse formatter; PermissionRequest
   auto-approving `npm test`).
2. Enforce project rules automatically (block dangerous commands, validate paths,
   naming conventions) — runs every time.
3. Inject dynamic context (SessionStart: git status and TODO list;
   UserPromptSubmit: sprint priorities).

## Claude Code hook types and when to use them
Eight hook events (as of the article):

| Hook | When it fires | Common uses |
|---|---|---|
| PreToolUse | Before a tool executes | Block dangerous commands, validate paths, auto-approve safe ops |
| PermissionRequest | Before a permission dialog | Auto-approve test commands, block sensitive files |
| PostToolUse | After a tool completes | Formatters, linters, log changes |
| PreCompact | Before context compaction | Back up transcripts, preserve decisions |
| SessionStart | Session begins or resumes | Inject git status, TODOs, environment context |
| Stop | Claude finishes responding | Verify completion, run tests, summaries |
| SubagentStop | A subagent completes | Validate subagent output, follow-ups |
| UserPromptSubmit | Prompt submitted | Inject sprint context, validate requests |

### PreToolUse
- Most common. Fires after Claude picks a tool, before it runs. The script can
  approve, block, request user confirmation, or modify parameters; a matcher
  filters tools. Example: matcher `Write`, `type: command`,
  `/path/to/validate-file-path.sh`.
- Uses: block dangerous Bash (`rm -rf`, force pushes); auto-approve safe repeated
  ops; validate write paths; modify tool inputs to inject defaults.

### PermissionRequest
- Fires when Claude would show a permission dialog; script decides allow, deny,
  or still ask. Example matcher `Bash(npm test*)` (argument patterns allowed).
- Uses: auto-approve frequent test commands; block writes to production config;
  allow reads in specific dirs; deny dangerous patterns.

### PostToolUse
- Fires right after a tool completes successfully; receives tool output.
  Example: matcher `Write|Edit` running `prettier --write
  "$CLAUDE_TOOL_INPUT_FILE_PATH"`.
- Uses: Prettier/Black/gofmt after writes; audit-log modifications; linters;
  notifications.

### PreCompact
- Fires before compaction (which summarizes older context and loses detail).
  Matcher `auto` or `manual` distinguishes automatic vs user-triggered
  compaction. Example: back up the transcript.
- Uses: back up transcript; save decisions/snippets; log milestones.

### SessionStart
- Fires on new or resumed session; script stdout is added to context. Example
  command: `git status --short && echo '---' && cat TODO.md`.
- Uses: branch and recent commits; TODO/sprint backlog; environment config.

### Stop
- Fires when Claude finishes responding; the script decides whether the task is
  really complete. The article says a script can return JSON with
  `"continue": true` to keep Claude working. Example uses `type: "prompt"` with a
  prompt asking the model to answer "complete" or "continue" plus what remains.
- Uses: force continuation until a checklist is done; verify tests pass; generate
  summaries; check code compiles.

### SubagentStop
- Fires when a subagent created via the Task tool finishes; same structure as
  Stop. Example `type: "prompt"` evaluating subagent output, answering "accept" or
  "reject" with reasons.
- Uses: validate subagent output; trigger follow-ups; log subagent activity.

### UserPromptSubmit
- Fires on prompt submission before processing; stdout is added to context with
  the prompt. Example: `cat ./current-sprint-context.md`.
- Uses: inject sprint context; validate prompts; block request types; add recent
  error logs or test results.

## Configuration and file locations
- Three levels: project `.claude/settings.json` (shared with team); user
  `~/.claude/settings.json` (all projects); local project
  `.claude/settings.local.json` (personal, uncommitted).
- The article states project-level settings take precedence over user-level;
  enterprise-managed policy settings also exist.
- Same files hold granular permissions (e.g. allow reads in a directory, block
  edits to sensitive files).

## Matcher syntax
- Matchers apply only to PreToolUse, PostToolUse, PermissionRequest.
- `"Write"` matches only Write; `"Write|Edit"` matches either; `"*"` or `""`
  matches all tools. Case-sensitive (`"bash"` won't match Bash).
- Argument patterns like `"Bash(npm test*)"`; MCP tools as `"mcp__memory__.*"`.

## Input, output, and structured responses

### What hooks receive
- JSON on stdin. Common fields: `session_id`, `transcript_path`, `cwd`,
  `permission_mode`, `hook_event_name`. Tool hooks also get `tool_name` and
  `tool_input`.

### How hooks respond
- Exit 0: success; stdout parsed for JSON or added to context. Exit 2: blocking
  error; stderr becomes the error message and the action is prevented. Other
  codes: non-blocking error; stderr shown in verbose mode.
- Structured JSON fields: `decision` (approve, block, allow, deny), `reason`
  (shown to Claude), `continue` (Stop hooks force continuation), `updatedInput`
  (modify tool parameters before execution).

## Environment and execution
- Env vars: `CLAUDE_PROJECT_DIR` (project root), `CLAUDE_CODE_REMOTE` (true in
  web environments), `CLAUDE_ENV_FILE` (SessionStart hooks persist variables);
  plus normal shell env.
- 60-second default timeout, configurable per hook. Multiple matching hooks run
  in parallel. Identical commands are deduplicated.

## Security considerations
- Hooks run arbitrary shell commands with user permissions. Safeguard: direct
  edits to hook config files require review in the `/hooks` menu before taking
  effect, so malicious code can't silently add hooks. Approved hooks run at your
  permission level.
- Practices: validate and sanitize stdin input; quote shell variables; absolute
  script paths; avoid processing sensitive files like `.env` or credentials.

## Debugging and testing
- Claude Code logs to transcript files; every hook gets `transcript_path` (a JSONL
  of full session history). Example SessionStart hook appends the transcript path
  to `~/.claude/sessions.log` via `jq`; then `tail -f <transcript>.jsonl | jq` to
  watch live.

### Hook-specific debugging
- Transcripts show what Claude did, not why a hook approved/blocked. Wrap hook
  commands in a logging script (example `log-wrapper.sh`: reads stdin, logs
  timestamp, `hook_event_name`, `tool_name` to `~/.claude/hooks.log`, pipes input
  to the real command, logs and returns its exit code). Use as
  `log-wrapper.sh your-tool-command.py` in the hook command.

## Building your own hooks
- Start with one hook for a real friction point; the PostToolUse formatter is a
  good first choice (immediate, visible feedback). Expand from there. Full
  reference: official hooks documentation.
