---
title: Agent Instructions
type: concept
created: 2026-06-21
updated: 2026-10-12
tags: [instructions, prompting, best-practices]
---

# Agent Instructions

> [[openai]]: "High-quality instructions are essential for any LLM-powered app,
> but especially critical for agents." Clear instructions reduce ambiguity and
> cut errors. (see [[openai-practical-guide-to-building-agents]])

## Best practices

- **Use existing documents.** Build routines from existing SOPs, support scripts,
  and policy docs (e.g., one routine per knowledge-base article).
- **Prompt agents to break down tasks.** Decompose dense resources into smaller,
  clearer steps to minimize ambiguity.
- **Define clear actions.** Every step should map to a specific action or output
  (ask for the order number, call an API, send a specific message).
- **Capture edge cases.** Anticipate incomplete information and unexpected
  questions; include conditional branches for handling them.
- **Make delegation packets complete.** Give each worker an objective, owned
  scope, settled inputs, output format, acceptance criteria, validation, and stop
  conditions. Require planners to decide shared architecture once rather than
  delegating the same decision to multiple workers. (see
  [[cursor-agent-swarm-model-economics]], [[agent-orchestration]])

## Instruction layers and precedence

A coding agent reads instructions from several layers at once: the system
prompt, a repo file (`CLAUDE.md` / `AGENTS.md`), skills, and the user's task
prompt. Both vendors now give architecture guidance for these layers.
- **Layers conflict; audit them.** Anthropic found the layers issuing conflicting
  instructions in one request, which costs the model reasoning to reconcile, and
  recommends auditing for over-constraint and conflict (see
  [[anthropic-new-rules-context-engineering-claude-5]]). OpenAI recommends
  auditing every skill and file the model can access (see
  [[openai-prompting-gpt-6-astra]]). See also [[context-engineering]].
- **Make precedence explicit.** OpenAI's prompts state that user instructions
  rank above skill instructions (see [[openai-prompting-gpt-6-astra]]).
- **One role per layer.** System prompt = product context, where harness builders
  should invest most; `CLAUDE.md` = brief purpose plus codebase gotchas, nothing
  the agent can discover itself; skills = lightweight guides split into files,
  tightly constrained only where it matters (see
  [[anthropic-new-rules-context-engineering-claude-5]]). Keep `AGENTS.md` small,
  highest-value rules first (see [[openai-skills-for-oss-maintenance]]).
- **Pointers, not blanket rules.** Replace "read these docs before every edit"
  with a pointer to each doc for the situation where it applies (see
  [[openai-rethinking-skills-prompts-gpt-6-astra]]). Replace blanket worst-case
  rules with an instruction to follow local context, e.g. match the surrounding
  code's comment density, naming, and idiom (see
  [[anthropic-new-rules-context-engineering-claude-5]]).
