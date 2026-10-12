---
title: "OpenAI: Using GPT-6 — prompting and migration (GPT-6 Astra)"
type: source
created: 2026-10-12
updated: 2026-10-12
author: OpenAI
date: accessed 2026-10-12
source_url: https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra
source_path: raw/openai-prompting-gpt-6-astra.md
models: [gpt-6-astra, gpt-6.1-sol, gpt-6-luna]
as_of: 2026-10-12
tags: [prompting, model-specific, openai, gpt-6, migration]
---

# OpenAI: Using GPT-6 — prompting and migration (GPT-6 Astra)

> OpenAI's "Using GPT-6" guide: the GPT-6 model picker, new API features,
> limitations, prompting best practices based on GPT-6 Astra, and a migration
> checklist from GPT-5.x.

## Summary

The page lists three current GPT-6 models: `gpt-6-astra` (highest
intelligence), `gpt-6.1-sol` (near-Astra performance at lower cost), and
`gpt-6-luna` (fastest, cheapest). `gpt-6-sol` appears only as a model to migrate
from and in the Limitations section.

**Scope of the prompting guidance.** OpenAI presents the prompts as a starting
point "across the GPT-6 model family". The same paragraph says the prompts
address behavior observed with GPT-6 Astra, and tells the reader to evaluate
them with the chosen model and workload. This page therefore lists all three
current models in `models:`, but the behavioral claims were measured on Astra
only (see open questions).

The central theme is a change in default initiative. OpenAI says Astra is more
likely than GPT-5.6 Sol to stop and ask for clarification, and more sensitive to
instructions in skills and `AGENTS.md`. Most of the supplied prompts therefore
push the model toward autonomous completion, and make the precedence between
user instructions and skill files explicit. See [[prompt-tuning-axes]] and
[[agent-instructions]].

## Key points

### Model notes
- Astra: OpenAI reports stronger eval results with substantially fewer output
  tokens, and lower estimated cost per task despite a higher per-token price.
  OpenAI also calls it its most aligned model.
- GPT-6.1 Sol: `reasoning.effort` = `low`, `medium` (default), `high`, `xhigh`,
  `max`; no `none` or `minimal`. Tool calling requires the Responses API.

### New API features (What's new)
- **Async tool calling:** `async: true` on a function or custom tool; return the
  result later with the original `call_id`. The model keeps working meanwhile.
- **Mid-turn steering:** send corrections while a response runs, over WebSocket;
  completed work is kept. See [[agent-steering]].
- **`configuration_update` input item:** change reasoning effort
  mid-conversation without rewriting the cached prompt prefix.
- **Misalignment monitoring:** asynchronous OpenAI-side monitoring for Astra.

### Limitations
- Astra and 6.1 Sol do not support `none` effort; `gpt-6-sol` and Luna do.
- Fast mode has no EU residency for Astra; Astra Ultrafast is US and global only.

### Prompting best practices (five observed behaviors)
1. **Initiative and follow-through.** Astra asks more and may stop early. The
   three prompts tell it to: infer intent and persist to completion unless an
   action is destructive or irreversible; treat "can you…" / "help me…" as
   requests to act; and finish all authorized work first, so that user approval
   is the final step on a concrete, reviewable result. The third prompt also
   forbids unsolicited warnings and approval flows for hypothetical risk.
2. **Instruction following.** Astra is more sensitive to skill and `AGENTS.md`
   text. Conflicting skill guidance can make it block early. OpenAI "strongly
   recommends" auditing every skill and file the model can access. The prompts
   (a) put user instructions above skill instructions, and (b) require the model
   to name the exact `SKILL.md` and quote the instruction whenever a skill makes
   it pause or diverge. See [[agent-skills]].
3. **Personality and writing style.** Astra tends to produce lists, tables, and
   Markdown, and reuses phrases. OpenAI supplies prompts for prose, plain
   technical language, and a list of banned stock phrases.
4. **Subagent delegation.** Astra may delegate less than desired. The prompt
   asks it to delegate whenever parallel work saves time or improves quality. A
   second prompt fixes spacing and grammar errors in messages between agents.
   See [[agent-orchestration]].
5. **Testing and verification.** Astra over-tests small changes. The prompt
   discourages tests that only mirror the implementation, and asks it to broaden
   testing only when new evidence justifies it.

### Migration quickstart
- Codex can run the migration: `$openai-docs migrate this project to the GPT-6
  model family` (OpenAI Docs skill). See [[openai-codex]].
