# Equipping agents for the real world with Agent Skills — Anthropic Engineering (raw capture)

> Source: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
> Publisher: Anthropic Engineering
> Captured: 2026-06-21 via WebFetch (condensed).

## What Agent Skills are

"Organized folders of instructions, scripts, and resources that agents can
discover and load dynamically to perform better at specific tasks." Composable
capabilities that specialize a general agent — "like putting together an
onboarding guide for a new hire."

## SKILL.md structure & frontmatter

Every skill has a `SKILL.md` starting with YAML frontmatter:
- **name** — identifier.
- **description** — how Claude decides when to activate it.
Frontmatter is "loaded into its system prompt at startup," so Claude can
recognize relevant skills without consuming full context.

## Progressive disclosure: three levels

1. **Names + descriptions** in the system prompt — recognize when a skill applies.
2. **Full SKILL.md** loads when Claude judges it relevant.
3. **Bundled files** (reference.md, forms.md, …) load only in scenario-specific
   situations (e.g. "when filling out a form").
Requires agents with a filesystem and code-execution tools; avoids loading entire
skill contents unnecessarily.

## Bundling scripts & resources

Skills package supplementary files referenced by name (e.g. the PDF skill ships
reference.md + forms.md), and "can also include code for Claude to execute as
tools at its discretion" — deterministic operations without loading code into
context.

## Composability

Rather than "building fragmented, custom-designed agents for each use case,"
specialize agents through reusable modular skills — "capturing and sharing
procedural knowledge."

## Authoring best practices

- **Evaluation-driven development** — find capability gaps via representative
  tasks before building.
- **Structural scaling** — split unwieldy SKILL.md into referenced docs.
- **User perspective** — watch Claude's actual usage and iterate.
- **Collaborative iteration** — work with Claude to capture patterns into skills.

## Security

Install skills only from trusted sources; audit less-trusted ones — code
dependencies, bundled resources, and instructions pointing Claude to untrusted
network connections.

## Platform support

Claude.ai, Claude Code, the Claude Agent SDK, and the Claude Developer Platform.
