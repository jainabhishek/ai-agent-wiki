# Lessons from building Claude Code: How we use skills (raw capture)

> Source: https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills
> Publisher: Anthropic (Claude blog) · Date: 2026-06-03
> Captured: 2026-06-21 via WebFetch (condensed).

## What skills are

Folders containing instructions, scripts, and resources that agents discover and
use. A misconception is that they're "just markdown files" — they leverage folder
structure and configuration for maximum utility.

## Nine skill categories (from hundreds in active use)

1. Library and API reference (correct usage, CLIs, SDKs, gotchas)
2. Product verification (test/verify code — highest impact on quality)
3. Data fetching and analysis
4. Business process automation
5. Code scaffolding
6. Code quality and review
7. CI/CD and deployment
8. Runbooks (investigate symptoms → structured report)
9. Infrastructure operations (with guardrails)

## Key principles for effective skills

- **Avoid restating the obvious** — focus on knowledge that pushes Claude out of
  its normal way of thinking, not basic coding it already knows.
- **Build gotchas sections** — capture common failure points; highest-value
  content; update continuously.
- **Use progressive disclosure** — structure as folders with referenced files
  read contextually, not all at once.
- **Avoid railroading** — give needed info but leave flexibility to adapt.
- **Think through setup** — store config in config.json; prompt users rather than
  hard-coding assumptions.
- **Write descriptions for models, not humans** — the description field is what
  Claude scans to trigger the skill; include triggers and use cases.
- **Help Claude remember** — append-only logs, JSON, or SQLite via
  `${CLAUDE_PLUGIN_DATA}` to maintain context across sessions.
- **Store scripts and generate code** — provide helpers so Claude composes rather
  than rebuilds boilerplate.
- **Use on-demand hooks** — opinionated hooks (e.g. `/careful` blocking
  destructive commands) that activate only when the skill is called.

## Distribution and scaling

- Small teams: check skills into `./.claude/skills`.
- Large orgs: internal plugin marketplaces; selective install.
- Organic growth: validate in sandboxes before promoting.
- Dependencies: reference other skills by name; the model invokes them if installed.

## Measuring success

Use PreToolUse hooks to log skill usage; find popular or under-triggering skills.

## Starting out

Skills improve iteratively — most began as "a few lines and a single gotcha,
then got better because people kept adding to them as Claude hit new edge cases."
