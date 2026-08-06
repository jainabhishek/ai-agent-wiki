---
title: "OpenAI: Model Guidance — GPT-5.6"
type: source
created: 2026-08-06
updated: 2026-08-06
author: OpenAI
date: accessed 2026-08-06
source_url: https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6
models: [gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna]
as_of: 2026-08-06
tags: [prompting, model-specific, openai, gpt-5-6]
---

# OpenAI: Model Guidance — GPT-5.6

> OpenAI's model-specific prompting guidance for the GPT-5.6 series — outcome-first
> prompts, aggressive scaffolding removal, and a staged migration workflow.

## Summary

The GPT-5.6 series comprises `gpt-5.6-sol` (flagship, also aliased `gpt-5.6`),
`gpt-5.6-terra` (balanced), and `gpt-5.6-luna` (cost-optimized). OpenAI describes
Sol/Terra/Luna as "durable capability tiers that can advance on their own cadence,"
so the tier names are intended to outlive the 5.6 generation number.

The guidance is built on two claims: prompts should **define destinations rather
than prescribe steps**, and prompt stacks carried over from earlier generations are
now actively counterproductive. See [[prompt-tuning-axes]].

## Key points

### Outcome-first prompt design
State the goal, relevant context, constraints, required evidence, success
criteria, and output format — then let the model "choose an efficient path."
OpenAI notes GPT-5.6 "can better infer the user's underlying goal from context, so
you often don't need to prescribe every step," while still requiring domain
context, hard constraints, approval boundaries, and success criteria to be given
explicitly.

### Lean prompts measurably win
OpenAI's headline data point: leaner configurations improved evaluation scores by
roughly **10–15% while reducing total tokens by 41–66% and cost by 33–67%**.

What to remove: repeated rule statements, style instructions that don't alter
behavior, examples that don't change outcomes, process instructions for behaviors
that are already reliable, and irrelevant tools.

What to preserve: user-visible outcomes, success criteria and stopping conditions,
safety/business/evidence constraints, context-dependent tool-routing rules, and
required output shape and validation.

### Stopping conditions
Explicit stopping guidance is one of the categories to keep, with the caveat that
loop minimization must not "outrank correctness, required evidence, calculations,
or required citations."

### Suggested prompt structure
Role → Personality → Goal → Success criteria → Constraints → Tools → Output →
Stop rules.

### Verbosity
GPT-5.6 defaults to more concise output than GPT-5.5. The `text.verbosity`
parameter (low/medium/high) is the recommended lever for consistent control, with
prompt-level instructions reserved for task-specific overrides. Personality (tone,
warmth, formality) and collaboration style (when to ask, assume, or explain
tradeoffs) should be defined separately and concisely.

### Autonomy and approval boundaries
Distinguish safe local actions (reading files, editing code, running tests) from
actions requiring confirmation (external writes, destructive operations,
purchases).

### Tool routing
Expose only task-relevant tools. For each, describe what it does, when to use it,
key return fields, and error behavior. State prerequisite-retrieval dependencies
explicitly when correctness depends on them.

### Programmatic tool calling
Recommended for bounded workflows involving filtering, joining, sorting,
deduplication, and aggregation across many similar records. Direct tool calls
remain preferable when intermediate outputs stay small or semantic judgment is
needed.

### Citation and grounding
"For ordinary Q&A, start with one broad search using short, discriminative
keywords." Additional retrieval only when required facts are missing, exhaustive
coverage is requested, or claims would otherwise lack support. Cite only retrieved
sources, and label inference separately from directly supported facts.

### Reasoning effort
Levels are none / low / medium / high / xhigh / max. Migration guidance is to
**preserve the existing effort setting** before adjusting anything else; `low` for
latency-sensitive work where quality holds, `medium` as a balanced starting point,
`high`/`xhigh` only when evals show meaningful gains, `max` for the hardest
quality-first workloads. A `pro` reasoning mode (`reasoning.mode: "pro"`) performs
additional model work for a single final answer when quality outranks latency and
token usage.

### Migration workflow
An explicitly staged procedure: switch model preserving reasoning effort → run
representative evals on the current prompt → remove scaffolding, repeated
instructions, and obsolete tools → add targeted fixes only for measured
regressions → re-test after each change. The stated rationale: "Do not rewrite a
working prompt stack all at once. Otherwise you cannot tell whether a behavior
change came from the model, reasoning setting, prompt, tool set, or runtime."

## Notable claims & data

- Leaner prompts: ~10–15% eval improvement, 41–66% fewer tokens, 33–67% lower cost.
- Tier names (Sol/Terra/Luna) are designed as durable, generation-independent
  identifiers.
- One-change-at-a-time migration is framed as an attribution requirement, not a
  style preference — the same logic as controlled evaluation in [[agent-evals]].

## Entities

[[openai]]

## Concepts

[[prompt-tuning-axes]], [[agent-instructions]], [[tool-design]],
[[agent-evals]], [[context-engineering]], [[guardrails]]

## Connections

The lean-prompt finding is OpenAI's independent measurement of the same effect
Anthropic reports as scaffolding removal in
[[anthropic-prompting-claude-fable-5]] and [[anthropic-prompting-claude-opus-5]] —
recorded here as a per-model contract, not as a cross-vendor generalization.
Relates to [[agent-design-principles]] principle 6 (prune scaffolding as the model
improves).

## Contradictions / open questions

- The page's substantive guidance is written for **Sol**; it does not give separate
  prompting guidance for **Terra** or **Luna**. Whether the guidance transfers
  unchanged to the lower tiers is unverified — a gap to close if OpenAI publishes
  tier-specific pages.
