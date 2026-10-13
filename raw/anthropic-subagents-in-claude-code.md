# How and when to use subagents in Claude Code — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/subagents-in-claude-code
> Publisher: Anthropic (claude.com articles) · Date: 2026-04-07
> Captured: 2026-10-12 via WebFetch (condensed).

No author listed. Category: Best practices. Product: Claude Code. Reading time
17 min. The page also shows 2026-10-05 to 2026-10-08 in "Related articles";
those dates belong to other articles. Code examples on the page (custom agent
file, CLAUDE.md snippet, skill) did not render in the fetched text.

## Intro (no heading)

Long sessions fill the context window with file reads and tangents; responses
slow and token cost rises. Example: a monorepo feature with side tasks (trace
auth, find a date-formatting util, check for an existing design-system
component) that could run in parallel. Analogy: subagents are like browser tabs
for tangents.

## What is a subagent?

An isolated Claude instance with its own context window. It does the work and
returns only the result. Each starts fresh, can run in parallel, and can have
different permissions (read-only research versus full-edit implementation).
Built-in types:
- **General-purpose** — complex multi-step tasks.
- **Plan** — researches the codebase before proposing a strategy.
- **Explore** — fast, read-only search.

## When should you use subagents?

- **Research-heavy tasks.** Signal: gathering context means reading dozens of
  files. Benefit: main thread stays clean and receives synthesized findings.
- **Multiple independent tasks.** Signal: no dependencies between subtasks (for
  example fixing errors across files). Benefit: parallel completion is faster
  (three subagents finish sooner).
- **Fresh perspective needed.** Signal: you want review without inherited
  assumptions. Pro-tip contrast: `/clear` also resets context but discards the
  history entirely.
- **Verification before committing.** Signal: a second opinion is warranted,
  for example checking for overfitting to tests or missed edge cases.
- **Pipeline workflows.** Signal: distinct sequential phases (design, implement,
  test) with clear handoffs.
- Pro-tip heuristic: point Claude to subagents when a task touches 10 or more
  files or has 3 or more independent pieces.

## How to direct subagent usage

### Conversational invocation
Works in terminal, VS Code, JetBrains, web, and desktop. Ask for a subagent to
explore a module, a separate security review, or parallel research across API
routes, database models, and frontend components. Tips: scope the task, ask for
parallelism explicitly, name the output format, ask for fresh context when you
want unbiased analysis. `Ctrl+B` moves a running subagent to the background;
`/tasks` lists background work.

### Custom subagents
- Markdown files in `.claude/agents/` (project, shared with the team) or
  `~/.claude/agents/` (user level).
- Each has its own system prompt, tool permissions, and optional model.
- Create with the `/agents` command (interactive; can draft from a description)
  or by hand. Invoke by name or let Claude route automatically.
- The `description` field drives automatic delegation: state trigger
  conditions, not only capability.

### CLAUDE.md instructions
Sets policy for when to use subagents (for example: code review always goes
through a read-only subagent). Loaded at the start of every conversation.

### Skills
- Live in `.claude/skills/`; invoked as `/skill-name` or loaded automatically
  when the description matches. Loaded on demand, unlike CLAUDE.md.
- A skill is a directory: `SKILL.md` plus optional templates, example outputs,
  scripts. The legacy `.claude/commands/` format was one flat file.
- Example: a `/deep-review` skill runs a three-part subagent analysis and can
  trigger before commits.

### Hooks
- User-defined shell commands, HTTP endpoints, or LLM prompts that fire at
  lifecycle points.
- Example: a **Stop** hook (`.claude/hooks/check-tests.sh`) runs the test
  suite; on failure it returns JSON with `decision: "block"` and a `reason`, so
  Claude keeps working. A `stop_hook_active` guard prevents an infinite loop.
- Described as the most automated option; adopt after simpler methods.

## Practical patterns

- **Research before implementing** — a subagent summarizes unfamiliar code first.
- **Parallel modifications** — one subagent per file for the same pattern change.
- **Independent review** — a subagent with no knowledge of earlier tradeoffs.
- **Pipeline workflow** — design, implement, test subagents with explicit handoffs.

## When shouldn't you use subagents?

- **Sequential, dependent work** — keep chained steps in one session.
- **Same-file edits** — parallel edits conflict.
- **Small tasks** — delegation overhead exceeds the benefit.
- **Too many specialists** — a large roster makes automatic delegation less
  reliable; a handful is typical.
- **Agents that must coordinate** — subagents report only to the main
  conversation. For peer communication use **agent teams**, which are heavier
  and more expensive.

## Start conversational, automate later

Start with conversational prompts; notice repeated requests; then encode them as
CLAUDE.md rules, skills, custom agents, and hooks.
