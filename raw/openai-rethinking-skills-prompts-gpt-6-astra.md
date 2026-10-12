# Rethinking skills and prompts for GPT-6 Astra — OpenAI (Developers blog) (raw capture)

> Source: https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
> Publisher: OpenAI (Developers blog) · Date: 2026-09-11 (page byline "Sep 11, 2026"; category tag "Codex")
> Author: Eric Provencher
> Subtitle: revisit skill descriptions, AGENTS.md, and task prompts to avoid bloated context.
> Captured: 2026-10-12 via curl of the .md endpoint plus the HTML page for the byline (condensed and paraphrased).
> Date note: one secondary source gave Sep 5; the page byline says Sep 11, 2026, which is used here.

## (Intro)

- Coding agents improved fast; scaffolding and handholding that older models needed is no longer required.
- Users of agents such as Codex have built up instructions over a year of steering. Revisiting them is worthwhile at every release, and the author says it matters more than ever with GPT-6 Astra.
- Instructions take three forms: skills, `AGENTS.md`, and task prompts.

## Better skills

- Skills = prompts stored as Markdown, optionally bundled with resources and scripts; most useful for one specific workflow or for using particular apps.
- Problem 1: projects now ship many skills. Each skill's name and description load into context so the model can choose. Many descriptions are too long, and with too many skills **Codex shortens the descriptions to fit**, so the model sees less of each and picks worse.
- Problem 2: descriptions contradict each other or over-state when to use a skill, so the model loads instructions that do not help.
- The `$skill-creator` skill (common way to write skills) was recently updated to address these failure modes.
- Rule 1 — descriptions as short as possible while clear about when to use. Illustration: a Postgres-migration skill whose description says to use it for anything touching databases, queries, models, or persistence (bad: fires on any DB work) versus one scoped to adding/changing a migration or reviewing its rollout (good).
- Rule 2 — progressive disclosure. Reading a skill costs context, moves the agent closer to compaction, and adds possibly irrelevant guidance. For multi-workflow skills, make the root document a minimal router to supporting docs and scripts.
- Rule 3 — many skills were written as elaborate itineraries/recipes. Models now handle nuance and ambiguity, so over-specific guidance can hurt where it once helped.
- Repository skills are also read by other contributors' agents, possibly on other models. Guidance that helps Sol or Luna may over-constrain GPT-6 Astra; consider which models will read the instructions.

## Up-to-date AGENTS.md

- `AGENTS.md` applies whenever the model works in the repo, so re-check each instruction often.
- Forcing a stack of docs or a full repo map before every edit is excessive (example: a typo fix). Astra can decide what to read.
- Illustration: bad = read `architecture.md`, `database.md`, `deployment.md` before every edit; good = point to each doc for its context (service boundaries, schema changes, deployment prep). Contextual pointers still help; keep docs current.
- Earlier models needed encouragement to test and check work; Astra does it unprompted, so such instructions cause unnecessary testing.
- Astra is thorough but can be tentative about how far to take a task. Use `AGENTS.md` to pre-authorize a known-safe workflow. The example describes a local suite whose fixtures are throwaway and cannot reach production, and grants standing permission to execute it, repair breakages introduced by the change, and re-execute the affected cases with no per-step approval.

## Decision boundaries

- If an earlier model acted without permission, you may have added strong "ask first" language. The author says Astra, as OpenAI's most aligned model, has better judgment and will not do things unless it knows they are safe.
- Boundary language written to restrain earlier models may be taken too seriously by Astra, which may stop where you would be happy for it to continue. Update that language when switching.

## Persistence

- Compared with GPT-5.6 Sol (which continues for long stretches), Astra can feel more tentative about when to stop; it may return after a first implementation with work left.
- Fix: define completion before starting. If the task includes running the implementation, inspecting results, and fixing failures, say so in the request.
- A requirement to stop for review after the first implementation pulls the model toward an earlier stop; check whether that review point is really needed.
- To get exploration beyond a first pass, state what to explore and where to stop.
- Closing suggestion: ask GPT-6 Astra itself to audit your skills/instructions against the article's points rather than reviewing everything manually.
