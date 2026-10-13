---
title: "Anthropic: Claude Opus 5.5 Is Built for Longer, Context-Heavy Coding Sessions"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Michael Segner (Anthropic)
date: 2026-09-24
source_url: https://claude.com/resources/articles/claude-opus-5-5-built-for-coding-sessions-that-use-more-context
source_path: raw/anthropic-opus-5-5-long-coding-sessions.md
models: [claude-opus-5-5]
as_of: 2026-10-12
tags: [model-specific, opus-5-5, claude-code, prompt-caching, token-cost, pricing, usage-trends]
---

# Anthropic: Claude Opus 5.5 Is Built for Longer, Context-Heavy Coding Sessions

> An Anthropic post that links Claude Code usage trends (longer runs, more context
> per request) to the pricing and harness changes behind Claude Opus 5.5's lower
> cost for long sessions.

## Summary

Published 2026-09-24 on claude.com articles by Michael Segner of [[anthropic]]. The
post has no formal applicability statement. Its model-specific claims concern
`claude-opus-5-5`, at the 2026-09-22 price sheet, compared against Opus 5 and
GPT-6 Astra. Anthropic estimates that Opus 5.5 costs about 40% less to run than
Opus 5 for typical token-billed workloads. The largest savings come in long,
high-context sessions. The post separates three causes: pricing (model-specific),
model behavior (model-specific), and the [[claude-code]] harness. The post itself
says the harness changes are "less specific to Opus 5.5".

## Key points

### Claude Code usage trends (March–September 2026, aggregate)
- Claude works 3.3x longer per prompt. Model calls per prompt rose by more than 40%
  (the text) or about 50% (the figure); this page records both values.
  Interruptions fell 68%. Prompts per session stayed steady.
- Developers are about 2x as likely to connect a tool server or use a skill, and a
  third less likely to paste text into a prompt.
- Context per request grew 2.6x. The input-to-output token ratio moved from 189:1
  to 324:1. The post concludes that cache reads now dominate cost.

### Model-specific: pricing and behavior (Opus 5.5)
- Versus Opus 5: input and output prices cut 20%; cached-read price cut 60%.
- From the figure (standard tier, short context, 2026-09-22), Opus 5.5 versus
  GPT-6 Astra per million tokens: input $4.00 vs $10.00; output $20.00 vs $50.00;
  cache read $0.20 vs $1.00.
- Evals from the same figure (Opus 5.5 at max effort unless noted):
  - Terminal-Bench 4.0: 66.4% vs 57.9% (Opus at xhigh, Astra at high; Astra
    scores as reported by OpenAI).
  - FrontierCode v1.1: 54.4% vs 53.3%.
  - GDPval-AA v2.1: 1846 vs 1542.
  - AutomationBench: 40.0% vs 41.4% (scores from Zapier).
  - Terminal-Bench-Science 0.1: 58.7% vs 64.6%.
- Fewer turns: Zeta Labs reported fewer turns and tool calls per task than on
  Opus 5, at nearly half the cost, with twice as many of its hardest tasks
  completed. This is a customer report.
- The post quotes Addy Osmani's "The cost of a task on Opus 5.5": on well-scoped
  tasks the turn counts match and only the price cut applies, and the gap is largest
  on open-ended tasks. That post is not in this wiki.
- Output generation is more than 30% faster than Opus 5.

### Claude Code harness (dated 2026-09; not specific to Opus 5.5)
- Cache-missing input fell by more than 50% despite the usage trends.
- Fewer accidental cache breaks: a login refresh, mid-conversation instructions,
  and on-demand tool loading no longer break the cache.
- On Opus 5.5 and Fable 5.1, a mid-session effort change no longer resets the cache.
- API-key and cloud-provider users can set a one-hour cache lifetime; subscribers
  already had it. Forked subagents start from the parent's cache.

### Protect your cached reads
- Run `/usage` to see the cached-read share. Pick the model at the session start,
  compact before stepping away, and set the one-hour cache on API or cloud.

## Entities

[[anthropic]], [[claude-code]], [[claude]], [[openai]]

## Concepts

[[context-engineering]]

## Notable claims & data

- The harness claims supersede two earlier statements in
  [[anthropic-claude-code-session-cost]] (2026-08-14): that `/effort` breaks the
  cache, and that API-key caches last five minutes by default. The new behavior
  applies to the named models; it is not a conflict.
- The per-message effort mechanism agrees with
  [[anthropic-prompting-claude-opus-5-5]].
- Benchmark and price comparisons are vendor-reported, dated 2026-09-22.

## Connections

The model's prompting contract is [[anthropic-prompting-claude-opus-5-5]]; the
user playbook is [[anthropic-getting-most-out-of-opus-5-5]]. The caching rationale
is in [[anthropic-prompt-caching-is-everything]]. The session habits are in
[[anthropic-claude-code-session-cost]] and
[[anthropic-claude-code-session-management]].
