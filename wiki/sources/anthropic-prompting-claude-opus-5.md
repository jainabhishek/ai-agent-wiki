---
title: "Anthropic: Prompting Claude Opus 5"
type: source
created: 2026-08-06
updated: 2026-08-06
author: Anthropic
date: accessed 2026-08-06
source_url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
source_path: raw/anthropic-prompting-claude-opus-5.md
models: [claude-opus-5]
as_of: 2026-08-06
tags: [prompting, model-specific, anthropic, opus-5]
---

# Anthropic: Prompting Claude Opus 5

> Anthropic's model-specific prompting page for Claude Opus 5 — the behaviors
> that most often require prompt tuning when moving from Claude Opus 4.8.

## Summary

Claude Opus 5 is positioned for complex agentic coding and enterprise work, with
particular strength on long-horizon tasks. Anthropic states it "performs well out
of the box on existing Claude Opus 4.8 prompts," so the page is framed as a list
of deltas rather than a from-scratch guide. The dominant theme is **subtraction**:
several instructions that earlier models needed — explicit verification steps,
"double-check your answer," forced status summaries — now compound with behaviors
the model performs natively and waste tokens without improving quality. See
[[prompt-tuning-axes]].

## Key points

### Response length and verbosity
Default user-facing responses run longer than prior Opus models'. Critically, the
`effort` parameter "controls how much the model thinks rather than how much it
says" — lowering effort reduces thinking volume without reliably shortening the
visible response. Length must be prompted for explicitly. In a long system prompt,
Anthropic recommends pairing the main instruction with a short reminder near the
end of the prompt (a `<tone_preference>` block).

### Written deliverable length
Separate axis from conversational verbosity: files written to disk (reports,
Markdown docs, summaries) are also longer than on prior models, and need their own
length-calibration instruction.

### Task scope and over-verification
Opus 5 verifies its own work unprompted. Anthropic's instruction is to *remove*
explicit verification instructions — "include a final verification step for any
non-trivial task," "use a subagent to verify" — because they "cause
over-verification on Claude Opus 5, and removing them reduces wasted tokens with
no loss in quality." The same applies to legacy harness scaffolding that adds
separate verification steps. The model can also expand task scope, adding steps
that weren't requested, so narrow tasks need explicit scope constraints.

### Self-correction
The model catches and fixes its own mistakes well without prompting; instructions
like "double-check your answer" or "re-verify before responding" compound with
that behavior and add cost without improving results. It also narrates corrections
to its earlier statements more than prior models, which the page flags as
undesirable in user-facing products — the fix is to limit correction narration to
errors that would change the user's decisions.

### Code review
High precision *and* recall — additional findings are "mostly real issues rather
than false positives," and accuracy holds at lower effort. But a review prompt
saying "only report high-severity issues" or "be conservative" may be followed
literally, reducing reported findings. Anthropic's recommendation: ask for
everything and filter in a separate pass. (Same failure mode documented for
[[anthropic-prompting-claude-sonnet-5]].)

### Subagent delegation
Opus 5 delegates more readily than prior models. Delegation "pays off on genuinely
independent, sizeable tracks of work, but it multiplies cost and time when applied
to small tasks." Recommended controls: explicit guidance on which scenarios
warrant delegation, or deterministic caps on spawn counts. Notably the sample
prompt tells the model *not* to use subagents to verify its own work — consistent
with the over-verification finding above.

### Effort
`low` and `medium` "produce strong quality at a fraction of the tokens and latency
of higher settings." Default is `high`; step up to `xhigh` for demanding coding and
agentic work. Effort defaults carried over from a prior model should be re-swept
against your own evals.

### Running with thinking disabled
Thinking is on by default and can only be disabled at effort `high` or below. Two
artifacts can appear when disabled: the model occasionally writes a **tool call as
plain text** instead of emitting a structured `tool_use` block (the call never
runs, and in agentic loops the leaked text persists in history, affecting later
turns), and it can emit **internal XML tags** such as `<thinking>` into visible
output. Anthropic's primary mitigation is to keep thinking enabled and control cost
with lower effort instead — "for most tasks, thinking enabled at `low` effort
performs better than thinking disabled at similar cost." A system-prompt rule
telling the model not to think or reason *increases* tag leakage, and instructions
naming thinking tags specifically are less effective than a general rule against
internal tags.

## Notable claims & data

- Effort controls thinking volume, not visible response length — a distinction
  that invalidates using effort as a verbosity lever.
- Removing verification instructions reduces token waste "with no loss in quality."
- Thinking-on at `low` effort beats thinking-off at comparable cost for most tasks.
- 1M token context window is both the default and the maximum, with instruction
  following, tool calling, and reasoning "consistent throughout the window."

## Entities

[[anthropic]], [[claude]]

## Concepts

[[prompt-tuning-axes]], [[agent-instructions]], [[agent-orchestration]],
[[agent-design-principles]], [[context-engineering]]

## Connections

The subtraction theme is the prompt-layer instance of the harness-pruning
principle in [[harnessing-claudes-intelligence]] and
[[anthropic-evolution-of-agentic-surfaces]] — scaffolding built for an older model
becomes dead weight. Sibling model pages:
[[anthropic-prompting-claude-sonnet-5]], [[anthropic-prompting-claude-fable-5]].

## Contradictions / open questions

- _None recorded._
