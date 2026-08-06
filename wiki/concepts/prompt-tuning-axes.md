---
title: Prompt Tuning Axes
type: concept
created: 2026-08-06
updated: 2026-08-06
tags: [prompting, migration, model-specific, checklist]
---

# Prompt Tuning Axes

> The knobs you re-tune when moving a prompt to a new model. This page holds the
> **axes**, which are stable across generations. It deliberately holds **no
> values** — those live on the dated, model-scoped source pages, because they
> expire.

## Why this page has no settings in it

Prompting guidance is a per-model contract, not a body of shared theory. A prompt
is written against one model's behavior, so "what both labs recommend" is not
actionable when you sit down to write one. What *is* portable across models is the
list of behaviors that tend to need tuning at all. That list barely moves between
generations; only the settings do.

This is the prompt-layer instance of the pruning principle in
[[agent-design-principles]] (#6, "ask what you can stop doing") and
[[agent-harness]]: scaffolding built for an older model becomes dead weight, and
sometimes worse than dead weight.

## The axes

**1. Verbosity — and it splits in two.** Conversational response length and the
length of written artifacts the model saves to disk are separate behaviors that
need separate instructions. (see [[anthropic-prompting-claude-opus-5]])

**2. Reasoning depth.** Effort level, whether thinking is on, and how thinking
interacts with the output budget. Two recurring traps: effort controls how much a
model *thinks*, not how much it *says*, so it is not a verbosity lever; and a
token budget that caps thinking plus response together can truncate the answer.
(see [[anthropic-prompting-claude-opus-5]],
[[anthropic-prompting-claude-sonnet-5]], [[openai-prompt-guidance-gpt-5-6]])

**3. Tool-use triggering and routing.** Whether the model reaches for tools
readily or needs a nudge, how thinking state changes that, and which tools are
even exposed. (see [[anthropic-prompting-claude-sonnet-5]],
[[openai-prompt-guidance-gpt-5-6]], [[tool-design]])

**4. Instruction literalness and scope.** Whether the model generalizes an
instruction beyond its stated target or applies it exactly as written. This axis
silently breaks prompts in both directions: a prompt relying on generalization
under-applies, and a filtering instruction ("only report high-severity issues") is
obeyed more faithfully than intended. (see
[[anthropic-prompting-claude-sonnet-5]], [[anthropic-prompting-claude-opus-5]])

**5. Delegation.** How readily the model spawns subagents, and whether the payoff
justifies the multiplied cost on small tasks. (see
[[anthropic-prompting-claude-opus-5]], [[anthropic-prompting-claude-fable-5]],
[[agent-orchestration]])

**6. Verification and self-correction.** How much checking the model does
unprompted — the axis most likely to need *removal* rather than addition, since
explicit verification instructions compound with native behavior. (see
[[anthropic-prompting-claude-opus-5]])

**7. User-facing narration.** Progress updates during agentic work, and the
readability of the final summary for a reader who saw none of the working thread.
(see [[anthropic-prompting-claude-fable-5]],
[[anthropic-prompting-claude-sonnet-5]])

**8. Autonomy boundaries and stopping conditions.** Which actions proceed without
asking, which require confirmation, and when the model should end its turn. (see
[[openai-prompt-guidance-gpt-5-6]], [[anthropic-prompting-claude-fable-5]],
[[guardrails]])

**9. Long-run state.** Memory across runs, grounding progress claims in actual
tool results, and how the harness's own signals (such as a visible remaining-token
countdown) change model behavior. Only relevant once runs get long enough to have
a middle. (see [[anthropic-prompting-claude-fable-5]],
[[context-engineering]], [[agent-harness]])

## The meta-axis: subtraction

Across every current model page, the most common instruction is to *delete*
something rather than add it — verification steps, forced status summaries,
exhaustive rule enumeration, over-thorough context gathering, obsolete tools. The
strongest form of the claim is that legacy prompt scaffolding does not merely
waste tokens but degrades output quality. Treat a model migration as a deletion
pass first and an addition pass second.

## What does not port across generations

- **Effort-level names.** The same label can mean materially different
  intelligence on a new model; benchmark by observed behavior, not by name.
- **Token budgets.** Tokenizer changes shift how much text fits in the same
  number of tokens.
- **Sampling parameters.** Levers available on one generation may be rejected
  outright on the next, forcing behavior into the prompt.
- **Prompts and skills tuned for an older model.** These are the first suspects
  when a new model appears to regress.

## How to migrate

Change one thing at a time and re-test between changes, so a behavior shift can be
attributed to the model, the reasoning setting, the prompt, the tool set, or the
runtime. Anything else confounds the result. (see
[[openai-prompt-guidance-gpt-5-6]], [[agent-evals]])

## Related concepts

- [[agent-instructions]], [[agent-design-principles]], [[agent-harness]],
  [[context-engineering]], [[agent-evals]], [[tool-design]],
  [[agent-orchestration]], [[agent-skills]], [[guardrails]]

## Key entities

- [[anthropic]], [[openai]], [[claude]]

## Appears in

- [[anthropic-prompting-claude-opus-5]]
- [[anthropic-prompting-claude-sonnet-5]]
- [[anthropic-prompting-claude-fable-5]]
- [[openai-prompt-guidance-gpt-5-6]]

## Contradictions / open questions

- Model-scoped pages carry `models:` and `as_of:` frontmatter. When a model leaves
  its vendor's current-models list, the pages scoped to it are stale by
  construction and should be re-checked or retired rather than silently trusted.
