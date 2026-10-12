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

## Contradictions / open questions

- Direct tool calls versus tools-as-code are presented as alternatives with a
  trade-off (sandbox cost), not as a replacement. No source gives a threshold
  for switching. (see [[anthropic-eng-code-execution-with-mcp]],
  [[anthropic-eng-advanced-tool-use]])
