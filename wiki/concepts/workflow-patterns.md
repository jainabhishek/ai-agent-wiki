---
title: Workflow Patterns
type: concept
created: 2026-06-21
updated: 2026-10-12
tags: [workflows, patterns, anthropic, architecture]
---

# Workflow Patterns

> [[anthropic]]'s five composable building blocks for agentic systems. Reach for
> these before a full agent — most needs are met by one or a combination. (see
> [[anthropic-building-effective-agents]])

## The five patterns

1. **Prompt chaining** — decompose into a fixed sequence of steps; each LLM call
   processes the prior output. Add programmatic **gates** between steps to
   validate progress. Best when a task cleanly decomposes; trades latency for
   accuracy.

2. **Routing** — classify the input and direct it to a specialized follow-up.
   Enables separation of concerns and prompts optimized per category. Best with
   distinct, accurately classifiable categories.
   Production examples:
   - Rocket Money reports a cheap classifier that routes each request to a
     single-responsibility subagent, and one formatter subagent that writes
     every reply. Repeated actions run as ordinary code; an agent steps in only
     when that code breaks, repairs it, and turns the fix back into code. (see
     [[claude-customer-rocket-money]])
   - Anthropic's CI/CD on-call agent keeps alert rules deterministic. The model
     reads each alert against written criteria and decides whether to page now
     or log to `lessons.md`. (see [[anthropic-ai-ci-cd-on-call]])
   - A proactive loop routes routine work to small models and judgment calls to
     the most capable model. (see [[anthropic-getting-started-with-loops]])
   Model-tier routing across a multi-agent system is on [[agent-orchestration]].

3. **Parallelization** — run work concurrently in two modes:
   - *Sectioning* — split a task into independent subtasks run in parallel.
   - *Voting* — run the same task multiple times for diverse outputs / consensus.
   Good for speed or when multiple perspectives raise confidence.
   A coarse-grained form: parallel isolated cloud sessions, one VM and branch
   per task, merged afterwards. Isolated sessions do not know about each other,
   so split work along file boundaries, merge in a sensible order, and expect
   duplicate problem reports. (see [[anthropic-claude-code-in-the-cloud]])

4. **Orchestrator-workers** — a central LLM dynamically breaks a task into
   subtasks, delegates to worker LLMs, and synthesizes results. Preferred over
   parallelization when subtasks **can't be predicted in advance**. This is the
   workflow analogue of OpenAI's **manager pattern** (see [[agent-orchestration]]).
   Cursor's coding case study adds two constraints: the orchestrator should own
   shared design decisions, and delegated leaves should not independently decide
   the same question. Because workers carry most execution volume, routing and
   decomposition determine total cost. (see
   [[cursor-agent-swarm-model-economics]], [[multi-agent-economics]])

5. **Evaluator-optimizer** — one LLM generates, another evaluates and gives
   feedback in a loop. Best with clear evaluation criteria and where iterative
   refinement measurably helps. Analogous to Anthropic's evaluator–optimizer and
   OpenAI's guardrail/eval loops.
   **Generator-verifier** is the name that Anthropic's 2026 coordination-patterns
   article uses for this pattern. The generator drafts; the verifier accepts or
   rejects against explicit criteria and returns feedback; the loop repeats until
   acceptance or an iteration cap. It has two failure modes: a vague verifier
   rubber-stamps, and the loop oscillates. Mitigate both with an iteration cap
   plus a fallback: escalate to a human, or return the best attempt with caveats.
   (see [[anthropic-multi-agent-coordination-patterns]]) Verifier isolation and
   the early victory problem are on [[agent-orchestration]].
   **Sprint contract:** in Anthropic's planner / generator / evaluator harness
   for multi-hour app builds, the generator and evaluator agree before each
   sprint on what "done" means and how it will be tested, and communicate
   through files. The evaluator fails the sprint if any criterion is under its
   hard threshold. A separate skeptical evaluator was more tractable than a
   self-critical generator. With a later model, sprints were dropped and the
   evaluator moved to a single end pass — the contract is scaffolding to remove
   when the model no longer needs it. (see
   [[anthropic-eng-harness-design-long-running-apps]], [[agent-harness]])

## Dynamic-workflow patterns (Claude Code)

[[anthropic-harness-for-every-task]] names six composable patterns that
[[claude-code]] uses when it writes a task-specific multi-agent harness at run
time. The post lists them by name only; the descriptions and the mapping to
the five patterns below are this wiki's reading, not the post's:

| Dynamic-workflow pattern | What it does | Relation to the five |
|---|---|---|
| **Classify-and-act** | a classifier agent sorts inputs, then a handler acts per class (also used for model routing) | Routing |
| **Fan-out-and-synthesize** | one subagent per unit or claim, results merged | Parallelization (sectioning) when units are known; orchestrator-workers when the orchestrator decides them |
| **Adversarial verification** | a separate agent checks work against a rubric | Evaluator half of evaluator-optimizer, run by a distinct agent to counter self-preferential bias |
| **Generate-and-filter** | produce many candidates, keep those that pass a check | Parallelization (voting) plus an evaluator as a filter |
| **Tournament** | N approaches judged pairwise | Voting with pairwise judging instead of consensus |
| **Loop until done** | repeat until an explicit stop condition holds | Evaluator-optimizer loop or a gated chain, with a hard completion check |

The post motivates splitting work across focused subagents with three failures
of a single plan-and-execute context: agentic laziness (stopping early), self-
preferential bias, and goal drift after compaction. It also composes a
**quarantine** chain: read-only reader agents summarize untrusted input into
structured output, and a separate privileged actor acts only on the summaries
(see [[guardrails]]). Costs are higher, so these suit complex, high-value tasks
(see [[multi-agent-economics]]).

