---
title: "Anthropic: Prompting Claude Sonnet 5.5"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic
date: accessed 2026-10-12
source_url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5
source_path: raw/anthropic-prompting-claude-sonnet-5-5.md
models: [claude-sonnet-5-5]
as_of: 2026-10-12
tags: [prompting, model-specific, anthropic, sonnet-5-5, harness, structured-output]
---

# Anthropic: Prompting Claude Sonnet 5.5

> Anthropic's model-specific prompting page for Claude Sonnet 5.5 — effort,
> initiative and scope, the `between_tools` thinking mode, JSON output on reasoning
> tasks, progress updates, mid-turn user messages, and refusal categories.

## Summary

The page states its scope as "the prompting patterns specific to Claude Sonnet 5.5"
and says existing Claude Sonnet 5 prompts "should perform well without changes," with
[[anthropic-prompting-claude-sonnet-5]] still a reasonable starting point. It also
says that for the hardest long-horizon work "an Opus model is the better choice." The
page has no byline date; this capture records the access date.

The central theme is that **behavior depends strongly on effort level**: at `low` and
`medium` the model can check in early, skip verification, and skip thinking on JSON
tasks; at `xhigh` and `max` it can start its own review rounds and launch reviewer
subagents. The page pairs each effort-dependent behavior with a system prompt
paragraph and a measured effect. A second theme is harness hygiene for message
placement: where user text, reminders, and tool results go so the model's
injection resistance does not misfire. See [[prompt-tuning-axes]] and
[[agent-harness]].

## Key points

### Effort recalibrated; levels not portable
Levels do not map to Sonnet 5 levels; re-sweep. Default `high` on the Claude API;
`medium` for well-specified agentic coding; `medium`/`low` for chat. From `medium` up
the model thinks briefly before almost every reply, and system prompt requests to
think less "doesn't reliably reduce" thinking — lower effort instead. Use per-message
effort changes (beta, adaptive thinking only) to avoid breaking the prompt cache.

### Initiative and scope are effort-dependent
- Low/medium effort: may stop to confirm a plan or ask whether to continue. Fix:
  raise effort, or add a "keep working until done; stop and report when done; no
  unrequested additions" two-paragraph prompt.
- All efforts: adds tests, docs, and small supporting files that match repo
  conventions. Anthropic expects most teams to welcome this; the second paragraph
  alone limits it.
- `xhigh`/`max`: self-started review rounds and reviewer subagents. A "stop when
  checks pass; no reviewer sub-agents unless asked" prompt cut session cost by about
  a third at `max` with no quality change.
- Open-ended asks can trigger building a presentation or video; tell it to stop at
  ideas or a plan.

### `between_tools` replaces thinking-off
`thinking: {"type": "between_tools"}` is the lowest thinking setting, accepted only at
`high` or below; it disallows per-message effort changes and the `display`,
`budget_tokens`, and `block_binding` fields (each a 400). Notes between tool calls
still arrive as `thinking` blocks with summaries and must be passed back unchanged.
Without tools, `between_tools` means no thinking at all, so use adaptive thinking for
reasoning tasks.

### JSON answers to reasoning tasks
With structured outputs all working must happen in thinking; the model often skips
it at `low`/`medium`. Fixes: a "think first" system line (at `high`, close to `xhigh`
accuracy), or `xhigh`. Treat `stop_reason: "max_tokens"` as failure even with valid
JSON. Without structured outputs, parse the **last** complete JSON value from `text`
blocks rather than the first-`{`-to-last-`}` span, because the model sometimes writes
a draft first. This made nearly every response usable.

### Progress updates and harness reminders
Longer notes arrive as progress-update `thinking` blocks (opt in with
`display: "updates"`, beta). Remove "hold all findings for the final response"-style
lines. A one-turn reminder after about five silent tool steps, appended as a
turn-scoped system message, shortened silent stretches with no quality change. Stop
after two or three reminders, because frequent harness text after tool results can
look like injection.

### Mid-turn user messages misread as injection
User text inside a `tool_result`, or a system message right after a tool result, can
be treated as injected. Rules: never put user text in `tool_result`; append user words
as a text block after the last `tool_result`; keep harness notices in a separate
system message; no custom token countdowns in interactive sessions (Task budgets beta
has not shown the problem).

### Other patterns
- Search: remove "minimize tool calls" language; tell the model to search for
  specifics that may have changed since training even when confident.
- Verification at `low`: a "run a real check that exercises the change" paragraph
  made skipped checks rare at slightly higher cost.
- Tolerant tool calls: accept case-only name mismatches, or return `is_error: true`
  with the exact name.
