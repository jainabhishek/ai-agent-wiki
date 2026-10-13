---
title: "OpenAI: Why We Built the Responses API"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Steve Coffey, Prashant Mital (OpenAI Developers blog)
date: 2025-09-22
source_url: https://developers.openai.com/blog/responses-api
source_path: raw/openai-why-we-built-responses-api.md
tags: [openai, responses-api, api-design, reasoning-state, hosted-tools, agent-loop]
---

# OpenAI: Why We Built the Responses API

> OpenAI's design rationale for `/v1/responses`: an API built as an agentic
> loop that keeps encrypted reasoning state across turns, emits typed output
> items, and runs hosted tools server-side.

## Summary

[[openai]] traces its API history: `/v1/completions`, then
`/v1/chat/completions` with roles, then function calling and the Assistants API
beta. The post says Assistants never reached mass adoption because its design
was limiting. `/v1/responses` was meant to combine Chat Completions' simplicity
with Assistants' power, for multimodal and reasoning models. The core argument:
Responses is an **agentic loop**, not a chat turn. It keeps the model's
reasoning state between turns, encrypted and hidden from the client, which
Chat Completions drops. **Model dependence:** written for the GPT-5 launch
(2025-09-22). The TAUBench +5% and 40–80% cache figures are GPT-5-era internal
benchmarks. The wiki later records the Assistants API shutdown on 2026-08-26
([[openai]]).

## Key points

- **Reasoning state persists.** Continue a run with `previous_response_id` or by
  passing reasoning items back. Raw chain of thought is never exposed. OpenAI
  cites hallucination, harmful-content, and competitive risks, plus CoT
  monitorability. See [[context-engineering]].
- **Typed, ordered output items.** Chat Completions returns one `message` with a
  `tool_calls` array, so the order of text and calls is unclear. Responses
  returns a list of polymorphic items (`reasoning`, `message`, `function_call`),
  so the order of actions is explicit. See [[tool-design]].
- **Hosted tools run server-side.** `file_search`, `code_interpreter`, web
  search, image generation, and MCP execute without a round trip through the
  developer's backend. See [[model-context-protocol]] and
  [[agent-core-components]].
- **Stateful by default.** Conversation and tool state are tracked
  automatically.
- **Developer ergonomics:** semantic streaming events, internally-tagged
  polymorphism, `output_text` SDK helper, and regrouped multimodal and
  reasoning parameters.
- **Chat Completions stays.** It "isn't going away", but Responses is expected
  to become the default, as Chat Completions replaced Completions.

## Entities

[[openai]], [[openai-agents-api]], [[openai-agents-sdk]]

## Concepts

[[agent-core-components]], [[agent-orchestration]], [[tool-design]],
[[context-engineering]], [[model-context-protocol]]

## Notable claims & data

- GPT-5 via Responses scores 5% higher on TAUBench than via Chat Completions,
  attributed to preserved reasoning alone (internal, no method given).
- 40–80% better cache utilization than Chat Completions (internal benchmarks),
  claimed to lower latency and cost.
- Chat Completions was reportedly built in one weekend.

## Contradictions / open questions

- This post (2025-09-22) says Chat Completions is not going away. The later
  [[openai-prompting-gpt-6-astra]] records that tool calling on GPT-6 requires
  Responses. Both can hold: the endpoint remains, but newer models gate agentic
  features to Responses.

## Connections

- The design rationale behind the case studies in
  [[openai-one-year-of-responses]], and the runtime under
  [[openai-agents-api-guide]] and [[openai-shell-skills-compaction]]
  (`previous_response_id` reuse on long runs).
- Server-side state parallels the durable session in
  [[anthropic-eng-scaling-managed-agents]]; both keep state outside the client.
