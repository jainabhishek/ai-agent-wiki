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

## Update: additional Anthropic operational depth (2026-06-21)

Four further Anthropic blog sources now extend this comparison beyond the two
original guides, adding *operational* best practices the OpenAI guide touches only
lightly:

- **Context engineering** — load on demand, let the agent manage/persist its own
  context, design for cache hits. ([[context-engineering]],
  [[harnessing-claudes-intelligence]])
- **Agent harness** — separate brain (harness) from hands (sandbox) via durable
  sessions; co-evolve the harness with the model and prune dead scaffolding.
  ([[agent-harness]], [[anthropic-evolution-of-agentic-surfaces]])
- **Skills & steering** — package procedural know-how as on-demand
  [[agent-skills]]; choose the right steering mechanism for the job
  ([[agent-steering]], [[anthropic-steering-claude-code]],
  [[anthropic-lessons-building-claude-code-skills]]).

These reinforce rather than contradict the shared thesis: the new principles
("ask what you can stop doing," progressive disclosure, harness co-evolution) are
all forms of *start simple and add complexity only when it earns its keep.*

## Caveats & open questions

- Anthropic's *Building Effective Agents* piece is condensed in our raw capture;
  re-verify against the source URL if a claim is load-bearing.
- The deeper Anthropic *engineering* posts (anthropic.com/engineering: context
  engineering, writing tools for agents, long-running harnesses) are still
  un-ingested — they would add primary-source depth behind the blog summaries.
- OpenAI-side depth on harness/context engineering is comparatively thin in the
  ingested guide — a candidate for a future OpenAI source.

## Sources & pages drawn on

- [[anthropic-building-effective-agents]]
- [[openai-practical-guide-to-building-agents]]
- [[anthropic-steering-claude-code]], [[anthropic-lessons-building-claude-code-skills]],
  [[harnessing-claudes-intelligence]], [[anthropic-evolution-of-agentic-surfaces]]
- [[agents-vs-workflows]], [[agent-design-principles]], [[agent-core-components]],
  [[tool-design]], [[workflow-patterns]], [[agent-orchestration]],
  [[agent-instructions]], [[guardrails]], [[agent-skills]], [[agent-steering]],
  [[context-engineering]], [[agent-harness]]
- [[anthropic]], [[openai]], [[openai-agents-sdk]], [[claude]], [[claude-code]],
  [[claude-agent-sdk]], [[claude-managed-agents]]
