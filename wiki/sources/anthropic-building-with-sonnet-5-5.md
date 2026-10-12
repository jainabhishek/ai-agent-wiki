---
title: "Anthropic: Building with Claude Sonnet 5.5"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Addy Osmani (Anthropic, claude.dev blog)
date: 2026-09-28
source_url: https://claude.dev/blog/building-with-claude-sonnet-5-5/
source_path: raw/anthropic-building-with-sonnet-5-5.md
models: [claude-sonnet-5-5]
as_of: 2026-10-12
tags: [model-specific, anthropic, sonnet-5-5, migration, effort, thinking, pricing, refusals]
---

# Anthropic: Building with Claude Sonnet 5.5

> Anthropic's launch playbook for building on Claude Sonnet 5.5. It covers model
> choice against Opus 5.5, pricing, model specs, six migration steps from Sonnet 5,
> and tuning. It is the blog companion to the docs page
> [[anthropic-prompting-claude-sonnet-5-5]].

## Summary

**Applicability.** The post names the model ID `claude-sonnet-5-5` on the Claude
API, Claude Platform on AWS, Google Cloud, and Microsoft Foundry (Global Standard
deployments only). On Amazon Bedrock the ID is `anthropic.claude-sonnet-5-5`. In
Claude Code from v2.1.284, the `sonnet` alias resolves to this model on the Claude
API. The post presents Sonnet 5.5 as the second Claude 5.5 model after Opus 5.5.
Its claims against Sonnet 5: smarter, more efficient, and 30% faster, at the same
per-token price. The post says Sonnet 5.5 costs "up to 30% less for most work"
because it uses fewer tokens.

**Positioning.** Sonnet 5.5 is for well-scoped everyday coding, high-volume
development, polished documents, slides, and spreadsheets, and well-defined
repeated agent tasks (investigation, review, drafting). Opus 5.5 is for complex
judgment work, long-horizon agentic coding, and the hardest problems. Sonnet fits
best when the task has a clear spec and a way to check the result. Haiku 5.5 is
announced "in the coming weeks". See [[prompt-tuning-axes]].

## Key points

### Model details
- Context window: 1M tokens, native, no beta header.
- Max output: 128k tokens. Up to 300k on the Message Batches API with the
  `output-300k-2026-03-24` beta header.
- Knowledge cutoff: June 2026. The tokenizer is the same as Sonnet 5's.
- Thinking is on by default (adaptive). The effort levels are `low`, `medium`,
  `high`, `xhigh`, and `max`. The default effort is `high` on the Claude API and
  `medium` in Claude Code.
- The minimum cacheable prompt is **512 tokens** (Sonnet 5: 1,024). Rate limits
  are separate from Sonnet 5's, with the same default tier values. Priority Tier
  and zero data retention are available for eligible customers.
- Images use a high-resolution tier, up to 2576 px on the long edge. A 2000×1500
  image costs about 2.5x the tokens it costs on Sonnet 4.6, Sonnet 4.5, or Haiku
  4.5.

### Pricing (per million tokens; Sonnet 5.5 / Opus 5.5)
- Input: $2 / $4. Output: $10 / $20.
- Cache write: $2.50 / $5 (5-minute) and $4 / $8 (1-hour).
- Cache read: $0.20 for both models.
- All Sonnet 5.5 prices equal Sonnet 5's. US-only inference
  (`inference_geo: "us"`) costs 1.1x the standard price.

### Migration from Sonnet 5 (five breaking changes + one response-shape change)
1. **Thinking off → `between_tools`.** `thinking: {"type": "disabled"}` returns a
   400 error. Use `{"type": "between_tools"}`, which thinks only between tool
   calls. The post says total response time stays the same or gets faster. Its
   limits:
   - It works only at `low`, `medium`, or `high` effort. At `xhigh` or `max` it
     returns a 400 error.
   - It accepts no other field. Sending `display`, `budget_tokens`, or
     `block_binding` with it returns a 400 error.
   - Effort cannot change mid-conversation.
   - Progress-update `thinking` blocks still come back and must be passed back
     unchanged.
   - Use adaptive thinking for tool-less tasks that need a few steps of working
     out.
2. **Forced `tool_choice` (`any` or `tool`) returns a 400 error**, including on the
   token counting endpoint. Use `auto` plus `strict: true` on the tool, and say in
   the prompt when to use it. Strict tool use requires
   `additionalProperties: false` on every object.
3. **Append-only conversations.** Thinking blocks are bound to the model and the
   conversation. Sonnet 5.5 can read Sonnet 5's thinking blocks. No other model can
   read Sonnet 5.5's blocks.
4. **Computer use moves to `computer_toolset_20260801`** on the Claude API and
   Google Cloud. `computer_20251124` returns a 400 error there.
   - Drop the `computer-use-2025-11-24` beta header and the SDK `betas` parameter.
   - Handle member `tool_use` blocks, batch actions, and `toolset_name` on results.
   - Replace the `fine-grained-tool-streaming-2025-05-14` header with
     `eager_input_streaming: true` on each tool.
   - Bedrock still accepts `computer_20251124`.
5. **Advisor pairing.** A Sonnet 5.5 executor rejects Opus 4.8, Opus 4.7, and
   Sonnet 5 as advisors. It accepts Opus 5.5, Opus 5, and Sonnet 5.5. Advice from
   every accepted advisor comes back encrypted (`advisor_redacted_result`).
6. **Text between tool calls** comes back as progress-update `thinking` blocks,
   which are empty at the default `display`. Fix:
   - With adaptive thinking, set `display: "updates"` (beta,
     `thinking-display-updates-2026-08-18`) or `"summarized"`.
   - Render each non-empty block before the `tool_use` that follows it.
   - With `between_tools`, the text comes back without a `display` setting.

