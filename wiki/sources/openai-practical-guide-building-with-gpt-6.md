---
title: "OpenAI: A practical guide to building with GPT-6 (A model guide for the GPT-6 family)"
type: source
created: 2026-10-12
updated: 2026-10-13
author: OpenAI
date: 2026-10-02
source_url: https://openai.com/index/practical-guide-building-gpt-6/
source_path: raw/openai-practical-guide-building-with-gpt-6.md
models: [gpt-6-astra, gpt-6.1-sol, gpt-6-luna]
as_of: 2026-10-12
tags: [openai, gpt-6, model-specific, prompting, production, long-running-agents, computer-use]
---

# OpenAI: A practical guide to building with GPT-6

> OpenAI's business-facing guide (Oct 2, 2026) to choosing a GPT-6 model,
> instructing it, running long tasks, and preparing for production. It is a
> shorter, buyer-oriented companion to the API docs page
> [[openai-prompting-gpt-6-astra]].

## Summary

The Learning Hub lists this guide as "A practical guide to building with GPT-6".
The page itself is titled "A model guide for the GPT-6 family". Both names refer
to the same URL.

**Scope.** The guide addresses "the GPT-6 family" and names three models by
display name: GPT-6 Astra, GPT-6.1 Sol, and GPT-6 Luna. It never gives API model
IDs. The IDs in `models:` come from the API docs page
[[openai-prompting-gpt-6-astra]], not from this guide. Some statements are
scoped to one model: Ultrafast ("available for GPT-6 Astra"), Responses
multi-agent ("GPT-6.1 Sol supports…", beta), and Codex clarification-asking
("with GPT-6 Astra"). Computer use is stated for all three.

The guide has three parts. (1) **Production:** prompt caching, compaction,
monitoring, data controls, and a test-before-deploy step that measures cost per
successful task. (2) **Prompts and skills:** a clear assignment, four review
areas taken from [[openai-rethinking-skills-prompts-gpt-6-astra]], and an
explicit output contract. (3) **Long-running tasks:** steering, async tools,
delegation, Codex clarification, and computer use. Four customer testimonials
close the page; their results are self-reported.

## Key points

### Production
- Cut context the task does not need, but keep the evidence it needs. Run
  independent steps in parallel. See [[context-engineering]].
- Cached input costs "up to 95% less" than uncached input, depending on the
  model. Put stable instructions and reference material first, and keep tool
  definitions consistent. Include cache writes and long-context rates in cost
  estimates.
- Use compaction for long conversations. Decide on behavior monitoring (the link
  goes to the misalignment-monitoring guide) and on data controls.
- Before deploying, measure task success, latency, and **cost per successful
  task** on representative tasks. See [[agent-evals]].

### Model, effort, and speed
- Astra: hardest reasoning. GPT-6.1 Sol: complex coding, research, computer use.
  Luna: focused, repeated tasks at scale (invoice fields, classification,
  structured summaries).
- Effort ladder: Low (routine), Medium (judgment), High (hard debugging, careful
  review), Extra high / Max (test where supported, keep only if the gain pays
  for the time and cost). API effort can change mid-conversation without
  breaking the cache. In Codex, start at the model default.
- Fast mode (API): faster, more consistent responses at a higher per-token
  price. Ultrafast (Codex and API): faster token generation independent of
  effort, "available for GPT-6 Astra".
- List prices per the page (input / output / cached): Astra $10 / $50 / $1;
  6.1 Sol $2 / $10 / $0.10; Luna $0.10 / $0.50 / $0.01.

### Prompts and skills
- An Eric Provencher (OpenAI) quote says overly specific guidance can now hinder
  results. See [[prompt-tuning-axes]].
- A clear assignment states the result, the audience, context and constraints,
  and what counts as done.
- Four review areas: short skill descriptions with explicit triggers and
  on-demand detail ([[agent-skills]]); an `AGENTS.md` that says when documents
  and tests matter and authorizes safe routine workflows; decision boundaries
  that replace blanket "always ask" rules; and a prescriptive "done" (implement,
  run, inspect, fix failures). See [[agent-instructions]].
- Output contract: which decisions the model owns, when to ask, and the shape
  of a useful response. The example handoff covers what changed, what was
  checked, and what still needs attention.

### Long-running tasks
- API: mid-turn steering over the Responses WebSocket API queues updates; it does
  not cancel running tools or undo completed actions ([[agent-steering]]).
  Async tools let the model continue while a slow tool runs; dependent work
  must wait for the result. Multi-agent delegation in Responses (6.1 Sol, beta)
  ([[agent-orchestration]]).
