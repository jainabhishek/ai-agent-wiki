# Unrolling the Codex agent loop — OpenAI (Engineering) (raw capture)

> Source: https://openai.com/index/unrolling-the-codex-agent-loop/
> Publisher: OpenAI (Engineering) · Date: 2026-01-23 · Author: Michael Bolin (Member of the Technical Staff)
> Captured: 2026-10-12 via built-in browser (get_page_text) (condensed). openai.com returns HTTP 403 to curl and WebFetch.

Page headings (table of contents): The agent loop · Model inference · Building
the initial prompt · The first turn · Performance considerations · Coming next.
Diagrams are images; their content is described in prose below.

## Intro

- Codex CLI is OpenAI's cross-platform local software agent; first launched in
  April (2025). This is the first post in a series on how Codex works. Source
  code and design history: `github.com/openai/codex` (issues and PRs record
  many design decisions).
- Topic: the agent loop, the core logic that orchestrates user, model, and the
  tools the model invokes. The post calls the agent the "harness".
- Terminology: "Codex" covers Codex CLI, Codex Cloud, and the Codex VS Code
  extension. The post covers the **Codex harness**: the core agent loop and
  execution logic under all Codex experiences, surfaced through Codex CLI.
  The post uses "Codex" and "Codex CLI" interchangeably.

## The agent loop

- Steps: user input goes into the prompt; the agent queries the model
  (inference: text → input tokens → sampled output tokens → text, streamed);
  the model either (1) returns a final response or (2) requests a tool call
  (e.g. run `ls`). For (2) the agent runs the tool, appends output to the
  prompt, and re-queries. The loop repeats until the model emits an
  **assistant message** instead of tool calls.
- The assistant message may answer the request or ask a follow-up question.
- A software agent's main output is often code edits on the machine, but every
  turn ends with an assistant message, which marks the loop's termination
  state; control returns to the user.
- One user-input-to-agent-response cycle is a **turn**; a conversation is a
  **thread** in Codex. A turn can contain many inference/tool iterations.
- Each new user message carries the full prior history (messages and tool
  calls) in the prompt, so the prompt grows. The context window bounds input
  plus output tokens per inference call; hundreds of tool calls in one turn can
  exhaust it. Context window management is one of the agent's
  responsibilities.

## Model inference

- Codex CLI sends HTTP requests to the **Responses API**. The endpoint is
  configurable; any endpoint implementing the Responses API works:
  - ChatGPT login: `https://chatgpt.com/backend-api/codex/responses`
  - API-key auth with OpenAI hosted models: `https://api.openai.com/v1/responses`
  - `--oss` with gpt-oss on ollama 0.13.4+ or LM Studio 0.3.39+: defaults to
    `http://localhost:11434/v1/responses`
  - Cloud-provider-hosted Responses API, e.g. Azure.

## Building the initial prompt

- The client does not write the prompt verbatim. It sends typed inputs; the
  Responses API server structures them into the prompt. Think of the prompt as
  a list of items.
- Each item has a role; priority order, highest first: `system`, `developer`,
  `user`, `assistant`.
- Three request parameters in focus:
  - `instructions` — system (or developer) message. In Codex it comes from
    `model_instructions_file` in `~/.codex/config.toml` if set, else the
    model's `base_instructions`. Model-specific instructions are bundled in the
    CLI from the repo (example: `gpt-5.2-codex_prompt.md`).
  - `tools` — tool definitions per the Responses API schema: Codex CLI tools,
    Responses-API-provided tools, and user tools (usually via MCP servers).
    Example list: `shell` (function; params `command` array [required],
    `workdir`, `timeout_ms`; `strict: false`); `update_plan` (function; params
    `plan` [required], `explanation`); `web_search` (hosted tool,
    `external_web_access: false`); an MCP tool named
    `mcp__weather__get-forecast` (params `latitude`, `longitude`).
  - `input` — list of text, image, or file items.
