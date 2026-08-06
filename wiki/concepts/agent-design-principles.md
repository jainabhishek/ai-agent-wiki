---
title: Agent Design Principles
type: concept
created: 2026-06-21
updated: 2026-08-06
tags: [agents, best-practices, principles, evals]
---

# Agent Design Principles

> The shared meta-principles both guides return to repeatedly: start simple,
> measure, and add complexity only when it earns its keep.

## The principles

**1. Start with the simplest thing that works.**
- [[anthropic]]: many applications need only a single LLM call with retrieval and
  in-context examples. Find the simplest solution; add complexity only when it
  demonstrably improves outcomes. (see [[anthropic-building-effective-agents]])
- [[openai]]: "maximize a single agent's capabilities first"; adopt an
  incremental approach rather than building a fully autonomous multi-agent system
  upfront. (see [[openai-practical-guide-to-building-agents]])

**2. Measure with evals before optimizing.** (see [[agent-evals]])
- [[openai]]'s model-selection loop: (1) set up evals for a performance baseline,
  (2) hit your accuracy target with the best models, (3) optimize cost/latency by
  swapping in smaller models where they still pass. Prototype with the most
  capable model first so you don't prematurely limit the agent.
- [[anthropic]]: optimize single calls with thorough evaluation before adding
  multi-step complexity; measure runtime/tokens/tool-calls/errors, not just
  accuracy.

**3. Transparency.** Show the agent's planning steps explicitly so behavior is
inspectable. (see [[anthropic-building-effective-agents]])

**4. Simplicity.** Keep the design simple; complexity is a cost paid in latency,
dollars, and debuggability. (see [[anthropic-building-effective-agents]])

**5. Understand your abstractions.** Frameworks help you start but add layers
that can hide the underlying prompts and control flow — know the code beneath.
[[openai]] makes the parallel point preferring **code-first** over declarative
graph frameworks (see [[openai-agents-sdk]]).

**6. Ask "what can I stop doing?" — prune scaffolding as the model improves.**
[[anthropic]]'s corollary to start-simple: harnesses must co-evolve with models,
and scaffolding built for an older model becomes dead weight. Re-test
assumptions about what the model "can't do" with each capability step change;
delete obsolete context resets, let the model orchestrate actions, manage its own
context, and persist its own memory. (see [[harnessing-claudes-intelligence]],
[[agent-harness]], [[context-engineering]])

Prompts are scaffolding too. Current model documentation from both labs
independently instructs *removing* prompt scaffolding rather than adding it —
explicit verification steps, forced status summaries, exhaustive rule
enumeration — with the strongest form of the claim being that legacy prompt
scaffolding degrades output quality rather than merely wasting tokens. (see
[[prompt-tuning-axes]], [[anthropic-prompting-claude-fable-5]],
[[openai-prompt-guidance-gpt-5-6]])

**7. Design for cache hits.** Order static content first, send updates as
messages, keep models and tools stable within a session, and manage cache
breakpoints — a cost/latency lever that compounds over long runs. (see
[[harnessing-claudes-intelligence]])

**8. Optimize the system, not the model call.** A cheaper planner can create
more expensive workers, and a costly frontier planner can be economical when it
collapses ambiguity into bounded work. Evaluate the whole task tree by accepted
outcomes, not isolated token prices. (see [[multi-agent-economics]],
[[cursor-agent-swarm-model-economics]])

## Why it matters

These principles are the through-line connecting every other best practice:
[[agents-vs-workflows]] (don't over-reach), [[agent-orchestration]] (single
before multi), and [[tool-design]] (clarity over count).

## Related concepts

- [[agents-vs-workflows]], [[agent-orchestration]], [[tool-design]],
  [[guardrails]], [[agent-harness]], [[context-engineering]], [[agent-skills]],
  [[multi-agent-economics]]

## Key entities

- [[anthropic]], [[openai]], [[claude]]

## Appears in

- [[anthropic-building-effective-agents]]
- [[openai-practical-guide-to-building-agents]]
- [[harnessing-claudes-intelligence]]
- [[anthropic-evolution-of-agentic-surfaces]]
- [[cursor-agent-swarm-model-economics]]

## Contradictions / open questions

- The architecture principles remain the strongest point of agreement between the
  two original guides.
- **Principle 3 (Transparency) needs a caveat as of 2026-08-06.** Claude Fable 5
  runs a `reasoning_extraction` classifier: prompts or skills instructing the
  model to echo, transcribe, or explain its internal reasoning as response text
  can trigger a refusal. Transparency should be obtained from structured
  `thinking` blocks rather than from prompted self-narration. The principle holds;
  the older implementation of it does not. (see
  [[anthropic-prompting-claude-fable-5]])
