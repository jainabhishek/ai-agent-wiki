# Speeding up agentic workflows with WebSockets in the Responses API — OpenAI (raw capture)

> Source: https://openai.com/index/speeding-up-agentic-workflows-with-websockets/
> Publisher: OpenAI (Engineering) · Date: 2026-04-22
> Authors: Brian Yu, Ashwin Nathan.
> Captured: 2026-10-12 via built-in browser (condensed).

## Introduction

- A Codex bug fix means dozens of Responses API round trips: decide the next
  action, run a tool locally, send the tool output back, repeat.
- Latency in the Codex agent loop splits into three stages: API service work
  (validation, processing), model inference on GPUs, and client-side time
  (running tools, building context). When inference was slow, API overhead was
  hidden; as inference speeds up, cumulative API overhead across a rollout
  becomes visible.
- Result claimed: agent loops on the API became 40% faster end-to-end, so users
  could feel an inference jump from about 65 to nearly 1,000 tokens per second.
  Levers: caching, removing network hops, a faster safety stack, and, mainly, a
  persistent connection instead of a series of synchronous calls.

## When the API became the bottleneck

- Earlier flagship models (GPT-5, GPT-5.2) ran at roughly 65 TPS in the
  Responses API. The target for GPT-5.3-Codex-Spark, a fast coding model on
  Cerebras hardware, was over 1,000 TPS.
- A performance sprint starting around November 2025 cut single-request
  critical-path latency:
  - caching rendered tokens and model configuration in memory to skip
    tokenization and network calls on multi-turn responses;
  - calling the inference service directly, removing intermediate services
    (for example image-processing resolution);
  - faster safety classifiers to flag conversations.
- These gave close to 45% better time to first token (TTFT), but overhead was
  still too large relative to Spark's speed: users waited on API CPUs before
  reaching the GPUs.
- Structural cause: each Codex request was treated as independent, so
  conversation state and reusable context were reprocessed every follow-up, and
  the cost grew with conversation length.

## Building a persistent connection

- Idea: keep a persistent connection, send only new information, and cache
  reusable state in memory for the life of the connection.
- Options considered: WebSockets and gRPC bidirectional streaming. WebSockets
  won because, as a plain message transport, it does not change Responses API
  input and output shapes.
- First prototype (built by a Codex-team engineer running a Codex agent
  overnight): a whole agentic rollout modeled as one long-running Response.
  With asyncio, the sampling loop blocked after a tool call was sampled, the
  server sent `response.done`, the client ran the tool and sent
  `response.append` with the result, and sampling resumed.
- Analogy: a local tool call treated like a hosted tool call (for example web
  search), except that the call is sent to the client over the socket.
- Effect: pre-inference work once, pause for tools, post-inference work once at
  the end. Cost: an unfamiliar, more complex API shape that would force
  developers to rewrite integrations.

## Keeping the API familiar while making the stack incremental

- Launched shape: keep `response.create` with the same body and continue with
  `previous_response_id`.
- On a WebSocket connection the server keeps a connection-scoped in-memory cache
  of previous response state. A follow-up `response.create` with
  `previous_response_id` reads that cache instead of rebuilding the conversation.
- Cached state: the previous response object; prior input and output items;
  tool definitions and namespaces; reusable sampling artifacts such as rendered
  tokens.
- Optimizations this enabled:
  - some safety classifiers and request validators process only new input;
  - an appendable in-memory cache of rendered tokens skips re-tokenization;
  - model resolution and routing logic is reused across requests;
  - non-blocking post-inference work (for example billing) overlaps with the
    next request.
- Goal: approach the minimal-overhead prototype with an API shape developers
  already know.

## Setting a new bar for speed

- About a two-month sprint, then an alpha with coding-agent startups; alpha
  users reported up to 40% improvement in agentic workflows.
- At launch Codex moved most of its Responses API traffic to WebSocket mode.
  GPT-5.3-Codex-Spark hit the 1,000 TPS target, with bursts to 4,000 TPS.
  Users of GPT-5.3-Codex, GPT-5.4, and later models also benefit.
- Third-party reports cited: Vercel AI SDK latency down up to 40%; Cline
  multi-file workflows 39% faster; OpenAI models in Cursor up to 30% faster.
- OpenAI calls WebSocket mode one of the most significant Responses API
  capabilities since its March 2025 launch. The broader point: as inference gets
  faster, the systems around inference must speed up too.
