---
title: "OpenAI: Model Guidance — GPT-5.6"
type: source
created: 2026-08-06
updated: 2026-10-12
author: OpenAI
date: accessed 2026-08-06
source_url: https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6
source_path: raw/openai-prompt-guidance-gpt-5-6.md
models: [gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna]
as_of: 2026-08-06
status: legacy
superseded_by: [openai-prompting-gpt-6-astra]
tags: [prompting, model-specific, openai, gpt-5-6]
---

# OpenAI: Model Guidance — GPT-5.6

> **Legacy (checked 2026-10-12).** OpenAI's models page no longer lists GPT-5.6 Sol, Terra, or Luna; the current lineup is GPT-6 Astra, GPT-6.1 Sol, and GPT-6 Luna. The claims below stay true of the legacy model; for the current model, see [[openai-prompting-gpt-6-astra]].

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

The removal procedure is itself specified: remove **one group** of instructions,
examples, or tools at a time, then rerun the same evals — the same
one-change-at-a-time discipline as the migration workflow below.

### Contradictions cost more than gaps
After trimming, review what remains for conflicting rules: "GPT-5-class models
follow prompt contracts closely, so conflicting rules can create more instability
than missing detail." OpenAI also warns against unnecessary absolute rules —
reserve ALWAYS / NEVER / must / only for true invariants such as safety rules or
required fields, and use decision rules for judgment calls like when to search,
ask, or keep iterating.

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
remain preferable when intermediate outputs stay small, each result may change the
next decision, an action requires approval, citations must be preserved, or
semantic judgment is needed between calls. Multiple, parallel, or dependent calls
alone "do not justify Programmatic Tool Calling."

Generic instructions ("use Programmatic Tool Calling efficiently") are called out
as insufficient — specify the bounded stage, eligible tools, output schema, retry
limit, stop condition, and the handoff back to direct model judgment. A testing
warning worth noting: the `program_output` item and the final assistant `message`
are separate outputs, and a program can return correct records while the message
omits a required field, citation, or caveat. Test both.

### Citation and grounding
"For ordinary Q&A, start with one broad search using short, discriminative
keywords." Additional retrieval only when required facts are missing, exhaustive
coverage is requested, or claims would otherwise lack support. Cite only retrieved
sources, and label inference separately from directly supported facts.

### Long-running workflows and state
Prompt for a short visible preamble before the first tool call, then sparse
outcome-based updates at major phase changes — explicitly *not* narration of
routine tool calls. Compaction should happen after major milestones rather than
every turn, with compacted items treated as opaque state. Persisted reasoning is
useful only while objective and priorities stay stable: "stale reasoning can add
tokens, increase latency, and anchor the model to an outdated approach." Prompt
caching shapes construction too — keep reusable prefixes stable, avoid churn in
large system prompts, and add explicit cache breakpoints only when they improve
measured cache behavior. (Converges with [[agent-design-principles]] #7.)

### Check work before finishing
Give the model tools that can validate output and state which validation matters:
targeted tests for changed behavior, type/lint checks, build checks, or a minimal
smoke test when full validation is too expensive — and if validation cannot be
run, say why and describe the next best check. For visual artifacts, render and
inspect before finalizing.

### Reasoning effort
Levels are none / low / medium / high / xhigh / max. Migration guidance is to
**preserve the existing effort setting** before adjusting anything else; `low` for
latency-sensitive work where quality holds, `medium` as a balanced starting point,
`high`/`xhigh` only when evals show meaningful gains, `max` for the hardest
quality-first workloads. A `pro` reasoning mode (`reasoning.mode: "pro"`) performs
additional model work for a single final answer when quality outranks latency and
token usage.

Notably, raising effort is framed as a *second* resort: "Before increasing
reasoning effort, check whether the prompt is missing a success criterion,
dependency rule, tool-routing rule, or verification loop." Under-performance is
treated as a prompt defect first and a capacity problem second.

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
