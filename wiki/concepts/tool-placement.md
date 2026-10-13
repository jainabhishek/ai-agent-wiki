---
title: Tool Placement
type: concept
created: 2026-10-13
updated: 2026-10-13
tags: [tools, mcp, computer-use, hosted-tools, agents]
---

# Tool Placement

> Where a tool runs, who owns it, and where its output lands: hosted versus
> client-side, API versus computer use, inside the IDE or browser, and behind a
> private network.

## Definition

[[tool-design]] covers the interface craft of a tool: names, descriptions,
responses, and errors. Tool placement covers the system around the tool: which
process runs it, which application decides that it is exposed, which network it
can reach, and how much of its output enters context. For the protocol detail of
MCP servers, see [[model-context-protocol]].

## Hosted tools versus client-side tools

- **Hosted tools versus custom tools.** In OpenAI's Responses API, hosted tools
  (file search, code interpreter, web search, image generation, MCP) run
  server-side with no round trip through the developer's backend (see
  [[openai-why-we-built-responses-api]]). With custom tools the API hands
  control back to the client's harness; with hosted tools the API runs the loop
  itself, for example forwarding shell commands to a hosted container (see
  [[openai-responses-api-computer-environment]], [[agent-core-components]]).
- **One tool interface for every "hand".** Anthropic's Managed Agents harness
  calls every sandbox or tool through one `execute(name, input) → string`
  interface; a dead container surfaces as a tool error the model can handle (see
  [[anthropic-eng-scaling-managed-agents]]).

## API or connector before computer use

- OpenAI's GPT-6 guide says to use an API or connector when one can do the
  step, and computer use only for screens, clicks, and forms; for your own app,
  give the model a code-running tool such as Playwright or PyAutoGUI (see
  [[openai-practical-guide-building-with-gpt-6]], model-scoped). OpenAI's Codex
  guide orders surfaces the same way: connectors for Slack, Gmail, Calendar, and
  GitHub, and computer use only for GUI-only apps (see
  [[openai-codex-maxxing-long-running-work]]).

## Tools inside the developer's environment

- **The IDE as a feedback tool.** A Skyscanner engineer reports that the
  JetBrains MCP server gives Codex IDE inspections (`get_file_problems`) and the
  team's existing run configurations (`execute_run_configuration`). The fix loop
  shrank from five steps to three, and the agent no longer has to discover how
  to run tests, format, or lint. The evidence is qualitative (see
  [[openai-skyscanner-codex-jetbrains-mcp]], [[model-context-protocol]]).
- **Browser-side tools.** Runme, a static client-side app, registers tools in
  the browser through WebMCP instead of running an MCP server, which would add
  infrastructure and change where notebook data is handled (see
  [[openai-automating-repetitive-work-codex]]).
- **Make the application legible to the agent.** OpenAI reports that, for one
  internal product, the app boots per git worktree. The agent drives the UI
  through Chrome DevTools Protocol (DOM snapshots, screenshots, navigation) and
  queries an ephemeral per-worktree observability stack with LogQL and PromQL.
  The post warns that this autonomy depends on the repository and may not
  generalize (see [[openai-harness-engineering]]).

## Private tool reach

- **Private MCP connectivity.** [[openai]]'s Secure MCP Tunnel lets hosted
  products reach [[model-context-protocol]] servers inside enterprise networks
  through an outbound-only, customer-run client that forwards only to an
  explicitly configured local server. OpenAI rejected public endpoints,
  third-party tunnels, and VPN/peering as too broad (see
  [[openai-private-mcp-servers]], [[guardrails]]).

## Who owns the tool surface

- **Host owns the tool surface.** In OpenAI's Codex platform the host
  application, not the harness, decides which context and tools (including
  app-owned MCP servers) are exposed and which actions need approval (see
  [[openai-codex-as-a-platform]]).

## Where tool output lands

- **Bound tool output.** OpenAI's hosted shell lets the model set an output cap
  per command; the API keeps the head and tail and marks the cut middle (see
  [[openai-responses-api-computer-environment]]). Claude Code writes command
  output over a size limit to a file and puts a preview in context (see
  [[anthropic-claude-code-session-cost]]). Both vendors bound tool output
  instead of passing it whole into context.

## Why it matters

The cases above show placement deciding which system runs the tool loop, which
network and data a tool can touch, and what the agent can observe and verify.
These choices sit outside the tool definition itself; see [[tool-design]] for
the definition side and [[guardrails]] for the safety side.

## Related concepts

- [[tool-design]] — interface craft for each tool; this page covers where the
  tool runs and who owns it.
- [[model-context-protocol]] — the protocol behind the hosted MCP tool, the
  JetBrains MCP server, WebMCP, and the Secure MCP Tunnel above.
- [[agent-core-components]] — hosted versus client-run tool loops.
- [[agent-harness]] — the harness that calls tools and bounds their output.
- [[context-engineering]] — output caps keep tool results from flooding context.
- [[guardrails]] — network reach and approval ownership as safety controls.

## Key entities

- [[openai]] — Responses API hosted tools, Secure MCP Tunnel, Codex platform.
- [[openai-codex]] — host-owned tool surface, IDE feedback tools, connectors.
- [[anthropic]] — Managed Agents tool interface.
- [[claude-managed-agents]] — the `execute(name, input)` tool interface.
- [[claude-code]] — output over a size limit written to a file.

## Appears in

- [[openai-why-we-built-responses-api]]
- [[openai-responses-api-computer-environment]]
- [[anthropic-eng-scaling-managed-agents]]
- [[openai-practical-guide-building-with-gpt-6]]
- [[openai-codex-maxxing-long-running-work]]
- [[openai-skyscanner-codex-jetbrains-mcp]]
- [[openai-automating-repetitive-work-codex]]
- [[openai-harness-engineering]]
- [[openai-private-mcp-servers]]
- [[openai-codex-as-a-platform]]
- [[anthropic-claude-code-session-cost]]

## Contradictions / open questions

- _None recorded._
