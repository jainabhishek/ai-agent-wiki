---
title: "OpenAI (Developer blog): Designing Failover across OpenAI Model Providers"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Oliver Steffmann, Vik Bomma (OpenAI)
date: 2026-10-14
source_url: https://developers.openai.com/blog/designing-failover-across-openai-model-providers
source_path: raw/openai-failover-across-model-providers.md
tags: [reliability, failover, routing, llm-gateway, retries, idempotency, private-connectivity, financial-services, primary-source]
---

# OpenAI (Developer blog): Designing Failover across OpenAI Model Providers

> OpenAI's guidance for critical workloads on routing between the direct OpenAI
> API (1P) and OpenAI models on a cloud provider (3P): which requests may fail
> over, a five-row decision table, one retry controller, and who owns recovery.

## Summary

Written for financial-services customers. The running example is a
self-contained, **read-only fraud assessment** in a payments workflow, called
through the Responses API. The post separates two ideas: multi-provider support
is a **platform capability**, and failover is a **workflow decision**. Provider
failover helps only when the request is safe to repeat and the secondary meets
the workflow's requirements. Recovery of an ongoing Agents API session (its
conversation, saved work, and earlier actions) is called much harder and is out
of scope. The post gives a Codex prompt to implement a disabled-by-default
failover policy in an existing LLM gateway, then a validation checklist. It
names no model and reports no measurements.

## Key points

- **Why two routes.** Direct access gives eligible teams preview models and
  features before a cloud provider has them, and a possible recovery route.
  Production route choice follows where the workflow runs and its controls.
- **Routing versus failover are separate decisions.** Planned splits and
  overflow need their own capacity, cost, quality, and recovery tests. If the
  Decisions API feeds routing, define behavior when it is down.
- **Platform router, workflow policy.** The platform team operates the router;
  the application defines policy and is responsible for recovery state,
  settling which actions completed, checkpoints, and blocking repeated actions. When no route is
  eligible: queue, degrade, hand off, or reject.
- **Private connectivity differs by route.** OpenAI Private Link uses an Azure
  Private Endpoint (AWS and Google Cloud workloads need their own connectivity
  into Azure). Amazon Bedrock uses interface VPC endpoints via AWS PrivateLink;
  Azure OpenAI uses Azure private endpoints. Private Link does not fail over
  between regions automatically; fallback to public HTTPS needs explicit
  approval.
- **Operations that must not fail over:** a capability missing on the secondary
  (do not silently skip, for example, web search), unvalidated behavior (a
  matching model name is not enough; run the workflow's harness and evals), and
  residency or state constraints.
- **Model fallback versus provider failover.** Model fallback swaps the model;
  provider failover swaps the provider; sometimes both. First check whether a
  shared dependency (gateway, retrieval, identity) would break both routes.
- **Decision table (conservative default).** Consider failover for transient
  service or connection failures, and for sustained throttling that would miss a
  deadline. Never auto-switch for invalid requests, 401/403, safety refusals, or
  exhausted quota, credits, or spend; **unclassified errors must not trigger
  failover**. Never blindly replay partial output or an uncertain tool action;
  reconcile first. For model-specific capacity limits, try another approved
  model first.
- **One retry controller** across application, SDK, and gateway with a shared
  retry budget; honor valid `Retry-After`, else bounded exponential backoff with
  jitter; per-request and per-workflow deadlines. Circuit breakers per provider,
  model, region, and workflow. Cap failover traffic; restore the primary
  gradually.
- **The Codex prompt** asks for minimal patches, tests mapped to requirements,
  local HTTP stubs with external networking blocked, assertions on route order,
  call counts, and elapsed time, no secondary call in any blocked case, "do not
  guess approvals or limits", no live calls without authorization, and every
  unverified path left disabled.
- **Validation:** run both routes against the workflow's acceptance criteria;
  review data handling with legal, privacy, security, and governance owners (an
  endpoint's location or a private link alone does not settle it); monitor per
  model, account, and region, because provider-wide dashboards hide throttling;
  load-test the secondary with its own load plus failover traffic; compare cost
  per successful assessment.
- **Ownership:** a platform team owns integrations, router, monitoring, audit
  logs, and on-call route disabling; application owners own which operations may
  fail over, targets, reduced-function modes, and duplicate-action protection.

## Entities

[[openai]], [[openai-codex]], [[openai-agents-api]]. Amazon Bedrock, Azure
OpenAI, OpenAI Private Link, and the Decisions API have no wiki page.

## Concepts

[[boundary-contracts]], [[agent-evals]], [[agent-harness]]

## Notable claims & data

- A matching model name or a compatible-looking API does not count as proof:
  the post requires the workflow's own harness and evals on the secondary before
  failover. This is the
  same rule as [[boundary-contracts]] (verify against the real dependency) and a
  model-swap gate in [[agent-evals]].
- "Unclassified errors should not trigger failover" matches the fail-loud rule
  in [[boundary-contracts]]: no catch-all classifier that remaps unknown errors.
- Agents API sessions are explicitly out of scope: the post gives no recovery
  design for stateful agent sessions. Open question for [[openai-agents-api]].
- Private-connectivity facts are dated "at the time of publishing"; the post says
  provider support can change.

## Connections

- Stateful-session recovery is the case the post leaves out: compare saved
  sessions in [[openai-agents-api-guide]] and structured state across context
  windows in [[anthropic-eng-effective-harnesses-long-running-agents]].
- Duplicate-action protection and staged writes: compare
  [[anthropic-anatomy-of-commerce-agents]] (harness applies only approved IDs).
- Responses API background: [[openai-why-we-built-responses-api]],
  [[openai-one-year-of-responses]].
- See also [[openai-run-long-horizon-tasks-codex]] (a long Codex build run).
