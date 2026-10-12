# Agents guide and API changelog (Aug–Oct 2026) — OpenAI (API docs) (raw capture)

> Source 1: https://developers.openai.com/api/docs/guides/agents
> Source 2: https://developers.openai.com/api/docs/changelog (entries from 2026-08-01 onward)
> Supporting pages (Section 3): https://developers.openai.com/api/docs/guides/agents-api/overview, .../agents-api/architecture, .../agents-api/tools/computer-use
> Publisher: OpenAI (API docs) · Date: no byline; accessed 2026-10-12
> Captured: 2026-10-12 via curl of the .md endpoints (condensed and paraphrased).

## Section 1 — Agents (guide)

Agents plan and complete tasks with tools, work with other agents, and keep context across steps. Choose a runtime by where orchestration should run and who manages state between tasks.

### Choose your starting point

| You want to | Start here |
|---|---|
| Run an agent on the Codex harness, managed by OpenAI | Agents API |
| Control the agent loop in your app with reusable agents, tools, handoffs | Agents SDK |
| Work directly with model responses and control the integration | Responses API |
| Add an embedded chat experience | ChatKit |

### Compare agent runtime options

| | Agents API | Agents SDK | Responses API |
|---|---|---|---|
| Use for | Long-running tasks where OpenAI manages the agent and saves progress | Agents with custom tools/workflows in your app | Calling models directly or building an agent from scratch |
| Where the agent runs | OpenAI runs a managed Codex harness | SDK runs inside your app | Your app, optional hosted orchestration |
| Integration effort | Low | Medium | High |
| State between tasks | Saved session configuration, turns, items | Your storage + SDK sessions, or Responses conversation state | Manual history, response chaining, or Conversations |
| Tool execution | Service-connected tools, app function handlers, optional sandbox | Tools/integrations configured in your app | Hosted tools and tools your app runs |
| Execution environment | OpenAI-hosted sandbox, self-hosted sandbox, or none | Your runtime + sandbox provider integrations | Your own environment |

- Agents API: runs the Codex harness and manages agent infrastructure; includes automatic context compaction, multi-agent orchestration, programmatic tool calling, MCP server support.
- Agents SDK: your app controls deployment, storage, approvals, runtime integration; its runner handles the loop and handoffs.

### Add tools, skills, and prompt caching

- Tool design, skills, and prompt caching apply across runtimes, but configuration and lifecycle differ by API. Pointers: Using tools (function calling, MCP, hosted tools); Programmatic Tool Calling (JavaScript orchestration, per-API config); Skills; Prompt caching, plus Agents API observability and usage for session accounting.
- An Agents API session, an SDK session, a Responses conversation, and a sandbox are **different resources**; follow each runtime's state and cleanup rules.

## Section 2 — API changelog, agent-related and model entries, 2026-08-01 to 2026-10-12

- **2026-08-26** — The **Assistants API shut down**; migrate to the Responses API and Conversations API. (Same entry: `whisper-1`, `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`, `gpt-4o-transcribe-diarize` deprecated, shutdown 2027-02-26.)
- 2026-08-21 — GPT-5.6 Sol price cut to $4 / $20 per 1M input/output tokens (promotional, at least through 2026-11-21).
- 2026-08-13 — Ultrafast mode announced for GPT-5.6 Sol (up to 14x faster than Standard; limited preview).
- **2026-09-03** — **GPT-6 Astra** (`gpt-6-astra`) released, Responses and Chat Completions. Migration notes: no `none` effort; no custom `temperature`/`top_p` or `logprobs`; tool calling requires Responses; misalignment monitoring asynchronously checks agent work in supported Responses requests and can raise safety alerts or stop a conversation for review.
- 2026-09-03 — Long-running-work controls in Responses: async tool calling; mid-turn steering over WebSockets; change reasoning effort mid-conversation while keeping the cached prefix.
- 2026-09-08 — Prompt Cache Diagnostics GA (Responses, GPT-5.6 and later).
- **2026-09-10** — **Agents API public beta.** Managed Codex harness; OpenAI handles session orchestration, context compaction, recovery. Durable sessions continue work across turns, stream progress, connect your own tools and MCP servers. Run in OpenAI-hosted sandboxes or connect a sandbox from your own infrastructure or a supported provider.
- 2026-09-10 — GPT-Live 1 GA (full-duplex voice; backend model/agent handles reasoning and tools; $0.05/min).
- **2026-09-22** — **GPT-6 Sol** (`gpt-6-sol`) and **GPT-6 Luna** (`gpt-6-luna`) released. Per 1M tokens (≤272K input): Sol $2 in / $0.20 cached / $10 out; Luna $0.10 / $0.01 / $0.50.
- 2026-09-25 — Fix: image-encoding bug that degraded image understanding in GPT-6 Sol and Luna, including computer use; rerun evals.
- **2026-09-29** — **Computer use added to the Agents API**: tasks in an OpenAI-hosted browser; website-access approvals and sign-in are handled by your application.
- **2026-09-29** — **GPT-6.1 Sol** (`gpt-6.1-sol`) released: lower cost than Astra; $2 in / $0.10 cached / $2.50 cache write / $10 out per 1M (≤272K input). Supports **Multi-agent in beta** (model delegates to subagents within a Responses API request). Tool calling via Responses.
- 2026-09-29 — Ultrafast mode for GPT-6 Astra (`service_tier: "ultrafast"`), global processing + US residency only.
- **2026-10-06** — **Decisions API** (`v1/decisions`) in beta with `gpt-6-luna`: text and images to typed answers, stated as 10x faster than the Responses API.
- 2026-10-08 — Ultrafast mode for GPT-6.1 Sol (US and EU residency).

