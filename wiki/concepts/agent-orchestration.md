---
title: Agent Orchestration
type: concept
created: 2026-06-21
updated: 2026-10-12
tags: [orchestration, multi-agent, single-agent, patterns]
---

# Agent Orchestration

> How to structure execution once you've chosen an agent: the run loop, when to
> stay single-agent, and the two multi-agent patterns. Both guides agree:
> **maximize a single agent first.** (see [[openai-practical-guide-to-building-agents]],
> [[agent-design-principles]])

## The agent run loop

Every orchestration needs a **run** — a loop that lets the agent operate until an
**exit condition**: a final-output tool, a structured output of a given type, an
error, or a maximum number of turns. In the [[openai-agents-sdk]], `Runner.run()`
loops the LLM until a final-output tool fires or the model replies with no tool
calls. (see [[openai-practical-guide-to-building-agents]])

[[anthropic]]'s agents work the same way: plan → act via tools → observe
environmental ground truth → repeat, with stopping conditions and guardrails.
(see [[anthropic-building-effective-agents]])

In production, the loop is realized as a durable **session** — an append-only log
of every model call, tool call, and result — with the harness (brain) separated
from the execution sandbox (hands). See [[agent-harness]] and
[[anthropic-evolution-of-agentic-surfaces]].

## Single-agent systems

A single agent handles many tasks by **incrementally adding tools**, keeping
evaluation and maintenance simple. To manage complexity without splitting:
use a single flexible **prompt template** with policy variables rather than many
bespoke prompts. (see [[openai-practical-guide-to-building-agents]])

**When to split into multiple agents:**
- **Complex logic** — prompts full of if-then-else branches that don't scale.
- **Tool overload** — driven by tool *overlap*, not count (see [[tool-design]]).

**Subagents** are a lightweight form of multi-agent: they run in an isolated
context window and return only a final summary, keeping the main thread clean.
Use them for deep search, log analysis, or audits whose intermediate results you
won't reference again; they can nest several levels and orchestrate many
background agents, with plans/results held in script variables rather than
context. (see [[anthropic-steering-claude-code]], [[context-engineering]])
A subagent can also add a capability without adding a tool: Claude Code's docs-search
subagent searches in its own context and returns only the answer. (see
[[anthropic-seeing-like-an-agent]])

A subagent is also the way to **switch models** inside a session. Prompt caches are
per model, so switching the main thread's model mid-session pays for the whole
prefix again; a subagent on the other model with a hand-off message avoids that.
Claude Code's Explore agents run on a smaller model this way. (see
[[anthropic-prompt-caching-is-everything]])

**Why split planning from execution.** One context that both plans and executes
shows three failure modes: *agentic laziness* (stopping partway through a long item
list), *self-preferential bias* (grading its own work), and *goal drift* (losing
requirements after compaction). Separate focused subagents counter all three. In
Claude Code's dynamic workflows the model writes a per-task orchestration script
with `agent`, `parallel`, and `pipeline` primitives; this costs more tokens, so it
suits complex, high-value tasks. (see [[anthropic-harness-for-every-task]],
[[workflow-patterns]], [[multi-agent-economics]])

How readily a given model delegates is a per-model behavior, tuned in the prompt;
see axis 5 of [[prompt-tuning-axes]]. For example, OpenAI supplies a prompt for a
model that delegates less than desired, plus one that fixes errors in messages
between agents. (see [[openai-prompting-gpt-6-astra]])

## Multi-agent patterns (OpenAI)

- **Manager (agents as tools)** — a central manager LLM delegates to specialized
  agents via tool calls and synthesizes results. Best when one agent should keep
  control and user contact. Mirrors Anthropic's **orchestrator-workers**
  ([[workflow-patterns]]).
- **Decentralized (handoffs)** — peer agents transfer execution to one another; a
  handoff is a one-way tool call that passes conversation state. Best for triage
  and when a specialist should fully take over.

Both can be modeled as graphs (agents = nodes; edges = tool calls or handoffs).
The guiding principle across patterns: keep components **flexible, composable,
and driven by clear prompts.**

## Trust and checks at the subagent boundary

- **Subagent output is an injection path.** An orchestrator that trusts subagent
  output more than raw tool output gives injected content a route to escalate
  trust; Anthropic lists this as an open containment problem. (see
  [[anthropic-eng-how-we-contain-claude]], [[guardrails]])
- **Check at both crossings.** Claude Code's auto-mode classifier checks the
  handoff on delegation, where it can deny (inside a subagent the orchestrator's
  instruction looks like a user message), and on return, where it only warns.
  (see [[anthropic-eng-claude-code-auto-mode]])
- **The orchestrator verifies subagent evidence.** For fan-out audits, migrations,
  and large reviews, tell the orchestrator to check each subagent's evidence
  before accepting it. (see [[anthropic-getting-most-out-of-opus-5-5]]) The
  architecture form is adversarial verification: a separate agent checks the work
  against a rubric. (see [[anthropic-harness-for-every-task]])
- **Quarantine untrusted input.** Read-only reader agents summarize untrusted
  content into structured output; a separate privileged actor acts only on the
  summaries. (see [[anthropic-harness-for-every-task]])
- **Some powers stay with the main agent.** In OpenAI's Agents API only the main
  agent may request browser sign-in; subagents cannot. (see
  [[openai-agents-api-guide]])

## Harness signals for parallel work

