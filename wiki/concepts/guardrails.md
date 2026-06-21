---
title: Guardrails & Safety
type: concept
created: 2026-06-21
updated: 2026-06-21
tags: [guardrails, safety, security, human-in-the-loop]
---

# Guardrails & Safety

> [[openai]]'s most developed area: guardrails as a **layered defense**. No single
> guardrail suffices; stack specialized ones for resilience, and pair them with
> auth, access controls, and standard software security. (see
> [[openai-practical-guide-to-building-agents]])

## Types of guardrails

| Guardrail | Purpose |
|-----------|---------|
| **Relevance classifier** | Keep responses in scope; flag off-topic queries. |
| **Safety classifier** | Detect jailbreaks / prompt injections. |
| **PII filter** | Vet output for personally identifiable information. |
| **Moderation** | Flag hate, harassment, violence, etc. |
| **Tool safeguards** | Rate each tool low/med/high risk (read vs. write, reversibility, permissions, financial impact); gate or escalate high-risk calls. |
| **Rules-based protections** | Blocklists, input length limits, regex (e.g., SQL-injection guards). |
| **Output validation** | Brand-aligned responses via prompt engineering + content checks. |

A robust setup combines **LLM-based + rules-based + moderation** guardrails to vet
inputs and outputs.

## How to build them

OpenAI's heuristic:
1. Start with **data privacy and content safety**.
2. Add guardrails for **real-world edge cases and failures** you encounter.
3. **Optimize for both security and UX**, tuning as the agent evolves.

In the [[openai-agents-sdk]], guardrails are first-class with **optimistic
execution**: the agent generates while guardrails run concurrently, raising a
**tripwire exception** on violation.

## Human-in-the-loop

A critical safeguard, especially early in deployment. Let the agent gracefully
transfer control when it can't complete a task. Two primary triggers:
- **Exceeding failure thresholds** — cap retries/actions; escalate past the limit.
- **High-risk actions** — sensitive/irreversible/high-stakes actions (cancel
  orders, large refunds, payments) get human oversight until confidence grows.

## Relation to Anthropic

[[anthropic]] addresses safety through **trusted environments**, **stopping
conditions**, transparency, and **poka-yoke** tool design ([[tool-design]]) rather
than a named guardrails taxonomy — complementary rather than conflicting. See
[[agent-building-best-practices-anthropic-vs-openai]].

The Anthropic sources add concrete deterministic and infrastructural guardrails:
- **Hooks** as deterministic policy — a PreToolUse hook can inspect any tool call
  and deny it (exit 2). The deterministic complement to LLM-based classifiers.
  (see [[agent-steering]], [[anthropic-steering-claude-code]])
- **Brain–hands separation + Vaults** — credentials live outside the execution
  sandbox, accessed via signed tokens; a production form of tool safeguards. (see
  [[agent-harness]], [[anthropic-evolution-of-agentic-surfaces]])

## Related concepts

- [[agent-orchestration]], [[tool-design]], [[agent-instructions]],
  [[agent-design-principles]], [[agent-steering]], [[agent-harness]]

## Key entities

- [[openai]], [[openai-agents-sdk]], [[anthropic]], [[claude-managed-agents]]

## Appears in

- [[openai-practical-guide-to-building-agents]]
- [[anthropic-steering-claude-code]]
- [[anthropic-evolution-of-agentic-surfaces]]

## Contradictions / open questions

- OpenAI still has the most explicit *classifier* taxonomy; Anthropic's
  contribution here is deterministic (hooks) and infrastructural (vaults,
  sandbox isolation). A dedicated Anthropic safety/guardrails post would round
  this out further.
