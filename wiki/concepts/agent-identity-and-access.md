---
title: Agent Identity and Access
type: concept
created: 2026-10-13
updated: 2026-10-13
tags: [identity, access-control, least-agency, credentials, rbac, security, guardrails]
---

# Agent Identity and Access

> Who an agent acts as, what it may reach, and how its credentials are held.
> Split out of [[guardrails]], which keeps risk assessment, environment
> containment, harness-enforced controls, and human-in-the-loop.

## Definition

Agent identity and access covers three questions. First, under whose identity
the agent acts: its own principal, or the user who invoked it. Second, how far
that identity reaches: per channel, per compartment, or bounded by the
triggering user. Third, how credentials are handled so the agent's sandbox
never holds a secret worth stealing. The risk-assessment question "what actions
can it take, and under whose identity?" comes from
[[anthropic-ciso-guide-agentic-ai]]; the rest of [[guardrails]] covers the
other three questions in that assessment.

## Least privilege and least agency

- **Least agency.** Grant the narrowest capability that still completes the
  task: least privilege extended to what each tool can do, how often, and
  where. Roll out to a small group first, watch telemetry, then expand. (see
  [[anthropic-ciso-guide-agentic-ai]], [[anthropic-zero-trust-for-ai-agents]])
- **No production credentials for change agents.** Anthropic's modernization
  guide gives agents write access only to modernization branches, no production
  credentials, masked secrets and PII, and every PR linked to the agent
  transcript and certificate evidence. (see [[anthropic-ai-code-modernization]])

## Who the agent acts as

- **The agent as its own principal.** In shared channels, Claude Tag acts under
  its own admin-provisioned accounts (Slack app, GitHub App, warehouse service
  account), scoped per channel, instead of borrowing any user's credentials. A
  shared channel then cannot reach a member's private documents. Workspace
  baselines are inherited and overridden per channel; revoking the identity cuts
  access everywhere. (see [[anthropic-agent-identity-access-model]])
  Multiplayer agents need credentials that belong to no single human. (see
  [[anthropic-building-effective-human-agent-teams]])
- **The cost: channel membership becomes an access grant.** A member without
  repo access can ask the agent to read the repo if the channel grants it.
  Mitigations: scope a channel profile to its least-privileged member, and use
  RBAC to limit who can invoke the agent. (see
  [[anthropic-agent-identity-access-model]]) Anthropic's analytics agent has the
  same property, so its data team scopes the service account to governed tables,
  gives it no PII clearance (PII labelled per column), owns channel membership as
  an access grant, and labels every query with surface, conversation, and user
  for audit. (see [[anthropic-claude-tag-analytics-in-slack]])
- **The alternative: bound access by the triggering user.** Asana reports that
  an agent's effective access never exceeds the permissions of the person who
  invokes it. (see [[anthropic-asana-coachable-agents]]) OpenAI's data agent
  lets users query only tables they already can access. (see
  [[openai-in-house-data-agent]]) Dust reports permission-aware retrieval and
  role-based access that keep each agent within its user's clearance. (see
  [[claude-customer-dust]]) Anthropic plans an identity-aware overlay that
  requires both the channel profile and the requesting user's permissions. (see
  [[anthropic-agent-identity-access-model]])
- **The identity spectrum.** One end is a single-purpose service account
  (incident agent, ticket triager); the other is a human credential with the
  person at the keyboard accountable. The middle, an agent carrying a person's
  delegated identity into systems that person is not watching, makes incidents
  hard to explain. (see [[anthropic-ciso-guide-agentic-ai]]) Anthropic's alert
  agent has three permissions (write new docs, post in channels, read
  production logs) and cannot deploy; its access to other agents is part of its
  boundary. (see [[anthropic-securing-ai-native-sdlc]])
- **One identity per agent.** When work is split across agents, each needs its
  own ID and credentials; shared credentials defeat the split. Receiving
  services should accept only named, cryptographically identified callers. (see
  [[anthropic-zero-trust-for-ai-agents]]) OpenAI's white paper agrees: agents
  need identities distinct from workforce identities, treated as non-human
  principals. (see [[openai-agent-security-enterprise]])
- **Context boundaries at workspace level.** Anthropic sets a few
  workspace-level security boundaries and lets context flow freely inside them,
  instead of per-item sharing decisions. (see
  [[anthropic-building-effective-human-agent-teams]])

## Task-scoped authority

OpenAI's agent security white paper frames identity around the task, not only
the agent. (see [[openai-agent-security-enterprise]])

- **A credential is not authorization.** A valid credential or tool connection
  gives access to a system without saying which actions are authorized. A
  runtime credential is not task authority, and a tool connection is not
  permission for every capability it exposes. Its example: an invoice agent
  renews a lapsing subscription to keep processing; every component allows the
  payment, but the contract was never part of its task.
- **Identity has facets.** A bill of materials (for provenance), a runtime
  identity (the workload doing the work), the task, and often client and
  session identifiers. Workforce identity names the person or organization
  behind a task; workload identity names the runtime performing it.
- **Task tokens exchanged for narrow credentials.** A request creates a task
  token bound to the runtime and the initiating user or system, carrying purpose
  and scope. The harness exchanges it for short-lived credentials scoped to one
  resource and action, so enforcement happens before any credential is issued.
  Avoid long-lived or shared keys; use enterprise SSO for people and workload
  identity federation for runtimes.
