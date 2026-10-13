---
title: Prompt Tuning Axes
type: concept
created: 2026-08-06
updated: 2026-10-12
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

Citations below pair each legacy page (2026-08-06 generation) with the current page
for the same model line. The legacy citations stay because the axis was first
observed there; the current pages hold the settings to use now.

## The axes

**1. Verbosity — and it splits in two.** Conversational response length and the
length of written artifacts the model saves to disk are separate behaviors that
need separate instructions. (see [[anthropic-prompting-claude-opus-5]]) Formatting
density and prose style sit on the same axis, and the direction can reverse between
generations: one model over-formats and the next under-formats, so suppression
lines written for the first must be removed for the second. (see
[[anthropic-prompting-claude-fable-5-1]], [[openai-prompting-gpt-6-astra]])

**2. Reasoning depth.** Effort level, whether thinking is on, and how thinking
interacts with the output budget. Two recurring traps: effort controls how much a
model *thinks*, not how much it *says*, so it is not a verbosity lever (a legacy
claim that current guidance disputes; see Contradictions); and a
token budget that caps thinking plus response together can truncate the answer.
(see [[anthropic-prompting-claude-opus-5]],
[[anthropic-prompting-claude-sonnet-5]], [[openai-prompt-guidance-gpt-5-6]],
[[anthropic-prompting-claude-opus-5-5]], [[anthropic-prompting-claude-sonnet-5-5]],
[[anthropic-prompting-claude-haiku-5-5]]) A third trap: prompt lines that ask the
model to think more or less are less reliable than the reasoning setting itself, so
legacy "think carefully" lines are deletion candidates. (see
[[anthropic-prompting-claude-opus-5-5]], [[anthropic-getting-most-out-of-opus-5-5]],
[[anthropic-building-with-sonnet-5-5]]) Two sub-axes recur: whether reasoning still
happens when a structured-output format is requested, and whether the reasoning
setting can change mid-conversation without breaking the prompt cache. (see
[[anthropic-prompting-claude-sonnet-5-5]], [[anthropic-prompting-claude-haiku-5-5]],
[[openai-prompting-gpt-6-astra]], [[context-engineering]]) The cache answer can
differ by access path for the same model, so check it for the platform you
deploy on. (see [[anthropic-what-a-task-costs-opus-5-5]],
[[anthropic-spending-your-effort]])

Three durable findings about what the reasoning setting buys:

- **Treat each effort level as a separate model.** Block reports that it
  benchmarks each use case on every model at every effort level, because effort
  levels behave like different models rather than a linear dial. Anthropic's
  commerce-agent guidance sweeps models and effort levels together against
  quality floors and latency budgets. Benchmark the model × effort grid, not
  the model alone. (see [[anthropic-block-orchestrates-fable]],
  [[anthropic-anatomy-of-commerce-agents]], [[anthropic-choosing-claude-model]])
- **Higher effort fixes missed edge cases, not a wrong approach.** In
  Anthropic's Terminal-Bench analysis, failures from bugs the tests missed fell
  as effort rose, while failures from a wrong reading of the task rose. The
  gain also varies by domain. Before raising effort, give the model a check that
  exercises the change. (see [[anthropic-spending-your-effort]],
  [[anthropic-what-a-task-costs-opus-5-5]])
- **Effort trades user time for autonomy.** With no user in the loop, higher
  effort explores other readings that one clarifying question would settle; a
  detailed spec narrows what effort changes. Effort can be set per phase of the
  work, not once per session. (see [[anthropic-spending-your-effort]],
  [[agent-steering]])

**3. Tool-use triggering and routing.** Whether the model reaches for tools
readily or needs a nudge, how thinking state changes that, and which tools are
even exposed. (see [[anthropic-prompting-claude-sonnet-5]],
[[openai-prompt-guidance-gpt-5-6]], [[tool-design]]) The search instance is the
most visible: whether the model searches for facts that may have changed since
training, and whether a blanket "always search" rule adds searches without adding
correct answers. A second instance is batching: whether the model issues
independent calls together or one per turn. (see
[[anthropic-prompting-claude-sonnet-5-5]], [[anthropic-prompting-claude-haiku-5-5]],
[[anthropic-prompting-claude-fable-5-1]])

