---
title: "Agent-Building Best Practices: Anthropic vs. OpenAI"
type: synthesis
created: 2026-06-21
updated: 2026-06-21
tags: [agents, best-practices, comparison, synthesis]
---

# Agent-Building Best Practices: Anthropic vs. OpenAI

> Side-by-side synthesis of [[anthropic-building-effective-agents]] and
> [[openai-practical-guide-to-building-agents]] — where they agree, where they
> emphasize differently, and the distilled checklist.

## The shared thesis

Both companies, writing from large numbers of real deployments, land on the same
core message: **don't build an agent until you need one, build the simplest
version that works, measure it, and add complexity only when it earns its keep.**
See [[agent-design-principles]].

## Where they agree

| Best practice | Anthropic | OpenAI |
|---------------|-----------|--------|
| **Start simple** | "Simplest solution possible"; single LLM call often enough | "Maximize a single agent first"; incremental approach |
| **Agent ≠ every LLM app** | Workflows vs. agents spectrum | Chatbots/classifiers are *not* agents |
| **Use evals to optimize** | Optimize single calls with evaluation | Baseline with best model, then down-size on evals |
| **Tools are high-leverage** | Agent-Computer Interface (ACI) craft | Standardized, documented, tested tools |
| **Tool clarity > tool count** | Clear descriptions, examples, poka-yoke | 15 clear tools beat 10 overlapping ones |
| **Single → multi only when needed** | Orchestrator-workers when subtasks unpredictable | Manager / decentralized patterns when single agent strains |
| **Watch your abstractions** | Frameworks can hide behavior | Prefer code-first over declarative graphs |

See [[agents-vs-workflows]], [[tool-design]], [[agent-orchestration]].

## Where they emphasize differently

- **Anthropic goes deeper on workflow patterns** — five named, composable
  building blocks (prompt chaining, routing, parallelization,
  orchestrator-workers, evaluator-optimizer). See [[workflow-patterns]].
- **OpenAI goes deeper on production safety** — a full **guardrails** taxonomy
  (relevance, safety, PII, moderation, tool safeguards, rules-based, output
  validation) plus explicit **human-in-the-loop** triggers. See [[guardrails]].
- **OpenAI offers a crisper component model** — Model / Tools / Instructions —
  and concrete instruction-writing advice. See [[agent-core-components]],
  [[agent-instructions]].
- **Anthropic offers crisper principles** — simplicity, transparency, ACI.

The two are largely **complementary**: read Anthropic for the architecture
vocabulary and tool-interface craft; read OpenAI for the component checklist,
orchestration recipes, and the safety layer.

## Distilled checklist

1. **Decide if you even need an agent** ([[agents-vs-workflows]]). Prefer a
   workflow or single call when the path is predictable.
2. **Nail the three components** ([[agent-core-components]]): right model
   (baseline high, then down-size), well-documented tools, clear instructions.
3. **Engineer the tools** ([[tool-design]]): clarity, examples, poka-yoke,
   testing; reduce overlap before adding agents.
4. **Write unambiguous instructions** ([[agent-instructions]]): from real SOPs,
   step-by-step, with edge cases.
5. **Start single-agent with a run loop + prompt templates**
   ([[agent-orchestration]]); split to manager/decentralized only when logic or
   tool overlap forces it.
6. **Layer guardrails and human-in-the-loop** ([[guardrails]]).
7. **Measure with evals throughout; add complexity only when it pays**
   ([[agent-design-principles]]).

## Caveats & open questions

- Anthropic's piece is condensed in our raw capture; the authoritative full text
  may add nuance — re-verify against the source URL if a claim is load-bearing.
- **Data gap:** Anthropic has separate writing on context engineering, tool
  writing, and long-running harnesses (surfaced during search) not yet ingested —
  ingesting them would deepen the tooling/safety coverage.

## Sources & pages drawn on

- [[anthropic-building-effective-agents]]
- [[openai-practical-guide-to-building-agents]]
- [[agents-vs-workflows]], [[agent-design-principles]], [[agent-core-components]],
  [[tool-design]], [[workflow-patterns]], [[agent-orchestration]],
  [[agent-instructions]], [[guardrails]]
- [[anthropic]], [[openai]], [[openai-agents-sdk]]