- **Four questions for every access request.** Who or what is acting; on whose
  behalf; for what purpose and within what bounds; and how another system can
  verify and audit that account. Audit should link principal → runtime → task
  → action → effect.
- **Expanding scope needs a new grant.** Sensitive actions require a new grant
  or stronger approval, not silent expansion; prefer time-limited grants to
  standing expansion, and re-evaluate the task after an approved crossing.
- **Stopping and revoking are separate operations.** Ending a task may leave a
  token valid at another service, and revoking a credential does not stop work
  already running. Revoke the narrowest authority that contains an incident and
  verify that downstream work is contained.

## Credential handling

- **Credentials never enter the sandbox.** The harness and sandbox see a
  placeholder or session token; a proxy or vault outside the sandbox injects the
  real credential on egress, only to allowlisted hosts. Instances: Managed Agents
  vault + MCP OAuth proxy (see [[anthropic-eng-scaling-managed-agents]],
  [[anthropic-evolution-of-agentic-surfaces]], [[anthropic-agents-production-systems-mcp]]);
  scheduled-agent vault with a `$SLACK_BOT_TOKEN`-style placeholder (see
  [[anthropic-building-effective-agent-automations]]); a short-lived push
  credential scoped to the session's own branch (see
  [[anthropic-claude-code-in-the-cloud]]); Claude Tag credentials mapped to the
  channel identity and injected per request (see
  [[anthropic-agent-identity-access-model]]); a reverse proxy that injects
  connector tokens so the sandbox holds nothing worth stealing (see
  [[anthropic-ciso-guide-agentic-ai]]); OpenAI hosted-shell `domain_secrets`
  sidecar, where the model and container see only placeholders (see
  [[openai-shell-skills-compaction]], [[openai-responses-api-computer-environment]]).
  OpenAI's white paper states the general rule: credential managers issue
  short-lived tokens and keep credential use outside the agent's context window.
  (see [[openai-agent-security-enterprise]])
  Symphony keeps the Linear token in the orchestrator and exposes a dynamic tool
  instead, so the token never reaches the agent's process. (see
  [[openai-symphony-codex-orchestration]]) Codex CLI and MCP OAuth tokens sit in
  the OS keyring. (see [[openai-running-codex-safely]]) For browser agents,
  sign-in values travel in a dedicated authentication event and never enter
  model input or history; tools whose results the model sees must never carry
  credentials. (see [[openai-agents-api-guide]])
- **Brain–hands separation + Vaults** (Anthropic) — credentials live outside the
  execution sandbox, accessed via signed tokens; a production form of tool
  safeguards. (see [[agent-harness]], [[anthropic-evolution-of-agentic-surfaces]],
  [[anthropic-eng-scaling-managed-agents]])

## Why it matters

Identity and credentials decide the blast radius when an agent is fooled or
wrong: environment controls cap what the sandbox can do, and identity caps what
the agent can reach outside it. Anthropic's guidance is to draw boundaries in
identity, permissions, and monitoring rather than in prompts, because those
survive model upgrades (see [[guardrails]], [[anthropic-ciso-guide-agentic-ai]]).

## Related concepts

- [[guardrails]] — the parent page: risk assessment, environment containment,
  harness-enforced controls, human-in-the-loop, observability.
- [[prompt-injection]] — identity and write scope bound what a followed
  injection can do.
- [[agent-harness]] — brain–hands separation keeps credentials outside the
  sandbox.
- [[model-context-protocol]] — MCP OAuth proxies inject connector credentials.
- [[agent-orchestration]] — one identity per agent when work is split.

## Key entities

- [[anthropic]], [[claude-managed-agents]], [[claude-code]], [[openai]],
  [[openai-codex]], [[openai-agents-api]]

## Appears in

- [[anthropic-ciso-guide-agentic-ai]]
- [[anthropic-zero-trust-for-ai-agents]]
- [[anthropic-ai-code-modernization]]
- [[anthropic-agent-identity-access-model]]
- [[anthropic-building-effective-human-agent-teams]]
- [[anthropic-claude-tag-analytics-in-slack]]
- [[anthropic-asana-coachable-agents]]
- [[openai-in-house-data-agent]]
- [[claude-customer-dust]]
- [[anthropic-securing-ai-native-sdlc]]
- [[anthropic-eng-scaling-managed-agents]]
- [[anthropic-evolution-of-agentic-surfaces]]
- [[anthropic-agents-production-systems-mcp]]
- [[anthropic-building-effective-agent-automations]]
- [[anthropic-claude-code-in-the-cloud]]
- [[openai-shell-skills-compaction]]
- [[openai-responses-api-computer-environment]]
- [[openai-symphony-codex-orchestration]]
- [[openai-running-codex-safely]]
- [[openai-agents-api-guide]]
- [[openai-agent-security-enterprise]]

## Contradictions / open questions

- **Agent identity versus per-user access (open, recorded 2026-10-12).**
  Claude Tag's own-principal model lets a channel member reach data that the
  member cannot reach directly ([[anthropic-agent-identity-access-model]],
  2026-06-24). Asana bounds access by the triggering user
  ([[anthropic-asana-coachable-agents]], 2026-09-29). The two designs trade
  long-running autonomy against per-user ACLs; Anthropic's planned overlay would
  combine them. OpenAI's white paper (Aug 2026) describes a third arrangement:
  the agent is a distinct non-human principal, but every task token is bound to
  the initiating user or system ([[openai-agent-security-enterprise]]).
