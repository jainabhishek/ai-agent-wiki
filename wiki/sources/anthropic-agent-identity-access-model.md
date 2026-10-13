---
title: "Anthropic: Agent Identity in Claude Tag"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Noah Zweben (Anthropic, Claude Code team)
date: 2026-06-24
source_url: https://claude.com/resources/articles/agent-identity-access-model
source_path: raw/anthropic-agent-identity-access-model.md
tags: [security, identity, access-control, permissions, multi-user, claude-tag]
---

# Anthropic: Agent Identity in Claude Tag

> Describes "agent identity": in a shared, multi-user setting the agent acts
> under its own admin-provisioned accounts, scoped per channel, instead of
> borrowing any human user's credentials.

## Summary

Noah Zweben (Anthropic, 2026-06-24) argues that "act as the user" breaks down
for team-wide agents such as Claude Tag (Claude in Slack). Agents now run long,
schedule their own work, and act after the requester logs off, and in a shared
channel no single person's permissions are the right ones. Under agent identity,
Claude has its own principal in each system (the Claude Slack app, the Claude
GitHub App, a service account for the warehouse). Admins set a workspace-wide
baseline of connections and skills; channels inherit it and can override it.
The access question becomes "what can this agent do in this compartment?". DMs
are the exception: they run under the individual user's own claude.ai account.
See [[agent-identity-and-access]].

## Key points

- **Own principal, no personal credentials.** A shared channel cannot be used to
  reach a member's private documents, because Claude never holds them.
- **Compartments.** Each private channel has its own identity; public channels
  share one workspace identity. Access and memory are isolated per channel.
- **Inherit, then override.** Workspace baseline → per-channel overrides for
  repo scope, connectors (different API keys for the same service give
  read-only vs. write), skills and plugins, and standing instructions.
- **Departure from per-user ACLs.** A member without repo access can still ask
  Claude to read the repo if the channel grants it. Mitigations: scope a channel
  profile to its least-privileged member; RBAC (Enterprise) limits who can
  invoke Claude.
- **Credential handling.** Credentials are stored apart from the agent, mapped
  to the channel identity, and injected at the network boundary per request;
  outbound traffic to non-allowlisted hosts is blocked.
- **Audit.** Routines, memory writes, and network calls are logged, and actions
  also show in each connected system's own logs because Claude uses its own
  service accounts. Revoking the identity cuts access everywhere at once.
- **Rollout advice.** Baseline profile in a few channels, review the audit
  trail, widen one deliberate grant at a time; keep personal or team tools in
  DMs.
- **Planned:** just-in-time credential grants for single sensitive actions; an
  identity-aware overlay requiring both channel profile and requesting user's
  permissions.

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[guardrails]], [[agent-identity-and-access]], [[agent-harness]], [[context-engineering]], [[tool-design]], [[human-agent-teams]].

## Notable claims & data

- Cites agent task length doubling about every four months (no source named in
  the post).
- The planned identity-aware overlay would re-introduce the user's own
  permissions as a second check, which narrows the ACL gap noted above.

## Connections

- Answers the open "agent identity (own principal vs. inherited user
  permissions)" question in [[anthropic-eng-how-we-contain-claude]] for the
  Slack surface by choosing the own-principal side.
- Network-boundary credential injection matches the vault pattern in
  [[anthropic-eng-scaling-managed-agents]].
- Product context: [[anthropic-claude-tag-analytics-in-slack]],
  [[anthropic-slack-human-agent-teams]]. Security framing:
  [[anthropic-zero-trust-for-ai-agents]].