`/claude-api migrate this project to claude-sonnet-5-5` automates the model ID
swap and the breaking parameter changes. The post also lists three new features:
per-message effort (beta), mid-conversation system messages, and
mid-conversation tool changes (beta).

### Tuning
- **Re-run the effort sweep.** Levels are recalibrated against Sonnet 5.
  - Start at `high` by default.
  - For agentic coding or multistep tool use, start at `medium` for
    well-specified tasks and move to `high` for harder ones.
  - For chat and latency-sensitive work, use `medium` or `low`.
  - Use `xhigh` or `max` only where your evals show a gain. At those levels the
    post suggests you consider Opus 5.5 instead.
- For agentic coding, set `max_tokens` to 128,000 and stream the response, because
  thinking counts toward `max_tokens`. A prompt that asks the model to think less
  does not reliably reduce thinking; lower the effort level instead.
- **Remove Sonnet 5 workarounds** before tuning: refusal steering, tool-call retry
  shims, and lines such as "do not be lazy". Then re-run your evals.
- **Real checks at `low` effort.** At `low`, the model sometimes reports a change as
  done without a check that exercises it. The post reprints the docs' system-prompt
  paragraph for this case. The paragraph asks for:
  - a real check (tests, type-checker, build, or the changed command) before
    reporting done;
  - no credit for syntax-only checks or for check commands that failed to start;
  - missing dependencies installed only with the project's own package manager,
    never with sudo or the system package manager;
  - an explicit statement of any check that could not run, and why.
- **Do not ask for reasoning in the reply.** It invites `reasoning_extraction`
  declines. Read `display: "summarized"` thinking instead, and use
  `display: "updates"` for progress notes.
- **Caching.** A cache read costs a tenth of the input price. Changing the
  top-level effort between requests invalidates the cache. Per-message effort
  (beta) keeps the cache.

### Refusals and fallback
- A decline returns HTTP 200 with `stop_reason: "refusal"`. `stop_details` names
  one of five categories: `cyber`, `bio`, `frontier_llm`,
  `reasoning_extraction`, or `general_harms`.
- Server-side fallback (`fallbacks: "default"`, beta) retries only `cyber` and
  `frontier_llm` declines, on Sonnet 5.
- Sonnet 5.5 is the first Sonnet with cybersecurity safeguards similar to those
  on Anthropic's most capable models. The post says the Cyber Verification Program
  "will soon expand" to include Sonnet 5.5.

### In Claude Code
- From Claude Code v2.1.284 (Agent SDK for TypeScript v0.3.284 or later), `sonnet`
  resolves to Sonnet 5.5 on the Claude API.
- It runs at `medium` effort by default, with the 1M context window native.
- You cannot turn thinking off. There is no fast mode.
- `default` stays Opus 5.5. Use `/model sonnet` for well-scoped tasks.

## Notable claims & data

- Up to 30% lower cost for most work, and 30% faster, than Sonnet 5 (vendor claim,
  no methodology given).
- Customer quote (Epic Games): Sonnet 5.5 met a higher-tier quality bar with "less
  prescriptive prompting".
- On Anthropic's automated behavioral audit, Sonnet 5.5 matches or improves on
  Sonnet 5 on most alignment and honesty measures.

## Entities

[[anthropic]], [[claude]], [[claude-code]], [[claude-agent-sdk]]

## Concepts

[[prompt-tuning-axes]], [[agent-instructions]], [[tool-design]], [[agent-harness]],
[[context-engineering]]

## Connections

- **Comparison with the docs page [[anthropic-prompting-claude-sonnet-5-5]]**
  (compared against the docs capture downloaded 2026-10-12). **No disagreement was
  found.** The following points match: effort starting points and recalibration;
  the `max_tokens` = 128,000 advice; that prompting to think less is unreliable;
  the `between_tools` limits (effort ≤ `high`, no other fields, no mid-conversation
  effort change, use adaptive for tool-less reasoning); the verification paragraph
  (reprinted verbatim); the five refusal categories; and fallback that retries only
  `cyber` and `frontier_llm`. The two pages differ in scope.
  - *Only in the blog*: pricing, model specs, availability per platform,
    computer-use toolset migration, advisor pairing, the `tool_choice` change, the
    Claude Code defaults, and the claim that `between_tools` keeps total response
    time the same or faster.
  - *Only in the docs*: initiative and scope steering prompts, JSON-output
    reasoning tactics, mid-turn user-message placement (injection misreads),
    tolerant tool-call handling, crop/zoom tools for visual inputs, the
    progress-reminder harness pattern, and the Life Sciences Verification Program.
  - *Minor wording difference*: the blog says the Cyber Verification Program "will
    soon expand" to Sonnet 5.5. The docs say you "can apply" to it. This is
    probably a timing difference between the two publications.
- Predecessor pages: [[anthropic-prompting-claude-sonnet-5]]. Sibling:
  [[anthropic-getting-most-out-of-opus-5-5]], [[anthropic-prompting-claude-opus-5-5]].
- "Remove Sonnet 5 workarounds" continues the subtraction theme in
  [[anthropic-prompting-claude-opus-5]] and [[harnessing-claudes-intelligence]].
- The cost hillclimb in [[anthropic-automating-eval-design-hillclimbing]] used
  Sonnet 5, not Sonnet 5.5, at `low` effort.

## Contradictions / open questions

- _None recorded._ This page is scoped to `claude-sonnet-5-5`. It becomes stale by
  construction if Anthropic moves the model to its legacy list.
