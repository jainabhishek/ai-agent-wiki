---
title: "OpenAI: Agent Security in the Enterprise"
type: source
created: 2026-10-13
updated: 2026-10-13
author: OpenAI
date: 2026-08 (PDF cover; listed on OpenAI's learning hub 2026-09-02)
source_url: https://openai.com/business/learn/
source_path: raw/openai-agent-security-enterprise.md
tags: [openai, security, identity, access, threat-modeling, guardrails, incident-response, ciso]
---

# OpenAI: Agent Security in the Enterprise

> OpenAI's 30-page white paper for CISOs on deploying autonomous agents safely:
> five principles, a reach-and-blast-radius risk model, task-scoped identity and
> credentials, capability governance, control placement, and incident response.
> The paper sits behind a lead form; the human downloaded it and supplied the PDF.

## Summary

The paper argues that a valid credential grants access without saying which
actions are authorized, so enterprises must bind each agent action to a task, a
responsible principal, and an independent boundary that limits its effect. It
names five principles: agents as identifiable actors; authority constrained to
the task; context assumed untrusted; boundaries enforced and actions observed;
deployment with a plan. It is vendor guidance with no measured results, and it
names no model. It cites NIST SP 800-207, the NIST/CAISI AI Agent Standards
Initiative, Google's Secure AI Framework, OWASP's agentic Top 10 and LLM06
Excessive Agency, STRIDE, and MITRE ATLAS and ATT&CK.

## Key points

- **Task-scoped authority, not reachable APIs, is the control question.** In the
  paper's invoice example, an agent renews a lapsing subscription to keep work
  moving; each component allows the payment, but the contract was never part of
  its task. The fix is task-scoped authority plus an independent approval
  boundary. See [[agent-identity-and-access]], [[guardrails]].
- **Reach and blast radius.** Three terms: *reachable surface* (data, actions,
  destinations); *effective blast radius* (harm still possible after controls);
  *maximum completed effect* (the worst outcome before another independent
  decision is required). An approval on "send" does not undo a sensitive read.
- **Shared responsibility.** Enterprise-managed vs platform-managed agents;
  locally managed, remote, and hybrid harnesses. A harness does not by itself
  provide isolation. A customer-run connector stays customer-managed even when a
  remote agent calls it. See [[agent-harness]], [[claude-managed-agents]],
  [[openai-agents-api]].
- **Threat modeling.** Trace each path from low-trust context to a consequential
  action and name the independent boundary that limits it. An eight-row table
  lists attack and failure classes and what to validate for each. Start with
  tasks, keys, and tokens; the runtime; action gateways; and tools. See
  [[prompt-injection]].
- **Agent identity has facets.** Bill of materials (e.g. OWASP AIBOM), runtime
  identity, task, and client and session identifiers. A task token bound to the
  runtime and the initiating principal is exchanged for short-lived, resource-
  and action-scoped credentials, so enforcement happens before credentials exist.
  A runtime credential is not task authority. See [[agent-identity-and-access]].
- **Four questions for every access request.** Who or what is acting; on whose
  behalf; for what purpose and within what bounds; how another system can verify
  and audit the answer.
- **Revocation and stopping are separate operations.** Ending a task may leave a
  token valid elsewhere; revoking a credential does not stop running work.
  Revoke the narrowest authority that contains the incident.
- **Tools are a supply chain and a capability grant.** Keep an inventory and
  registry with owners, provenance, and expected effects; treat action or schema
  changes as security-relevant; test capabilities in combination (sensitive read
  plus external send; shell plus open egress). See [[model-context-protocol]],
  [[tool-design]].
- **Advisory checks are never the only control** for effects that must not occur
  automatically. Place enforced controls as close as possible to the effect;
  five layers from model and orchestration down to detection and response. When a
  block fires, tell operators which boundary fired.
- **Operations.** Minimum telemetry set; "guardian agents" in the harness as an
  added layer; a stop–contain–recover–learn incident plan; automated response
  limited to pre-approved, bounded containment; response drills before broad
  autonomy. A seven-item CISO checklist closes the paper.

## Entities

[[openai]], [[openai-agents-api]], [[openai-codex]].

## Concepts

[[agent-identity-and-access]], [[guardrails]], [[prompt-injection]],
[[agent-harness]], [[tool-design]], [[model-context-protocol]],
[[agent-memory]], [[human-agent-teams]].

## Notable claims & data

- The paper reports no measurements; every claim is a recommendation.
- "Guardian agents" are named as an enforcement aid inside the harness; the paper
  does not describe one in detail.
- It treats context and memory poisoning as a threat class whose control is
  isolating and reviewing persistent context (see [[agent-memory]]).

## Connections

- **Agrees with Anthropic's security guidance on almost every point.** Anthropic's
  CISO guide ([[anthropic-ciso-guide-agentic-ai]]) asks about untrusted input,
  identity, blast radius, and observability, and names "least agency"; this paper
  uses reach, blast radius, and task-scoped authority. Anthropic's Zero Trust
  ebook ([[anthropic-zero-trust-for-ai-agents]]) also gives each agent its own
  identity and verifies delegation. Both vendors put credentials outside the
  agent's context ([[anthropic-eng-scaling-managed-agents]],
  [[openai-responses-api-computer-environment]]).
- **Same "capability grant" framing as Anthropic.** Anthropic's containment post
  calls an allowlist "a capability grant, not just a destination filter"
  ([[anthropic-eng-how-we-contain-claude]]); this paper calls each tool
  integration a capability grant.
- **Advisory vs enforced controls** matches OpenAI's own Codex deployment guidance
  ([[openai-running-codex-safely]]) and its source-sink view of injection
  ([[openai-designing-agents-resist-prompt-injection]]).
- **Difference in emphasis.** Anthropic's Claude Tag lets an agent act as its own
  principal per channel ([[anthropic-agent-identity-access-model]]); this paper
  binds each task to its initiating user or system and treats the agent as a
  distinct non-human principal. The two are compatible, but they place the
  authority check at different points.
