---
title: Claude Managed Agents
type: entity
subtype: product
created: 2026-06-21
updated: 2026-06-21
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
deployment plumbing.

## Key facts

- **Brain–hands separation**: harness runs separately from the sandbox; a
  **session** (append-only event log) connects them. (see [[agent-harness]])
- Benefits: parallel spin-up latency wins (~60% p50 / ~90% p95), credential
  isolation via **Vaults**, durable resumable/auditable sessions.
- **Three configurable resources**: Agents (model/prompt/tools/guardrails),
  Environments (sandbox/networking/packages), Sessions.
- Deployment options: Anthropic-managed containers, self-hosted sandboxes (VPC),
  MCP tunnels.

## Relationships

- Built by [[anthropic]]; successor surface to [[claude-agent-sdk]]; underpins
  the agent runtime concepts in [[agent-orchestration]].

## Appears in

- [[anthropic-evolution-of-agentic-surfaces]]

## Contradictions / open questions

- Several related product-update posts (memory, scheduling, self-hosted
  sandboxes, MCP tunnels) were *not* ingested — candidates if deeper coverage of
  the platform is wanted.
