---
title: "Anthropic: Maximizing the Value of Your Claude Code Sessions"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Lydia Hallie (Anthropic)
date: 2026-08-14
source_url: https://claude.com/resources/articles/maximizing-the-value-of-your-claude-code-sessions
source_path: raw/anthropic-claude-code-session-cost.md
tags: [claude-code, prompt-caching, token-cost, context-engineering, subagents, compaction, best-practices]
---

# Anthropic: Maximizing the Value of Your Claude Code Sessions

> A cost model for [[claude-code]] sessions: what sets the price of a token, what
> sets how many tokens a session sends, and which user habits break the prompt
> cache or bloat the context.

## Summary

Published 2026-08-14 on claude.com articles by Lydia Hallie of [[anthropic]]. The
post says token efficiency means spending tokens on the task asked for, not spending
fewer tokens overall. Three factors set the price of a token: the model, input versus
output, and cached versus uncached. Three factors set the volume: how many tokens
enter the context, how many turns they stay, and how many contexts run at once.
Everything in the conversation is re-sent on every later turn. The cache makes each
re-send cheap, but each re-send still costs money and adds to what the model must
reason over.

## Key points

- **Prefill versus decode.** Output is priced at roughly 5x input, because decode
  runs the model once per token. Thinking tokens are output, and the effort level
  controls them.
- **Prompt caching mechanics.** A cache read costs 0.1x input; a cache write costs
  up to 2x, once per token. The request order is tool definitions, then the system
  prompt, then the conversation (with `CLAUDE.md` at its front). Any change in that
  prefix re-prefills everything after it. A worked example shows five requests for
  one small test fix, each one re-sending the whole conversation.
- **Cache breakers listed in the post.** `/model` (including opusplan's mode
  switches), `/effort`, fast mode (re-prefill at fast-mode prices), `/compact`,
  and expiry. Expiry is one hour on a subscription and five minutes on an API key,
  unless `ENABLE_PROMPT_CACHING_1H=1` is set. The cheap moments to switch are the
  session start or right after `/clear`. `/rewind` trims only the tail of the
  conversation, so the earlier turns stay cached.
- **Context volume.** Run `/context` in a fresh session to see what loads at
  startup. Move workflow-specific instructions from `CLAUDE.md` into
  [[agent-skills]], and turn off unused MCP servers with `/mcp`. An @-mention
  attaches the file and saves a Read call.
- **Command output.** Output over 30,000 characters goes to a file with a preview in
  context (`BASH_MAX_OUTPUT_LENGTH` changes the limit). The real cost is output
  under that limit, such as 400 passing-test lines. Put quiet-flag commands in
  `CLAUDE.md`.
- **Session length.** Turn 40 re-reads the 39 turns before it. Use `/clear` per
  task and `/compact` between phases. On 1M models, `/autocompact 200k` restores
  the earlier auto-compact threshold (Claude Code v2.1.221+). A `/loop` carries
  its whole session on every turn.
- **Subagents.** A subagent pays off for jobs with much disposable output; for small
  jobs it is overhead. A repeated noisy job can get its own subagent definition with
  `model: haiku`.
- **Where to look first** (from the closing figure, in cost order): long sessions,
  too much in the context, a bigger model or higher effort than the task needs,
  and breaking the prompt cache.

## Entities

[[anthropic]], [[claude-code]], [[claude]]

## Concepts

[[context-engineering]], [[agent-orchestration]], [[agent-skills]],
[[model-context-protocol]], [[tool-placement]]

## Notable claims & data

- `MAX_THINKING_TOKENS=0` turns thinking off for one session, except on Fable 5.
- **Dated and model-dependent:** this post (2026-08-14) says `/effort` breaks the
  cache and API-key caches last five minutes by default. The later
  [[anthropic-opus-5-5-long-coding-sessions]] (2026-09-24) says that on Opus 5.5
  and Fable 5.1 effort changes no longer reset the cache, and that API-key users
  can now set a one-hour lifetime. The later post supersedes this one for those
  models; it does not contradict it.

## Connections

The user-side counterpart to [[anthropic-prompt-caching-is-everything]], which gives
the harness-side caching rules. The post points to [[anthropic-choosing-claude-model]]
for model and effort choice. It extends [[anthropic-claude-code-session-management]]
(rewind, compact, clear, subagents) with cost numbers. The subagent trade-off matches
[[anthropic-subagents-in-claude-code]].
