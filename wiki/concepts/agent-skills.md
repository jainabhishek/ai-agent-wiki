---
title: Agent Skills
type: concept
created: 2026-06-21
updated: 2026-10-12
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

**Cross-vendor adoption.** [[openai]] ships skills aligned with the Agent Skills
open standard in the Responses API (skills encode the *how*, a hosted or local
shell executes the *do*) and in [[openai-codex]], which loads each skill's name
and description into context (see [[openai-shell-skills-compaction]],
[[openai-rethinking-skills-prompts-gpt-6-astra]]). The OpenAI Agents API loads
skills from configured directories (see [[openai-agents-api-guide]]). Skills
added to a repo travel with it: in Claude Code cloud sessions, repo skills come
along while `~/.claude` stays on the laptop (see
[[anthropic-claude-code-in-the-cloud]]).

**Skills grow from saved code.** An agent with code execution can save a working
function to a skills directory and add a `SKILL.md` to make it reusable (see
[[anthropic-eng-code-execution-with-mcp]]). Claude Code can ship a saved
multi-agent workflow inside a skill folder (`SKILL.md` + workflow script +
rubric) as a template (see [[anthropic-harness-for-every-task]]). Skills also add
capability without adding a tool: progressive disclosure through a skill is
Anthropic's stated alternative to a new tool definition (see
[[anthropic-seeing-like-an-agent]]).

## Converging architecture (Anthropic and OpenAI)

Both vendors now give the same structural advice. This is an architecture
convergence, not shared prompting advice:

| Practice | Anthropic | OpenAI |
|----------|-----------|--------|
| **Description = routing logic** — say when to use, when not, and the expected output; short | [[anthropic-lessons-building-claude-code-skills]] | [[openai-shell-skills-compaction]], [[openai-skills-for-oss-maintenance]], [[openai-rethinking-skills-prompts-gpt-6-astra]] |
| **Root file as router / progressive disclosure** — a small root that points to supporting files | [[anthropic-eng-agent-skills]], [[anthropic-new-rules-context-engineering-claude-5]] | [[openai-rethinking-skills-prompts-gpt-6-astra]] |
| **Scripts for deterministic work**, model for interpretation | [[anthropic-eng-agent-skills]], [[anthropic-eng-code-execution-with-mcp]] | [[openai-skills-for-oss-maintenance]] |
| **Trigger evals** — measure whether the skill fires when it should and not otherwise | [[anthropic-automating-eval-design-hillclimbing]] | [[openai-testing-agent-skills-with-evals]] |

## Authoring best practices

- **Write the description for models, not humans** — it's what the agent scans to
  decide whether to trigger; include triggers and use cases. (Mirrors the
  tool-clarity finding in [[tool-design]].) Treat it as routing logic: when to
  use, when *not* to use, outputs and success criteria, and whether the skill is
  mandatory (see [[openai-shell-skills-compaction]],
  [[openai-skills-for-oss-maintenance]]).
  - **Negative examples fix misfires.** Adding skills can first *reduce*
    correct triggering: Glean saw triggering drop about 20% in targeted evals
    until "don't use this skill when…" cases and edge cases were added (see
    [[openai-shell-skills-compaction]]).
  - **Description count has a cost.** With many skills installed, Codex shortens
    descriptions to fit and selection gets worse; contradictory or over-broad
    descriptions load irrelevant instructions (see
    [[openai-rethinking-skills-prompts-gpt-6-astra]]). See
    [[context-engineering]].
- **Build a gotchas section** — common failure points are the highest-value
  content; update continuously.
- **Avoid restating the obvious** — capture what pushes the model out of its
  default behavior, not basics it already knows.
- **Map stale training priors explicitly.** Skill content that is present can
  still lose to the model's training priors: Claude kept writing older API shapes
  despite a skill documenting the current ones. A "remembered form → current
  form" table near the top of the skill raised its eval score from 77% to 80%
  (see [[anthropic-automating-eval-design-hillclimbing]]).
- **Avoid railroading** — provide needed info but leave room to adapt. Both
  vendors' current-generation guidance pushes further: keep skills as lightweight
  guides and constrain tightly only where it matters
  ([[anthropic-new-rules-context-engineering-claude-5]], Claude 5 generation);
  replace step-by-step recipes with less specific guidance
  ([[openai-rethinking-skills-prompts-gpt-6-astra]], GPT-6 Astra). Both are
  scoped to their models.
