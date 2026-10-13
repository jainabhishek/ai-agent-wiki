# How CodeRabbit used Claude to build an agent orchestration system — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/how-coderabbit-used-claude-to-build-an-agent-orchestration-system
> Publisher: Anthropic (claude.com articles) · Date: 2026-05-27
> Captured: 2026-10-12 via WebFetch (condensed).

No author byline. People quoted: David Loker (VP of AI, CodeRabbit) and Harjot
Gill (CEO and founder). The page also shows dates of 2026-10-05 to 2026-10-08;
those belong to the "Related articles" list, not to this article.

## Intro (no heading)

- CodeRabbit is an AI code review platform, founded in 2023.
- It built a layer that sits between a coding request and the coding agent. The
  layer produces a structured plan that people review before any code exists.
- Stack: Claude Platform and Claude Code.
- Scale (self-reported): about 2 million PRs reviewed per week, for 15,000+
  customers.
- Observation: AI-generated code often compiles and passes tests but misses what
  the developer intended.

## Addressing the internal knowledge gap in AI coding

- In a study of AI-generated PRs, the most common failure was code that worked
  technically but did not solve the intended problem.
- Experienced developers assume shared context and leave obvious requirements
  unstated. The agent then fills the gaps with plausible guesses.
- Example from Loker: a side-project memory system had no login flow, because
  he never said how users would sign in.
- In AI workflows, a gap found late is expensive.

## An orchestration layer that runs before AI coding solutions

- A planning system runs before code generation. Several Claude models analyze
  requirements, surface assumptions, and produce a structured execution plan.
- It does not replace Claude Code Plan Mode. It works at a higher level and
  gives Claude Code a narrower, more explicit direction.
- Output: a collaborative product requirements document (PRD) that stakeholders
  validate before implementation.
- Claude Code then turns the PRD into a fine-grained implementation plan. The
  plan is also a record of decisions: it helps prevent rework, verify intent,
  and onboard people.

## Routing across the Claude model family

- Opus: runs the orchestration loop and high-level problem understanding.
- Sonnet: sequences the output into structured planning steps.
- Haiku: narrow tasks, for example context distillation and targeted tool use.
- Model choice comes from eval results, balancing cost and latency, not from
  assumptions. (No model versions are named.)

## Building an eval harness for plan quality

- CodeRabbit had mature evals for code review but none for planning.
- Start: hand-tuned examples and manual inspection. Then: a library of LLM
  judges, each scoring one plan dimension.
- Downstream measures: does the generated code work, does it add extra scope,
  how many tokens it uses.
- A/B runs with and without the planning step isolate the value of the step.
- Plan granularity took iteration. Plans that were too granular went stale as
  code changed. Plans that were too high-level left room for harmful
  assumptions.

## Catching errors before any code gets written

- Many issues that used to appear in code review now get caught in the planning
  layer.
- The plan acts as a team-wide quality gate. The team says strong upfront plans
  give noticeably better downstream code (no figure given).

## Best-practice box (no heading)

Questions to ask before coding: what outcome is the target and how is it
measured; which assumptions are still implicit; which edge cases are easy to
forget; how will output be checked against intent before rollout. Keep a saved,
reusable record of planning artifacts.
