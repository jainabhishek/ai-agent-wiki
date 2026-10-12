---
title: Agent Harness
type: concept
created: 2026-06-21
updated: 2026-10-12
tags: [harness, architecture, agents, sessions, best-practices]
---

# Agent Harness

> The harness is the scaffolding around the model — the loop, tool wiring, context
> management, and execution environment that turn a model into an agent. Two
> ingested Anthropic sources argue the harness must **co-evolve with the model**
> and should stay as thin as the model allows.

## Definition

The code that calls the model, manages its context, executes its tool calls, and
decides when a run ends. Historically hand-rolled ("tokens in, tokens out"), then
tuned in SDKs ([[claude-agent-sdk]], [[openai-agents-sdk]]), then partly delegated
to managed platforms ([[claude-managed-agents]]). (see
[[anthropic-evolution-of-agentic-surfaces]])

## Brain–hands separation

A durable production pattern: run the **harness (brain)** separately from the
**sandbox (hands)** where code/tools execute, connected by a **session** — an
append-only log of every model call, tool call, and result. Yields latency wins
(mechanism disputed; see Contradictions), credential isolation (vaults outside
the sandbox), and resumable, auditable runs. This is the concrete form of the
run-loop / exit-condition idea in [[agent-orchestration]] and the persistence
idea in [[context-engineering]].

- **Interfaces are the stable part.** Because every harness component goes
  stale as models improve, [[claude-managed-agents]] fixes small interfaces
  instead of a harness (a "meta-harness"): one `execute(name, input) → string`
  call for every sandbox or tool, so a dead container is a tool error the model
  can handle, and a session log outside the harness, so a fresh harness can
  resume from the last event. Session storage stays separate from context
  management. (see [[anthropic-eng-scaling-managed-agents]])
- **Secrets stay outside the sandbox.** A proxy or vault holds the real
  credential and injects it on egress, only to allowlisted hosts; the sandbox
  sees a placeholder or a session token. Seen in Managed Agents (MCP OAuth
  vault, Git token used only at init), scheduled automations, and Claude Code
  cloud sessions (a branch-scoped push credential). (see
  [[anthropic-eng-scaling-managed-agents]],
  [[anthropic-building-effective-agent-automations]],
  [[anthropic-claude-code-in-the-cloud]], [[guardrails]])
- **Isolation strength follows oversight.** Anthropic matches the isolation
  pattern to how much the user can oversee: an ephemeral container where no one
  watches, an OS-level sandbox with a human in the loop, a sealed local VM for a
  desktop agent. Across deployments, standard primitives (hypervisors, syscall
  filters, container runtimes) held; custom glue around them failed. (see
  [[anthropic-eng-how-we-contain-claude]])
- **Resource headroom is part of the environment.** In one agentic coding
  benchmark, extra container resources up to about 3x the task spec fixed
  infrastructure errors without changing the score; beyond that, resources let
  the agent use different strategies, so the limit changes what is measured.
  Specify a guaranteed floor and a separate kill ceiling. (see
  [[anthropic-eng-infrastructure-noise-evals]], [[agent-evals]])

## Harness–model co-evolution

The central best practice: **re-test your harness assumptions with every model
upgrade, and delete scaffolding the model has outgrown.**
- Example: Sonnet 4.5 "context anxiety" (rushing near the context limit) led teams
  to add context resets; Opus 4.5 removed the behavior, making those resets pure
  overhead. (see [[anthropic-evolution-of-agentic-surfaces]])
- The general rule from [[harnessing-claudes-intelligence]]: "Assumptions about
  what Claude can't do need to be re-tested with each step change in its
  capability." Prefer general-purpose tools and let the model do more
  ([[tool-design]], [[agent-design-principles]]).

- **Every component encodes an assumption** about what the model cannot do.
  When a new model ships, remove components one at a time and re-measure; in
  the planner / generator / evaluator case study some components became
  unnecessary while others still paid off. (see
  [[anthropic-eng-harness-design-long-running-apps]],
  [[anthropic-eng-scaling-managed-agents]])