- Codex: Astra may ask for clarification mid-run. Answer the questions that
  block the next step, and say which work can continue meanwhile and when to
  pause. Steer with what should change and what should stay. See
  [[openai-codex]].
- Computer use: prefer an API or connector when one can do the step; use
  computer use for screens, clicks, and forms. For your own app, give the model
  a code-running tool (Playwright for browsers, PyAutoGUI for desktop apps). See
  [[tool-placement]].

### Testimonials (self-reported)
- Harvey: more context gives better-structured legal drafts. Cognition: Devin
  returns evidence (simulator recording plus a passed/untested report). Hex:
  the model also checks whether its numbers make sense. Invideo: about 3x the
  success rate on color-grading tasks, and about 50 effects in one day.

## Comparison with the API docs page ([[openai-prompting-gpt-6-astra]])

**In this guide, not in the docs page:** per-model list prices; the "up to 95%"
cached-input discount; cost per successful task as a deploy metric; a task-type
mapping for each effort level; the Codex advice to start at default effort;
Playwright and PyAutoGUI as harness choices for computer use; the handoff shape
(changed / checked / open); and the customer testimonials.

**In the docs page, not in this guide:** API IDs; the `none` and `minimal` effort
restrictions; `configuration_update`, `async: true`, `call_id`, and
`prompt_cache_options.ttl` parameter names; the migration checklist; the
removal of `temperature`, `top_p`, and logprobs; data-residency limits; and
the five Astra behaviors with their prompt blocks. The behaviors are
formatting and stock phrases, under-delegation, over-testing, skill sensitivity,
and early stopping. The guide keeps only the decision-boundary and persistence
advice, through its summary of the skills post.

**Stated differently:**
- *Clarification-asking.* The docs page treats Astra's tendency to stop and ask
  as a behavior to counter, with prompts that push toward finishing the work.
  This guide presents mid-run clarification in Codex as a feature to manage:
  answer blocking questions, and name the work that may continue.
- *Ultrafast scope.* See Contradictions.
- *Multi-agent scope.* See Contradictions.
- *Steering semantics.* Both pages say completed work is kept. Only this guide
  adds that updates are queued and do not cancel running tools.

## Entities

[[openai]], [[openai-codex]], [[openai-agents-api]]

## Concepts

[[prompt-tuning-axes]], [[agent-instructions]], [[agent-skills]],
[[agent-steering]], [[agent-orchestration]], [[context-engineering]],
[[agent-evals]], [[tool-design]], [[tool-placement]], [[guardrails]]

## Notable claims & data

- List prices per the page (input / output / cached): Astra $10 / $50 / $1;
  6.1 Sol $2 / $10 / $0.10; Luna $0.10 / $0.50 / $0.01. The tagline calls
  6.1 Sol near-Astra intelligence "for a fifth of the price".
- Cached input costs "up to 95% less" than uncached input, depending on the
  model.
- The recommended pre-deploy metric is cost per successful task, measured
  together with task success and latency.
- Invideo (self-reported): about 3x the success rate on color-grading and
  correction tasks, and about 50 effects created in one day.

## Connections

Companion to [[openai-prompting-gpt-6-astra]] (API docs) and
[[openai-rethinking-skills-prompts-gpt-6-astra]] (its source for the four review
areas). Long-run mechanics overlap with [[openai-run-long-horizon-tasks-codex]]
and [[openai-codex-maxxing-long-running-work]]. Async tools, steering, and
multi-agent are also exposed through [[openai-agents-api-guide]].

## Contradictions / open questions

- **Ultrafast availability.** This guide says Ultrafast is "available for GPT-6
  Astra" and names no other model. The docs page's Limitations section gives
  Ultrafast data-residency terms for GPT-6.1 Sol too (US, EU, and global). The
  likely reading is that this guide is incomplete, not that 6.1 Sol lacks
  Ultrafast. This is unverified.
- **Multi-agent scope.** This guide says "GPT-6.1 Sol supports multi-agent
  workflows in the Responses API", currently in beta. The docs page lists
  multi-agent orchestration as carried over from GPT-5.6, with no model
  restriction. It is not stated whether Astra or Luna support Responses
  multi-agent.
- **Model IDs.** This page uses display names only. The mapping to
  `gpt-6-astra`, `gpt-6.1-sol`, and `gpt-6-luna` comes from the docs page.