**4. Instruction literalness and scope.** Whether the model generalizes an
instruction beyond its stated target or applies it exactly as written. This axis
silently breaks prompts in both directions: a prompt relying on generalization
under-applies, and a filtering instruction ("only report high-severity issues") is
obeyed more faithfully than intended. (see
[[anthropic-prompting-claude-sonnet-5]], [[anthropic-prompting-claude-opus-5]])
Two newer instances. **Scope drift:** the model adds unrequested tests, docs, or
fixes, or quietly narrows or widens the deliverable. (see
[[anthropic-prompting-claude-sonnet-5-5]], [[anthropic-prompting-claude-fable-5-1]])
**Sensitivity to instruction files:** text in skills and `AGENTS.md` can outweigh
the user's request, so the precedence between user and file instructions must be
stated and old files audited. (see [[openai-prompting-gpt-6-astra]],
[[openai-rethinking-skills-prompts-gpt-6-astra]], [[agent-instructions]],
[[agent-skills]])

**5. Delegation.** How readily the model spawns subagents, and whether the payoff
justifies the multiplied cost on small tasks. (see
[[anthropic-prompting-claude-opus-5]], [[anthropic-prompting-claude-fable-5]],
[[agent-orchestration]]) The direction varies by model and by reasoning setting:
one current model may delegate less than desired, another may launch reviewer
subagents on its own at high effort. (see [[openai-prompting-gpt-6-astra]],
[[anthropic-prompting-claude-sonnet-5-5]], [[anthropic-getting-most-out-of-opus-5-5]],
[[anthropic-prompting-claude-fable-5-1]])

**6. Verification and self-correction.** How much checking the model does
unprompted — the axis most likely to need *removal* rather than addition, since
explicit verification instructions compound with native behavior. (see
[[anthropic-prompting-claude-opus-5]]) The current generation shows the axis cuts
both ways: one model over-tests small changes and needs restraint, while others
skip real checks at low effort and need a "run a check that exercises the change"
instruction. The right direction depends on the model *and* the reasoning setting.
(see [[openai-prompting-gpt-6-astra]], [[anthropic-prompting-claude-sonnet-5-5]],
[[anthropic-prompting-claude-haiku-5-5]], [[anthropic-building-with-sonnet-5-5]])

**7. User-facing narration.** Progress updates during agentic work, and the
readability of the final summary for a reader who saw none of the working thread.
(see [[anthropic-prompting-claude-fable-5]],
[[anthropic-prompting-claude-sonnet-5]]) A harness sub-axis now matters: where the
progress notes arrive. When notes come back in a channel the client does not
render, the fix is in the harness (receive and render them), not in the prompt.
(see [[anthropic-prompting-claude-opus-5-5]], [[anthropic-prompting-claude-sonnet-5-5]],
[[anthropic-prompting-claude-fable-5-1]]) For the reader, put what the model needs
from the user first in the final report. (see
[[anthropic-getting-most-out-of-opus-5-5]])

**8. Autonomy boundaries, initiative, and stopping conditions.** Which actions
proceed without asking, which require confirmation, and when the model should end
its turn. (see [[openai-prompt-guidance-gpt-5-6]], [[anthropic-prompting-claude-fable-5]],
[[guardrails]]) Initiative and follow-through is the same axis seen from the
model's default: whether it persists to completion or stops early to ask, offer, or
report. Current pages from both labs document early stops — asking for
clarification, treating "can you…" as a question, ending an unattended turn with a
report, checking in at low effort. (see [[openai-prompting-gpt-6-astra]],
[[anthropic-prompting-claude-opus-5-5]], [[anthropic-prompting-claude-sonnet-5-5]],
[[anthropic-prompting-claude-haiku-5-5]], [[anthropic-prompting-claude-fable-5-1]])
Two durable methods: name the specific unwanted stops and the wanted ones, and
define "done" up front. Strong "ask first" language written for an earlier model is
a common cause of early stops on a newer one. (see
[[anthropic-getting-most-out-of-opus-5-5]],
[[openai-rethinking-skills-prompts-gpt-6-astra]], [[agent-steering]])

**9. Long-run state.** Memory across runs, grounding progress claims in actual
tool results, and how the harness's own signals (such as a visible remaining-token
countdown) change model behavior. Only relevant once runs get long enough to have
a middle. (see [[anthropic-prompting-claude-fable-5]],
[[context-engineering]], [[agent-harness]]) Harness signals cut both ways: an
elapsed-time budget line helped a lead agent pace and parallelize, while a token
countdown after tool results caused injection misreads. Where harness text sits
relative to tool results is part of this axis. (see
[[anthropic-prompting-claude-opus-5-5]], [[anthropic-prompting-claude-sonnet-5-5]],
[[anthropic-prompting-claude-haiku-5-5]]) What a compaction summary must preserve,
and keeping the task list in a file that survives summarization, are the other
current instances. (see [[anthropic-prompting-claude-fable-5-1]],
[[anthropic-getting-most-out-of-opus-5-5]])

