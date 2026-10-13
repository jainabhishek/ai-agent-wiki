---
title: Agent Skills
type: concept
created: 2026-06-21
updated: 2026-10-13
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

**Approximate cost per level.** Anthropic gives about 50 tokens of metadata per
skill at start, about 500 tokens for a full `SKILL.md`, and 2,000+ tokens for
reference files loaded only when needed; this lets one agent hold hundreds of
skills (see [[anthropic-building-agents-with-skills]]). The skills guide adds two
budget checks: keep `SKILL.md` under 5,000 words, and review the set when more
than 20–50 skills are enabled at once (see
[[anthropic-complete-guide-building-skills]], [[context-engineering]]).

**Frontmatter rules (Anthropic skills guide, Jan 2026).** The file is exactly
`SKILL.md`; the folder and `name` are kebab-case; no `README.md` inside the
skill. The `description` states what the skill does and when to use it, stays
under 1,024 characters, and contains no `<` or `>`. Names with "claude" or
"anthropic" are reserved. The guide gives the reason: frontmatter enters the
system prompt, so it could inject instructions (see
[[anthropic-complete-guide-building-skills]], [[guardrails]],
[[prompt-injection]]).

**Loading paths differ by platform.** On OpenAI's hosted runtime, the platform
loads skills deterministically: skills are versioned bundles stored by ID, and
before the model call the API fetches the metadata, unpacks the bundle into the
container, and adds metadata and path to context (see
[[openai-responses-api-computer-environment]]). Codex CLI inserts skill metadata
into a fixed prelude together with the `AGENTS.md` chain (see
[[openai-unrolling-codex-agent-loop]]). In Claude Code, skills can be
path-scoped to a directory, so a team's deploy skill stays out of unrelated
sessions (see [[anthropic-claude-code-large-codebases]]). A harness can also
inject a skill before the first model call when a signal such as the entry page
predicts it (see [[anthropic-anatomy-of-commerce-agents]]).

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

## Skill types

- **Capability uplift vs encoded preference.** A capability-uplift skill
  teaches what the base model cannot do, or cannot do consistently. An
  encoded-preference skill sequences steps the model can already do, in a
  team's own process. The two need tests for different reasons: if the base
  model passes a capability-uplift skill's evals without the skill, the skill is
  obsolete, not broken; an encoded-preference skill lasts longer but is only as
  good as its fidelity to the real workflow (see
  [[anthropic-improving-skill-creator]]).
- **Use-case categories.** The skills guide names three: document and asset
  creation, workflow automation, and MCP enhancement (see
  [[anthropic-complete-guide-building-skills]]). Observed categories in practice
  are listed under "Categories" below.

## Skills beside MCP, subagents, memory, and the system prompt

- **MCP gives access; skills give the procedure.** MCP is connectivity ("what
  Claude can do") and a skill is knowledge ("how Claude should do it") (see
  [[anthropic-complete-guide-building-skills]]). Ship both together as a
  **plugin** (skills, MCP servers, hooks, LSP servers, subagents), or publish a
  skill beside the server (see [[anthropic-agents-production-systems-mcp]],
  [[model-context-protocol]]).
- **One general agent plus skills, not one agent per domain.** Anthropic says it
  stopped building specialized agents: code is a general interface, so a
  general agent with bash and a filesystem covers many domains, and skills
  supply the domain expertise. Its four layers are agent loop, agent runtime,
  MCP servers, and skills library, each changeable on its own (see
  [[anthropic-building-agents-with-skills]], [[agent-core-components]]).
- **Skills vs subagents.** Anthropic's applied team reports that, across
  commerce deployments, one agent with skills beat both a single prompt and a
  subagent-per-domain design on quality, often at lower cost per task, because
  each handoff loses state and adds tokens and latency. Subagents fit only as
  tools for self-contained work that returns a compact answer; the test for a
  handoff is who owns the conversation (see
  [[anthropic-anatomy-of-commerce-agents]], [[agent-orchestration]]).
- **Skill vs system prompt, by frequency.** Content relevant to about one third
  or more of traffic, and critical rules (safety, legal, brand), go in the
  system prompt; other content goes in skills (see
  [[anthropic-anatomy-of-commerce-agents]]). Domain guidance that most requests
  do not need belongs in a skill, so unrelated tasks carry no tokens for it (see
  [[anthropic-improving-frontend-design-through-skills]]).
- **Skills vs memory.** Skills are procedural, stable, and changed on purpose by
  humans; memory is written by the agent at inference time and changes
  constantly (see [[anthropic-warp-builds-self-improving-agents]],
  [[agent-memory]]).
- **Skills vs hooks.** A skill is an advisory control that makes compliance
  likely; a hook is the deterministic layer behind it. Policies that must
  always hold need both (see [[anthropic-ai-native-sdlc-playbook]],
  [[agent-steering]]).

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
- **Description formula.** What the skill does, when to use it, and key
  capabilities, in phrases users actually say. Under-triggering → add detail and
  keywords; over-triggering → add negative triggers and narrow the scope; to
  debug, ask the model when it would use the skill (see
  [[anthropic-complete-guide-building-skills]]).