- Items Codex inserts into `input` before the user message, in order:
  1. `role=developer` message describing the sandbox. It applies **only to
     the Codex-provided shell tool**; other tools, including MCP tools, are not
     sandboxed by Codex and must enforce their own guardrails. Built from
     bundled Markdown snippets such as `workspace_write.md` and
     `on_request.md`, wrapped in `<permissions instructions>`: sandbox file
     permissions and network access, when to ask the user for permission to
     run a shell command, and the list of writable folders.
  2. Optional `role=developer` message with `developer_instructions` from
     `config.toml`.
  3. Optional `role=user` message of aggregated "user instructions"; more
     specific instructions come later:
     - `AGENTS.override.md` and `AGENTS.md` in `$CODEX_HOME`.
     - Subject to a limit (32 KiB by default), each folder from the Git/project
       root of the cwd down to the cwd: contents of `AGENTS.override.md`,
       `AGENTS.md`, or any filename in `project_doc_fallback_filenames`.
     - If skills are configured: a short skills preamble, each skill's
       metadata, and a section on how to use skills.
  4. `role=user` message with `<environment_context>` giving `<cwd>` and
     `<shell>` (e.g. `zsh`).
  Then the user message is appended.
- Each input element is a JSON object with `type` (e.g. `message`), `role`, and
  `content` (e.g. `[{"type":"input_text","text":...}]`).
- Codex POSTs the payload with an `Authorization` header that depends on the
  endpoint config in `~/.codex/config.toml`, plus any configured extra headers
  and query parameters.
- On an OpenAI Responses API server, the prompt order is: system message
  (server-controlled content), then tools, then instructions (both
  client-controlled), then the `input` items. The server decides the order of
  the first three; a custom Responses API implementation could choose
  differently.

## The first turn

- The server replies with a Server-Sent Events (SSE) stream; each event's
  `type` starts with `response`, e.g. `response.reasoning_summary_text.delta`,
  `response.reasoning_summary_text.done`, `response.output_item.added`,
  `response.output_text.delta`, `response.completed`.
- Codex republishes events as internal event objects for clients.
  `response.output_text.delta` drives UI streaming; items like
  `response.output_item.added` become objects appended to the next request's
  input.
- Example: two `response.output_item.done` events (a `reasoning` item with
  `summary` and `encrypted_content`, and a `function_call` to `shell` with
  `arguments` and `call_id`) are appended to the input, followed by a
  `function_call_output` item with the matching `call_id`.
- The old prompt is an **exact prefix** of the new prompt, by design, to get
  prompt caching.
- The turn ends with `response.output_text.done` and `response.completed`.
  The CLI shows the assistant message and focuses the composer. A new user
  message appends both the prior assistant message (`output_text`) and the new
  user message (`input_text`) to the input; the input keeps growing.

## Performance considerations

- The agent loop is quadratic in JSON sent over a conversation. The Responses
  API offers optional `previous_response_id` to mitigate this; Codex does not
  use it, to keep every request stateless and to support **Zero Data Retention
  (ZDR)**. Storing state for `previous_response_id` conflicts with ZDR.
- ZDR customers still benefit from prior-turn reasoning: `encrypted_content`
  is decrypted on the server. OpenAI keeps a ZDR customer's decryption key but
  not their data. Related Codex PRs: #642 and #1641.
- Sampling cost dominates network cost, so efficiency work targets sampling.
  With prompt-cache hits, sampling is linear rather than quadratic. Cache hits
  need exact prefix matches: static content (instructions, examples, images,
  tools) first, variable content last; tools and images must be identical.
- Cache-miss causes in Codex:
  - changing the available tools mid-conversation;
  - changing the target model (this changes the third prompt item, the
    model-specific instructions);
  - changing sandbox configuration, approval mode, or cwd.
- Example bug: early MCP support enumerated tools in an inconsistent order,
  causing cache misses. MCP servers can change their tool list at runtime via
  `notifications/tools/list_changed`; honoring it mid-conversation causes an
  expensive cache miss.
- Mid-conversation config changes are appended as new messages rather than
  editing earlier ones: a new `role=developer` `<permissions instructions>`
  message for sandbox/approval changes; a new `role=user`
  `<environment_context>` message for cwd changes.
- Context window: compact once tokens exceed a threshold, replacing `input`
  with a smaller representative item list. Early version: user-invoked
  `/compact`, which queried the Responses API with the conversation plus custom
  summarization instructions and used the summary assistant message as the new
  input.
- Now: the Responses API `/responses/compact` endpoint returns a replacement
  item list including a `type=compaction` item with opaque `encrypted_content`
  that preserves the model's latent understanding of the conversation. Codex
  calls it automatically when `auto_compact_limit` is exceeded.

## Coming next

- Planned posts: the CLI architecture, how tool use is implemented, and Codex's
  sandboxing model.
