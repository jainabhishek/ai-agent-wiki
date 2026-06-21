---
title: Agent Instructions
type: concept
created: 2026-06-21
updated: 2026-06-21
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

## Automate instruction-writing

Advanced reasoning models can convert help-center docs into numbered, unambiguous
agent instructions — OpenAI gives a sample meta-prompt that turns a policy
document into an instruction list. (see [[openai-practical-guide-to-building-agents]])

## Relation to Anthropic

[[anthropic]] folds much of this into [[tool-design]] and transparency: write for
the model as you would for a new teammate, with examples and explicit boundaries.
The shared principle: **ambiguity is the enemy.** See [[agent-design-principles]].

## Related concepts

- [[agent-core-components]], [[tool-design]], [[guardrails]],
  [[agent-design-principles]]

## Key entities

- [[openai]]

## Appears in

- [[openai-practical-guide-to-building-agents]]

## Contradictions / open questions

- _None recorded._
