---
title: "Anthropic: Prompting Claude Fable 5"
type: source
created: 2026-08-06
updated: 2026-08-06
author: Anthropic
date: accessed 2026-08-06
source_url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5
source_path: raw/anthropic-prompting-claude-fable-5.md
models: [claude-fable-5, claude-mythos-5]
as_of: 2026-08-06
tags: [prompting, model-specific, anthropic, fable-5, mythos-5, long-horizon]
---

# Anthropic: Prompting Claude Fable 5

> Anthropic's model-specific prompting page for Claude Fable 5 and Claude Mythos 5
> — long-horizon autonomy, memory systems, scaffolding removal, and the
> `reasoning_extraction` refusal category.

## Summary

Claude Fable 5 targets "problems that were previously too complex, long-running, or
ambiguous," and is described as particularly effective at end-to-end work "that
takes a person hours, days, or weeks." Anthropic explicitly warns that testing it
only on simpler workloads "tends to undersell its capability range." Claude Mythos
5 shares this page: it has the same specs and pricing and is invitation-only under
Project Glasswing, scoped to defensive cybersecurity.

This is the most scaffolding-heavy of the model pages, because the shift is not
just tonal — turn durations, harness timeouts, memory, and subagent communication
patterns all change. See [[prompt-tuning-axes]] and [[agent-harness]].

## Key points

### Longer turns by default
Individual requests on hard tasks "can run for many minutes at higher effort
settings," and autonomous runs can extend for hours. Anthropic calls this "one of
the largest shifts teams encounter." Client timeouts, streaming, and progress
indicators must be adjusted *before* migrating, and harnesses should be
restructured to check on runs asynchronously rather than blocking.

### Effort
`high` is the default, `xhigh` for capability-sensitive work, `medium`/`low` for
routine work. Anthropic's claim: lower effort settings on Fable 5 "still perform
well and often exceed `xhigh` performance on prior models." At higher effort the
model can gather context and deliberate beyond what a routine task needs, and can
perform unrequested tidying or refactoring — both are prompt-controllable.

### Strong instruction following changes prompt economics
Instruction following is improved "enough that you can steer most behaviors with a
brief instruction rather than enumerating each behavior by name." A short brevity
instruction is stated to be as effective as listing each unwanted pattern
individually. This inverts the older practice of exhaustive rule enumeration.

### Ground progress claims during long runs
On long autonomous runs, instruct the model to audit each progress claim against an
actual tool result from the session. Anthropic reports this "nearly eliminated
fabricated status reports even on tasks designed to elicit them" — the strongest
empirical claim on the page.

### Memory systems
Fable 5 "performs particularly well when it can record lessons from previous runs
and reference them." A plain Markdown file suffices. The recommended note
discipline — one lesson per file, one-line summary at top, record corrections and
confirmed approaches with the reasoning, update rather than duplicate, delete what
turns out wrong — plus a bootstrap prompt that reviews past sessions via subagents
to extract themes.

### Parallel subagents
Dispatches parallel subagents more readily and "reliably manages ongoing
communication with long-running subagents and peer agents." Anthropic recommends
asynchronous orchestrator↔subagent communication over blocking, and notes that
long-lived subagents that retain context across subtasks "save time and cost
through cache reads and avoid bottlenecking on the slowest subagent."

### Failure modes specific to long sessions
- **Early stopping.** Deep into a session the model can end a turn with a
  text-only statement of intent ("I'll now run X") without issuing the tool call.
  A "continue" resolves it; autonomous pipelines need a system reminder that the
  user is not watching and cannot answer mid-task.
- **Context-budget concern.** In very long sessions the model may suggest a new
  session or trim its own work — "most often triggered when the harness shows a
  remaining-token countdown to the model." Anthropic's guidance is to avoid
  surfacing explicit context-budget counts at all, and to add reassurance if the
  harness must show them.
- **Readability drift.** In extended agentic conversations the model can produce
  dense shorthand, arrow chains, and references to thinking the user never saw. The
  recommended mitigation treats the final summary as a re-grounding for a reader
  who saw none of the working thread.

### `send_to_user` tool
For long asynchronous agents, Anthropic recommends a client-side tool that
surfaces a message verbatim without ending the turn, because **tool inputs are
never summarized**. Defining the tool is insufficient on its own — "without an
instruction in the system prompt, Claude Fable 5 rarely calls it."

### Safety classifiers and `reasoning_extraction`
Fable 5 runs classifiers targeting offensive cybersecurity, biology/life sciences,
and extraction of the model's summarized thinking; benign work in those areas may
also trigger them, returning `stop_reason: "refusal"`. Anthropic recommends
configuring fallback to Claude Opus 4.8.

Critically for prompt authors: **prompts, skills, or harness instructions that tell
the model to echo, transcribe, or explain its internal reasoning as response text
can trigger the `reasoning_extraction` refusal category**, causing elevated
fallbacks. Existing skills and system prompts must be audited for
show-your-thinking instructions when migrating. Reasoning visibility should come
from structured `thinking` blocks instead.

### Recommended scaffolding changes
- Start at the top of your difficulty range rather than benchmarking on easy tasks.
- Make self-verification explicit in long-run prompts — and note that "separate,
  fresh-context verifier subagents tend to outperform self-critique."
- Refactor existing prompts and skills: those developed for prior models "are often
  too prescriptive for Claude Fable 5 and can degrade output quality."

## Notable claims & data

- Progress-claim auditing "nearly eliminated fabricated status reports."
- Lower effort on Fable 5 "often exceed[s] `xhigh` performance on prior models."
- Fresh-context verifier subagents outperform self-critique — a concrete
  orchestration finding, not just a prompting one.
- Over-prescriptive legacy skills actively *degrade* output quality.

## Entities

[[anthropic]], [[claude]]

## Concepts

[[prompt-tuning-axes]], [[agent-harness]], [[agent-orchestration]],
[[context-engineering]], [[agent-skills]], [[agent-instructions]],
[[tool-design]], [[agent-evals]]

## Connections

The scaffolding-removal guidance is the sharpest statement yet of the pruning
principle in [[harnessing-claudes-intelligence]] and
[[anthropic-evolution-of-agentic-surfaces]] — here old scaffolding is not merely
wasteful but harmful. The verifier-subagent finding connects to
[[anthropic-eng-effective-harnesses-long-running-agents]] and
[[anthropic-eng-multi-agent-research-system]]. The memory-system guidance connects
to [[context-engineering]]. Siblings:
[[anthropic-prompting-claude-opus-5]], [[anthropic-prompting-claude-sonnet-5]].

## Contradictions / open questions

- The `reasoning_extraction` classifier penalizes show-your-thinking instructions,
  which sits in tension with the long-standing transparency principle recorded in
  [[agent-design-principles]] ("show the agent's planning steps explicitly").
  Both can hold — transparency via structured `thinking` blocks rather than via
  prompted self-narration — but prompts written under the older guidance will now
  fail. Flagged for the human.
