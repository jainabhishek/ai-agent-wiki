---
title: OpenAI Codex
type: entity
subtype: product
created: 2026-10-12
updated: 2026-10-12
tags: [openai, codex, coding-agent, harness]
---

# OpenAI Codex

> OpenAI's coding agent, and the open-source agent harness behind it. The same
> harness runs the Codex app, CLI, IDE extension, Codex Web, and the
> [[openai-agents-api]].

## Overview

OpenAI presents the Codex harness as a reusable agent runtime, separate from any
one product. The host application owns the UI, context, tools, approvals, and the
system of record. The harness owns the agent loop. (see
[[openai-codex-as-a-platform]], [[openai-codex-app-server-harness]])

Most of OpenAI's 2026 guidance on skills, `AGENTS.md`, and long-running agents is
written against Codex. (see [[openai-shell-skills-compaction]],
[[openai-testing-agent-skills-with-evals]],
[[openai-skills-for-oss-maintenance]],
[[openai-rethinking-skills-prompts-gpt-6-astra]],
[[openai-run-long-horizon-tasks-codex]],
[[openai-codex-maxxing-long-running-work]])

## Key facts

### Platform and integration

- The harness is open source at `github.com/openai/codex`. (see
  [[openai-codex-as-a-platform]])
- The harness is the loop plus three services: thread lifecycle and persistence
  (create, resume, fork, archive), config and auth, and tool execution under one
  policy model for shell, MCP servers, and skills. All of it lives in "Codex
  core". (see [[openai-codex-app-server-harness]])
- Four integration paths: `codex exec` for CI and one-off scripts, the Codex
  SDK, the App Server, and `codex mcp-server`. The App Server is the default.
  The MCP-server path loses richer session semantics such as diff updates.
  [[openai-codex-as-a-platform]] lists only the first three. (see
  [[openai-codex-app-server-harness]])
- **App Server protocol.** Bidirectional "JSON-RPC lite" framed as JSONL over
  stdio, backward-compatible. The client sends one `initialize` request first.
  Three primitives: item (with `item/started`, optional deltas, and
  `item/completed`), turn, and thread. The server can pause a turn with an
  approval request until the client answers. OpenAI first tried exposing Codex
  as an MCP server and judged MCP too narrow for an interactive UI. (see
  [[openai-codex-app-server-harness]])
- Client layouts: local apps and IDEs run the App Server as a child process.
  Codex Web runs it inside the workspace container. (see
  [[openai-codex-app-server-harness]])
- **Symphony** is an open spec, with an Elixir reference implementation, that
  runs one Codex App Server session per active Linear ticket. OpenAI says it
  will not maintain Symphony as a product. (see
  [[openai-symphony-codex-orchestration]])

### Agent loop internals (Codex CLI, January 2026)

- Each Responses API request has three fields: `instructions`, `tools`, and
  `input`. Before the user message, `input` holds a sandbox `developer`
  message, optional `developer_instructions`, the `AGENTS.md` chain from root
  to cwd (32 KiB default limit) with skill metadata, and an
  `<environment_context>` message. (see [[openai-unrolling-codex-agent-loop]])
- Each request extends the previous prompt as an exact prefix, for prompt
  caching. Changing tools, model, sandbox, approval mode, or cwd mid-thread
  causes a cache miss. Config changes are appended as new messages. (see
  [[openai-unrolling-codex-agent-loop]])
- Codex does not use `previous_response_id`. Requests stay stateless to support
  Zero Data Retention; encrypted reasoning still carries across turns. (see
  [[openai-unrolling-codex-agent-loop]])
- Past `auto_compact_limit`, Codex calls `/responses/compact`, which returns
  replacement items that include an encrypted compaction item. Thread history
  is stored apart from the model input. (see
  [[openai-unrolling-codex-agent-loop]], [[openai-codex-app-server-harness]])
- The Codex sandbox covers only the shell tool. MCP tools must enforce their
  own guardrails. (see [[openai-unrolling-codex-agent-loop]])