Other sources show the same dynamic-workflow patterns in use:
- **Adversarial verification:** a security verifier in a fresh container,
  prompted to assume each finding is a false positive (see
  [[anthropic-llms-secure-source-code]]); several narrow reviewer agents per PR,
  one concern each (see [[anthropic-securing-ai-native-sdlc]]).
- **Generate-and-filter / tournament:** an hourly triage loop that gets three
  parallel worktree solutions per fix and an adversarial judge (see
  [[anthropic-getting-started-with-loops]]); best-of-N candidates in Codex,
  where you pick one or combine parts (see [[openai-how-openai-uses-codex]]).
- **Loop until done:** a goal loop that stops on a deterministic criterion or a
  turn cap, for example a score threshold with a retry limit (see
  [[anthropic-getting-started-with-loops]]).

## Skill-level patterns

[[anthropic-complete-guide-building-skills]] (2026-01-29) names five patterns for
skills that work with MCP servers, and frames the choice as problem-first or
tool-first. The mapping in the third column is this wiki's reading, not the
guide's. So is the observation that these patterns run as instructions inside
one agent, not as separate LLM calls:

| Skill pattern | What it does | Relation to the five |
|---|---|---|
| **Sequential workflow orchestration** | fixed step order, validation between steps, rollback on failure | Prompt chaining with gates |
| **Multi-MCP coordination** | phases across several MCP servers, with data passed between phases | Prompt chaining across tool boundaries |
| **Iterative refinement** | a validation script checks the output; repeat until a stop criterion holds | Evaluator-optimizer, with a script as the evaluator |
| **Context-aware tool selection** | a decision tree picks the tool, and the agent explains the choice | Routing |
| **Domain-specific intelligence** | a compliance check before the action, and an audit trail after it | A gate before the action |

See [[agent-skills]] and [[model-context-protocol]].

## Composed examples

- **Sequential specialists with refinement loops** — Hexagon runs four
  specialized agents in sequence with refinement loops: prompt chaining plus
  evaluator-optimizer. (see [[openai-one-year-of-responses]])
- **Plan, approve, execute, document** — Codex writes a plan into a Runme
  notebook, waits for human approval, then executes and records decisions; the
  finished notebook is context for the next run. A chain with a human gate.
  (see [[openai-automating-repetitive-work-codex]]) monday.com reports the same
  shape for marketing: a strategist agent structures the brief, a builder agent
  generates the landing page, and a reviewer agent checks brand and legal rules;
  a human then makes one decision, publish or refine. (see
  [[anthropic-monday-agent-first-platform]]) OpenAI's Codex guidance gets a plan
  in Ask mode and feeds it to Code mode, with good tasks sized at about one hour
  of human work or a few hundred lines. (see [[openai-how-openai-uses-codex]])
- **Artifact-handoff SDLC loop** — Anthropic's AI-native SDLC playbook turns the
  development lifecycle into a loop of committed artifacts: `intent.md` →
  `spec.md` → `plan.md` → diff and tests → PR with review findings → incident
  record → a new `intent.md`. Each accepted artifact triggers the next stage, a
  human owner accepts each artifact, and the commit chain is the audit trail.
  This is prompt chaining with human gates, closed into a loop. (see
  [[anthropic-ai-native-sdlc-playbook]])
- **File-chained stages** — LG CNS reports a migration harness that splits work
  into small YAML-defined tasks; each stage writes files that the next stage
  reads. The company kept this design after larger context windows arrived,
  because context taxonomy and output consistency mattered more than raw
  context length. (see [[claude-customer-lg-cns]], [[context-engineering]])
- **Pilot, then fix the workflow** — Anthropic's modernization guide fans a
  custom workflow out to parallel subagent workstreams, proves it end to end on
  a small partition, then scales. When issues surface, fix the workflow or the
  certificate at the source, not each change. (see
  [[anthropic-ai-code-modernization]], [[boundary-contracts]])

## Why it matters

These patterns are the "composable, simple" middle ground that
[[agent-design-principles]] urges you to exhaust before building a true agent
([[agents-vs-workflows]]). They're predictable, debuggable, and cheap.

## Related concepts

- [[agents-vs-workflows]], [[agent-orchestration]], [[agent-design-principles]],
  [[agent-evals]], [[multi-agent-economics]], [[agent-harness]], [[agent-skills]],
  [[model-context-protocol]], [[context-engineering]], [[boundary-contracts]]

## Key entities

- [[anthropic]], [[claude-code]], [[openai]], [[openai-codex]]

## Appears in

- [[anthropic-building-effective-agents]]
- [[cursor-agent-swarm-model-economics]]
- [[anthropic-harness-for-every-task]]
- [[anthropic-eng-harness-design-long-running-apps]]
- [[anthropic-claude-code-in-the-cloud]]
- [[openai-one-year-of-responses]]
- [[openai-automating-repetitive-work-codex]]
- [[anthropic-multi-agent-coordination-patterns]]
- [[anthropic-complete-guide-building-skills]]
- [[anthropic-ai-native-sdlc-playbook]]
- [[anthropic-ai-code-modernization]]
- [[anthropic-ai-ci-cd-on-call]]
- [[anthropic-getting-started-with-loops]]
- [[anthropic-llms-secure-source-code]]
- [[anthropic-securing-ai-native-sdlc]]
- [[anthropic-monday-agent-first-platform]]
- [[claude-customer-rocket-money]]
- [[claude-customer-lg-cns]]
- [[openai-how-openai-uses-codex]]

## Contradictions / open questions

- OpenAI doesn't enumerate these workflow patterns by name but its
  single-agent-loop + prompt-templates advice and manager/handoff patterns cover
  much of the same ground. (see [[agent-orchestration]])
