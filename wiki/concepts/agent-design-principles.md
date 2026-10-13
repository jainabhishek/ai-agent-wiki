---
title: Agent Design Principles
type: concept
created: 2026-06-21
updated: 2026-10-13
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

The migration order follows from this: remove the previous model's workarounds
first (refusal steering, retry shims, lines such as "do not be lazy"), then re-run
the evals, and only then tune. (see [[anthropic-building-with-sonnet-5-5]],
[[agent-evals]])

**7. Design for cache hits.** Order static content first, send updates as
messages, keep models and tools stable within a session, and manage cache
breakpoints — a cost/latency lever that compounds over long runs. (see
[[harnessing-claudes-intelligence]])

**8. Optimize the system, not the model call.** A cheaper planner can create
more expensive workers, and a costly frontier planner can be economical when it
collapses ambiguity into bounded work. Evaluate the whole task tree by accepted
outcomes, not isolated token prices. (see [[multi-agent-economics]],
[[cursor-agent-swarm-model-economics]])

The unit of cost is the **completed task, not the token**. Anthropic's
model-selection guide says a smarter model often costs less per task because it
needs fewer turns and less thinking, and it recommends starting with the most
capable model and stepping down. Anthropic's commerce-agent guide sweeps models
and effort levels and measures cost per completed task. JetBrains reports a
model that is pricier per token but cheaper per task on some complex,
long-running work. (see [[anthropic-choosing-claude-model]],
[[anthropic-anatomy-of-commerce-agents]], [[anthropic-jetbrains-evaluates-fable-5]])

**9. Fail loud; record only confirmed effects.** An agent must not turn a failure
into a quiet success. If a source cannot be read (a server is down, a token has
expired), the agent reports that source as unreadable, never as "nothing new", and
leaves that source's state unchanged. A side effect (a post, a write) counts as done
only after the destination confirms it; the agent updates its own records after
that confirmation, and records an unclear result as unclear. Re-check the live
source right before acting, because the world changes between read and write. (see
[[anthropic-building-effective-agent-automations]], [[boundary-contracts]])

**10. Earn autonomy per task type.** Grant autonomy in proportion to the
reliability the agent has shown, and track it separately for each task type.
Review agent work by hand at first. Retest when the model changes, because old
guardrails can constrain a stronger model. (see
[[anthropic-building-effective-human-agent-teams]], [[guardrails]])

**11. Give the agent the controls a human in that role would have.** OpenAI's
prompt-injection guidance treats the agent like a human customer-service
worker: limit damage with the same caps, flags, and approvals that the role
would carry, rather than relying on the model to resist manipulation. (see
[[openai-designing-agents-resist-prompt-injection]], [[prompt-injection]])

**12. Code is the general interface.** Anthropic argues that code covers
almost any digital work, so one general agent with bash and a filesystem plus a
library of skills replaces many specialized agents. The general agent lacks
domain expertise, and skills supply it as files. (see
[[anthropic-building-agents-with-skills]], [[agent-skills]])

**13. A loop needs correct stopping and recovery.** An open-ended loop is only
viable when the agent stops at the right time and reroutes after a tool error.
Anthropic defines each loop type by its trigger and its stop condition. Genspark
reports that its ReAct-style loop failed for two years through infinite loops,
repeated errors, and not knowing when to stop, and that it replaced its fixed
workflow graph only once a model could stop correctly and try an alternative
after a tool error. (see [[anthropic-getting-started-with-loops]],
[[claude-customer-genspark]], [[agent-harness]])

**14. Plan the infrastructure around agents for agent-scale load.** Anthropic
reports that its CI jobs grew 25x in six months as agents wrote more code, and
that a stateless redesign succeeded where three patches to a single-writer
service failed. Its transferable rules: keep state out of the process from the
start, and plan for 25x load within two quarters. (see
[[anthropic-agentic-coding-ci-test-impact]])

## Why it matters

These principles are the through-line connecting every other best practice:
[[agents-vs-workflows]] (don't over-reach), [[agent-orchestration]] (single
before multi), and [[tool-design]] (clarity over count).

## Related concepts

- [[agents-vs-workflows]], [[agent-orchestration]], [[tool-design]],
  [[guardrails]], [[agent-harness]], [[context-engineering]], [[agent-skills]],
  [[multi-agent-economics]], [[boundary-contracts]], [[agent-evals]],
  [[prompt-injection]]

## Key entities

- [[anthropic]], [[openai]], [[claude]]

## Appears in

- [[anthropic-building-effective-agents]]
- [[openai-practical-guide-to-building-agents]]
- [[harnessing-claudes-intelligence]]
- [[anthropic-evolution-of-agentic-surfaces]]
- [[cursor-agent-swarm-model-economics]]
- [[anthropic-building-effective-agent-automations]]
- [[anthropic-building-with-sonnet-5-5]]
- [[anthropic-choosing-claude-model]]
- [[anthropic-anatomy-of-commerce-agents]]
- [[anthropic-jetbrains-evaluates-fable-5]]
- [[anthropic-building-effective-human-agent-teams]]
- [[openai-designing-agents-resist-prompt-injection]]
- [[anthropic-building-agents-with-skills]]
- [[anthropic-getting-started-with-loops]]
- [[claude-customer-genspark]]
- [[anthropic-agentic-coding-ci-test-impact]]
- [[anthropic-prompting-claude-fable-5]]
- [[openai-prompt-guidance-gpt-5-6]]

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
