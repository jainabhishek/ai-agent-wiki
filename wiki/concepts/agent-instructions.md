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
  [[context-engineering]], [[agent-skills]], [[agent-steering]]

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
  task types still benefit from step-level instructions.
