---
title: Model Context Protocol (MCP)
type: concept
created: 2026-10-12
updated: 2026-10-12
tags: [mcp, tools, context-engineering, security, connectivity]
---

# Model Context Protocol (MCP)

> The open protocol that agents use to connect to external tool servers. The
> wiki's sources treat it less as a protocol to explain and more as a scaling
> problem: how many tools, how much context, and which credentials an agent
> exposes through it.

## Definition

An MCP server exposes tools to an agent over JSON-RPC. Both [[anthropic]] and
[[openai]] products consume MCP servers: Claude Code reads a repository's
`.mcp.json`, and the [[openai-agents-api]] lists MCP servers as part of an
agent's definition. (see [[anthropic-claude-code-in-the-cloud]],
[[openai-agents-api-guide]])

## When to use MCP: API, CLI, or MCP

Anthropic compares three ways to connect an agent to an external system (see
[[anthropic-agents-production-systems-mcp]], 2026-04-22):

| Path | Strength | Limit |
|------|----------|-------|
| **Direct API calls** | Simple for one agent and one service | Every agent–service pair becomes a bespoke integration (the M×N problem) |
| **CLI** | Fast; reuses existing tooling | Needs a shell and a filesystem; auth is usually a credential file on disk; best for local, permissive setups |
| **MCP** | Standard auth, discovery, and semantics; one remote server reaches any compatible client | Higher upfront cost |

Anthropic argues that production agents run in the cloud against remote,
authenticated systems, so MCP is the layer that compounds as clients adopt spec
extensions. Mature integrations ship all three: an API foundation, a CLI for
local work, and MCP for cloud agents.

- **Build order.** Anthropic's large-codebase guidance puts MCP last, after
  `CLAUDE.md`, hooks, skills, and plugins; building MCP connections before the
  basics work is a common mistake (see
  [[anthropic-claude-code-large-codebases]]).
- **Practitioner framing.** Twilio's Michael Carpenter reports the rule "CLI is
  for humans. MCP is for agents." His pipeline produced a Claude Code plugin with
  425 MCP tools for Twilio APIs (see [[claude-customer-twilio]]).
- **MCP for access, skills for procedure.** MCP gives access ("what Claude can
  do"); skills give the procedure ("how Claude should do it"). Anthropic ships
  both together as a plugin (see [[anthropic-agents-production-systems-mcp]],
  [[anthropic-complete-guide-building-skills]], [[agent-skills]]).

## Server design

From [[anthropic-agents-production-systems-mcp]] unless noted:

- **Build remote.** Only a remote server runs across web, mobile, and
  cloud-hosted agents.
- **Group tools by intent, not by endpoint.** Do not mirror an API one-to-one.
  For hundreds of operations, expose a thin tool that runs a script in a
  server-side sandbox; Cloudflare's server covers ~2,500 endpoints with two
  tools (`search`, `execute`) in ~1K tokens. See [[tool-design]].
- **Elicitation.** A tool call can pause for user input in two modes. *Form
  mode* renders a native form from a schema (a missing parameter, or
  confirmation of a destructive action). *URL mode* hands off to a browser for
  downstream OAuth, payments, or credentials that must not pass through the
  client; at publication only Claude Code supported URL mode.
- **MCP Apps.** The first official extension returns inline interactive UI.
- **Standard auth.** Anthropic recommends CIMD (Client ID Metadata Documents)
  for OAuth client registration. Claude Managed Agents vaults hold and refresh
  user OAuth tokens (see [[claude-managed-agents]]).
- **The IDE as an MCP server.** A Skyscanner engineer reports that the JetBrains
  MCP server gives Codex IDE inspections and existing run configurations as
  feedback tools, which shortened the fix loop from five steps to three (see
  [[openai-skyscanner-codex-jetbrains-mcp]]).
- **Servers for live data.** In a legacy-codebase case study, Claude wrote a C#
  MCP server to view screenshot diffs and a Python MCP server over test results,
  team email, and GitHub release tags (see
  [[anthropic-onboarding-claude-code-legacy-codebase]]).

## Platforms and agents as MCP servers

MCP runs in both directions, and an agent can itself be a tool:

- Dust reports that it is both an MCP client (one interface to any tool) and an
  MCP server that exposes its agents and context (see [[claude-customer-dust]]).
- OpenAI's in-house data agent is reached from Codex CLI through MCP and from
  internal ChatGPT through an MCP connector (see [[openai-in-house-data-agent]]).
- Asana exposes its planning data through its MCP server (see
  [[anthropic-asana-coachable-agents]]).
- In Anthropic's CI/CD on-call setup, an orchestrator spawns one executor
  subagent per source of truth (Grafana, logs, PagerDuty, GitHub, Kubernetes,
  Slack), all through MCP connectors (see [[anthropic-ai-ci-cd-on-call]]).
- OpenAI offers Codex as an MCP server (`codex mcp-server`), but judged MCP too
  narrow for an interactive agent UI: it loses richer session semantics such as
  diff updates. OpenAI built the JSON-RPC App Server
  instead. MCP fits "call an agent as a tool", not "render an agent's live
  session" (see [[openai-codex-app-server-harness]]).
- OpenAI's Responses API runs MCP as a hosted tool, server-side, with no round
  trip through the developer's backend (see [[openai-why-we-built-responses-api]],
  [[agent-core-components]]).

