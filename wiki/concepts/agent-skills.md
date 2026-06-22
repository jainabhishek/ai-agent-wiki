---
title: Agent Skills
type: concept
created: 2026-06-21
updated: 2026-06-21
tags: [skills, agents, context-engineering, best-practices]
---

# Agent Skills

> Skills are folders of instructions, scripts, and resources that an agent
> discovers and loads **on demand** — a context-engineering mechanism for giving
> an agent procedural know-how without bloating its system prompt. (see
> [[anthropic-lessons-building-claude-code-skills]], [[anthropic-steering-claude-code]])

## Definition

Not "just markdown files." A skill is a folder with a description (for matching),
a body of instructions, and optional referenced files, scripts, and config.
Names/descriptions load at session start; the full body loads only when the skill
is invoked (auto-matched or via slash command) — **progressive disclosure**. See
[[context-engineering]].

## SKILL.md & three-level progressive disclosure

The architectural form ([[anthropic-eng-agent-skills]]): every skill is a
`SKILL.md` whose YAML frontmatter (`name`, `description`) loads into the system
prompt at startup. Disclosure has **three levels**:
1. **names + descriptions** in the system prompt (cheap recognition);
2. **full SKILL.md** loads when the agent judges it relevant;
3. **bundled files** (e.g. `reference.md`, `forms.md`) load only in
   scenario-specific situations.
Skills can also **bundle executable code** the agent runs as tools at its
discretion — deterministic operations without loading code into context (see
[[tool-design]]). Requires an agent with a filesystem and code execution.

**Composability & reach:** reusable modular skills specialize a general agent
instead of building a bespoke agent per use case, and they work across a surface —
Claude.ai, [[claude-code]], the [[claude-agent-sdk]], and the Claude Developer
Platform. **Security:** install only from trusted sources; audit dependencies,
bundled resources, and any instructions pointing at untrusted networks (see
[[guardrails]]).

## Authoring best practices

- **Write the description for models, not humans** — it's what the agent scans to
  decide whether to trigger; include triggers and use cases. (Mirrors the
  tool-clarity finding in [[tool-design]].)
- **Build a gotchas section** — common failure points are the highest-value
  content; update continuously.
- **Avoid restating the obvious** — capture what pushes the model out of its
  default behavior, not basics it already knows.
- **Avoid railroading** — provide needed info but leave room to adapt.
- **Progressive disclosure** — split into referenced files read contextually.
- **Store scripts / generate code** — let the model compose, not rebuild boilerplate.
- **Help the agent remember** — append-only logs, JSON, or SQLite for
  cross-session state.
- **Thoughtful setup** — config files; prompt the user instead of hard-coding.
- **On-demand hooks** — opinionated hooks that activate only with the skill.

## Categories (observed in practice)

Library/API reference · product verification (highest quality impact) · data
fetch/analysis · business-process automation · scaffolding · code quality/review ·
CI/CD · runbooks · infra ops.

## Why it matters

Skills are how the "let Claude manage context" principle of
[[harnessing-claudes-intelligence]] is operationalized, and they start tiny and
compound — a direct application of start-simple ([[agent-design-principles]]).

## Related concepts

- [[agent-steering]], [[context-engineering]], [[tool-design]],
  [[agent-design-principles]], [[agent-evals]], [[guardrails]]

## Key entities

- [[anthropic]], [[claude-code]], [[claude-agent-sdk]]

## Appears in

- [[anthropic-lessons-building-claude-code-skills]]
- [[anthropic-steering-claude-code]]
- [[anthropic-eng-agent-skills]]

## Contradictions / open questions

- _None recorded._