- Keep the current effective effort; replace `none` (Astra, 6.1 Sol) or
  `minimal` with `low`.
- Tool calling requires Responses. GPT-6 Sol and Luna allow Chat Completions
  function calling only with `reasoning_effort: "none"`.
- When effort is not `none`, remove `temperature`, `top_p`, `top_logprobs`
  (and `logprobs` / `message.output_text.logprobs`).
- To change effort between turns, use `configuration_update` and keep the
  request-level `reasoning.effort` fixed, so the cache prefix survives.
- From GPT-5.5 or earlier: replace `prompt_cache_retention` with
  `prompt_cache_options.ttl: "30m"`.
- If the model keeps pausing for approval, apply the initiative prompts.

## Changes from the previous generation

Compared with [[openai-prompt-guidance-gpt-5-6]] (GPT-5.6 Sol/Terra/Luna):

- **Initiative tuning shifts toward persistence.** The GPT-5.6 page focused on
  removing scaffolding and stating outcomes. This page says Astra stops to ask
  where GPT-5.6 Sol persisted, so prompts now push toward persistence and
  autonomous completion.
- **New guidance axes** with no section on the GPT-5.6 page: sensitivity to
  skills and `AGENTS.md` (with an audit recommendation), formatting and
  stock-phrase defaults, delegation frequency, and test-scope restraint.
- **Continuity on conflicts.** The GPT-5.6 page said conflicting rules create
  more instability than missing detail. This page gives a concrete case:
  conflicting skill guidance makes Astra pause and block work early.
- **Approval boundaries.** The GPT-5.6 page separated safe local actions from
  actions that need confirmation. This page keeps that split, but adds that
  approval should come after the work is prepared, and should not be added for
  hypothetical risk.
- **Verification.** The GPT-5.6 page asked the model to check work before
  finishing. This page asks it to check less on small changes.
- **Reasoning effort.** The GPT-5.6 levels were none / low / medium / high /
  xhigh / max. Astra and GPT-6.1 Sol drop `none`; `minimal` maps to `low`.
  "Preserve the existing effort first" is unchanged. Pro mode carries over.
- **New parameters:** `async` tools, mid-turn steering, `configuration_update`,
  `prompt_cache_options.ttl`. Removed with reasoning: `temperature`, `top_p`,
  logprobs. Tool calling now requires the Responses API.
- **Verbosity:** the GPT-5.6 page made `text.verbosity` the main length lever.
  This page does not mention `text.verbosity`; it handles style through prompts.
  This is recorded as "not mentioned", not as "removed".
- **Model lineup:** GPT-5.6 had Sol/Terra/Luna. GPT-6 lists Astra, 6.1 Sol, and
  Luna, with no Terra (see open questions).

## Notable claims & data

- Astra: stronger eval results with substantially fewer output tokens; lower
  estimated cost per task than earlier models (no figures on this page).
- `prompt_cache_options.ttl: "30m"` replaces `prompt_cache_retention`.
- The guidance is family-scoped by OpenAI's wording but derived from Astra only.

## Entities

[[openai]], [[openai-codex]]

## Concepts

[[prompt-tuning-axes]], [[agent-instructions]], [[agent-skills]],
[[agent-orchestration]], [[agent-steering]], [[guardrails]], [[context-engineering]]

## Connections

Successor to [[openai-prompt-guidance-gpt-5-6]]. The blog post
[[openai-rethinking-skills-prompts-gpt-6-astra]] applies the same findings to
skills, `AGENTS.md`, and decision boundaries. The API features (async tools,
steering, multi-agent) are also exposed through the managed harness in
[[openai-agents-api-guide]].

## Contradictions / open questions

- **Tier durability.** [[openai-prompt-guidance-gpt-5-6]] records OpenAI's claim
  that Sol/Terra/Luna are "durable capability tiers". The GPT-6 lineup on this
  page has no Terra and adds Astra above Sol. The Aug–Oct 2026 changelog shows
  no `gpt-6-terra`. Flag this on the GPT-5.6 page.
- **Status of `gpt-6-sol`.** It was released 2026-09-22 but is not in the
  page's model picker. The page treats it only as a model to migrate from. Its
  current/legacy status is not stated.
- **Transfer to Sol and Luna.** The behaviors were observed on Astra. OpenAI
  asks readers to evaluate the prompts on their chosen model; no Sol- or
  Luna-specific behavior is documented.