- **Mandatory triggers as short if/then rules.** `AGENTS.md` can make a skill
  mandatory ("when runtime code changes, run the verification skill; do not mark
  work complete until it passes"); the skill, not the repo file, defines
  "verified" (see [[openai-skills-for-oss-maintenance]], [[agent-skills]]).
- **Pre-authorize known-safe workflows** in `AGENTS.md`, e.g. a local test suite
  with disposable fixtures and no production access (see
  [[openai-rethinking-skills-prompts-gpt-6-astra]], [[guardrails]]).
- **`AGENTS.md` as a table of contents.** OpenAI's harness-engineering team
  reports that one large `AGENTS.md` failed: it crowded context, made everything
  "important", rotted, and resisted mechanical checks. A ~100-line `AGENTS.md`
  that points into a structured `docs/` directory, the system of record, replaced
  it; linters and CI keep those docs current (see
  [[openai-harness-engineering]], [[context-engineering]]).
- **Directory-scoped rules.** Codex reads every `AGENTS.md` from the repo root
  down to the working directory into a fixed prelude (see
  [[openai-unrolling-codex-agent-loop]]). Codex Code Review applies root rules
  repo-wide and nested rules only to the changed files they cover (see
  [[openai-codex-code-review-rules]]).
- **Write each rule as an invariant plus a safe path.** Name the risk and the
  allowed alternative, e.g. "keep the name or add a backward-compatible event".
  Include only consequential, non-obvious rules: if removing a rule would not
  change the output, delete it. Keep judgment in rules and mechanics in CI and
  linters. OpenAI reports that rule-guided review recovered 98% of required
  custom findings vs 58.3% for the baseline on its eval suite (see
  [[openai-codex-code-review-rules]], [[agent-evals]]).
- **Record what the code does not reveal.** `AGENTS.md` holds naming
  conventions, business logic, known quirks, and dependencies the code does not
  show (see [[openai-how-openai-uses-codex]]). Skyscanner reports putting
  post-edit checks there (format, then lint) (see
  [[openai-skyscanner-codex-jetbrains-mcp]]).

## Task prompts: goals, done-criteria, and output contracts

- **Goal and context over prescriptive procedure (observed reports).** Each
  report is tied to its own deployment and model generation:
  - Anthropic's buying agent: a one-sentence goal outperformed a flowchart of
    qualification rules; shorter prompts plus domain knowledge worked best
    (self-reported, Sep 2026; see [[anthropic-sales-inbound-managed-agents]]).
  - Anthropic's vulnerability-discovery guidance: prescriptive checklists
    reduced novel findings. Give the goal and context, leave the method to the
    model, define ordered output fields, and include an escape hatch for weak
    findings (May 2026; see [[anthropic-llms-secure-source-code]]).
  - OpenAI's in-house data agent: goal-level guidance beat prescriptive
    prompting (self-reported, Jan 2026; see [[openai-in-house-data-agent]]).
- **Specificity has two failure modes.** Anthropic's field guide splits a problem
  into known knowns, known unknowns, unknown knowns (criteria you recognize only
  on sight), and unknown unknowns. Too-specific instructions make the model
  follow a path even when a pivot is better; too-vague instructions make it fill
  gaps with generic best practice. The fix is to state your starting point and
  use the model to find unknowns early, through a blind-spot pass, interviews
  (one question at a time), and prototypes (see
  [[anthropic-fable-field-guide-unknowns]]). The same "right altitude" idea:
  neither exact values nor vague taste words (see
  [[anthropic-improving-frontend-design-through-skills]]).
- **Give a verifiable done-criterion.** "Implement the plan in this file" is a
  weak goal; a strong goal names a test standard, e.g. keep the public API and
  treat the original unit tests as the success check (see
  [[openai-codex-maxxing-long-running-work]], [[agent-evals]]).
- **Prompt like an issue.** Give file paths, component names, diffs, doc
  snippets, and "do it the way module X does" (see
  [[openai-how-openai-uses-codex]]).
- **Output contracts and handoffs.** OpenAI's GPT-6 guide asks for a clear
  assignment (result, audience, context and constraints, what counts as done)
  and an output contract: which decisions the model owns, when it asks, and the
  shape of a useful response. Its example handoff covers what changed, what was
  checked, and what still needs attention. Decision boundaries replace blanket
  "always ask" rules (see [[openai-practical-guide-building-with-gpt-6]]; the
  page is scoped to GPT-6 models).
- **Define the role before the agent.** Asana reports defining each AI
  teammate's purpose, instructions, and owned jobs before building it (see
  [[anthropic-asana-coachable-agents]]).
- **Narrow task instructions limit injection damage.** OpenAI advises users to
  give specific, scoped instructions instead of "take whatever action is
  needed" (see [[openai-understanding-prompt-injections]],
  [[openai-hardening-atlas-prompt-injection]], [[prompt-injection]]). This is
  about the scope of authority granted, not about prescribing the method.

## Prune instructions at each model change

