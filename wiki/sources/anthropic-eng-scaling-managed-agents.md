---
title: "Anthropic (Eng): Scaling Managed Agents — Decoupling the Brain from the Hands"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Lance Martin, Gabe Cemaj, Michael Cohen (Anthropic Engineering)
date: 2026-04-08
source_url: https://www.anthropic.com/engineering/managed-agents
source_path: raw/anthropic-eng-scaling-managed-agents.md
tags: [harness, architecture, claude-managed-agents, sessions, sandboxing, security, primary-source]
---

# Anthropic (Eng): Scaling Managed Agents

> The engineering design of Claude Managed Agents: three virtualized
> components (session, harness, sandbox) behind small interfaces, so each can
> fail or be replaced without the others. Primary source for the brain–hands
> separation.

## Summary

Harnesses encode assumptions about what Claude cannot do, and those go stale
as models improve (the Sonnet 4.5 "context anxiety" reset was unnecessary on
Opus 4.5). [[claude-managed-agents]] therefore fixes stable interfaces, not a
harness — a "meta-harness", modeled on how an OS virtualizes hardware. The
three components are the **session** (append-only event log), the **harness**
(loop that calls Claude and routes tool calls), and the **sandbox** (where code
runs). The first design put all three in one container, which became a "pet":
sessions died with the container, debugging needed shell access to containers
holding user data, and customer VPCs needed network peering. See
[[agent-harness]] and [[agent-orchestration]].

## Key points

- **Hands as tools.** The harness calls every sandbox or tool through one
  interface, `execute(name, input) → string`. A dead container is a tool error
  Claude can handle; a new one comes from `provision({resources})`.
- **Disposable harness.** The session log lives outside the harness:
  `wake(sessionId)` + `getSession(id)` resume from the last event;
  `emitEvent(id, event)` writes durably during the run.
- **Credentials never reach the sandbox.** Auth is bundled with a resource or
  held in a vault. Git tokens are used only at sandbox init to clone and set the
  remote. MCP OAuth tokens sit in a vault; a proxy swaps a session token for
  real credentials, so the harness never sees them.
- **The session is not the context window.** Compaction, the memory tool, and
  trimming discard irreversibly. The session is durable external context;
  `getEvents()` returns positional slices so the harness can resume, rewind, or
  reread, and can transform events before they enter context (e.g. for
  prompt-cache hit rate). Storage (session) is separate from context
  management (harness). See [[context-engineering]].
- **Many brains, many hands.** Stateless harnesses scale out; any hand
  (container, phone, emulator, MCP server) sits behind the same interface;
  brains can pass hands to each other.

## Entities

[[anthropic]], [[claude]], [[claude-managed-agents]], [[claude-code]]

## Concepts

[[agent-harness]], [[agent-orchestration]], [[context-engineering]],
[[guardrails]], [[agent-identity-and-access]], [[tool-design]], [[tool-placement]], [[agent-core-components]]

## Notable claims & data

- Time-to-first-token fell about 60% at p50 and over 90% at p95. Cause, as this
  post states it: containers are provisioned **only when a tool call needs
  one**, and inference starts as soon as the orchestration layer pulls pending
  events, instead of every session provisioning a container before inference.
- Earlier models reasoned poorly about multiple execution environments; the
  many-hands design depends on current models doing so.

## Connections

- Relation to [[anthropic-evolution-of-agentic-surfaces]] (claude.com blog,
  2026-06-10): that post is the product-level history (2023 loops → 2025 SDK →
  2026 managed agents) and the Agents / Environments / Sessions resource model.
  This earlier engineering post adds the **interface contract**
  (`execute`, `provision`, `wake`, `getSession`, `emitEvent`, `getEvents`), the
  "pet vs. cattle" failure story, the Git and MCP-proxy credential patterns,
  the "session is not the context window" argument, and the many-brains /
  many-hands generalization.
- Nuance for [[claude-managed-agents]]: the entity page says reasoning starts
  "while the sandbox spins up"; this post attributes the latency win to lazy
  provisioning (no container until a tool call needs one).
- The stale-assumption argument matches
  [[anthropic-eng-harness-design-long-running-apps]] (stress-test each harness
  component per model) and [[harnessing-claudes-intelligence]].
- Its credential pattern is the server-side counterpart of the local
  containment in [[anthropic-eng-how-we-contain-claude]].
