---
title: Agents vs. Workflows
type: concept
created: 2026-06-21
updated: 2026-06-21
tags: [agents, workflows, architecture]
---

# Agents vs. Workflows

> The foundational distinction in both guides: when does an LLM system need to
> *dynamically direct itself* (agent) versus follow *predefined paths* (workflow
> / conventional automation)?

## Definition

[[anthropic]] frames a spectrum of **agentic systems**:
- **Workflows** — LLMs and tools orchestrated through **predefined code paths**.
  Predictable and consistent; best for well-defined tasks. (see [[anthropic-building-effective-agents]])
- **Agents** — LLMs **dynamically direct their own processes and tool usage**,
  controlling how they accomplish a task. (see [[anthropic-building-effective-agents]])

[[openai]] defines an **agent** as a system that *independently accomplishes
tasks on your behalf*, using an LLM to manage workflow execution and select
tools within guardrails. Crucially, apps that integrate LLMs but **don't** use
them to control execution — chatbots, single-turn LLMs, sentiment classifiers —
are **not** agents. (see [[openai-practical-guide-to-building-agents]])

## When to build an agent

Both guides converge: reach for an agent only when simpler approaches fall short.

- **Anthropic:** use agents for open-ended problems where the number of steps
  can't be predicted and you can't hardcode a fixed path; use [[workflow-patterns]]
  or a single LLM call otherwise.
- **OpenAI:** prioritize workflows that resisted traditional automation —
  **complex decision-making** (nuanced judgment/exceptions), **hard-to-maintain
  rules** (unwieldy rulesets), and **heavy reliance on unstructured data**. If a
  deterministic solution suffices, use it.

## Why it matters

This choice sets the entire architecture. Picking an agent for a task a workflow
could handle adds latency, cost, and unpredictability for no benefit — the most
common anti-pattern both guides warn against. See [[agent-design-principles]].

## Related concepts

- [[workflow-patterns]] — the composable middle ground before full agents.
- [[agent-orchestration]] — once you've chosen an agent, how to structure it.
- [[agent-design-principles]] — start simple; add complexity only when justified.

## Key entities

- [[anthropic]], [[openai]]

## Appears in

- [[anthropic-building-effective-agents]]
- [[openai-practical-guide-to-building-agents]]

## Contradictions / open questions

- Mostly terminological: Anthropic treats "workflow" as one kind of *agentic
  system*; OpenAI treats "workflow" as the goal an agent executes. The
  substance — dynamic control is what makes something an agent — agrees.