Two vendors independently advise removing instructions written to compensate for
weaker models. Anthropic removed over 80% of [[claude-code]]'s system prompt for
its Claude 5 generation with no measurable loss on its coding evals (see
[[anthropic-new-rules-context-engineering-claude-5]], Jul 2026). OpenAI says
instructions accumulated for earlier models now hurt its current coding model,
and recommends auditing skills, `AGENTS.md`, and task prompts (see
[[openai-rethinking-skills-prompts-gpt-6-astra]], Sep 2026). Anthropic's
migration method: remove the previous model's workarounds first, then re-run
evals (see [[anthropic-building-with-sonnet-5-5]]). The convergence is about
architecture — instructions are written against a model, so the instruction
set is versioned with it and re-audited on upgrade. Which specific wording to
remove is per-model and lives on the model-scoped source pages, not here.

## Automate instruction-writing

Advanced reasoning models can convert help-center docs into numbered, unambiguous
agent instructions — OpenAI gives a sample meta-prompt that turns a policy
document into an instruction list. (see [[openai-practical-guide-to-building-agents]])

## Relation to Anthropic

[[anthropic]] folds much of this into [[tool-design]] and transparency: write for
the model as you would for a new teammate, with examples and explicit boundaries.
The shared principle: **ambiguity is the enemy.** See [[agent-design-principles]].

## Model-specific instruction behavior

This page covers *what to say* and *where to put it*. How a specific model
interprets what you said — literalism, scope generalization, verbosity defaults,
how much verification it performs unprompted — varies by model and is filed
per-model rather than generalized. See [[prompt-tuning-axes]] for the axes and the
model-scoped source pages for current values.

## Related concepts

- [[agent-core-components]], [[tool-design]], [[guardrails]],
  [[agent-design-principles]], [[agent-orchestration]], [[prompt-tuning-axes]],
  [[context-engineering]], [[agent-skills]], [[agent-steering]],
  [[agent-evals]], [[prompt-injection]]

## Key entities

- [[openai]], [[openai-codex]], [[anthropic]], [[claude-code]]

## Appears in

- [[openai-practical-guide-to-building-agents]]
- [[cursor-agent-swarm-model-economics]]
- [[anthropic-new-rules-context-engineering-claude-5]]
- [[openai-rethinking-skills-prompts-gpt-6-astra]]
- [[openai-prompting-gpt-6-astra]]
- [[openai-skills-for-oss-maintenance]]
- [[anthropic-building-with-sonnet-5-5]]
- [[openai-harness-engineering]]
- [[openai-unrolling-codex-agent-loop]]
- [[openai-codex-code-review-rules]]
- [[openai-how-openai-uses-codex]]
- [[openai-skyscanner-codex-jetbrains-mcp]]
- [[anthropic-sales-inbound-managed-agents]]
- [[anthropic-llms-secure-source-code]]
- [[openai-in-house-data-agent]]
- [[anthropic-fable-field-guide-unknowns]]
- [[anthropic-improving-frontend-design-through-skills]]
- [[openai-codex-maxxing-long-running-work]]
- [[openai-practical-guide-building-with-gpt-6]]
- [[anthropic-asana-coachable-agents]]
- [[openai-understanding-prompt-injections]]
- [[openai-hardening-atlas-prompt-injection]]

## Contradictions / open questions

- **Detailed steps and edge-case branches vs. judgement.**
  [[openai-practical-guide-to-building-agents]] (2025) advises breaking tasks into
  explicit steps, mapping every step to an action, and adding conditional
  branches for edge cases. [[anthropic-new-rules-context-engineering-claude-5]]
  (2026-07-24) recommends deleting blanket worst-case rules in favour of the
  model's judgement, and [[openai-rethinking-skills-prompts-gpt-6-astra]]
  (2026-09-11) recommends replacing step-by-step skill "recipes" with less
  specific guidance. The later sources tie the change to newer models, so this
  reads as generation-dependent, not a reversal; open which current models and
  task types still benefit from step-level instructions. Later reports add to
  the judgement side: a one-sentence goal beat a qualification flowchart
  ([[anthropic-sales-inbound-managed-agents]], 2026-09-30), prescriptive
  checklists cut novel security findings
  ([[anthropic-llms-secure-source-code]], 2026-05-27), and goal-level guidance
  beat prescriptive prompting ([[openai-in-house-data-agent]], 2026-01-29).
  None of these tests a customer-service routine of the kind the 2025 guide
  describes, so the scope question stays open.
