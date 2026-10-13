# Unlocking the Codex harness: how we built the App Server — OpenAI (Engineering) (raw capture)

> Source: https://openai.com/index/unlocking-the-codex-harness/
> Publisher: OpenAI (Engineering) · Date: 2026-02-04 · Author: Celia Chen (Member of the Technical Staff); contributors Michael Bolin, Owen Lin, Eric Traut, Rasmus Rygaard
> Captured: 2026-10-12 via built-in browser (get_page_text) (condensed). openai.com returns HTTP 403 to curl and WebFetch.

Page headings: Origin of the App Server · Inside the Codex harness · The
conversation primitives · Integrating with clients (Local Apps & IDEs; Codex
Web; TUI/Codex CLI) · Choosing the right protocol (JSON-RPC protocols: Codex as
an MCP server; Cross-provider agent harness protocols; Codex App Server) ·
Other ways to Embed Codex (Codex Exec; Codex SDK) · Taking this forward.
Diagrams are images; their content is described in prose.

## Intro

- Codex surfaces: web app, CLI, IDE extension, and the new Codex macOS app.
  All run the same **Codex harness** (agent loop and logic). The link between
  them is the **Codex App Server**, a client-friendly, bidirectional JSON-RPC
  API.
- Use cases named: turn Codex into a code reviewer, an SRE agent, or a coding
  assistant.

## Origin of the App Server

- Codex CLI began as a TUI. The VS Code extension needed the same agent loop
  from an IDE UI without re-implementation, with interaction beyond
  request/response: workspace exploration, streaming progress while the agent
  reasons, emitting diffs.
- OpenAI first tried exposing Codex as an **MCP server**; keeping MCP
  semantics sensible for VS Code proved difficult. They instead built a
  JSON-RPC protocol mirroring the TUI loop: the unofficial first App Server,
  not designed as a stable API.
- Demand grew: JetBrains and Xcode wanted an IDE-grade agent; the Codex desktop
  app needed to orchestrate many agents in parallel. Requirements became: easy
  to integrate and **backward compatible** (protocol evolves without breaking
  clients).

## Inside the Codex harness

- Beyond the core agent loop, the harness provides:
  1. **Thread lifecycle and persistence** — create, resume, fork, archive
     threads; persist event history so clients reconnect and render a
     consistent timeline.
  2. **Config and auth** — load config, manage defaults, run auth flows like
     "Sign in with ChatGPT", hold credential state.
  3. **Tool execution and extensions** — run shell/file tools in a sandbox;
     wire MCP servers and skills into the loop under one policy model.
- **Codex core**: the part of the Codex CLI codebase holding all agent logic.
  It is both a library and a runtime that runs the loop and persists one
  thread.
- The **App Server** is both the JSON-RPC protocol and a long-lived process
  hosting core threads. Four components: stdio reader, Codex message
  processor, thread manager, core threads. The thread manager starts one core
  session per thread; the message processor talks to each session directly.
- One client request can yield many events. The stdio reader and message
  processor translate JSON-RPC requests into core operations and turn core's
  low-level internal events into a **small set of stable, UI-ready JSON-RPC
  notifications**.
- Fully bidirectional: the server can send requests (e.g. an approval) and
  pause the turn until the client answers.

## The conversation primitives

