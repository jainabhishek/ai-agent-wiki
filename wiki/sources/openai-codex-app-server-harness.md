---
title: "OpenAI (Eng): Unlocking the Codex harness — how we built the App Server"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Celia Chen (OpenAI)
date: 2026-02-04
source_url: https://openai.com/index/unlocking-the-codex-harness/
source_path: raw/openai-codex-app-server-harness.md
tags: [openai, codex, agent-harness, app-server, json-rpc, protocol-design, mcp, primary-source]
---

# OpenAI (Eng): Unlocking the Codex harness — how we built the App Server

> Second post in OpenAI's Codex engineering series. It explains the Codex App
> Server: the bidirectional JSON-RPC protocol and long-lived process that
> expose one [[openai-codex]] harness to the web app, CLI, IDE extensions, the
> macOS app, and partner products.

## Summary

The App Server began as an internal shortcut. The VS Code extension needed the
TUI's agent loop with streaming progress, workspace exploration, and diffs.
OpenAI first tried exposing Codex as an MCP server, found MCP semantics a poor
fit, and wrote a JSON-RPC protocol that mirrored the TUI loop. Demand from
JetBrains, Xcode, and the desktop app (many agents in parallel) turned it into
a stable, **backward-compatible** platform surface. The post describes the
harness components, the process architecture, three conversation primitives
(item, turn, thread), three client-integration patterns, and how to choose
between App Server, MCP, cross-provider protocols, `codex exec`, and the Codex
SDK. See [[agent-harness]].

## Key points

- **Harness = loop + three services.** Thread lifecycle and persistence
  (create, resume, fork, archive; event history persisted for reconnects),
  config and auth (including "Sign in with ChatGPT"), and tool execution and
  extensions (sandboxed shell/file tools; MCP servers and skills under one
  policy model). All of it lives in **Codex core**, a library plus a runtime
  for one thread.
- **Process architecture.** Four components: stdio reader, Codex message
  processor, thread manager, core threads (one core session per thread). The
  reader and processor translate JSON-RPC into core operations and collapse
  core's low-level events into a **small set of stable, UI-ready
  notifications**.
- **Bidirectional.** The server can send requests, such as an approval, and
  pause the turn until the client answers allow or deny. See [[guardrails]].
- **Primitives.** *Item*: typed atomic unit (user message, agent message,
  tool execution, approval request, diff) with lifecycle `item/started` →
  optional `item/*/delta` → `item/completed`. *Turn*: one unit of work from
  one user input. *Thread*: durable container of turns.
- **Handshake.** The client sends exactly one `initialize` request first; the
  server advertises capabilities and both sides agree on protocol version,
  feature flags, and defaults.
- **Transport.** "JSON-RPC lite" (no `"jsonrpc": "2.0"` header) framed as
  JSONL over stdio. Bindings via `codex app-server generate-ts` or
  `codex app-server generate-json-schema`; clients exist in Go, Python,
  TypeScript, Swift, and Kotlin.
- **Three client patterns.** Local apps and IDEs run a pinned App Server
  binary as a child process (Xcode can point a stable client at a newer
  server). Codex Web runs the App Server inside the workspace container; the
  browser gets events over HTTP and SSE, and server-side thread state survives
  closed tabs. The TUI, formerly in-process, will become an ordinary client so
  it can attach to a remote Codex server.
- **Choosing an integration.** App Server is the default and first-class
  option. Codex as an MCP server (`codex mcp-server`) loses richer session
  semantics such as diff updates. Cross-provider harness protocols converge on
  the common subset of capabilities. `codex exec` suits CI and one-off
  non-interactive runs; the TypeScript Codex SDK predates App Server and has a
  smaller surface.

## Entities

[[openai]], [[openai-codex]], [[openai-agents-sdk]]

## Concepts

[[agent-harness]], [[model-context-protocol]], [[guardrails]],
[[agent-orchestration]], [[context-engineering]]

## Notable claims & data

- Claim: Codex can write much of a client binding when given the JSON schema
  and docs; many partner teams reached a working integration quickly this way.
- MCP was judged too narrow for an interactive agent UI; this is a design
  judgement by OpenAI, not a measured comparison.

## Connections

- **Primary source behind** [[openai-codex-as-a-platform]] (2026-08-19), which
  presents the same three layers (`codex exec`, SDK, app-server) to external
  builders. The two agree; this post adds the internals and the reasons.
- **Same bet as Anthropic on stable interfaces.** "A small set of stable
  notifications" plus backward compatibility matches the "interfaces are the
  stable part, not the harness" design of [[anthropic-eng-scaling-managed-agents]].
- **Layout differs from Anthropic's.** Codex Web runs the harness process
  inside the workspace container. [[anthropic-eng-scaling-managed-agents]]
  describes that co-located layout as the first design that became a "pet"
  and moved the harness out of the sandbox. OpenAI relies on persisted thread
  history for reconnection; the post does not say whether a thread survives
  loss of its container. Open question, not a contradiction of fact.
- Thread history is stored apart from the model `input`, which compaction
  rewrites (see [[openai-unrolling-codex-agent-loop]]). This supports "the
  session is not the context window" in [[anthropic-eng-scaling-managed-agents]].
- The MCP-server option complements [[model-context-protocol]]: MCP fits
  "call an agent as a tool", not "render an agent's live session".
