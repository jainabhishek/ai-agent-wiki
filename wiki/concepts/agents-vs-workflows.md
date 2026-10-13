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

## Migrations from fixed workflows to agent loops

Several builders report replacing fixed workflows or graphs with one agent loop.
All of these are self-reported case studies, not controlled comparisons.

- **Genspark** reports that its directed graph of workflow nodes broke on edge
  cases, over-processed simple queries, and could not route around problems.
  It moved to a model-driven loop over 150+ tools once a model could stop
  correctly and recover from tool errors. (see [[claude-customer-genspark]])
- **Greptile** reports that its orchestration forced specialized review tools
  into a fixed sequence, so one step's findings could not steer the next. The
  agent now picks its next investigation step (multi-hop). (see
  [[claude-customer-greptile]])
- **OffDeal** reports that a separate workflow per task broke whenever a
  problem fell outside its predefined path or a procedure changed. One general
  agent with skills replaced 12+ workflows; its internal eval rose from 25% to
  85%. (see [[claude-customer-offdeal]])
- **Symphony** (OpenAI) reports that treating agents as "rigid nodes in a state
  machine" failed; agents now get objectives plus tools. The scheduler around
  them stays ordinary deterministic code. (see
  [[openai-symphony-codex-orchestration]])
- **CLUE** (Anthropic's alert triage) rejected the SOAR-playbook habit of
  defining every step. The team constrains which tools and data the agent can
  use and leaves the investigation strategy open. (see
  [[anthropic-cybersecurity-triage-agents]])

The shared reasons: fixed paths break on exceptions and changed procedures, and
a fixed order prevents one step's result from steering the next. Genspark's
account adds the precondition: the loop must stop correctly and recover from
errors (see [[agent-design-principles]]).

## Keep critical paths deterministic

The migrations do not remove deterministic code; they move it.
- Cresta reports hardening only the enterprise-critical workflows, because
  making everything deterministic yields a giant decision tree. Tests for the
  deterministic parts must change when business rules change. (see
  [[anthropic-cresta-agent-builder]])
- Caylent reports that scripts handle exact precision work and the model
  handles judgment and language. (see [[claude-customer-caylent]])
- Rocket Money reports running repeated actions as ordinary code, with an agent
  that steps in only when the code breaks, repairs it, and turns the fix back
  into code. A cheap classifier routes requests to single-purpose subagents.
  (see [[claude-customer-rocket-money]], [[workflow-patterns]])
- Symphony keeps the orchestration layer a deterministic workflow and makes the
  agent inside each ticket autonomous. (see [[openai-symphony-codex-orchestration]])

## Single agent before multi-agent

Anthropic's multi-agent guide states its thresholds for splitting into several
agents as guidelines that move as models improve; compaction now extends how
far a single agent can go before context limits force a split. (see
[[anthropic-building-multi-agent-systems]], [[agent-orchestration]])

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
- [[claude-customer-genspark]]
- [[claude-customer-greptile]]
- [[claude-customer-offdeal]]
- [[openai-symphony-codex-orchestration]]
- [[anthropic-cybersecurity-triage-agents]]
- [[anthropic-cresta-agent-builder]]
- [[claude-customer-caylent]]
- [[claude-customer-rocket-money]]
- [[anthropic-building-multi-agent-systems]]

## Contradictions / open questions

- Mostly terminological: Anthropic treats "workflow" as one kind of *agentic
  system*; OpenAI treats "workflow" as the goal an agent executes. The
  substance — dynamic control is what makes something an agent — agrees.
- Open question (2026-10-12): model-written workflow code
  ([[anthropic-harness-for-every-task]]) fits neither definition cleanly. It is
  a workflow per run and an agent across runs; neither guide classifies it.
- Evidence quality (2026-10-12): every workflow-to-loop migration above is a
  self-reported case study. No source gives a controlled comparison of the same
  task under both designs.