- **Start from one hard task.** Iterate on one hard task until it works, extract
  the winning approach into a skill, then broaden the test cases (see
  [[anthropic-complete-guide-building-skills]]). Related habits: package a
  workflow as a skill once it succeeds (see
  [[openai-codex-maxxing-long-running-work]]); build a skill once a pattern
  recurs (see [[anthropic-unreasonable-effectiveness-of-html]], personal
  opinion). Anthropic's CI team reports writing a 617-line investigation skill
  by debugging one live incident turn by turn with Claude, then asking Claude to
  write the skill (see [[anthropic-ai-ci-cd-on-call]]).
- **For domains with generic default output** (distributional convergence),
  Anthropic's method has four steps: name the convergent defaults, give concrete
  alternatives, write at the right altitude (neither exact values nor vague
  taste words), and package the result as a skill. Its frontend-aesthetics
  skill is about 400 tokens (see
  [[anthropic-improving-frontend-design-through-skills]]).
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
  [[anthropic-new-rules-context-engineering-claude-5]]). A MacCoss Lab case study
  reports "reference, do not embed": each skill points into a central
  documentation base instead of copying it, so skills stay light (see
  [[anthropic-onboarding-claude-code-legacy-codebase]]). Put critical rules at
  the top and link `references/` explicitly (see
  [[anthropic-complete-guide-building-skills]]).
- **Explicit triggers for critical skills.** The same case study reports a
  `debugging` skill whose description says to always load it for bugs, failures,
  or unexpected behavior (see
  [[anthropic-onboarding-claude-code-legacy-codebase]]).
- **Store scripts / generate code** — let the model compose, not rebuild
  boilerplate. If the model keeps rediscovering the same shell recipe, make it a
  tiny script with deterministic output that fails loudly; keep interpretation
  with the model (see [[openai-skills-for-oss-maintenance]]). For critical
  validations, bundle a script, because "code is deterministic; language
  interpretation isn't" (see [[anthropic-complete-guide-building-skills]]). When
  Claude kept rewriting a slide-styling script, Anthropic saved it in the skill
  (see [[anthropic-building-agents-with-skills]]).
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
  [[openai-testing-agent-skills-with-evals]]). Anthropic's skills guide uses the
  same 10–20 query count with obvious, paraphrased, and unrelated queries, and
  targets triggering on 90% of relevant queries. It adds functional tests
  (Given/When/Then) and a performance comparison against a no-skill baseline
  (see [[anthropic-complete-guide-building-skills]]). Anthropic calls these
  targets rough benchmarks with some "vibes-based" judgment.
- **Isolated runs and blind comparison.** skill-creator runs each eval in a
  separate agent with a clean context, and comparator agents judge skill v1 vs
  v2, or skill vs no skill, without knowing which is which. Benchmark mode
  tracks pass rate, elapsed time, and token usage (see
  [[anthropic-improving-skill-creator]]).
- **Re-run on every model change.** Evals catch regressions on a new model
  before the team notices drift, and show when a capability-uplift skill has
  become obsolete (see [[anthropic-improving-skill-creator]]).
- **Grade the trace, not only the output** — check that the skill fired and its
  steps ran; goal types are outcome, process, style, and efficiency (see
  [[openai-testing-agent-skills-with-evals]]).
- **Trigger rate as a hillclimb target.** Skill triggering is a good case for
  iterative optimization because the trigger rate is directly coupled to the
  description being edited; use a train/test split to catch overfitting (see
  [[anthropic-automating-eval-design-hillclimbing]]).

## Verification skills and where to place them

Manual checks that a developer repeats on every feature become verification
loops when written as skills (see [[anthropic-verification-loops-with-skills]],
[[anthropic-getting-started-with-loops]]). Anthropic gives four placements:
- **Standalone** — invoked on purpose, for cross-cutting checks (security scan,
  accessibility audit). Running it after every change is the signal to embed or
  chain it.
- **Embedded** — a one-line step appended to the producing skill. Use it only
  for skills you can edit, not built-in or plugin-managed skills that updates
  overwrite.
- **Chained** — a skill invokes the next at its end; a wrapper skill adds checks
  to a skill you cannot modify. Chains trade flexibility for automation and can
  raise token spend.
- **On every PR** — the same skills gate every teammate's change. Wait until the
  chain is stable, because each tweak is then visible to the team.
(see [[anthropic-verification-loops-with-skills]], [[agent-evals]])

## Keeping skills current

- **Skills are served content.** Anthropic's data team reports that Claude Tag
  re-reads the data repo's `skills/` directory on every conversation, because
  data models change several times a day and a stale skill produces confident
  wrong answers (see [[anthropic-claude-tag-analytics-in-slack]]). The same team
  reports that unmaintained skills drifted from about 95% to about 65% offline
  accuracy within a month. Its fix: keep skill docs in the same repo as the data
  models, and use a code-review hook that flags model changes that do not touch
  a skill (see [[anthropic-self-service-data-analytics]]).
