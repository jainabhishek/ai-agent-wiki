---
title: "Anthropic: What a Task Costs on Opus 5.5"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Addy Osmani (Anthropic)
date: 2026-09-25
source_url: https://claude.dev/blog/what-a-task-costs-on-opus-5-5/
source_path: raw/anthropic-what-a-task-costs-opus-5-5.md
models: [claude-opus-5-5]
as_of: 2026-10-12
tags: [model-specific, opus-5-5, claude-code, token-cost, pricing, prompt-caching, effort, compaction, subagents]
---

# Anthropic: What a Task Costs on Opus 5.5

> A cost model for one [[claude-code]] task on Claude Opus 5.5: what sets the bill
> (turns, cache reads, output, model), what changed from Opus 5, and which
> settings and habits change the cost per finished task.

## Summary

Published 2026-09-25 on the claude.dev blog ("Playbooks") by Addy Osmani of
[[anthropic]]. The page has no formal applicability statement. Its nearest one is
"Our examples use Opus 5.5 API list prices". All prices, effort defaults, and cache
rules on this page are for `claude-opus-5-5`. Opus 5 and Fable 5.1 appear only as
price comparators. The thesis is that the unit of cost is a finished task, not a
token. Every turn resends the conversation, so turn count and cache hit rate
dominate the bill. A retry costs more than any saving from lower effort, a smaller
model, or less context. The post separates two effects of the move to Opus 5.5.
The first is the price change, which is certain. The second is how much work the
model does per task, which varies and must be measured.

## Key points

### Cost drivers
- Four drivers: turns, cache reads, output tokens, and the model. Thinking is billed
  as output. Output costs 5x input and, on Opus 5.5, 100x a cache read.
- Turns example: a task whose context grows from 20K to 120K over 40 turns sends
  ~2.8M input tokens. At a 90% cache hit rate that costs ~$1.62. In 25 turns it sends
  ~1.75M tokens for ~$1.02.
- Cache hit rate moves input cost more than any other setting. The same 2.8M tokens
  cost $11.20 with no cache, $1.62 at a 90% hit rate, and ~$0.99 at 96%.
- A check that the model can run (a test, a build, an endpoint script) cuts turns,
  because the model finds its mistakes earlier. Batched tool calls also cut resends.

### Opus 5.5 versus Opus 5 (prices per million tokens)
- Input $5 → $4 and output $25 → $20 (both 20% lower). Cache reads $0.50 → $0.20
  (60% lower). The read rate falls from 1/10 to 1/20 of input.
- Subscription limits go ~25% further. Five-hour limits rose separately, with a
  one-time limit reset under Settings > Usage.
- Same-token receipt (2.0M cached, 200K fresh, 60K output): $3.50 on Opus 5 and
  $2.40 on Opus 5.5, about 31% less from price alone. A mostly-cached session saves
  up to 60% on input; an uncached, output-heavy request saves up to 20%.
- The "40% cheaper" figure is an estimate for typical workloads at default settings.
  It also assumes fewer tokens per task, so it is not a per-token cut. On well-scoped
  tasks the two models need about the same number of turns.

### Effort
- Levels are low, medium, high, xhigh, and max (max for one session only). The
  default is medium; on Opus 5 it was high. At a given level Opus 5.5 thinks more than
  Opus 5, so a level chosen for Opus 5 does not carry over.
- Effort shapes all output: thinking, written text, and tool calls. Low effort makes
  fewer and shorter tool calls.
- Break-even: 20K extra thinking tokens cost $0.40. That equals a ten-turn retry at
  100K cached context, so high effort pays off only when it saves a retry.
- Symptom of too little effort: a fix that stops at one layer. Before you raise
  effort, give the model a test that runs through both layers.
- Effort changes keep the cache on an API key or a subscription. On Amazon Bedrock,
  Google Cloud's Agent Platform, or a Claude apps gateway, an effort change still
  clears the cache. Thinking is always on.