The sources address three problems that grow with the number of MCP servers:
context cost, data flow, and the security boundary.

## Context cost: do not load every tool up front

- **Deferred loading and tool search.** Loading every tool definition from
  several MCP servers fills the context before the task starts. Anthropic's Tool
  Search Tool defers definitions and lets the model search for them. Whole MCP
  servers can be deferred at once. Tool names and descriptions then work as
  search keys. (see [[anthropic-eng-advanced-tool-use]])
- **Deferred schemas keep the cache.** Claude Code defers MCP tool schemas
  behind stubs instead of adding or removing tools mid-session, because changing
  the tool list invalidates the prompt cache. (see
  [[anthropic-prompt-caching-is-everything]], [[context-engineering]])
- **OpenAI hit the same cache problem.** In Codex, an early MCP bug listed tools
  in an unstable order, and a `notifications/tools/list_changed` message
  mid-conversation forces an expensive cache miss (see
  [[openai-unrolling-codex-agent-loop]]). Both vendors treat a stable tool list
  as part of the cache prefix.
- **Connecting a server costs a cache write.** Anthropic lists an MCP server
  connect or disconnect among the events that cause a cache write (see
  [[anthropic-what-a-task-costs-opus-5-5]]), and advises turning off unused MCP
  servers to cut startup context (see [[anthropic-claude-code-session-cost]]).

## Data flow: tools as code, not as calls

Anthropic's alternative to direct tool calls presents each MCP server as a
directory of generated code files in a code-execution sandbox. The agent reads
tool files on demand and writes a script that moves data between tools. The data
then never passes through the model's context: one example task fell from about
150K to about 2K tokens. The same layer can tokenize personal data before the
model sees it, and saved scripts can become [[agent-skills]]. The cost is
running a secure sandbox for agent-written code. (see
[[anthropic-eng-code-execution-with-mcp]], [[tool-design]])

## Security boundary

- **Credentials stay out of the sandbox.** In Claude Managed Agents, MCP OAuth
  tokens sit in a vault. A proxy swaps the session's token for the real
  credential, so neither the sandbox nor the harness sees it. (see
  [[anthropic-eng-scaling-managed-agents]], [[claude-managed-agents]])
- **Tool output is untrusted.** Remote tools can change after a user approves
  them, so their output must be inspected before it reaches the model. (see
  [[anthropic-eng-how-we-contain-claude]], [[guardrails]])
- **Private servers stay private.** OpenAI's Secure MCP Tunnel runs an
  outbound-only client next to a private MCP server. The client long-polls an
  OpenAI endpoint and forwards requests only to explicitly configured
  destinations, so the server never accepts inbound traffic. (see
  [[openai-private-mcp-servers]])
- **The host owns the tools.** In OpenAI's Codex platform model, the host
  application owns its MCP tools and approvals, and the harness only runs the
  loop. (see [[openai-codex-as-a-platform]])

- **Threats specific to tools.** Anthropic's Zero Trust eBook names tool
  poisoning and rug pulls through MCP metadata, and tool chaining, which uses
  only legitimate tools and so is invisible to host monitoring. It says that
  each service should accept only named, cryptographically identified callers, and
  that each agent should have its own identity and credentials (see
  [[anthropic-zero-trust-for-ai-agents]], [[prompt-injection]]).
