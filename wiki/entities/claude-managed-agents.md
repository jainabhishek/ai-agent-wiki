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
  (see [[anthropic-building-effective-agent-automations]], [[agent-memory]])
- Deployment options: Anthropic-managed containers, self-hosted sandboxes (VPC),
  MCP tunnels. MCP tunnels use an outbound-only connection with no exposed
  ports. **Vaults** hold and refresh user OAuth tokens, and a session references
  a vault by ID at creation. (see [[anthropic-agents-production-systems-mcp]],
  [[guardrails]])
- **Rubrics** (beta) let a separate grader agent check an agent's output. (see
  [[anthropic-verification-loops-with-skills]], [[agent-evals]])

### Operating agents: versions, staging, and agents as code
- **Console edits and versions.** In Anthropic's own sales deployment, sales
  and content leads edited the system prompt in the Console. Each change went
  to a staging agent first, every change is a new version, and sessions can be
  pinned back to an earlier version. Anthropic reports seven versions within a
  week of internal testing. (see [[anthropic-sales-inbound-managed-agents]])
- **Agents as code.** ABC Legal reports that each agent is a folder in git: a
  JSON config, a Markdown system prompt, deploy scripts, and ops docs. Prompt,
  tool list, schedule, credentials, and memory live as config files, and a
  merge to main deploys the agent. The pull request is the control surface for
  review, rollback, and audit. (see [[anthropic-abc-legal-managed-agents]])
- **Responsibility split.** ABC Legal describes the platform as owning the
  loop, sessions, memory, Console, and models, while the customer owns the
  prompt, tools, triggers, audit trail, and outcome feedback. (see
  [[anthropic-abc-legal-managed-agents]], [[agent-harness]])

### Case studies (self-reported)
- **ABC Legal** (as of July 2026) reports 50+ agents in production, about 310
  daily users, and up to ~50% lower cost on some covered tasks. Agents start in
  recommendation mode and move to automation only after they match or beat
  humans on the task. A harvester-tuner loop turns Slack feedback into prompt
  and config PRs that a human merges. (see
  [[anthropic-abc-legal-managed-agents]])
- **Anthropic sales inbound** (2026-09-30): an opt-in buying agent that answers
  pricing, security, and data questions and ends in a purchase or a hand-off
  to a rep. Anthropic reports that a one-sentence goal outperformed a
  qualification flowchart, and that fixing the most common escalation reasons
  halved the share of conversations that needed a human. (see
  [[anthropic-sales-inbound-managed-agents]])
- **monday.com** offers "Bring Your Own Agent" for Managed Agents as assignable
  teammates on its boards, and a coding integration where Managed Agents run in
  the customer's environment and post results back to the ticket. (see
  [[anthropic-monday-agent-first-platform]])
- **Datadog** uses its Temper kernel as the managed-agent control plane in its
  Helix "dark factory". A Twilio engineer built memory and "dreaming" locally
  to evaluate Managed Agents on first-hand cost and latency data. (see
  [[anthropic-datadog-universal-machine-tool]], [[claude-customer-twilio]])

## Relationships

- Built by [[anthropic]]; successor surface to [[claude-agent-sdk]]; underpins
  the agent runtime concepts in [[agent-orchestration]].
- Architecturally parallel to [[openai-agents-api]] (a vendor-hosted harness
  with durable sessions and sandboxes). (see [[openai-agents-api-guide]])
- Identity: Managed Agents keeps credentials in Vaults and out of the sandbox
  (see [[anthropic-eng-scaling-managed-agents]]). Anthropic's Deputy CISO lists
  the same rule, that the sandbox never holds a credential worth stealing, among
  seven controls, using Claude Cowork as the example (see
  [[anthropic-ciso-guide-agentic-ai]]). The agent-as-own-principal model, with
  credentials injected at the network boundary per channel, is described for
  Claude Tag (Claude in Slack), not for Managed Agents (see
  [[anthropic-agent-identity-access-model]], [[guardrails]]).
- The single-agent-first guidance for when to build multi-agent systems on the
  platform is in [[anthropic-building-multi-agent-systems]].

## Appears in

- [[anthropic-evolution-of-agentic-surfaces]]
- [[anthropic-eng-scaling-managed-agents]]
- [[anthropic-building-effective-agent-automations]]
- [[openai-agents-api-guide]]
- [[openai-codex-as-a-platform]]
- [[anthropic-abc-legal-managed-agents]]
- [[anthropic-sales-inbound-managed-agents]]
- [[anthropic-monday-agent-first-platform]]
- [[anthropic-agents-production-systems-mcp]]
- [[anthropic-verification-loops-with-skills]]
- [[anthropic-datadog-universal-machine-tool]]
- [[anthropic-building-multi-agent-systems]]
- [[anthropic-building-agents-claude-agent-sdk]]
- [[anthropic-agent-identity-access-model]]
- [[anthropic-ciso-guide-agentic-ai]]
- [[claude-customer-twilio]]

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
- **Scheduled tasks or Managed Agents for recurring agents?** ABC Legal
  (2026-08-17) built scheduled tasks and local routines first, because Managed
  Agents was newly in beta, and now advises going straight to Managed Agents
  ([[anthropic-abc-legal-managed-agents]]). Anthropic's loops guide
  (2026-06-30) recommends `/loop` and `/schedule` in [[claude-code]] for
  recurring work and polling ([[anthropic-getting-started-with-loops]]). The
  advice may differ by scope: always-on, versioned production agents versus a
  developer's recurring task. Neither source compares the two.