- **Self-improving loop with a human gate.** Warp reports a two-skill loop: a
  base skill does the task, humans comment on its output, and a scheduled
  improver skill opens a PR with the smallest edit to the base skill. The normal
  code-review workflow is the approval gate. Warp advises assuming some feedback
  is wrong and keeping a human at the filtering or final-review stage (see
  [[anthropic-warp-builds-self-improving-agents]], [[guardrails]]).
- **Promote recurring lessons into skills.** Anthropic's CI on-call agent
  appends each resolved incident to a lessons log and promotes recurring
  patterns into the skill (see [[anthropic-ai-ci-cd-on-call]],
  [[agent-memory]]). Rocket Money reports running procedures as code by default;
  when one breaks, the agent repairs it and re-codifies it, and bundled skill
  scripts made this pattern concrete (see [[claude-customer-rocket-money]]).
- **Turn build lessons into skills.** Cresta reports that its agent builder
  shares a build's patterns, business rules, and eval approaches as a skill (see
  [[anthropic-cresta-agent-builder]]).

## Who writes skills

Anthropic observes that most skill authors are subject-matter experts, not
engineers, and built skill-creator's evals so they can test without code (see
[[anthropic-improving-skill-creator]]). Because skills are files, PMs, analysts,
and domain experts author them alongside engineers (see
[[anthropic-building-agents-with-skills]]). Case reports: an OffDeal banker, not
an engineer, built a branded-deck skill with 20 slide templates (see
[[claude-customer-offdeal]]); Anthropic's multiplayer-agent guidance uses skill
files to define agent roles, so others can stand up the same agent type (see
[[anthropic-building-effective-human-agent-teams]]).

## Categories (observed in practice)

Library/API reference · product verification (highest quality impact) · data
fetch/analysis · business-process automation · scaffolding · code quality/review ·
CI/CD · runbooks · infra ops. OpenAI's Agents SDK repos add docs sync, release
review, PR summaries, and test-coverage skills (see
[[openai-skills-for-oss-maintenance]]). Anthropic's data team pairs a thin
knowledge skill that routes to about 30 per-domain reference files with runbook
skills for analytic methods (see [[anthropic-self-service-data-analytics]],
[[anthropic-claude-tag-analytics-in-slack]]). Kepler reports idempotent skills
that wrap recurring workflows and coordinate deterministic and nondeterministic
stages (see [[anthropic-kepler-verifiable-ai]]).

## Why it matters

Skills are how the "let Claude manage context" principle of
[[harnessing-claudes-intelligence]] is operationalized, and they start tiny and
compound — a direct application of start-simple ([[agent-design-principles]]).

## Related concepts

- [[agent-steering]], [[context-engineering]], [[tool-design]],
  [[agent-design-principles]], [[agent-evals]], [[guardrails]],
  [[agent-instructions]], [[model-context-protocol]], [[agent-orchestration]],
  [[agent-memory]], [[agent-core-components]]

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
- [[anthropic-complete-guide-building-skills]]
- [[anthropic-building-agents-with-skills]]
- [[anthropic-improving-skill-creator]]
- [[anthropic-agents-production-systems-mcp]]
- [[anthropic-improving-frontend-design-through-skills]]
- [[anthropic-anatomy-of-commerce-agents]]
- [[anthropic-verification-loops-with-skills]]
- [[anthropic-getting-started-with-loops]]
- [[anthropic-warp-builds-self-improving-agents]]
- [[anthropic-claude-tag-analytics-in-slack]]
- [[anthropic-self-service-data-analytics]]
- [[anthropic-ai-ci-cd-on-call]]
- [[anthropic-onboarding-claude-code-legacy-codebase]]
- [[anthropic-claude-code-large-codebases]]
- [[anthropic-ai-native-sdlc-playbook]]
- [[anthropic-building-effective-human-agent-teams]]
- [[anthropic-cresta-agent-builder]]
- [[anthropic-kepler-verifiable-ai]]
- [[anthropic-unreasonable-effectiveness-of-html]]
- [[claude-customer-offdeal]]
- [[claude-customer-rocket-money]]
- [[openai-responses-api-computer-environment]]
- [[openai-unrolling-codex-agent-loop]]
- [[openai-codex-maxxing-long-running-work]]
- [[harnessing-claudes-intelligence]]
- [[openai-prompting-gpt-6-astra]]

## Contradictions / open questions

- **skill-creator and automated tests, superseded (recorded 2026-10-12).**
  [[anthropic-complete-guide-building-skills]] (Jan 2026) says skill-creator
  does not run automated test suites or produce quantitative evaluation results.
  [[anthropic-improving-skill-creator]] (2026-03-03) adds evals, benchmark mode,
  isolated parallel runs, and blind comparators. The later post supersedes the
  guide on this point; the guide's other testing advice still stands.
- **Reserved-name rule is internally inconsistent.** The same guide reserves
  names *containing* "claude"/"anthropic" in one chapter and names with that
  *prefix* in its reference appendix (see
  [[anthropic-complete-guide-building-skills]]). Open which rule the platform
  enforces.
- **Model-specific skill handling** (for example, GPT-6 Astra's higher
  sensitivity to skill text and the prompt to name the exact `SKILL.md` when a
  skill makes it pause) lives on [[openai-prompting-gpt-6-astra]], not here.