## The meta-axis: subtraction

Across every current model page, the most common instruction is to *delete*
something rather than add it — verification steps, forced status summaries,
exhaustive rule enumeration, over-thorough context gathering, obsolete tools. The
strongest form of the claim is that legacy prompt scaffolding does not merely
waste tokens but degrades output quality. Treat a model migration as a deletion
pass first and an addition pass second.

The 2026-10 generation keeps the deletion pass — remove the previous model's
workarounds, suppression lines, and "ask first" language before tuning (see
[[anthropic-building-with-sonnet-5-5]], [[anthropic-prompting-claude-fable-5-1]],
[[openai-rethinking-skills-prompts-gpt-6-astra]], [[openai-practical-guide-building-with-gpt-6]],
[[anthropic-what-a-task-costs-opus-5-5]]) — but adds a second pattern: detect
a specific misbehavior and redirect it, often with a harness change rather than
prompt text. (see [[anthropic-prompting-claude-opus-5-5]])

## What does not port across generations

- **Effort-level names.** The same label can mean materially different
  intelligence on a new model; benchmark by observed behavior, not by name.
  Internal effort values map to named levels differently for each model. (see
  [[anthropic-spending-your-effort]], [[anthropic-what-a-task-costs-opus-5-5]])
- **Effort calibration.** Each generation recalibrates its effort levels and
  defaults, so a sweep from the previous model does not carry over. Re-run the
  effort sweep on every migration. (see [[anthropic-building-with-sonnet-5-5]],
  [[anthropic-prompting-claude-opus-5-5]], [[anthropic-prompting-claude-sonnet-5-5]],
  [[anthropic-prompting-claude-fable-5-1]])
- **Token budgets.** Tokenizer changes shift how much text fits in the same
  number of tokens.
- **Sampling parameters and thinking switches.** Levers available on one
  generation may be rejected outright on the next, forcing behavior into the
  prompt or the reasoning setting. (see [[anthropic-prompting-claude-opus-5-5]],
  [[openai-prompting-gpt-6-astra]])
- **Prompts and skills tuned for an older model.** These are the first suspects
  when a new model appears to regress.
- **The direction of a fix.** An instruction that pushed a behavior one way on the
  previous model can be the cause of the opposite failure on the next (see the
  reversals below).

## How to migrate

Change one thing at a time and re-test between changes, so a behavior shift can be
attributed to the model, the reasoning setting, the prompt, the tool set, or the
runtime. Anything else confounds the result. (see
[[openai-prompt-guidance-gpt-5-6]], [[agent-evals]]) Remove the previous model's
workarounds first, then re-run the evals before adding anything. (see
[[anthropic-building-with-sonnet-5-5]]) Equal quality at lower cost is a valid
migration goal, even on an eval the model already saturates. (see
[[anthropic-automating-eval-design-hillclimbing]])

Production teams report the per-model contract directly. Dust reports a
separate prompt and context strategy for each model behind its model picker.
Cognition reports that moving a part of the workflow to a different model
forces changes to prompts, tool definitions, context management, trajectory
monitoring, and guardrails. n8n reports prompts tailored to one model and
per-node-type prompt tuning. (see [[claude-customer-dust]],
[[claude-customer-cognition]], [[claude-customer-n8n]], [[agent-harness]])

## Related concepts

- [[agent-instructions]], [[agent-design-principles]], [[agent-harness]],
  [[context-engineering]], [[agent-evals]], [[tool-design]],
  [[agent-orchestration]], [[agent-skills]], [[guardrails]], [[agent-steering]]

## Key entities

- [[anthropic]], [[openai]], [[claude]]

## Appears in