- Codex moved most of its traffic to the Responses API WebSocket mode. (see
  [[openai-websockets-agentic-workflows]])

### Sandbox and safe deployment

- Default local policy: read almost anywhere, write only in the workspace, and
  no network unless the user asks. (see [[openai-codex-windows-sandbox]])
- On Windows, commands run as dedicated local users, `CodexSandboxOffline`
  (firewall blocks all outbound traffic) or `CodexSandboxOnline`, with a
  write-restricted token. `.git`, `.codex`, and `.agents` stay read-only inside
  writable roots. A setup binary crosses UAC once; a command-runner binary
  spawns children. (see [[openai-codex-windows-sandbox]])
- OpenAI's internal deployment uses six config surfaces: sandbox plus approval
  policy, network proxy, credentials, rules, managed configs, and OpenTelemetry
  logs. (see [[openai-running-codex-safely]])
  - **Auto-review** (`approvals_reviewer = "auto_review"`) sends the planned
    action and recent context to a subagent that approves low-risk actions.
  - **Rules** are Starlark `prefix_rule` entries that allow, block, or gate
    named commands outside the sandbox.
  - **`requirements.toml`** holds admin requirements that users cannot
    override (for example, `allowed_sandbox_modes` without full access).
    **`config.toml`** holds user settings.
  - Credentials sit in the OS keyring; login is pinned to one ChatGPT
    enterprise workspace. A security triage agent reads the telemetry on
    alerts.

### Long-running and parallel work

- **Thread automations** wake the same thread on a schedule until a condition
  holds, instead of starting fresh. (see [[openai-codex-maxxing-long-running-work]])
- Named features include persistent goals and automatic approval review. (see
  [[openai-automating-repetitive-work-codex]])
- A ~25-hour GPT-5.3-Codex run relied on four Markdown files (spec, plan,
  runbook, status log) and checks after each milestone. (see
  [[openai-run-long-horizon-tasks-codex]])
- OpenAI's internal habits (pre-2026 cloud Codex): size tasks at about one hour
  of human work or a few hundred lines, and use Best-of-N, generating several
  candidates in parallel and picking or combining. (see
  [[openai-how-openai-uses-codex]])
- Code Review applies directory-scoped `AGENTS.md` rules and cites the rule in
  each finding. (see [[openai-codex-code-review-rules]])
- When many skills are loaded, Codex shortens skill descriptions. (see
  [[openai-rethinking-skills-prompts-gpt-6-astra]])
- With GPT-6 Astra, Codex may ask for clarification mid-run; the guide says to
  start at the model's default effort in Codex. (see
  [[openai-practical-guide-building-with-gpt-6]])
- OpenAI ships an `$openai-docs` skill for migrating prompts to GPT-6. (see
  [[openai-prompting-gpt-6-astra]])

### Harness engineering and case studies (self-reported)

- **Harness engineering.** An internal OpenAI team reports shipping a product
  in which Codex wrote every line (about 1M lines, about 1,500 PRs). It uses a
  ~100-line `AGENTS.md` that points into `docs/`, custom linters whose messages
  carry fixes, and background "garbage collection" tasks. (see
  [[openai-harness-engineering]])
- **Sora Android.** Four engineers report shipping Sora for Android in 28 days
  with GPT-5.1-Codex writing about 85% of the code. (see
  [[openai-sora-android-with-codex]])
- **Tax AI.** OpenAI and Thrive report a loop in which reviewed practitioner
  corrections become evals and Codex fixes the product in a bounded worktree.
  (see [[openai-self-improving-tax-agents-codex]])
- **Data agent.** OpenAI's internal data agent uses Codex to read pipeline code
  and enrich table metadata; Codex CLI reaches the agent through MCP. (see
  [[openai-in-house-data-agent]])
- **Skyscanner.** An engineer reports connecting Codex CLI to the JetBrains MCP
  server for inspections and run configurations. (see
  [[openai-skyscanner-codex-jetbrains-mcp]])
