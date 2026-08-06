---
title: Agent Instructions
type: concept
created: 2026-06-21
updated: 2026-08-06
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

## Automate instruction-writing

Advanced reasoning models can convert help-center docs into numbered, unambiguous
agent instructions — OpenAI gives a sample meta-prompt that turns a policy
document into an instruction list. (see [[openai-practical-guide-to-building-agents]])

## Relation to Anthropic

[[anthropic]] folds much of this into [[tool-design]] and transparency: write for
the model as you would for a new teammate, with examples and explicit boundaries.
The shared principle: **ambiguity is the enemy.** See [[agent-design-principles]].

## Model-specific instruction behavior

This page covers *what to say*. How a specific model interprets what you said —
literalism, scope generalization, verbosity defaults, how much verification it
performs unprompted — varies by model and is filed per-model rather than
generalized. See [[prompt-tuning-axes]] for the axes and the model-scoped source
pages for current values.

## Related concepts

- [[agent-core-components]], [[tool-design]], [[guardrails]],
  [[agent-design-principles]], [[agent-orchestration]], [[prompt-tuning-axes]]

## Key entities

- [[openai]]

## Appears in

- [[openai-practical-guide-to-building-agents]]
- [[cursor-agent-swarm-model-economics]]

## Contradictions / open questions

- _None recorded._