Two current Anthropic harness patterns change how a lead agent paces subagents.
Both are model-scoped; the source pages hold the details.
- **Elapsed-time budget.** A line on each message stating elapsed time against an
  advisory budget let a lead agent pace and parallelize, and teams finished sooner
  at comparable quality. Keep a hard timeout as well. (see
  [[anthropic-prompting-claude-opus-5-5]]) Contrast the warning against showing a
  remaining-*token* countdown, recorded on [[prompt-tuning-axes]].
- **Non-blocking subagent start.** A subagent-start tool that returns at once,
  plus a separate wait tool, lowered average time to completion at similar
  quality, tokens, and cost. (see [[anthropic-prompting-claude-fable-5-1]])
- An unattended lead agent must wait for background subagents before it treats a
  task as complete. (see [[anthropic-prompting-claude-opus-5-5]])

## Evidence from Anthropic's multi-agent research system

[[anthropic-eng-multi-agent-research-system]] quantifies the tradeoff:
- A lead-agent + parallel-subagent system **beat single-agent Opus 4 by 90.2%**
  on breadth-first research; parallelism (3–5 subagents, 3+ parallel tool calls
  each) cut research time up to 90%.
- But **token usage alone explains ~80% of performance variance** — the gain
  comes from spreading work across separate context windows
  ([[context-engineering]]), not orchestration complexity itself.
- It's expensive (~15× chat tokens) and **fails when context must be shared**
  (e.g. most coding), so it isn't a default — consistent with single-agent-first
  and [[agents-vs-workflows]].
- Prompt the orchestrator with **effort-scaling rules** (agent count by query
  complexity) and **explicit delegation** (objective, output format, boundaries).

## Coding swarms and coordination

Cursor's SQLite experiment shows that shared-context coding is not categorically
incompatible with multi-agent work, but the harness must carry coordination that
ordinary Git workflows leave to humans. Its new swarm assigned shared design
decisions to planners, delegated disjoint leaves, reconciled decision documents,
used neutral conflict resolution, decomposed contested megafiles, and stacked
independent review lenses. The authors attribute scaling primarily to context
efficiency rather than parallelism. (see
[[cursor-agent-swarm-model-economics]], [[multi-agent-economics]])

Isolation has the opposite cost. In Claude Code cloud sessions each task gets its
own VM and branch, so parallel sessions cannot see each other's fixes: one session
found the same bug a sibling session was fixing. The advice is to split parallel
tasks along file boundaries, merge in a sensible order, and expect duplicate
problem reports. (see [[anthropic-claude-code-in-the-cloud]])

## Declarative vs. code-first

OpenAI contrasts **declarative graph** frameworks (define every branch/loop
upfront) with the [[openai-agents-sdk]]'s **code-first** approach (express logic
with normal programming constructs). Echoes Anthropic's caution about framework
abstraction in [[agent-design-principles]].

## Related concepts

- [[workflow-patterns]], [[agent-core-components]], [[tool-design]],
  [[agent-design-principles]], [[guardrails]], [[agent-harness]],
  [[context-engineering]], [[prompt-tuning-axes]], [[multi-agent-economics]]

## Key entities

- [[openai]], [[openai-agents-sdk]], [[anthropic]], [[claude-code]],
  [[claude-managed-agents]]

## Appears in

- [[openai-practical-guide-to-building-agents]]
- [[anthropic-building-effective-agents]]
- [[anthropic-steering-claude-code]]
- [[anthropic-evolution-of-agentic-surfaces]]
- [[anthropic-eng-context-engineering]]
- [[anthropic-eng-effective-harnesses-long-running-agents]]
- [[anthropic-eng-multi-agent-research-system]]
- [[cursor-agent-swarm-model-economics]]
- [[anthropic-seeing-like-an-agent]]
- [[anthropic-prompt-caching-is-everything]]
- [[anthropic-harness-for-every-task]]
- [[anthropic-eng-how-we-contain-claude]]
- [[anthropic-eng-claude-code-auto-mode]]
- [[anthropic-getting-most-out-of-opus-5-5]]
- [[anthropic-claude-code-in-the-cloud]]
- [[anthropic-prompting-claude-opus-5-5]]
- [[anthropic-prompting-claude-fable-5-1]]
- [[openai-agents-api-guide]]
- [[openai-prompting-gpt-6-astra]]

## Contradictions / open questions

- [[anthropic-eng-multi-agent-research-system]] reports that multi-agent systems
  are a poor fit when agents must share context, including most coding.
  [[cursor-agent-swarm-model-economics]] demonstrates a counterexample at extreme
  scale using a custom VCS and explicit coordination mechanisms. The practical
  boundary appears to be harness capability and task partitionability, not a
  categorical research-versus-coding distinction; replication on ordinary Git
  repositories remains open.
- **Separate verifier agents: architecture pattern vs model default.**
  [[anthropic-harness-for-every-task]] (written when Claude Opus 4.8 was current)
  builds adversarial verification from separate agents, and the legacy
  [[anthropic-prompting-claude-fable-5]] page recommended fresh-context verifier
  subagents. [[anthropic-prompting-claude-sonnet-5-5]] (2026-10-12) says not to let
  the model launch reviewer subagents unless asked, because they raised cost with
  no quality change. The two may not conflict — one is a harness the developer
  designs, the other is the model's unprompted habit — but no source tests when a
  separate verifier still pays for itself on current models. See
  [[prompt-tuning-axes]].
