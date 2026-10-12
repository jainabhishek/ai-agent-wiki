---
title: Claude Managed Agents
type: entity
subtype: product
created: 2026-06-21
updated: 2026-10-12
tags: [anthropic, agents, infrastructure, sessions, harness]
---

# Claude Managed Agents

> Anthropic's managed agent platform (2026): decouples the reasoning engine
> (harness) from the execution environment (sandbox), connected by durable
> sessions.

## Overview

The current stage in the agentic-surface evolution
([[anthropic-evolution-of-agentic-surfaces]]). Implements **brain–hands
separation** so teams configure agents without maintaining custom loops or
deployment plumbing. The engineering design fixes stable interfaces rather than
a harness — a "meta-harness" modeled on how an OS virtualizes hardware — so
session, harness, and sandbox can each fail or be replaced without the others.
(see [[anthropic-eng-scaling-managed-agents]])

## Key facts

- **Brain–hands separation**: harness runs separately from the sandbox; a
  **session** (append-only event log) connects them. (see [[agent-harness]])
- **Interface contract** (see [[anthropic-eng-scaling-managed-agents]]):
  - `execute(name, input) → string` — the harness calls every sandbox or tool
    through one interface; a dead container is a tool error Claude can handle.
  - `provision({resources})` — creates a new container from a standard recipe.
  - `wake(sessionId)` + `getSession(id)` — a fresh harness resumes from the last
    event; `emitEvent(id, event)` writes durably during the run.
  - `getEvents()` — positional slices of the session, so the harness can resume,
    rewind, reread, or transform events before they enter context. The session
    is storage, not the context window. (see [[context-engineering]])
- **Why the split**: the first design put session, harness, and sandbox in one
  container, which became a "pet": sessions died with it, debugging needed shell
  access to containers holding user data, and customer VPCs needed network
  peering. (see [[anthropic-eng-scaling-managed-agents]])
- Benefits: time-to-first-token ~60% lower at p50 and ~90% (engineering post:
  "over 90%") at p95, credential isolation via **Vaults**, durable
  resumable/auditable sessions. The two sources give different mechanisms for
  the latency win; see Contradictions.
- **Credentials never reach the sandbox**: Git tokens are used only at sandbox
  init to clone and set the remote; MCP OAuth tokens sit in a vault, and a proxy
  swaps a session token for real credentials. (see
  [[anthropic-eng-scaling-managed-agents]], [[guardrails]]) In a scheduled
  automation, shell calls see only a placeholder such as `$SLACK_BOT_TOKEN`; the
  platform injects the real token on egress, only to allowlisted hosts. (see
  [[anthropic-building-effective-agent-automations]])
- **Many brains, many hands**: stateless harnesses scale out; any hand
  (container, phone, emulator, MCP server) sits behind the same interface;
  brains can pass hands to each other. (see
  [[anthropic-eng-scaling-managed-agents]])
- **Three configurable resources**: Agents (model/prompt/tools/guardrails),
  Environments (sandbox/networking/packages), Sessions.
- **Agent vs. deployment**: an agent is a versioned configuration (model, system
  prompt, tools). A separate **deployment** binds agent, environment, schedule,
  vault, memory stores, budget, and the first message of each run. Every
  scheduled firing starts a fresh session in a fresh sandbox; declarative files
  are applied with the `ant apply` CLI. (see
  [[anthropic-building-effective-agent-automations]])
- **Memory stores** mount into the sandbox (e.g. a user-owned `read_only`
  preferences store and an agent-owned `read_write` state store). A spend cap
  *pauses* a run (`budget_reached`) rather than failing it. MCP tools ask for
  approval by default, which an unattended deployment must configure around.
  (see [[anthropic-building-effective-agent-automations]])
- Deployment options: Anthropic-managed containers, self-hosted sandboxes (VPC),
  MCP tunnels.

## Relationships

- Built by [[anthropic]]; successor surface to [[claude-agent-sdk]]; underpins
  the agent runtime concepts in [[agent-orchestration]].
- Architecturally parallel to [[openai-agents-api]] (a vendor-hosted harness
  with durable sessions and sandboxes). (see [[openai-agents-api-guide]])

## Appears in

- [[anthropic-evolution-of-agentic-surfaces]]
- [[anthropic-eng-scaling-managed-agents]]
- [[anthropic-building-effective-agent-automations]]
- [[openai-agents-api-guide]]
- [[openai-codex-as-a-platform]]

## Contradictions / open questions

- **Mechanism of the latency win.**
  [[anthropic-evolution-of-agentic-surfaces]] (claude.com blog, 2026-06-10) says
  reasoning starts *while the sandbox spins up* in parallel.
  [[anthropic-eng-scaling-managed-agents]] (Anthropic Engineering, 2026-04-08)
  says containers are created lazily, *only when a tool call needs one*, and
  inference starts as soon as the orchestration layer pulls pending events; the
  old design provisioned a container before inference in every session. Both
  report the same ~60% p50 / ~90% p95 figures. The claims may be compatible
  (neither design waits for a container before inference), but "parallel
  spin-up" and "no container until needed" describe different mechanisms. The
  engineering post is the more detailed primary account.
- Several related product-update posts (memory, scheduling, self-hosted
  sandboxes, MCP tunnels) were *not* ingested — candidates if deeper coverage of
  the platform is wanted. [[anthropic-building-effective-agent-automations]]
  partly covers scheduling and memory stores.