## Section 3 — Supporting detail from linked Agents API pages

### From /guides/agents-api/overview

- The Agents API gives an app the Codex harness through an OpenAI-managed API. OpenAI manages sessions, orchestration, compaction, recovery; the app provides tools and chooses the execution environment. In a sandbox, agents run code, edit files, connect to MCP servers, produce artifacts.
- Pricing: model usage at model API rates; OpenAI tools at standard rates; hosted sandboxes at container rates.
- Four core concepts: **Agent** (model, instructions, tools, MCP servers); **Environment** (optional sandbox/computer for files, skills, commands); **Session** (durable agent instance that works on tasks and takes input); **Events and items** (inputs and outputs in a session).
- Session lifecycle: create session (OpenAI provisions environment) → give task (starts a turn) → follow progress (stream or webhooks) → continue or steer.
- Managed harness supports: commands/code in a sandbox; skills and instructions; external data via tools or MCP; steering mid-work; summarizing earlier work to manage context; subtasks delegated to subagents; resuming a session.
- Example session config: `client.beta.agents.sessions.create` with `agent.model: "gpt-6-astra"`, tools `programmatic_tool_calling`, `mcp` (with `server_label`, `transport.type: "http"`, `server_url`), `web_search`; `multi_agent: { enabled: true, max_concurrent_subagents: 4 }`; `environment: { type: "self_hosted", workspace_directory: "/workspace", capability_directories: ["/workspace/capabilities/skills"] }`. REST: `POST https://api.openai.com/v1/agents/sessions` with header `OpenAI-Beta: agents=v1`.
- Bedrock Managed Agents (AWS) is built on the Agents API.
- Session state is retained across turns; sessions and published artifacts can be deleted.
- Data: US data residency only; **no Zero Data Retention**; a self-hosted sandbox does not make it ZDR-eligible.
- Sample apps: incident response agent (approval for recovery actions), Slack bot, data analyst (read-only SQL), GitHub issue investigator, document reviewer.

### From /guides/agents-api/architecture

- Pieces: **Harness** (OpenAI-hosted Codex instance running model and tool loop, keeping session); **Environment** (remote sandbox, laptop, Docker container, or AWS Lambda); **Application server** (your code: submits tasks, receives events, handles function tools, manages environment lifecycle if you provide it).
- `environment.type: "none"`: harness calls remote MCP tools directly; function tools run in your code; built-in Bash, apply-patch, workspace files, executor MCPs unavailable.
- `environment.type: "openai_hosted"`: OpenAI creates/manages a sandbox; you configure packages, files, network access.
- `environment.type: "self_hosted"`: your code starts the environment and connects an **executor** that runs harness-requested commands; you own provisioning, reconnection, shutdown, file preservation. Confirm no pending execution before stopping compute.
- Progress: streaming and/or webhooks. If a function-tool handler is unavailable, the agent can stay waiting.

### From /guides/agents-api/tools/computer-use (approval model)

- Enable with `{ "type": "computer_use" }` in `agent.tools`, `environment.type: "openai_hosted"`, `environment.desktop.enabled: true`. Optional `include_screenshots: true` on the tool (screenshots excluded from API output by default; the agent still sees them).
- **Origin access:** the browser needs the user's approval for each new website origin, including public sites. Enabling network access does not approve origins. Flow: on `agent.session.requires_action`, read the session's `required_actions`; find `computer_use_approval_request` with `request.type: "browser_origin_access"`; show `origin` and `reason`; submit `approve` / `deny` / `cancel` via the session events endpoint with the same `request_id`. `202` = decision accepted, not navigation done. Cancelling an approval does not cancel the task.
- **Origin approval does not enforce confirmation of individual actions.** To guarantee confirmation before purchases or destructive changes, restrict the hosted browser to resources that cannot perform them, or use a browser runtime you control. A function-tool confirmation depends on the agent choosing to call it. Website content is untrusted and cannot grant permission or override user instructions.
- Network policy (`network` config of the hosted environment) is separate from origin approval and is not overridden by it.
- **Sign-in:** `request.type: "browser_authentication"` with `reason`, `credential_origin`, `fields`, `options`. Only the **main agent** can request browser auth; subagents cannot. Supports email, password, verification codes; not passkeys or QR-code sign-in. Submit with `action: "submit"` (or `cancel`); values go only through this dedicated event, stay **outside model input**, and are omitted from history. Cancel if the credential origin is missing or unfamiliar. Disable automatic retries for credential submissions. Auth requests expire after **5 minutes**; origin requests last for the owning turn. Limits: up to 6 field values, 16,384 chars each, 120 KiB total.
- Clarifying questions use an app-defined function tool (e.g. `request_user_response`); function-tool results are visible to the model and saved — never use them for passwords or codes.
- Recovery status codes: `202` accepted; `400` bad payload; `404` session/request not found; `409` expired, turn ended, or a different response already accepted (changing an accepted decision returns `409`).
- Browser activity appears as `computer_use_call` items (`id`, `turn_id`, `title`, `status` in `in_progress|completed|failed|incomplete`, `output`). Screenshots may contain sensitive data; retained history can omit image bytes.
