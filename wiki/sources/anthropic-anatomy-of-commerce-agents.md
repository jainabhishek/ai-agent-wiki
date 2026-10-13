---
title: "Anthropic: A guide to the anatomy of effective commerce agents"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com articles) — Ali Shazal, Matthew Koen
date: 2026-09-02
source_url: https://claude.com/resources/articles/the-anatomy-of-effective-commerce-agents
source_path: raw/anthropic-anatomy-of-commerce-agents.md
tags: [agents, commerce, architecture, skills, tool-design, latency, prompt-caching, memory, guardrails, evals]
---

# Anthropic: A guide to the anatomy of effective commerce agents

> A field guide to consumer and merchant commerce agents. It covers one agent
> loop with skills, latency and cost techniques, memory, safety enforced in the
> harness, and snapshot evals.

## Summary

Anthropic's applied team (Ali Shazal, Matthew Koen) wrote this guide from a
year of production commerce deployments. It ships with a reference
implementation, `anthropics/commerce-agents`, which has a shopping agent and a
merchant agent. The architecture is one model in a standard agent loop, with
no intent router and no per-domain subagents. Skills cover the long tail, and
tools call the systems the company already runs. Part 2 treats latency as a
sum over turns and makes prompt caching the main cost lever. Part 3 covers
four production topics. Memory is an asynchronous extractor with three read
layers. Safety means the model only stages actions and the harness enforces
them. Evals are snapshots of constructed state. Multi-team ownership runs
through targeted CI. Model-specific mentions (Sonnet-class schema reliability,
Opus 5 vs Sonnet on cart tasks) are from September 2026.

## Key points

- **Skills, not subagents** (Part 1). Each handoff to a subagent loses state,
  can cost several times the tokens, and adds seconds of latency. The authors
  report that one agent with skills beat both a single prompt and a subagent
  design on quality, often at lower cost per task. Subagents fit only as tools
  for self-contained work, such as deep research that returns a compact
  answer. A hand-off fits a domain that already has its own agent. The test is
  who owns the conversation. See [[agent-skills]] and [[agent-orchestration]].
- **Prompt or skill by frequency.** Content relevant to about one third or more
  of traffic goes in the system prompt. The same applies to critical rules
  (safety, legal, brand, allergies). Other content goes in skills. If a signal
  such as the entry page predicts a skill, the harness injects the skill before
  the first model call.
- **Tools sit on core systems.** Tools call the existing search, cart, and
  inventory systems, and `search_products` returns results already ranked.
  Tools trim fields and return instructions, not error codes, on failure. See
  [[tool-design]].
- **UI components are tools** (`present_products`, ...). Tools are more
  reliable than custom markup tags, keep native history, and record what is on
  screen. The tradeoff is that streaming arrives per argument. The flag
  `eager_input_streaming: true` gives token-level streaming but drops the
  schema check, so the call needs a retry.
- **Latency = Σ(time to last token + tool time) over turns.** The levers are
  fewer turns, faster tools, and faster tokens. A smarter model can be faster
  when tasks take more than about 5 turns. Tools dispatch eagerly as their
  arguments complete, which cut gaps to a few hundred ms. Perceived latency
  drops with progressive rendering of a 500–700-token response and with
  progress lines.
- **Caching.** The target is a 90–99% hit rate. Cached reads cost one tenth of
  fresh input, writes cost about 1.25x, and cached reads are about 1.5–2x
  faster at ~100k tokens. The prefix has three segments: global, then session,
  then volatile. Skills load as tool results, and the cache breakpoint rolls
  forward each turn. See [[context-engineering]].
- **Model choice by sweep.** The sweep covers models and effort levels against
  quality floors and p50/p99 budgets. Each candidate's prompt gets tuned
  before that candidate is ruled out. The measure is cost per completed task.
  When results are close, choose intelligence.
- **Memory** (see [[agent-memory]]). Facts are typed records in the
  company's own database. An asynchronous extractor reads only user and
  assistant text and gave 13% higher recall than a save-memory tool. Reads
  happen in three layers: always in context, prefetched per turn, and behind
  a lookup tool. A validator on the write path, user deletion, a retention
  period, and a per-deployment switch govern the data.
- **Safety in the harness** (see [[guardrails]]). The model stages changes,
  and `apply_change` accepts only approved IDs, re-checked at apply time.
  Writes and renders accept only server-issued IDs. Caps apply to the
  resulting state, and writes are serialized per session. Third-party content
  passes through a sanitizer and gets a fence. Regulated copy comes from the
  server.
- **Evals** (see [[agent-evals]]). Evals are snapshots of constructed state
  graded on the outcome, not the path. Simulated-user evals serve only to
  discover cases. Cases encode tough preconditions, pair every positive with a
  negative, and cover cross-capability requests. A starting size is 50–100
  cases per flow, written with SMEs and drawn from real incidents.
- **Multi-team shipping.** Each skill or tool has one owner. Each change ships
  with its own cases. CI runs core and safety cases plus the cases the change
  touches, and gates on pass rate, cache hit rate, and cost per turn. Prompt
  and skill changes go to a canary first. Each skill has a kill switch, and
  changes freeze before peak periods.

## Connections

- Applies [[anthropic-eng-writing-tools-for-agents]],
  [[anthropic-prompt-caching-is-everything]], and
  [[anthropic-eng-demystifying-evals]] to one domain.
- Model-choice advice matches [[anthropic-choosing-claude-model]].
- The staged-change and approval pattern parallels
  [[anthropic-abc-legal-managed-agents]] and
  [[anthropic-building-effective-human-agent-teams]].
- Entities: [[anthropic]], [[claude-agent-sdk]] (eager dispatch by default),
  [[claude-managed-agents]] (tool-approval prompt).
