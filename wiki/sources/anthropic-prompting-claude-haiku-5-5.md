---
title: "Anthropic: Prompting Claude Haiku 5.5"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic
date: accessed 2026-10-12
source_url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5
source_path: raw/anthropic-prompting-claude-haiku-5-5.md
models: [claude-haiku-5-5]
as_of: 2026-10-12
tags: [prompting, model-specific, anthropic, haiku-5-5, search, chatbots]
---

# Anthropic: Prompting Claude Haiku 5.5

> Anthropic's model-specific prompting page for Claude Haiku 5.5 — the first Haiku
> model with effort levels — covering effort, search grounding, JSON output with
> tools, early stopping, verification, mid-turn messages, chatbot adherence, and
> refusals.

## Summary

The page states its scope as "the prompting patterns specific to Claude Haiku 5.5"
and says existing **Claude Haiku 4.5** prompts "should perform well without changes."
There is no Haiku 5 page; the predecessor is Haiku 4.5. The page has no byline date;
this capture records the access date.

Two framing facts shape the page. First, Haiku 5.5 is "the first Haiku model with
effort levels," and thinking is on by default, which replaces Haiku 4.5's
`budget_tokens`. Second, many fixes are system prompt additions, and the page warns
that changing `system` in a stored conversation that carries thinking blocks can
return a 400 error. So the additions apply to new conversations only, or go in the
newest turn. The page focuses on deployments typical for a small model: chatbots,
support assistants, search-backed answering, and high-volume tool tasks. See
[[prompt-tuning-axes]].

## Key points

### Effort replaces the thinking budget
`low` for chat and high-volume work; `medium` (default) for most work including
agentic coding; `high` for knowledge work, longer agent tasks, and strict instruction
following; `xhigh`/`max` only with measured gains, and compare against Claude Sonnet
5.5 at that point. `max_tokens` up to 128,000 must leave room for thinking. Prompting
the model to answer directly did not stop thinking; lower effort instead.
`thinking: {"type": "disabled"}` works only at `low`–`high`. At `xhigh` in multi-turn
chat the model can put the whole answer in thinking and return no visible text.
Per-message effort changes (beta, `mid-conversation-output-config-2026-07-01`) keep
the cache.

### Search grounding needs the date
Give today's date with any search tool, rendered once per conversation so `system`
and `tools` stay byte-stable. With long system prompts or `low` effort, add a
paragraph saying training data is old and listing what changes (office holders,
prices, versions, rules, "latest"). That raised search on changed facts and added
needless searches on only 0–3 percent of prompts. A blanket "always search" rule made
the model search on half of the no-search prompts without more correct answers.

### Thinking-off plus structured output can skip tool calls
Use adaptive thinking; or drop `output_config.format` on requests needing a tool; or
force the call with `tool_choice`. If thinking must stay off, a line saying the JSON
format applies only to the final answer raised complete-and-correct JSON rates.

### Early stopping and verification at low effort
Long coding-agent prompts at `low` can cause early hand-back. The keep-working
paragraph fixes it; moving `low`→`medium` without it roughly halved early stopping
but more than doubled output tokens. At `low`/`medium` the model can claim a change
is done without a check; the shared "run a real check" paragraph raised checking and
performance.

### Chatbot adherence
One paragraph telling the model that system prompt rules hold against arguing,
sympathetic reasons, partial asks, claimed approvals, and repetition made it keep to
its system prompt more often. Use `high` effort where instruction following matters
most. Reasoning-like text in replies is fixed by adaptive thinking at `medium`.

### Mid-turn messages and refusals
Same placement rules as Sonnet 5.5: no user text in `tool_result`; user words after
the last `tool_result`; notices in a separate system message. Refusal categories are
`cyber`, `frontier_llm`, `bio`, and `general_harms`; refusals are new relative to
Haiku 4.5. There is no server-side fallback, and resending usually refuses again.

## Changes from the previous generation

The wiki has **no predecessor page** for Haiku: no Haiku 4.5 or Haiku 5 prompting
page was ingested. The page itself names Claude Haiku 4.5 as the predecessor. The
changes below are the ones the page states relative to Haiku 4.5, not a comparison
against a wiki page.

**Added (per the page, relative to Haiku 4.5)**
- Effort levels (first Haiku with them); thinking on by default.
- Safety classifiers and `stop_reason: "refusal"`, with no server-side fallback.
- All prompt sections on the page (search date, JSON with tools, early stopping,
  verification, mid-turn messages, chatbot adherence, reasoning in replies) are
  framed as Haiku 5.5 behaviors, not deltas from Haiku 4.5.

**Removed (per the page)**
- `budget_tokens` thinking budgets: "there's no old setting to carry over."

**Cross-generation observations (relative to sibling 5.x pages, not a predecessor)**
- The keep-working, verification, and mid-turn message guidance is shared almost
  word for word with [[anthropic-prompting-claude-sonnet-5-5]].
- Haiku 5.5 still accepts `thinking: {"type": "disabled"}` (at `low`–`high`), unlike
  Opus 5.5 (always on) and Sonnet 5.5 (uses `between_tools`).
- Unlike the Opus 5.5 and Sonnet 5.5 pages, the Haiku page has no progress-update
  section and lists no `reasoning_extraction` refusal category.

## Notable claims & data

- Search nudge: needless searches rose by only 0–3 percent of no-search prompts;
  blanket rule caused searches on half of them.
- `low`→`medium`: early stopping roughly halved; output tokens more than doubled.
- Changing `system` mid-conversation with thinking blocks present can return 400.

## Entities

[[anthropic]], [[claude]]

## Concepts

[[prompt-tuning-axes]], [[guardrails]], [[agent-harness]], [[context-engineering]],
[[tool-design]], [[agent-instructions]]

## Connections

Siblings in the same generation: [[anthropic-prompting-claude-sonnet-5-5]],
[[anthropic-prompting-claude-opus-5-5]], [[anthropic-prompting-claude-fable-5-1]].
The byte-stable `system`/`tools` advice connects to
[[anthropic-prompt-caching-is-everything]]. The chatbot adherence paragraph is a
prompt-level instance of the input guardrails in [[guardrails]].

## Contradictions / open questions

- The Haiku page omits `reasoning_extraction` from its refusal list, while the Opus
  5.5, Sonnet 5.5, and Fable 5.1 pages all list it. Unclear whether Haiku 5.5 lacks
  that classifier or the page omits it.
