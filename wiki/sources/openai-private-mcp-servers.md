---
title: "OpenAI: Making Private MCP Servers Reachable Without Making Them Public"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Denys Kurylenko (OpenAI)
date: 2026-06-26
source_url: https://developers.openai.com/blog/connect-private-mcp-servers-to-openai-products
source_path: raw/openai-private-mcp-servers.md
tags: [mcp, networking, security, enterprise, tunnel, connectivity]
---

# OpenAI: Making Private MCP Servers Reachable Without Making Them Public

> Design notes on Secure MCP Tunnel: a customer-run, open-source client that
> opens an outbound HTTPS long-poll to OpenAI so ChatGPT and Codex can reach
> private MCP servers without inbound exposure, VPNs, or third-party tunnels.

## Summary

[[openai]] built Secure MCP Tunnel for MCP servers inside enterprise networks
and on developer laptops. A small client next to the server makes an outbound
HTTPS connection; OpenAI products send MCP JSON-RPC to an OpenAI-hosted tunnel
endpoint; the service queues work per tunnel; the client long-polls, forwards
to an explicitly configured local server, and returns responses and
server-sent events on the same path. Design principles: outbound-only
connectivity, explicit destination configuration, MCP streaming compatibility,
and an inspectable customer-run client (`openai/tunnel-client`). Access is tied
to the customer's OpenAI organization/workspace and a tunnel identity. OAuth
discovery travels through the tunnel; the client supports custom CA bundles,
proxies, and MCP-side mTLS. **Harpoon** extends the model to labeled, bounded
REST targets. Date from page byline: 2026-06-26.

## Key points

- **Rejected defaults:** public endpoints weaken the boundary; third-party
  tunnels add a vendor to the trust path; VPN/peering grants broad
  connectivity for a narrow need.
- **Long-poll by design:** familiar to firewalls; the client pulls only what it
  can process, giving natural backpressure.
- **Narrow, explicit boundary:** not a general network bridge; a private
  authorization server must still be reachable by whichever component runs
  the OAuth flow. See [[guardrails]], [[boundary-contracts]].
- **Same loop laptop to production:** a Codex plugin (`tunnel-mcp`) guides
  setup and emits production-shaped config; health checks, readiness, logs,
  and a local admin UI; an assistant reads local tunnel context to
  troubleshoot from real state.
- **Harpoon:** customer-registered labeled REST targets with allowed methods,
  response-size limits, timeouts, redirect rules, and access controls.

## Entities

[[openai]], [[openai-codex]]

## Concepts

[[tool-design]], [[guardrails]], [[agent-harness]]

## Notable claims & data

- Three-step client loop: receive MCP request → forward to approved local
  server → return responses and notifications on the same connection.
- The post gives no performance or adoption figures.
- No contradiction with existing pages; this is the wiki's first source on
  network reachability for MCP tools.

## Connections

Infrastructure counterpart to MCP tool design in
[[anthropic-eng-code-execution-with-mcp]] and [[anthropic-eng-advanced-tool-use]].
Security posture parallels the network allowlists in
[[openai-shell-skills-compaction]]. Codex integration relates to
[[openai-codex-as-a-platform]].