- Vision: crop/zoom/code tools beat raising effort for charts.
- Refusal categories: `cyber`, `bio`, `frontier_llm`, `reasoning_extraction`,
  `general_harms`. Server-side fallback retries only `cyber` and `frontier_llm`, on
  Claude Sonnet 5.

## Changes from the previous generation

Compared with [[anthropic-prompting-claude-sonnet-5]] (Claude Sonnet 5, now legacy).

**Added**
- Steer initiative and scope (early check-ins, unrequested additions, self-started
  review at `xhigh`/`max`, open-ended requests) with three prompts.
- `between_tools` thinking mode and its constraints.
- Reasoning tasks with JSON output, including the last-JSON-value parsing rule.
- Mid-turn user message placement rules.
- Verification-on-coding-tasks paragraph for `low` effort.
- Tolerant tool-call handling for case and parameter-name near-misses.
- Tools for complex visual inputs.
- Safeguard refusals with five named categories and fallback-to-Sonnet-5 behavior.
- Progress updates as `thinking` blocks, the send-a-message tool, and the appended
  silent-step reminder.

**Removed** (no counterpart on the Sonnet 5.5 page)
- More literal instruction following (the Sonnet 5 page's distinctive theme).
- The cross-model effort mapping to Sonnet 4.6 and "match by observed thinking
  length."
- Response length and verbosity guidance; tone and writing style; the removal of
  `temperature`/`top_p`/`top_k`.
- Design and frontend defaults, including the propose-four-directions prompt and the
  `<frontend_aesthetics>` block.
- Interactive coding products (front-load the task spec in the first turn).
- Code review harnesses (separate finding from filtering).
- Computer use specs (`computer_20251124`, resolution guidance).
- The new-tokenizer note (about 30% more tokens than Sonnet 4.6).
- Manual extended thinking removal note (`budget_tokens` 400).

**Reversed or changed**
- Scope: Sonnet 5 "scopes its work to what was asked" at `low`/`medium`; Sonnet 5.5
  adds unrequested tests and docs at every effort and checks in early at
  `low`/`medium`.
- Tool use: Sonnet 5 was "more agentic … reach for tools more readily"; Sonnet 5.5
  sometimes answers from training knowledge and needs a search instruction.
- Thinking control by prompt: Sonnet 5 offered a prompt to make thinking rarer
  ("When in doubt, respond directly"); Sonnet 5.5 says asking to think less does not
  reliably work and effort is the lever.
- Thinking off: `thinking: {type: "disabled"}` → `between_tools`.
- Progress updates: Sonnet 5 said remove forced-update scaffolding because updates
  were regular; Sonnet 5.5 says updates may be invisible to text-only clients, and
  recommends a harness reminder after silent steps.
- Effort guidance: Sonnet 5 recommended `xhigh` for hardest coding; Sonnet 5.5
  recommends `medium` as the starting point for agentic coding and reserving `xhigh`
  for measured gains.

## Notable claims & data

- Reviewer-subagent suppression at `max`: session cost down about a third, no quality
  change.
- "Think first" line at `high` brings JSON-task accuracy close to `xhigh`.
- Last-JSON-value parsing made "nearly every response usable."
- With tools at `high`, chart reading beat no-tools at `max`, at a fraction of the
  cost.

## Entities

[[anthropic]], [[claude]]

## Concepts

[[prompt-tuning-axes]], [[agent-harness]], [[agent-steering]], [[tool-design]],
[[guardrails]], [[context-engineering]], [[agent-instructions]]

## Connections

Predecessor: [[anthropic-prompting-claude-sonnet-5]]. Siblings:
[[anthropic-prompting-claude-opus-5-5]], [[anthropic-prompting-claude-haiku-5-5]],
[[anthropic-prompting-claude-fable-5-1]]. The keep-working and verification
paragraphs are near-identical to those on the Haiku 5.5 page; the mid-turn message
rules repeat on Haiku 5.5. Related: [[anthropic-building-with-sonnet-5-5]]. The
tolerant tool-call advice connects to [[anthropic-eng-writing-tools-for-agents]].

## Contradictions / open questions

- Sonnet 5.5 says do not launch reviewer subagents unless asked; the legacy
  [[anthropic-prompting-claude-fable-5]] page recommended fresh-context verifier
  subagents over self-critique. The two pages target different models and task
  lengths, but the cross-model tension on verifier subagents is unresolved.
- Sonnet 5.5 says token countdowns after tool results cause injection misreads; Task
  budgets (beta) add a similar countdown but "haven't been seen" to cause it. The
  page gives no mechanism for the difference.