- **Tools are harness too.** Claude Code retired tools and reminders that had
  helped earlier models but constrained later ones. (see
  [[anthropic-seeing-like-an-agent]], [[tool-design]])

**Implication:** delegate harness tuning to the platform/SDK where you can, and
spend your effort on domain expertise, tools, and context — not on maintaining a
custom loop.

The harness moves scores as much as the model does: on one fixed optimization
task, the same model scored from 1790 down to 1363 cycles (lower is better)
depending on the harness and the time budget. (see [[anthropic-eng-ai-resistant-evaluations]])

## Harness as a reusable runtime

- **The agent loop is the reusable part; the product is separate.** OpenAI
  presents the open-source [[openai-codex]] harness (conversation state,
  streaming, tool use, sandbox and approval policies) as a runtime to embed. The
  host application owns the UI, the context and tools exposed, where the agent
  runs, which actions need approval, and how results return. Harness settings
  alone (retained reasoning plus compaction) more than doubled one model's
  ARC-AGI-3 score with sixfold fewer output tokens (secondary figure). (see
  [[openai-codex-as-a-platform]])
- **Who runs the loop** is a choice: a vendor-managed harness
  ([[openai-agents-api]], [[claude-managed-agents]]), an SDK in your app
  ([[openai-agents-sdk]], [[claude-agent-sdk]]), or your own loop over a raw
  model API. OpenAI's rule trades integration effort against control of
  deployment, storage, and approvals. (see [[openai-agents-api-guide]])
- **Repo-level configuration is the portable part.** In Claude Code cloud
  sessions, `CLAUDE.md`, rules, skills, agents, commands, `.mcp.json`, and
  project hooks travel with the repo; per-user config (`~/.claude`) does not.
  Test commands must therefore live in repo config. (see
  [[anthropic-claude-code-in-the-cloud]], [[agent-steering]])
- **Model-written harnesses.** Claude Code can write a task-specific
  multi-agent harness per request (dynamic workflows); static harnesses such as
  an SDK must stay generic. (see [[anthropic-harness-for-every-task]],
  [[workflow-patterns]])

## Loop mechanics in production

- **Cache hit rate is a production metric.** The Claude Code team lays out the
  request static-first, sends changing state as messages, never swaps models or
  tool sets mid-session, and treats hit-rate drops as incidents (SEVs). (see
  [[anthropic-prompt-caching-is-everything]], [[context-engineering]])
- **Append-only history.** Return assistant turns exactly as received and never
  edit earlier turns; add reminders by appending them (for example as
  turn-scoped system messages) and leaving them in place, never by inserting and
  later deleting. Edits that break the prompt cache also invalidate preserved
  thinking. Exact API behaviors are model-scoped; see
  [[anthropic-prompting-claude-fable-5-1]],
  [[anthropic-prompting-claude-opus-5-5]],
  [[anthropic-prompting-claude-sonnet-5-5]].
- **Message placement affects injection resistance.** Never put user text inside
  a tool result; append mid-turn user words after the last tool result; keep
  harness notices in a separate system message; cap repeated harness reminders,
  because frequent harness text after tool results can look like injection.
  (see [[anthropic-prompting-claude-sonnet-5-5]], [[guardrails]])
- **Unattended loops need explicit stop handling.** A text-only end of turn can
  be a progress report rather than completion. Pattern: a model-updated
  checklist; a continuation message naming open items when no blocker is
  stated; optionally a small model judging a stated completion condition; a cap
  of two or three automatic continuations; wait for background commands and
  subagents. (see [[anthropic-prompting-claude-opus-5-5]])
- **The client must be able to see progress.** On some current models,
  between-tool notes arrive as thinking blocks that a text-only client does not
  show unless it opts in. Check the model-scoped page before assuming a silent
  agent is idle. (see [[anthropic-prompting-claude-opus-5-5]],
  [[anthropic-prompting-claude-sonnet-5-5]])