### Model routing
- Escalate to Fable 5.1 ($10/$50 per million tokens, cache reads $0.25) when Opus 5.5
  at xhigh fails twice. Switch back after the fix, at a natural break, because a model
  switch rewrites the cache.
- Use Sonnet or Haiku for lookups and log reading, never for code edits. Set this
  with `model:` in a subagent definition or with `CLAUDE_CODE_SUBAGENT_MODEL`. A small
  model's misread sends the main model on a detour that it pays for.
- Agent teams in plan mode use ~7x the tokens of a standard session (costs docs).
  The `opusplan` alias puts edits on Sonnet, which contradicts this advice; the post
  says to measure it first.

### Prompt audit
- `/claude-api prompt-audit` finds legacy prompting anti-patterns in skills,
  `CLAUDE.md`, and Claude Platform app code. On a 44-ticket internal benchmark, the
  move from Opus 4.8 to Opus 5.5 at low effort cut cost ~18%. The audit then took the
  total to ~25% below the start, by removing a six-step ritual, a scratchpad rule, a
  verify-twice rule, and contradictory instructions. This result is from one
  benchmark.

### Caching and compaction
- A cache write costs 1.25x input (5-minute cache) or 2x input (1-hour cache). A
  read costs 0.05x input. In Claude Code the cache lifetime is one hour on a
  subscription and five minutes on an API key or cloud provider.
- Events that cause a cache write: a pause longer than the lifetime, an effort change
  on a cloud provider or gateway, the first fast-mode toggle, an MCP server connect or
  disconnect, a model switch, and compaction.
- A compaction at 150K costs ~$0.25 and pays back in ~10 turns. Compact before a
  break, not after one; after a break it costs ~$0.75. Use `/rewind` to drop a wrong
  path, and `/clear` between unrelated tasks.
- Fast mode costs 2x the price ($8/$40) for up to 2.5x the speed. Turn it on at the
  session start.

## Entities

[[anthropic]], [[claude-code]], [[claude]]

## Concepts

[[context-engineering]], [[agent-orchestration]], [[multi-agent-economics]],
[[prompt-tuning-axes]], [[agent-skills]], [[model-context-protocol]]

## Notable claims & data

- Baseline from the costs docs: ~$13 per developer per active day across enterprise
  deployments, and under $30 for 90% of users.
- Opus 5.5 needs Claude Code v2.1.280 or later. Measure with `/usage` (same as
  `/cost`): check the cache share, the ratio of output to input, and the ratio of
  total input to conversation size.
- **Supersedes, does not contradict:** [[anthropic-claude-code-session-cost]]
  (2026-08-14) gives cache reads at 0.1x input and says `/effort` breaks the cache.
  For Opus 5.5 the read is 0.05x, and an effort change keeps the cache on first-party
  access. The exception for Bedrock, Agent Platform, and gateways is new, and it
  qualifies [[anthropic-opus-5-5-long-coding-sessions]], which states the cache rule
  without that exception.
- **Tension with [[prompt-tuning-axes]]:** that page says effort controls thinking,
  not output volume. This post says effort applies to every output token (text, tool
  calls, and thinking). The Opus 5.5 prompting page dropped the Opus 5 "thinks, not
  says" claim.
- Fig C presets: a small edit is 150K input and 5K output. A long agentic run is 20M
  input, 96% cached, and 600K output.

## Connections

[[anthropic-opus-5-5-long-coding-sessions]] quotes this post under the title "The cost
of a task on Opus 5.5". Michael Segner wrote that post and also reviewed this one.
This post is the Opus 5.5 update of [[anthropic-claude-code-session-cost]]. The
effort and API contract is in [[anthropic-prompting-claude-opus-5-5]]. The effort
rule of thumb pairs with [[anthropic-spending-your-effort]], published the same day.
The cache rules come from [[anthropic-prompt-caching-is-everything]]. The rule to
start smart and judge cost per task matches [[anthropic-choosing-claude-model]]. The
user playbook is [[anthropic-getting-most-out-of-opus-5-5]]. Subagent economics
match [[anthropic-subagents-in-claude-code]].
