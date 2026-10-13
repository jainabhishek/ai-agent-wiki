---
title: "Anthropic: Building agents that reach production systems with MCP"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com articles)
date: 2026-04-22
source_url: https://claude.com/resources/articles/building-agents-that-reach-production-systems-with-mcp
source_path: raw/anthropic-agents-production-systems-mcp.md
tags: [mcp, tool-design, integrations, context-engineering, skills, auth, cloud-agents]
---

# Anthropic: Building agents that reach production systems with MCP

> Anthropic's comparison of API calls, CLIs, and MCP as ways to connect agents to external systems, with design patterns for MCP servers, MCP clients, and MCP-plus-skills distribution.

## Summary

The post (claude.com, 2026-04-22) names three integration paths. **Direct API calls** suit one agent and one service, but at scale every agent–service pair becomes a bespoke integration (the "M×N integration problem"). **CLIs** are fast and reuse existing tooling, but they need a shell and filesystem, and auth is usually a credential file on disk; best for local, permissive setups. **MCP** standardizes auth, discovery, and semantics, so one remote server reaches any compatible client in any environment, at higher upfront cost. Anthropic argues production agents run in the cloud against remote, authenticated systems, so MCP is the layer that "compounds": a server gains capability as clients adopt spec extensions. Mature integrations ship all three (API foundation, CLI for local, MCP for cloud).

## Key points

- **Server: build remote.** Only a remote server runs across web, mobile, and cloud-hosted agents. (see [[model-context-protocol]])
- **Server: group tools by intent, not endpoint.** Do not mirror an API one-to-one; one `create_issue_from_thread` beats four primitive calls. (see [[tool-design]], [[anthropic-eng-writing-tools-for-agents]])
- **Server: code orchestration for large surfaces.** For hundreds of operations, expose a thin tool that accepts a script run in a server-side sandbox. Cloudflare's server: two tools (`search`, `execute`) cover ~2,500 endpoints in ~1K tokens.
- **Server: rich semantics.** MCP Apps (first official extension) returns inline interactive UI. Elicitation pauses a tool call for user input: *form mode* (schema → native form; missing parameter, destructive-action confirmation) and *URL mode* (browser hand-off for downstream OAuth, payments, credentials that must not transit the client; Claude Code only at publication).
- **Server: standardized auth.** CIMD (Client ID Metadata Documents) for OAuth client registration is Anthropic's recommended approach. Claude Managed Agents Vaults hold and refresh user OAuth tokens, referenced by vault ID at session creation. (see [[claude-managed-agents]], [[guardrails]])
- **Private networks.** MCP tunnels in Claude Managed Agents use an outbound-only connection; no exposed ports.
- **Client: progressive disclosure.** Tool search cuts tool-definition tokens by 85%+; programmatic tool calling cuts ~37% of tokens on complex multi-step workflows (Anthropic testing, from [[anthropic-eng-advanced-tool-use]]). (see [[context-engineering]])
- **MCP + skills.** MCP gives access; skills give the procedure. Ship both as a plugin (skills, MCP servers, hooks, LSP servers, subagents) or publish a skill beside the server; an MCP extension to deliver skills from servers is in progress. (see [[agent-skills]])

## Notable claims & data

- MCP SDKs: 300M+ downloads/month, up from 100M at the start of 2026. 200+ servers in Anthropic's directory.
- Servers that ship MCP Apps reportedly see higher adoption and retention than text-only servers (no figure given).
- Cowork data plugin: 10 skills + 8 MCP servers (Snowflake, Databricks, BigQuery, Hex, others).

## Entities

[[anthropic]], [[claude]], [[claude-code]], [[claude-managed-agents]]

## Concepts

[[model-context-protocol]], [[tool-design]], [[context-engineering]], [[agent-skills]], [[guardrails]]

## Connections

Tool-search and programmatic-calling numbers originate in [[anthropic-eng-advanced-tool-use]]; tools-as-code in [[anthropic-eng-code-execution-with-mcp]]. Vault credential handling: [[anthropic-eng-scaling-managed-agents]]. OpenAI's outbound-only tunnel for private servers: [[openai-private-mcp-servers]]. Skills side: [[anthropic-building-agents-with-skills]], [[anthropic-complete-guide-building-skills]].