- OpenAI uses Codex in CI and review for the [[openai-agents-sdk]] repositories.
  (see [[openai-skills-for-oss-maintenance]])

## Relationships

- Built by [[openai]]. Runs inside the [[openai-agents-api]].
- Plays the role for OpenAI that [[claude-code]] plays for [[anthropic]]: the
  first-party coding agent and the testbed for skills and harness guidance.
- Codex's cache rules (append, do not edit; no mid-session tool or model swaps)
  match the Claude Code team's rules, reached independently. (see
  [[openai-unrolling-codex-agent-loop]],
  [[anthropic-prompt-caching-is-everything]])
- Auto-review parallels Claude Code auto mode. (see
  [[openai-running-codex-safely]], [[anthropic-auto-mode-default]])

## Appears in

- Platform and loop: [[openai-codex-as-a-platform]],
  [[openai-unrolling-codex-agent-loop]], [[openai-codex-app-server-harness]],
  [[openai-websockets-agentic-workflows]],
  [[openai-responses-api-computer-environment]]
- Safety: [[openai-running-codex-safely]], [[openai-codex-windows-sandbox]],
  [[openai-understanding-prompt-injections]], [[anthropic-auto-mode-default]]
- Usage guidance: [[openai-automating-repetitive-work-codex]],
  [[openai-rethinking-skills-prompts-gpt-6-astra]],
  [[openai-practical-guide-building-with-gpt-6]],
  [[openai-shell-skills-compaction]], [[openai-testing-agent-skills-with-evals]],
  [[openai-skills-for-oss-maintenance]], [[openai-private-mcp-servers]],
  [[openai-run-long-horizon-tasks-codex]],
  [[openai-codex-maxxing-long-running-work]], [[openai-how-openai-uses-codex]],
  [[openai-codex-code-review-rules]]
- Builds and case studies: [[openai-harness-engineering]],
  [[openai-symphony-codex-orchestration]], [[openai-sora-android-with-codex]],
  [[openai-self-improving-tax-agents-codex]], [[openai-in-house-data-agent]],
  [[openai-skyscanner-codex-jetbrains-mcp]]

## Contradictions / open questions

- **`previous_response_id`.** [[openai-shell-skills-compaction]] recommends it
  for long runs. Codex avoids it to stay stateless and support ZDR
  ([[openai-unrolling-codex-agent-loop]], 2026-01-23). This is a tradeoff by
  data-retention need, not a conflict of fact.
- **Harness inside the container.** Codex Web runs the App Server inside the
  workspace container ([[openai-codex-app-server-harness]], 2026-02-04).
  [[anthropic-eng-scaling-managed-agents]] calls that co-located layout a "pet"
  and moved its harness out. Open: does a Codex thread survive loss of its
  container?
- **Auto-review scope.** Auto-review may approve high-risk actions when user
  authorization is judged sufficient ([[openai-running-codex-safely]],
  2026-05-08). Anthropic found that most auto-mode misses were this same
  judgment ([[anthropic-eng-claude-code-auto-mode]]). A third-party test
  reported by Anthropic measured 5.83% injection success under Codex
  Auto-review vs 19.03% under Full Access, with caveats
  ([[anthropic-auto-mode-default]]).
- **Allowlisted vendor domains.** The example network config allowlists
  `*.openai.com` ([[openai-running-codex-safely]]). Anthropic reports an
  exfiltration through its own allowlisted API domain
  ([[anthropic-eng-how-we-contain-claude]]). OpenAI does not discuss this risk.
- **Windows network policy.** The Windows sandbox is offline or online per
  user, with no per-domain policy described ([[openai-codex-windows-sandbox]]).
  The internal deployment uses a per-domain proxy
  ([[openai-running-codex-safely]]). Open: whether the proxy applies on
  Windows.
- **Dated: app verification.** In December 2025 Codex could not see the app run
  ([[openai-sora-android-with-codex]]). By April 2026 OpenAI's harness drove
  the app through Chrome DevTools ([[openai-symphony-codex-orchestration]],
  [[openai-harness-engineering]]). Read as harness evolution.