- An agent-loop API is not plain request/response; one request unfolds into
  input, incremental progress, and artifacts (e.g. diffs). Three primitives:
  1. **Item** — atomic unit of input/output; typed (user message, agent
     message, tool execution, approval request, diff). Lifecycle:
     `item/started` → optional `item/*/delta` (streaming types) →
     `item/completed` with terminal payload. Clients render on started, stream
     on delta, finalize on completed.
  2. **Turn** — one unit of agent work started by user input (e.g. "run tests
     and summarize failures"); ends when the agent finishes outputs for that
     input; contains a sequence of items.
  3. **Thread** — durable container for an ongoing session; holds multiple
     turns; created, resumed, forked, archived; history persisted.
- **Initialize handshake**: the client must send one `initialize` request
  before any other method; the server responds. This lets the server
  advertise capabilities and both sides agree on protocol version, feature
  flags, and defaults. Example from the VS Code extension: `method:
  "initialize"`, `id: 0`, `params.clientInfo` with `name: "codex_vscode"`,
  `title: "Codex VS Code Extension"`, `version: "0.1.0"`. The server returns
  `result.userAgent` (e.g. `codex_vscode/0.94.0-alpha.7 (Mac OS 26.2.0; arm64)
  vscode/2.4.22 (codex_vscode; 0.1.0)`).
- Flow: client creates a thread then a turn; server sends `thread/started` and
  `turn/started`; inputs (user message) come back as items; tool calls come
  back as items; the server may send an approval request that pauses the turn
  until the client replies allow or deny; the agent message streams as delta
  events until `item/completed`; the turn ends with `turn/completed`.
- Full-turn JSON can be seen with the repo's test client:
  `codex debug app-server send-message-v2 "run tests and summarize failures"`.

## Integrating with clients

- Three patterns: local apps and IDEs, Codex web runtime, TUI. Transport in
  all three: **JSON-RPC over stdio (JSONL)**. Clients exist in Go, Python,
  TypeScript, Swift, Kotlin.
- Bindings: `codex app-server generate-ts` generates TypeScript definitions
  from the Rust protocol; `codex app-server generate-json-schema` emits a JSON
  Schema bundle for other code generators.

### Local Apps & IDEs

- Clients bundle or fetch a platform-specific App Server binary, launch it as a
  long-running child process, and keep a bidirectional stdio channel. The VS
  Code extension and desktop app pin a tested binary version.
- Some partners (Xcode) keep the client stable and point it at a newer App
  Server binary, adopting server-side fixes (e.g. better auto-compaction in
  Codex core, new config keys) without a client release. The JSON-RPC surface
  is backward compatible so older clients can talk to newer servers.

### Codex Web

- Runs the harness in a container: a worker provisions a container with the
  checked-out workspace, launches the App Server inside, and holds a
  long-lived JSON-RPC over stdio channel. The browser talks to the Codex
  backend over HTTP and SSE, which streams task events from the worker.
- Web sessions are ephemeral, so the browser cannot be the source of truth.
  State and progress live on the server; work continues if the tab closes;
  saved thread sessions let a new session reconnect and catch up.

### TUI/Codex CLI

- Historically the TUI ran in-process with the agent loop and used Rust core
  types directly — fast early iteration, but a special case.
- Plan: refactor the TUI to be an ordinary App Server client (child process,
  JSON-RPC over stdio). This enables connecting the TUI to a Codex server on a
  remote machine, so the agent stays near compute and keeps working if the
  laptop sleeps, with live local updates and controls.

## Choosing the right protocol

- App Server is the first-class integration OpenAI will maintain and the
  default recommendation; other methods have more limited functionality.

### JSON-RPC protocols

- **Codex as an MCP server** — `codex mcp-server`, connect from any stdio MCP
  client (e.g. OpenAI Agents SDK). Fits existing MCP workflows that call Codex
  as a tool. Downside: only what MCP exposes; richer session semantics (e.g.
  diff updates) may not map cleanly.
- **Cross-provider agent harness protocols** — portable interfaces across
  model providers and runtimes; good for one abstraction coordinating many
  agents. Tradeoff: they tend toward the common subset of capabilities, so
  provider-specific tool and session semantics are hard to represent. OpenAI
  expects common standards to emerge; skills cited as an example.
- **Codex App Server** — full harness as a stable, UI-friendly event stream,
  plus Sign in with ChatGPT, model discovery, config management. Cost: you
  build the client-side JSON-RPC binding; Codex itself can do much of this
  when given the JSON schema and docs.

## Other ways to Embed Codex

- **Codex Exec** — lightweight, scriptable, non-interactive CLI mode for
  one-off tasks and CI; runs to completion, streams structured output for
  logs, exits with clear success/failure.
- **Codex SDK** — TypeScript library to control local Codex agents from your
  app; shipped before App Server, so fewer languages and a smaller surface.
  OpenAI may add SDKs that wrap the App Server protocol.

## Taking this forward

- All source is in the Codex CLI open-source repo; OpenAI invites feedback.

## Footnotes

1. "JSON-RPC lite": keeps request/response/notification shape but omits the
   `"jsonrpc": "2.0"` header and is framed as JSONL over stdio, not strict
   JSON-RPC 2.0.
2. "stdio" in Codex Web means the app-server's stdin/stdout inside the
   container, often tunneled over a persistent network connection
   (WebSocket-like) to the container runtime.
