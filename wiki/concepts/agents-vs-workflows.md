---
title: Agents vs. Workflows
type: concept
created: 2026-06-21
updated: 2026-10-12
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

## Model-written workflows blur the line

[[claude-code]] dynamic workflows have the model write a task-specific
orchestration script (JavaScript built from `agent()`, `parallel()`, and
`pipeline()`) at run time. Each run then follows a predefined code path, as a
workflow does, but the model chose that path, as an agent does. The
predefined-code-path property belongs to each run, not to the system. (see
[[anthropic-harness-for-every-task]], [[workflow-patterns]])

## Who runs the loop

Once an agent is the right choice, a separate decision is who operates its loop.
[[openai]]'s runtime guide gives three options: the **Agents API**
([[openai-agents-api]]) runs a managed Codex harness for long-running tasks
with saved sessions; the [[openai-agents-sdk]] runs the loop inside your app
when you must control deployment, storage, approvals, and runtime; the
**Responses API** is for calling models directly or building an agent from
scratch. OpenAI rates integration effort low, medium, and high respectively.
(see [[openai-agents-api-guide]], [[agent-harness]]) [[anthropic]]'s managed
counterpart is [[claude-managed-agents]].

## Why it matters

This choice sets the entire architecture. Picking an agent for a task a workflow
could handle adds latency, cost, and unpredictability for no benefit — the most
common anti-pattern both guides warn against. See [[agent-design-principles]].

## Related concepts

- [[workflow-patterns]] — the composable middle ground before full agents.
- [[agent-orchestration]] — once you've chosen an agent, how to structure it.
- [[agent-design-principles]] — start simple; add complexity only when justified.
- [[agent-harness]] — the runtime that operates an agent's loop.

## Key entities

- [[anthropic]], [[openai]], [[claude-code]], [[openai-agents-api]],
  [[openai-agents-sdk]]

## Appears in

- [[anthropic-building-effective-agents]]
- [[openai-practical-guide-to-building-agents]]
- [[anthropic-harness-for-every-task]]
- [[openai-agents-api-guide]]

## Contradictions / open questions

- Mostly terminological: Anthropic treats "workflow" as one kind of *agentic
  system*; OpenAI treats "workflow" as the goal an agent executes. The
  substance — dynamic control is what makes something an agent — agrees.
- Open question (2026-10-12): model-written workflow code
  ([[anthropic-harness-for-every-task]]) fits neither definition cleanly. It is
  a workflow per run and an agent across runs; neither guide classifies it.
