---
title: "Anthropic: Self-hosted Claude Managed Agents"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Anthropic (claude.com articles)
date: 2026-11-12
source_url: https://claude.com/resources/articles/self-hosted-claude-managed-agents
source_path: raw/anthropic-self-hosted-managed-agents.md
tags: [managed-agents, self-hosting, deployment, security, credentials, sandboxing, observability, product-update]
---

# Anthropic: Self-hosted Claude Managed Agents

> Anthropic's launch post for a private beta that lets customers run the whole Claude Managed Agents service in their own cloud or on-premise, with four security principles that apply in every deployment mode.

## Summary

Anthropic published this product update on claude.com on 2026-11-12. The page has no byline. The page heading is "Operate Claude Managed Agents inside your security perimeter". Self-hosted [[claude-managed-agents]] is in private beta. No model is named.

Managed Agents first ran only as a service that Anthropic hosts. Anthropic then added self-hosted sandboxes. With this release, the customer can host every part of the service: the harness, the sandboxes, the credentials, and the session history. Developers use the same core APIs as in the hosted service.

## Key points

- **Three deployment modes.** Anthropic hosts everything, the customer hosts only the sandbox, or the customer hosts the whole service. The four security principles apply in all three modes.
- **What the customer runs.** In the self-hosted mode, the customer operates the Managed Agents server, its database, and the workers that run the agents' shell and file tools.
- **Model routing.** Model requests go to Anthropic, to a cloud provider (Amazon Bedrock, Google's Agent Platform, Microsoft Foundry), or to the customer's own gateway.
- **Data retention.** Session history stays in the customer's database. An existing zero data retention (ZDR) agreement covers the Claude requests in the same way as any Messages API call.
- **Principle 1: the brain and the hands are split.** The harness calls Claude, and the sandbox runs the agent's code. The agent loop, session history, and vault secrets stay outside the sandbox. Sandboxes start only when a tool needs one. (see [[agent-harness]])
- **Principle 2: credentials stay out of the sandbox.** A proxy outside the sandbox adds credentials to MCP tool calls and supported API calls. Self-hosted customers can keep credentials in their own secrets manager. (see [[agent-identity-and-access]])
- **Principle 3: network access can be limited.** Each environment can have an allowlist of hosts, and the service blocks other hosts. The post's example is an agent that fixes broken builds, which needs only the git host and the package registry. (see [[guardrails]])
- **Principle 4: every session leaves a full record.** The service records each tool call and its result. The record exports over OpenTelemetry to existing monitoring tools.

## Notable claims & data

- Example workloads: fixing broken builds, testing releases, triaging alerts, and working through a bug backlog. These agents run unattended with access to internal systems.
- The post states the design rule in one line: unattended agents cannot rely on a person who checks every step, so the limits must be in the architecture.
- Before this release, a team that wanted the full service in its own environment had to build the platform itself.

## Entities

[[anthropic]], [[claude]], [[claude-managed-agents]].

## Concepts

[[agent-harness]], [[agent-identity-and-access]], [[guardrails]], [[model-context-protocol]].

## Connections

- Brain–hands split, lazy sandboxes, and the session event log: [[anthropic-eng-scaling-managed-agents]].
- Credential proxy for always-on agents: [[anthropic-building-always-on-agents]].
- Sandbox and network limits: [[anthropic-eng-claude-code-sandboxing]], [[anthropic-eng-how-we-contain-claude]].
- The Contradictions / open questions section of [[claude-managed-agents]] lists self-hosted posts as not ingested. This page fills part of that gap.
