---
title: "OpenAI: Using GPT-6.2 — prompting and migration"
type: source
created: 2026-11-24
updated: 2026-11-24
author: OpenAI
date: accessed 2026-11-24 (models released 2026-11-17)
source_url: https://developers.openai.com/api/docs/guides/latest-model/gpt-6.2-astra
source_path: raw/openai-prompting-gpt-6-2.md
models: [gpt-6.2-astra, gpt-6.2-sol]
as_of: 2026-11-24
tags: [prompting, model-specific, openai, gpt-6-2, migration, prompt-caching, responses-api]
---

# OpenAI: Using GPT-6.2 — prompting and migration

> OpenAI's model guide for GPT-6.2 Astra and GPT-6.2 Sol. It covers two
> Responses API changes that affect caching and reasoning, prompts for four
> observed behaviors, and a migration checklist. It replaces the GPT-6 guide as
> OpenAI's current per-model contract.

## Summary

On 2026-11-17, OpenAI released `gpt-6.2-astra` (for the hardest tasks) and
`gpt-6.2-sol` (for complex work at lower cost). The models overview now
lists four current models: GPT-6.2 Astra, GPT-6.2 Sol, GPT-6.1 Terra, and GPT-6
Luna. GPT-6 Astra and GPT-6.1 Sol moved to "More models".

Two platform changes matter more than the prompts:

1. **Prefix edits drop reasoning.** If you edit earlier history, change some
   models, or change the user or the organization, the Responses API discards
   the stored reasoning items. Quality can fall, and token use can rise.
2. **Top-level `instructions` now come after `input`.** Reusable instructions
   belong in a leading `developer` message, or they cannot be cached.

Both changes reward one rule: keep the prefix fixed. See [[context-engineering]].

The prompting section is shorter than the GPT-6 page's. The theme moves away
from GPT-6 Astra's stop-and-ask habit. GPT-6.2 Astra writes tersely, may still
propose a next step and wait when intent is unclear, and writes better code. The
prompts push toward finishing the work, a self-contained final answer, and
readable code. See [[prompt-tuning-axes]] and [[agent-instructions]].

## Key points

### What's new (platform)
- **Prefix edits** drop reasoning items. Keep the prefix unchanged between
  responses.
- **`instructions` placement:** use a first `developer` message for stable
  text. Use top-level `instructions` only for guidance that applies to one
  request.
- **Background mode (public beta):** two-hour or eight-hour completion windows
  at a discount (30% and 40% below Standard, per the changelog). The windows
  replace Flex, which GPT-6.2 does not support.

### Prompting: four observed behaviors
1. **Writing style.** The default output is terse and direct, so revisit "be
   concise" lines. The guide gives three prompts:
   - A collaborator style: the user's terms, key points first, enough context.
   - An external-audience style: add the background the reader lacks, and keep
     the author's wording when editing.
   - A **self-contained final answer**: progress notes are collapsed, so the
     final answer must stand alone, written fresh, with no shorthand carried
     over from reasoning or subagents.
2. **Task completion.** The model may stop at a plan or a suggestion. The
   prompts tell it not to end the turn while authorized steps remain, and to do
   those steps itself. It stops only for a scope change, a real blocker, a
   decision that only the user can make, or an irreversible action. Other
   prompts tell it to persist and verify before it finishes, and to make
   reversible assumptions and state them. Higher effort helps it persist through
   the final checks. With `request_user_input_async`, it can ask and keep
   working (see [[openai-time-awareness-async-input-agents]]).
3. **Coding style.** The prompt asks the model to reuse existing logic and
   preserve the behavior that callers rely on. It skips new tests unless they
   are needed. It ranks readability over line count and avoids needless
   abstraction.
4. **Frontend design.** Specify imagery and typography. The prompt prefers
   realistic images and removes decorative text. For visual work, use a
   reference image, then build, render, and refine against it.