- **The client sandbox may not cover MCP tools.** Codex tells the model that
  its sandbox covers only the Codex shell tool, so MCP tools must enforce their
  own guardrails (see [[openai-unrolling-codex-agent-loop]]). Gusto reports
  routing MCP traffic through a governed proxy with tool guards and prompt
  inspection before it enabled auto mode (see [[anthropic-auto-mode-production]]).
  OpenAI keeps MCP OAuth tokens in the OS keyring and exports MCP usage in its
  agent telemetry (see [[openai-running-codex-safely]]).
- **Silent failure.** Twilio reports that its MCP server failed from day one:
  Claude Code spawned the process, got EOF, and continued with no error or
  warning. Work went on without the tools for 35 days or sessions (the post uses both terms); the fix was 53
  lines of TypeScript (see [[claude-customer-twilio]], [[boundary-contracts]]).
- **Sandbox the server process.** Anthropic's open-source sandbox runtime can
  confine arbitrary processes, agents, and MCP servers with OS-level isolation,
  without a container. (see [[anthropic-eng-claude-code-sandboxing]])

## Alternatives to an MCP server

A static client-side app can register browser-side tools through WebMCP instead
of running an MCP server. This keeps data where the app already handles it. (see
[[openai-automating-repetitive-work-codex]])

## Why it matters

MCP makes adding tools cheap, which moves the bottleneck to context budget and
trust. Both vendors converge on the same architecture: load tool definitions on
demand, keep bulky data out of context, and keep credentials out of the agent's
reach. (see [[tool-design]], [[context-engineering]], [[guardrails]])

## Related concepts

- [[tool-design]] — MCP is one way tools reach an agent; tool-design rules apply.
- [[context-engineering]] — deferred loading and code execution are context
  techniques.
- [[guardrails]] — credential isolation and untrusted tool output.
- [[agent-skills]] — saved MCP scripts plus a `SKILL.md` become skills.
- [[boundary-contracts]] — an MCP server is an external boundary, so its
  ground-truth rules apply before building against it.

## Key entities

- [[claude-code]], [[claude-managed-agents]], [[openai-agents-api]],
  [[openai-codex]]

## Appears in

- [[anthropic-eng-code-execution-with-mcp]]
- [[anthropic-eng-advanced-tool-use]]
- [[anthropic-prompt-caching-is-everything]]
- [[anthropic-eng-scaling-managed-agents]]
- [[anthropic-eng-how-we-contain-claude]]
- [[anthropic-claude-code-in-the-cloud]]
- [[openai-private-mcp-servers]]
- [[openai-agents-api-guide]]
- [[openai-codex-as-a-platform]]
- [[openai-automating-repetitive-work-codex]]
- [[anthropic-eng-claude-code-sandboxing]]
- [[anthropic-agents-production-systems-mcp]]
- [[anthropic-claude-code-large-codebases]]
- [[claude-customer-twilio]]
- [[anthropic-complete-guide-building-skills]]
- [[openai-skyscanner-codex-jetbrains-mcp]]
- [[anthropic-onboarding-claude-code-legacy-codebase]]
- [[claude-customer-dust]]
- [[openai-in-house-data-agent]]
- [[anthropic-asana-coachable-agents]]
- [[anthropic-ai-ci-cd-on-call]]
- [[openai-codex-app-server-harness]]
- [[openai-unrolling-codex-agent-loop]]
- [[anthropic-what-a-task-costs-opus-5-5]]
- [[anthropic-claude-code-session-cost]]
- [[anthropic-zero-trust-for-ai-agents]]
- [[anthropic-auto-mode-production]]
- [[openai-running-codex-safely]]
- [[openai-why-we-built-responses-api]]

## Contradictions / open questions

- Direct tool calls versus tools-as-code are presented as alternatives with a
  trade-off (sandbox cost), not as a replacement. No source gives a threshold
  for switching. (see [[anthropic-eng-code-execution-with-mcp]],
  [[anthropic-eng-advanced-tool-use]])
- **How broad is MCP?** Anthropic (2026-04-22) calls MCP the integration layer
  that "compounds" for production agents, including rich UI through MCP Apps
  ([[anthropic-agents-production-systems-mcp]]). OpenAI (2026-02-04) judged MCP
  too narrow to drive an interactive agent client and built a separate JSON-RPC
  protocol ([[openai-codex-app-server-harness]]). The claims target different
  jobs: tool access versus rendering a live agent session. OpenAI's view is a
  design judgement, not a measured comparison.
- **Twilio duration.** The Twilio source page says the MCP server was broken for
  "35 days"; the raw text gives that heading and also says "35 sessions"
  ([[claude-customer-twilio]]). This page uses sessions.