- [[anthropic-prompting-claude-opus-5]] (legacy)
- [[anthropic-prompting-claude-sonnet-5]] (legacy)
- [[anthropic-prompting-claude-fable-5]] (legacy)
- [[openai-prompt-guidance-gpt-5-6]] (legacy)
- [[anthropic-prompting-claude-opus-5-5]]
- [[anthropic-prompting-claude-sonnet-5-5]]
- [[anthropic-prompting-claude-haiku-5-5]]
- [[anthropic-prompting-claude-fable-5-1]]
- [[openai-prompting-gpt-6-astra]]
- [[openai-rethinking-skills-prompts-gpt-6-astra]]
- [[anthropic-building-with-sonnet-5-5]]
- [[anthropic-getting-most-out-of-opus-5-5]]
- [[anthropic-automating-eval-design-hillclimbing]]
- [[anthropic-spending-your-effort]]
- [[anthropic-what-a-task-costs-opus-5-5]]
- [[anthropic-block-orchestrates-fable]]
- [[anthropic-anatomy-of-commerce-agents]]
- [[anthropic-choosing-claude-model]]
- [[openai-practical-guide-building-with-gpt-6]]
- [[claude-customer-dust]]
- [[claude-customer-cognition]]
- [[claude-customer-n8n]]

## Contradictions / open questions

- **The four 2026-08-06 pages are legacy as of 2026-10-12.**
  [[anthropic-prompting-claude-opus-5]], [[anthropic-prompting-claude-sonnet-5]],
  [[anthropic-prompting-claude-fable-5]], and [[openai-prompt-guidance-gpt-5-6]]
  carry `status: legacy` and `superseded_by:` per the schema's legacy convention.
  Their claims stay true of the legacy models and remain cited above as the first
  evidence for each axis; settings for current models come from the current pages.
- **Cross-generation reversals.** The three cases below are recorded as evidence
  that the axes are stable while the settings flip. They are not one rule, and
  none is resolved by picking a side: each claim holds for the model it was
  measured on.
  - *Instruction form (axis 4).* The Sonnet 5 page (echoed for Opus 5) says positive
    examples outperform "what not to do" instructions (see
    [[anthropic-prompting-claude-sonnet-5]]). The Opus 5.5 page says a list of
    *named* patterns to avoid works where a vague negative fails (see
    [[anthropic-prompting-claude-opus-5-5]],
    [[anthropic-getting-most-out-of-opus-5-5]]). Named negatives vs vague negatives
    may reconcile the two; no page tests it.
  - *Verifier subagents (axes 5 and 6).* Fable 5 recommended fresh-context
    verifier subagents over self-critique (see
    [[anthropic-prompting-claude-fable-5]]). Sonnet 5.5 says not to launch reviewer
    subagents unless asked, with session cost down and no quality change (see
    [[anthropic-prompting-claude-sonnet-5-5]]). Fable 5.1 drops the recommendation
    without saying whether it still holds (see
    [[anthropic-prompting-claude-fable-5-1]]).
  - *Budget signals (axis 9).* Fable 5 warned against showing a remaining-token
    countdown, because it triggered context-budget concern (see
    [[anthropic-prompting-claude-fable-5]]). Opus 5.5 recommends an elapsed-time
    budget line on each message (see [[anthropic-prompting-claude-opus-5-5]]).
    Sonnet 5.5 adds a third effect: a token countdown after tool results causes
    injection misreads (see [[anthropic-prompting-claude-sonnet-5-5]]). Time and
    token signals are different, and no page says whether a time countdown causes
    budget anxiety.
- **Does effort shape output, or only thinking? (axis 2 trap).** The first
  trap under axis 2 comes from [[anthropic-prompting-claude-opus-5]]
  (2026-08-06, legacy), which says effort controls how much the model thinks,
  not how much it says. [[anthropic-what-a-task-costs-opus-5-5]] (2026-09-25)
  says effort shapes all output: thinking, written text, and tool calls, with
  fewer and shorter tool calls at low effort. The current
  [[anthropic-prompting-claude-opus-5-5]] page removed the "thinks, not says"
  claim with no counterpart. Each claim may hold for the model it describes,
  but the trap is unconfirmed for current models. Whether lower effort shortens
  visible output on a current model is open: test it rather than assume either
  claim.
- **Initiative is folded into axis 8, not a tenth axis.** The GPT-6 Astra page
  treats "initiative and follow-through" as its own behavior (see
  [[openai-prompting-gpt-6-astra]]). Its content — persist versus stop to ask,
  approval as the last step — is the default-behavior side of the stopping and
  confirmation boundaries in axis 8. The scope half of Sonnet 5.5's "initiative
  and scope" section (unrequested additions) is filed under axis 4 (see
  [[anthropic-prompting-claude-sonnet-5-5]]). Split initiative out if a source
  shows it tuned independently of the stopping boundaries.