### Migration quickstart
- Set the model to `gpt-6.2-astra` or `gpt-6.2-sol`.
- Start new integrations at `medium` effort, and replace `none` or `minimal`
  with `low`. GPT-6.2 Sol rejects `none`.
- Tool calling requires the Responses API.
- Remove `temperature`, `top_p`, and the logprobs fields.
- Move stable instructions into a leading `developer` message.
- From GPT-5.5 or earlier, replace `prompt_cache_retention` with
  `prompt_cache_options.ttl: "30m"`.
- ZDR is supported. Under ZDR, `store` is treated as `false`, so pass the prior
  output items back, including the encrypted reasoning.
- US and EU residency for Standard, Fast, and Batch. Ultrafast is US only.

## Changes from GPT-6 (Astra)

Compared with [[openai-prompting-gpt-6-astra]]:

- **Initiative.** GPT-6 Astra asked more often and stopped early. GPT-6.2 Astra
  "may propose a next step and wait" when intent is unclear. The fix is the
  same kind of prompt: finish authorized work before you hand off.
- **Removed sections:** instruction sensitivity to skills and `AGENTS.md`
  (the skill audit), subagent delegation, and test restraint (over-testing).
  These are "not mentioned", not "reversed". The coding prompt still says to
  skip new tests unless needed.
- **New sections:** coding style (reuse, readability, no needless
  abstraction), frontend design, and the self-contained final answer.
- **Style.** GPT-6 Astra overused lists, tables, and stock phrases. GPT-6.2
  Astra is terse by default, so the advice is to loosen "be concise".
- **Platform.** New on this page: reasoning dropped after prefix edits,
  `instructions` placed after `input`, and background windows replacing Flex.
  The GPT-6 page's `configuration_update` (change effort without breaking the
  cache) is not mentioned. The prefix-edit rule makes that kind of mechanism
  more important.
- **Effort.** New integrations start at `medium`. The GPT-6 page said to
  preserve the current effort. `none` and `minimal` map to `low` in both.
- **Price.** GPT-6.2 Astra costs $8 input and $40 output per 1M tokens. GPT-6
  Astra cost $10 and $50.

## Entities

[[openai]], [[openai-codex]] (OpenAI Docs skill for migration),
[[openai-agents-api]].

## Concepts

[[prompt-tuning-axes]], [[agent-instructions]], [[context-engineering]],
[[agent-verification]], [[human-agent-teams]].

## Notable claims & data

- GPT-6.2 Astra: 1,050,000 context, 128,000 max output, cutoff 2026-05-18,
  $8 / $0.4 cached / $40 per 1M tokens.
- GPT-6.2 Sol: same limits, cutoff 2026-06-01, $2 / $0.1 cached / $2.5 cache
  write / $10. Ultrafast is 3x Standard until 2027-02-28 and 6x after.
- The Responses API discards reasoning items after a change of end user or
  organization, not only after edits.

## Connections

- Supersedes [[openai-prompting-gpt-6-astra]] for GPT-6.2 Astra and Sol. GPT-6
  Luna is still current and has no newer guide.
- The self-contained final answer matches Anthropic's advice for Fable 5.2 on
  final reports written for the reader
  ([[anthropic-prompting-claude-fable-5-2]]). That is a parallel only, because
  prompting guidance does not port across vendors.
- The prefix rule extends the cache-design advice in [[context-engineering]]
  and [[openai-time-awareness-async-input-agents]] (append the time, never
  rewrite earlier messages).

## Contradictions / open questions

- **Luna's guide.** GPT-6 Luna is current, but its model page links no
  prompting guide. The GPT-6 guide is still online. It is unclear whether the
  GPT-6 prompts still apply to Luna.
- **GPT-6.2 Sol behavior.** The behavior list is headed "GPT-6.2 Astra
  behavior". The guide says the prompts apply across the family, but it names no
  Sol-specific behavior.
