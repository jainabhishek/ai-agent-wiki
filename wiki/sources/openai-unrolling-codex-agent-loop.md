---
title: "OpenAI (Eng): Unrolling the Codex agent loop"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Michael Bolin (OpenAI)
date: 2026-01-23
source_url: https://openai.com/index/unrolling-the-codex-agent-loop/
source_path: raw/openai-unrolling-codex-agent-loop.md
tags: [openai, codex, agent-harness, agent-loop, responses-api, prompt-caching, compaction, primary-source]
---

# OpenAI (Eng): Unrolling the Codex agent loop

> First post in OpenAI's engineering series on the [[openai-codex]] harness. It
> walks through one agent loop request by request: how Codex CLI builds the
> Responses API payload, how a turn grows, and how Codex protects the prompt
> cache and the context window.

## Summary

The post defines the **Codex harness** as the core agent loop and execution
logic under every Codex surface (CLI, Cloud, VS Code extension). The loop is
the standard one: the model either answers or requests a tool call; the
harness runs the tool, appends the output, and re-queries until the model
emits an assistant message, which ends the **turn**. A conversation is a
**thread**. Codex CLI talks to any endpoint that implements the Responses
API (see [[openai-why-we-built-responses-api]]): the ChatGPT backend, the public
API, local gpt-oss through ollama or LM Studio, or Azure. The post then shows
the exact request layout, the event stream, and two efficiency concerns:
prompt-cache hits and context-window compaction. The named model files (for
example `gpt-5.2-codex_prompt.md`) date the post to January 2026. See
[[agent-harness]] and [[context-engineering]].

## Key points

- **Three request fields.** `instructions` (from `model_instructions_file` in
  `~/.codex/config.toml`, else the model's bundled `base_instructions`),
  `tools` (Codex tools such as `shell` and `update_plan`, hosted tools such as
  `web_search`, and MCP tools), and `input` (a list of typed items).
- **Fixed prelude in `input`.** Before the user message, Codex inserts: a
  `developer` message describing the sandbox (it covers only the Codex shell
  tool; MCP tools must enforce their own guardrails); optional
  `developer_instructions`; optional aggregated user instructions from
  `AGENTS.md` / `AGENTS.override.md` files (root to cwd, 32 KiB default limit)
  plus skill metadata; and an `<environment_context>` message with cwd and
  shell. See [[agent-instructions]] and [[agent-skills]].
- **Server owns the first three prompt slots.** An OpenAI Responses API server
  orders the prompt as system message, tools, instructions, then `input`.
- **Exact-prefix growth.** Each request appends `reasoning`, `function_call`,
  and `function_call_output` items, so the old prompt is an exact prefix of
  the new one. This is deliberate, for prompt caching.
- **Stateless by choice.** Codex does not use `previous_response_id`, to keep
  requests stateless and support Zero Data Retention (ZDR). Encrypted
  reasoning (`encrypted_content`) still carries across turns, because OpenAI
  keeps the ZDR customer's decryption key but not the data.
- **Cache-miss causes.** Changing tools, the target model, the sandbox
  configuration, the approval mode, or the cwd mid-conversation. An early MCP
  bug listed tools in an unstable order. `notifications/tools/list_changed`
  mid-conversation forces an expensive miss.
- **Append, do not edit.** Config changes become new messages: a new
  `developer` permissions message, or a new `user` environment-context
  message. See [[agent-harness]].
- **Compaction.** First a manual `/compact` that summarized via a normal
  request; now the `/responses/compact` endpoint returns replacement items
  including an opaque encrypted `type=compaction` item. Codex calls it
  automatically past `auto_compact_limit`.

## Entities

[[openai]], [[openai-codex]]

## Concepts

[[agent-harness]], [[context-engineering]], [[agent-instructions]],
[[agent-skills]], [[model-context-protocol]], [[guardrails]],
[[agent-core-components]]

## Notable claims & data

- The agent loop is quadratic in JSON sent; with cache hits, sampling cost is
  linear. Sampling cost dominates network cost.
- Endpoints: `https://chatgpt.com/backend-api/codex/responses` (ChatGPT login),
  `https://api.openai.com/v1/responses` (API key),
  `http://localhost:11434/v1/responses` (`--oss`, ollama 0.13.4+ or LM Studio
  0.3.39+).
- Related Codex PRs for ZDR: #642 and #1641.

## Connections

- **Cross-vendor convergence on cache discipline.** The cache-miss list and
  the append-only rule match the Claude Code team's practice in
  [[anthropic-prompt-caching-is-everything]] (static-first layout, no model or
  tool-set swaps mid-session, changes sent as messages). The two vendors
  reached the same rules independently.
- **Intra-OpenAI tradeoff.** [[openai-shell-skills-compaction]] recommends
  passing `previous_response_id` on long runs; this post explains why Codex
  avoids it (statelessness and ZDR). Both are valid; the choice depends on
  data-retention needs. See also [[openai-why-we-built-responses-api]].
- Follow-up posts: [[openai-codex-app-server-harness]] (how the harness is
  exposed to clients) and [[openai-responses-api-computer-environment]]
  (server-side loop, hosted shell, native compaction).
- Compaction here rewrites only the `input`; the thread's event history is
  stored separately (see [[openai-codex-app-server-harness]]). This agrees with
  the "session is not the context window" argument in
  [[anthropic-eng-scaling-managed-agents]].