- **Write for every model that will read it.** Repo skills are read by other
  contributors' agents on other models (see
  [[openai-rethinking-skills-prompts-gpt-6-astra]]).
- **Progressive disclosure** — split into referenced files read contextually; the
  root `SKILL.md` is a tree of files, not a catch-all (see
  [[anthropic-new-rules-context-engineering-claude-5]]).
- **Store scripts / generate code** — let the model compose, not rebuild
  boilerplate. If the model keeps rediscovering the same shell recipe, make it a
  tiny script with deterministic output that fails loudly; keep interpretation
  with the model (see [[openai-skills-for-oss-maintenance]]).
- **Put templates in skills, not the system prompt** — they cost nothing until
  invoked (see [[openai-shell-skills-compaction]]).
- **Help the agent remember** — append-only logs, JSON, or SQLite for
  cross-session state.
- **Thoughtful setup** — config files; prompt the user instead of hard-coding.
- **On-demand hooks** — opinionated hooks that activate only with the skill.
- **Making skills mandatory.** Short if/then rules in `AGENTS.md` can require a
  skill (e.g. run the verification skill when runtime code changes), and the
  skill then defines what "verified" means; naming the skill in the request is
  OpenAI's determinism lever for production (see
  [[openai-skills-for-oss-maintenance]], [[openai-shell-skills-compaction]],
  [[agent-instructions]]).

## Evaluating skills

A skill is a prompt and is evaluated like one (see [[agent-evals]]):
- **Trigger tests** — 10–20 prompts per skill covering explicit, implicit, and
  contextual invocations plus a negative control that should *not* trigger (see
  [[openai-testing-agent-skills-with-evals]]).
- **Grade the trace, not only the output** — check that the skill fired and its
  steps ran; goal types are outcome, process, style, and efficiency (see
  [[openai-testing-agent-skills-with-evals]]).
- **Trigger rate as a hillclimb target.** Skill triggering is a good case for
  iterative optimization because the trigger rate is directly coupled to the
  description being edited; use a train/test split to catch overfitting (see
  [[anthropic-automating-eval-design-hillclimbing]]).

## Categories (observed in practice)

Library/API reference · product verification (highest quality impact) · data
fetch/analysis · business-process automation · scaffolding · code quality/review ·
CI/CD · runbooks · infra ops. OpenAI's Agents SDK repos add docs sync, release
review, PR summaries, and test-coverage skills (see
[[openai-skills-for-oss-maintenance]]).

## Why it matters

Skills are how the "let Claude manage context" principle of
[[harnessing-claudes-intelligence]] is operationalized, and they start tiny and
compound — a direct application of start-simple ([[agent-design-principles]]).

## Related concepts

- [[agent-steering]], [[context-engineering]], [[tool-design]],
  [[agent-design-principles]], [[agent-evals]], [[guardrails]],
  [[agent-instructions]]

## Key entities

- [[anthropic]], [[claude-code]], [[claude-agent-sdk]], [[openai]],
  [[openai-codex]]

## Appears in

- [[anthropic-lessons-building-claude-code-skills]]
- [[anthropic-steering-claude-code]]
- [[anthropic-eng-agent-skills]]
- [[anthropic-eng-code-execution-with-mcp]]
- [[anthropic-new-rules-context-engineering-claude-5]]
- [[anthropic-seeing-like-an-agent]]
- [[anthropic-automating-eval-design-hillclimbing]]
- [[anthropic-claude-code-in-the-cloud]]
- [[anthropic-harness-for-every-task]]
- [[openai-shell-skills-compaction]]
- [[openai-testing-agent-skills-with-evals]]
- [[openai-skills-for-oss-maintenance]]
- [[openai-rethinking-skills-prompts-gpt-6-astra]]
- [[openai-agents-api-guide]]

## Contradictions / open questions

- _None recorded._ Model-specific skill handling (for example, GPT-6 Astra's
  higher sensitivity to skill text and the prompt to name the exact `SKILL.md`
  when a skill makes it pause) lives on [[openai-prompting-gpt-6-astra]], not
  here.
