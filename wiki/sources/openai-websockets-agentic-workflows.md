---
title: "OpenAI (Eng): Speeding Up Agentic Workflows with WebSockets in the Responses API"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Brian Yu, Ashwin Nathan (OpenAI)
date: 2026-04-22
source_url: https://openai.com/index/speeding-up-agentic-workflows-with-websockets/
source_path: raw/openai-websockets-agentic-workflows.md
tags: [latency, responses-api, websockets, agent-loop, caching, codex, infrastructure]
---

# OpenAI (Eng): Speeding Up Agentic Workflows with WebSockets in the Responses API

> OpenAI Engineering post (2026-04-22) on WebSocket mode for the Responses API:
> a persistent connection with a connection-scoped cache of prior response
> state. OpenAI reports that it made API-driven agent loops about 40% faster end
> to end.

## Summary

An agent rollout is dozens of model-call and tool-call round trips. Each step's
latency has three parts: API service work, model inference, and client-side
tool execution and context building. OpenAI argues that when inference was slow
(about 65 tokens/s for GPT-5 and GPT-5.2 in the Responses API), API overhead was
hidden. With GPT-5.3-Codex-Spark on Cerebras hardware targeting over 1,000
tokens/s, the API became the bottleneck. A per-request optimization sprint
improved TTFT by about 45% but was not enough. The structural cause was that
each follow-up request reprocessed the full conversation.

The fix is WebSocket mode. The client keeps `response.create` and
`previous_response_id` unchanged. The server keeps the previous response, its
input and output items, tool definitions, and rendered tokens in an in-memory
cache scoped to the connection. Validators and some safety classifiers then
process only new input, and billing overlaps with the next request. Reported
results: Spark hit 1,000 tokens/s with bursts to 4,000, and Codex moved most of
its traffic to this mode. Third parties report gains of up to 40% (Vercel AI
SDK), 39% (Cline), and up to 30% (Cursor). The numbers are tied to the models
current in April 2026.

## Key points

- **Faster inference exposes harness and API overhead.** Agent-loop latency must
  be budgeted per stage, not only per token.
- **Stateless follow-ups cost more as conversations grow.** Caching reusable
  state across turns turns per-turn work from full-history to incremental.
- **Rejected prototype: one Response per rollout.** The sampling loop blocked
  after each tool call (`response.done`). The client returned results with
  `response.append`. This treated a local tool call like a hosted tool. It had
  the lowest overhead, but OpenAI rejected the unfamiliar API shape in favor of
  drop-in compatibility.
- **Transport choice:** WebSockets beat gRPC bidirectional streaming because a
  plain message transport left request and response shapes unchanged.

## Entities

[[openai]], [[openai-codex]], [[openai-agents-api]]

## Concepts

[[agent-harness]], [[context-engineering]], [[agent-orchestration]]

## Notable claims & data

- About 65 TPS (GPT-5, GPT-5.2) versus a target of over 1,000 TPS
  (GPT-5.3-Codex-Spark), with bursts to 4,000 TPS.
- About 45% TTFT improvement from the per-request sprint (started about
  November 2025). About 40% end-to-end agent-loop improvement from WebSocket
  mode.
- About a two-month build, then an alpha with coding-agent startups before
  general launch.

## Connections

- Server-side counterpart to [[anthropic-prompt-caching-is-everything]]. That
  post keeps cache hit rate high from the client by keeping the prefix static.
  This post caches rendered tokens and state on the server per connection.
- Extends the stateful `previous_response_id` design argued for in
  [[openai-why-we-built-responses-api]] and [[openai-one-year-of-responses]].
- Mid-turn steering over WebSocket is mentioned as a GPT-6 feature in
  [[openai-prompting-gpt-6-astra]].
- The loop being optimized is the Codex loop described in
  [[openai-unrolling-codex-agent-loop]] and [[openai-codex-as-a-platform]].
