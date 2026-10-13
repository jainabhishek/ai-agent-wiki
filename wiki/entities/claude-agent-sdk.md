---
title: Claude Agent SDK
type: entity
subtype: product
created: 2026-06-21
updated: 2026-10-12
tags: [anthropic, sdk, agents, harness]
---

# Claude Agent SDK

> Anthropic's agent SDK (2025): a tuned agent **harness** — the middle stage
> between hand-rolled loops and fully managed agents.

## Overview

In the evolution traced by [[anthropic-evolution-of-agentic-surfaces]], the Agent
SDK provided a tuned harness over raw "tokens in, tokens out," but left deployment
complexity (sandboxing, sessions, secrets) to the developer — the gap later
closed by [[claude-managed-agents]]. The Anthropic counterpart to the
[[openai-agents-sdk]].

## Key facts

- **Renamed in September 2025.** On 2025-09-29 Anthropic renamed the Claude
  Code SDK to the Claude Agent SDK, because the harness behind [[claude-code]]
  now powered almost all of Anthropic's major agent loops, including non-coding
  work. (see [[anthropic-building-agents-claude-agent-sdk]])
- **"Give your agents a computer."** The core design principle: bash plus file
  tools let an agent work like a person. The loop is gather context → take
  action → verify work → repeat. Context comes first from agentic search over
  the file system, with semantic search added only when needed. Verification
  methods rank by robustness: rules-based feedback such as linting, then visual
  feedback from screenshots, then an LLM judge. (see
  [[anthropic-building-agents-claude-agent-sdk]], [[agent-harness]],
  [[context-engineering]], [[agent-evals]]) Anthropic's later loops guide
  describes the same cycle for Claude Code. (see
  [[anthropic-getting-started-with-loops]])
- A tuned **agent harness** rather than just an API. (see [[agent-harness]])
- Superseded for production deployment concerns by [[claude-managed-agents]],
  which decouples reasoning from execution.
- Provides automatic compaction: once Opus 4.5 removed "context anxiety", the
  long-running app harness dropped context resets for one continuous session
  with SDK compaction. (see [[anthropic-eng-harness-design-long-running-apps]])
- A **static** harness: the SDK and `claude -p` must stay generic, whereas
  Claude Code's dynamic workflows write a harness tailored to each task. (see
  [[anthropic-harness-for-every-task]])
- Claude Code's dedicated tools are callable from the SDK (the AskUserQuestion
  tool's composability was one reason to prefer a tool over a prompt format).
  (see [[anthropic-seeing-like-an-agent]])
- The `sonnet` alias resolves to Claude Sonnet 5.5 from Claude Code v2.1.284
  and Agent SDK for TypeScript v0.3.284 or later. (see
  [[anthropic-building-with-sonnet-5-5]])
- Skills work with the SDK. (see [[anthropic-complete-guide-building-skills]],
  [[agent-skills]]) By default the SDK dispatches each tool as soon as its
  arguments are complete, which Anthropic's commerce guide credits with cutting
  gaps between calls to a few hundred milliseconds. (see
  [[anthropic-anatomy-of-commerce-agents]])

### Adopters (self-reported case studies)
- **Cresta** uses the SDK as the execution harness for Conductor, an agent that
  builds customer-experience agents; Cresta adds policy, observability,
  verification, and feedback on top. (see [[anthropic-cresta-agent-builder]])
- **OffDeal** replaced 12+ fixed workflows with one general agent built from
  skills, relying on SDK subagents and automatic compaction. It reports an
  internal eval rising from 25% to 60% from the SDK switch alone. (see
  [[claude-customer-offdeal]])
- **Greptile** chose the SDK over a homegrown harness so a 10-engineer team
  could focus on review tools, arguing that models and harnesses are coupled.
  It uses hooks to guarantee every PR file is examined. (see
  [[claude-customer-greptile]])
- **Caylent** rebuilt its brittle homegrown migration harness on the SDK, with
  staged tool-scoped agents defined in markdown prompts. (see
  [[claude-customer-caylent]])
- **Spotify** runs "Honk", the SDK in a Kubernetes pod with internal tools and
  CI verification, and reports 73% of PRs AI-authored. (see
  [[claude-customer-spotify-boris-office-hours]])
- **Outtake** prototyped its cyber investigator in Claude Code, then moved to
  the SDK for control of memory, context, and filesystem without rebuilding the
  loop; skills carried over. (see [[anthropic-outtake-cyber-investigator]])
- Others on the SDK: eSentire's security-investigation platform and Vapi's
  Composer. (see [[claude-customer-esentire]], [[claude-customer-vapi]])

## Relationships

- Built by [[anthropic]]; predecessor surface to [[claude-managed-agents]];
  analogous to [[openai-agents-sdk]]. The harness/product split parallels the
  open [[openai-codex]] harness and its SDK. (see [[openai-codex-as-a-platform]])

## Appears in

- [[anthropic-evolution-of-agentic-surfaces]]
- [[anthropic-eng-effective-harnesses-long-running-agents]]
- [[anthropic-eng-agent-skills]]
- [[anthropic-eng-harness-design-long-running-apps]]
- [[anthropic-harness-for-every-task]]
- [[anthropic-seeing-like-an-agent]]
- [[anthropic-building-with-sonnet-5-5]]
- [[openai-codex-as-a-platform]]
- [[anthropic-building-agents-claude-agent-sdk]]
- [[anthropic-getting-started-with-loops]]
- [[anthropic-complete-guide-building-skills]]
- [[anthropic-anatomy-of-commerce-agents]]
- [[anthropic-cresta-agent-builder]]
- [[anthropic-outtake-cyber-investigator]]
- [[claude-customer-offdeal]]
- [[claude-customer-greptile]]
- [[claude-customer-caylent]]
- [[claude-customer-spotify-boris-office-hours]]
- [[claude-customer-esentire]]
- [[claude-customer-vapi]]

## Contradictions / open questions

- The harness case study ([[anthropic-eng-effective-harnesses-long-running-agents]])
  builds *on* the SDK but doesn't document the SDK itself.
  [[anthropic-building-agents-claude-agent-sdk]] (2025-09-29) now documents the
  design principle and loop, but the SDK reference docs remain a candidate for
  a dedicated source. That post is the oldest source in the wiki, and later
  sources update its compaction and subagent details.
