# Steering Claude Code: CLAUDE.md files, skills, hooks, rules, subagents and more (raw capture)

> Source: https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more
> Publisher: Anthropic (Claude blog) · Date: 2026-06-18
> Captured: 2026-06-21 via WebFetch (condensed).

## Seven mechanisms for steering Claude Code

Each controls *when* instructions load, *whether* they persist, and *how much*
authority they carry:

1. **CLAUDE.md files** — project overview and conventions.
2. **Rules** — specific constraints, optionally path-scoped.
3. **Skills** — procedural workflows triggered on-demand.
4. **Subagents** — isolated assistants for parallel side tasks.
5. **Hooks** — deterministic automation on lifecycle events.
6. **Output styles** — system-prompt modifications for role changes.
7. **System prompt appending** — additive instructions at invocation.

## When to use each

- **CLAUDE.md** — keep under ~200 lines. Build commands, directory structure,
  monorepo layout, team norms. Root loads at session start and persists;
  subdirectory files load on-demand. In shared repos assign ownership; push
  team conventions into path-scoped rules and procedures into skills to save
  tokens.
- **Rules** — load at session start or when matching files are touched. Use
  `paths:` frontmatter for cross-cutting constraints (e.g. "migrations are
  append-only").
- **Skills** — names/descriptions load at start; full body only when invoked.
  Best for repeatable procedures (deploy, release checklist, code review).
  Auto-matched or slash-triggered; re-injected up to a token budget on compaction.
- **Subagents** — run in isolated context windows; only final summaries return.
  Ideal for deep search, log analysis, dependency audits. Use subagents for side
  tasks whose intermediate results you won't reference; use skills when you want
  to see and steer each step.
- **Hooks** — fire deterministically on lifecycle events (edits, tool calls,
  session start). Linters, notifications, command blocking, backups. A PreToolUse
  hook can inspect any tool call and exit code 2 to deny it.
- **Output styles** — injected into system prompt, never compacted; high weight,
  use sparingly. Custom styles override default guidance (scope, comments,
  security, testing) — caution.
- **System prompt appending** — additive only; cached after first request. Good
  for coding standards, formatting, domain knowledge.

## Anti-patterns

- Procedural workflows in CLAUDE.md → move to skills.
- "Never do this" rules alone → use deterministic hooks or managed settings.
- API-specific rules without path scoping → add `paths:` frontmatter.
- Personal preferences in project files → use user-level equivalents.
- Unscoped rules → path-scope to load only when relevant.

## Scaling

Subagents can nest up to five levels and orchestrate tens-to-hundreds of
background agents. Orchestration plans and intermediate results live in script
variables rather than context, enabling scale without fidelity loss. Bundles of
skills, subagents, hooks, and styles can be packaged as **plugins** for sharing.