## Concrete long-running patterns

From the case study in [[anthropic-eng-effective-harnesses-long-running-agents]]:
- **Two-agent pattern** — a one-time **initializer** (environment, spec file, git,
  progress file) and a per-session **coding agent** doing one feature at a time.
- **Structured JSON state** the agent only partially edits (flip a "passes" field)
  — models inappropriately edit Markdown more readily than JSON.
- **Session startup sequence** — `pwd` → read git log + progress → pick top
  incomplete feature → smoke-test → implement, to avoid re-establishing context.
- **Verify like a human user** (e.g. browser automation), but only reliably once
  *explicitly* prompted. See [[agent-evals]].
- **Failure modes to design against:** premature completion, half-finished
  features, undocumented progress, code-only (non-end-to-end) verification.

- **The verifier is the steering wheel.** An autonomous agent solves whatever
  the tests define, so the tests must be nearly perfect, and a CI gate should
  block any commit that breaks existing tests. Write test output for the model:
  a few lines on screen and details in a log file, `ERROR` and its reason on one
  line that grep can find, summary statistics already computed, and a fast
  sampled mode that is stable for one agent and varies across agents. (see
  [[anthropic-eng-building-c-compiler]])
- **A concrete target to iterate against** — tests, a visual mock, or expected
  output — is the most reliable way to get good results from a coding agent.
  (see [[anthropic-eng-claude-code-best-practices]])

## Coordination-bearing harnesses

At multi-agent coding scale, the harness also becomes the coordination system.
Cursor placed design ownership, decision reconciliation, merge mediation,
modularity enforcement, review, and shared memory around the models; its new
harness outperformed the old one under every tested model mix. This reinforces
harness-model co-evolution: model swaps and prompt reuse must be evaluated as a
system, including downstream worker behavior. (see
[[cursor-agent-swarm-model-economics]], [[multi-agent-economics]])

## Related concepts

- [[agent-orchestration]], [[context-engineering]], [[agent-design-principles]],
  [[tool-design]], [[agent-core-components]], [[agent-evals]]

## Key entities

- [[anthropic]], [[claude]], [[claude-agent-sdk]], [[claude-managed-agents]],
  [[claude-code]], [[openai-codex]], [[openai-agents-api]]

## Appears in

- [[anthropic-evolution-of-agentic-surfaces]]
- [[harnessing-claudes-intelligence]]
- [[anthropic-eng-effective-harnesses-long-running-agents]]
- [[anthropic-eng-context-engineering]]
- [[cursor-agent-swarm-model-economics]]
- [[anthropic-eng-scaling-managed-agents]]
- [[anthropic-eng-harness-design-long-running-apps]]
- [[anthropic-eng-how-we-contain-claude]]
- [[anthropic-eng-infrastructure-noise-evals]]
- [[anthropic-prompt-caching-is-everything]]
- [[anthropic-seeing-like-an-agent]]
- [[anthropic-harness-for-every-task]]
- [[anthropic-building-effective-agent-automations]]
- [[anthropic-claude-code-in-the-cloud]]
- [[anthropic-prompting-claude-opus-5-5]]
- [[anthropic-prompting-claude-sonnet-5-5]]
- [[anthropic-prompting-claude-fable-5-1]]
- [[openai-codex-as-a-platform]]
- [[openai-agents-api-guide]]
- [[anthropic-eng-building-c-compiler]]
- [[anthropic-eng-claude-code-best-practices]]
- [[anthropic-eng-ai-resistant-evaluations]]

## Contradictions / open questions

- Otherwise strongly consistent with the start-simple / prune-complexity theme.
- **Mechanism of the brain–hands latency win.**
  [[anthropic-evolution-of-agentic-surfaces]] (2026-06-10) says reasoning starts
  while the sandbox spins up in parallel;
  [[anthropic-eng-scaling-managed-agents]] (2026-04-08) says containers are
  provisioned only when a tool call needs one. Both report the same figures.
  Recorded in full on [[claude-managed-agents]].
