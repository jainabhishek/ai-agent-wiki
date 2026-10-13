---
title: "Claude customer story: Rocket Money on agents that fix their own code"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com customer stories); interviewees Aaron Dignan and Chase Adams, Rocket Money
date: "accessed 2026-10-12"
source_url: https://claude.com/customers/rocket-money-qa
source_path: raw/claude-customer-rocket-money.md
tags: [case-study, routing, agents-vs-workflows, agent-skills, self-healing-automation, structured-output, consumer-finance]
---

# Claude customer story: Rocket Money on agents that fix their own code

> Vendor-published Q&A on the architecture of Rowan, a text-message personal
> finance agent: a routed agent-workflow hybrid plus code that agents repair.

## Summary

Anthropic published this interview on claude.com. The page shows no
publication date; the wiki records it as accessed 2026-10-12. All claims are
self-reported by Rocket Money through Anthropic. The architecture names Haiku
4.5 (classifier), Sonnet 5 (most subagents), and Opus (unversioned, for hard
financial reasoning).

Rowan is not one agent with many tools. A cheap classifier routes each request
to a single-responsibility subagent, and one formatter subagent writes every
reply. Repeated actions such as subscription cancellations run as ordinary code.
An agent steps in only when that code breaks, repairs it, and turns the fix
back into code. Rocket Money calls this "third way engineering".

## Key points

- **Routing over a monolithic tool-heavy agent.** Classifier, specialized
  subagents, and a response formatter. Each failure traces to one classifier
  or call.
- **Small contexts, many calls.** Adams prefers five small-context calls to
  one large one, citing recency and primacy effects.
- **Code by default, agent on failure.** The agent self-heals a broken
  procedure (often after a website change) and re-codifies it. Skills that
  bundle scripts made this pattern concrete for the team.
- **Deterministic evals via structured output** instead of model
  self-grading.
- **Early off-topic fall-throughs** keep the agent in its domain.
- **Outcome classification then human handoff.** Claude judges whether an
  action succeeded and why not, then a human decides.
- **Plan for better models** (they assume 10–20% better in a couple of years).

## Entities

[[anthropic]], [[claude]]

## Concepts

[[workflow-patterns]], [[agents-vs-workflows]], [[agent-skills]],
[[agent-evals]], [[guardrails]], [[context-engineering]]

## Notable claims & data

- "No meaningful hallucination patterns" with beta users; suspected cases were
  data problems (self-reported, no numbers given).
- Interviewees say finance needs 100% accuracy, so a generic harness is
  insufficient. This is an opinion, not a measured result.

## Connections

The routing hybrid is the Routing pattern in [[workflow-patterns]] and
[[anthropic-building-effective-agents]]. "Scripts for deterministic work, model
for interpretation" matches [[agent-skills]] and
[[anthropic-eng-agent-skills]].
