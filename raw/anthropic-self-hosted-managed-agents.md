# Operate Claude Managed Agents inside your security perimeter (Self-hosted Claude Managed Agents) — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/self-hosted-claude-managed-agents
> Publisher: Anthropic (claude.com articles) · Date: 2026-11-12
> Author: no byline on the page (no Person author in page metadata)
> Captured: 2026-11-24 via curl (HTML stripped to text). Condensed paraphrase, not a copy.
> Title note: the URL slug and link text say "Self-hosted Claude Managed Agents"; the page H1 is "Operate Claude Managed Agents inside your security perimeter".

Page labels: Category Product updates · Product Claude Platform, Claude Managed Agents · Reading time 5 min. No model is named.

Subtitle (paraphrased): launch of self-hosted Claude Managed Agents. Agents run in the customer's cloud or data center; the customer hosts agents, credentials, and session history, and decides where Claude requests are routed.

Intro:
- Status: **private beta**. Developers build agents that work in their company's code and internal systems and run them in their own environment.
- Self-hosting is a new deployment mode for Managed Agents, which Anthropic describes as composable APIs for building and shipping autonomous agents. The product provides the harness, sandboxes, credential handling, and session history that long-running production agents need.

## Run your agent control plane in your own environment

- History: Managed Agents launched as a hosted service on the Claude Platform (Anthropic runs infrastructure). Self-hosted sandboxes were added next, for teams whose code had to stay in their environment.
- Since then agents took on more critical work — fixing broken builds, testing releases, triaging alerts, working a bug backlog — unattended, on your code, with access to internal systems. Some teams want the whole service in their environment, not only the sandbox. Before this, that meant building the platform themselves.
- Now every part runs in your cloud or on-premise: harness, sandboxes, credentials, session history. The customer runs the Managed Agents server and its database, plus the workers that execute the agents' shell and file tools.
- Model requests go where you choose: Anthropic directly; a cloud provider (Amazon Bedrock, Google's Agent Platform, Microsoft Foundry); or your own gateway.
- Developers use the same core APIs as hosted Managed Agents.
- Session history sits in your own database. If your org has zero data retention (ZDR) with Anthropic, ZDR covers the Claude requests the same as any other Messages API call.

## Designed for agent security

Unattended agents cannot depend on a person checking each step, so limits must be in the system's design; agent security starts with architecture. Four principles apply in all three modes: fully Anthropic-hosted, customer-hosted sandbox only, or fully customer-hosted.

**The brain and the hands are split**
- Claude is called by the harness ("brain"); the sandbox ("hands") runs the agent's code. They are separate by design. Agent loop, session history, and vault secrets stay outside the sandbox.
- Effects: an agent does not need one sandbox to survive its whole run; sandboxes start only when a tool needs one; session history is kept as an event log outside the sandbox.

**Credentials stay out of the sandbox**
- Vaults are the mechanism that keeps secrets away from the sandbox. When the agent calls an MCP tool or a supported API, a proxy running outside the sandbox inserts the credential.
- Self-hosted: credentials can also live in your own secrets manager.

**Network access can be limited**
- Each environment can be limited to an allowlist of hosts; requests to other hosts are blocked. Example: an agent that fixes broken builds might need only your git host and package registry.
- When the sandbox is yours to host, your own firewall enforces the equivalent rules.

**Every session leaves a full record**
- The service logs each step the agent takes, including every tool call and its result. The record exports over OpenTelemetry to your existing monitoring tools, so agent activity can be reviewed with the rest of your systems.

## Get started

Private beta. Contact your Anthropic account team for access, or read the docs.
