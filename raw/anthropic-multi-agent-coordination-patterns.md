# Multi-agent coordination patterns — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/multi-agent-coordination-patterns
> Publisher: Anthropic (claude.com articles) · Date: 2026-04-10
> Captured: 2026-10-12 via WebFetch (condensed).

Author: Cara Phillips, with contributions from Eugene Yan, Jiri De Jonghe,
Samuel Weller, and Erik S. Category: Best practices. Product: Claude Platform.
Reading time 19 min. The page also shows 2026-10-05 to 2026-10-08 in the
"Related articles" list; those dates belong to other articles.

## Intro (no heading)

Follows an earlier post on when one agent beats several. Advice: start with the
simplest pattern that could work, watch where it struggles, then evolve. Five
patterns are covered.

## Pattern 1: Generator-verifier

- **How it works.** A generator drafts output. A verifier accepts or rejects it
  against explicit criteria and returns feedback. The generator revises. The
  loop ends on acceptance or at a maximum iteration count.
- **Where it works well.** Example: support-ticket replies, checked by a
  verifier for accuracy against the knowledge base, brand tone, and coverage of
  every issue. Fits quality-critical output with explicit criteria: code plus
  tests, fact-checking, rubric grading, compliance checks.
- **Where it struggles.** A vague verifier rubber-stamps output: quality
  control in appearance only. The pattern assumes generating and verifying are
  separable skills. Loops can oscillate; mitigate with an iteration cap plus a
  fallback (human escalation, or return the best attempt with caveats).

## Pattern 2: Orchestrator-subagent

- **How it works.** A lead agent plans, does some subtasks itself, dispatches
  bounded subtasks to subagents, and synthesizes their results. Claude Code is
  the cited example: subagents run searches or side investigations in their own
  context windows and return distilled findings.
- **Where it works well.** Example: automated code review that sends security,
  test coverage, style, and architecture checks to separate subagents and
  merges the results into one review. Fits clear decomposition with little
  interdependence between subtasks.
- **Where it struggles.** The orchestrator is an information bottleneck;
  details are lost over repeated handoffs when one subagent's finding affects
  another. Sequential execution limits throughput and can add token cost with
  no speed gain unless work runs in parallel.

## Pattern 3: Agent teams

- **How it works.** A coordinator spawns workers that claim tasks from a shared
  queue, work autonomously over many steps, and signal completion. Unlike
  subagents (which end after one task), teammates persist and build context and
  specialization across assignments.
- **Where it works well.** Example: a large codebase migration, one service per
  teammate (dependencies, code changes, tests, validation); the coordinator runs
  integration tests at the end. Fits independent subtasks that benefit from
  sustained work.
- **Where it struggles.** Needs true independence: teammates cannot easily share
  intermediate findings, so outputs can conflict. Completion is harder to detect
  when durations vary (two minutes versus twenty). Shared resources (codebase,
  database, file system) cause conflicting edits; needs careful partitioning and
  conflict resolution.

## Pattern 4: Message bus

- **How it works.** Agents publish and subscribe to topics on a shared
  communication layer; a router delivers matching messages. New agents join
  without rewiring existing ones.
- **Where it works well.** Example: security operations. A triage agent
  classifies alerts and routes them to network or identity investigators;
  enrichment requests and findings flow to a response coordinator. Fits
  event-driven pipelines where the workflow emerges from events and the set of
  agents is expected to grow.
- **Where it struggles.** Tracing cascades of events across many agents needs
  careful logging and correlation; harder than following an orchestrator's
  sequence. Misrouted or dropped events can fail silently. An LLM-based router
  adds its own failure modes.

## Pattern 5: Shared state

- **How it works.** No central coordinator. An initialization step seeds a
  persistent store; agents read it, act, and write findings back. Work ends on a
  time limit, a convergence threshold, or a designated agent that judges the
  answer sufficient.
- **Where it works well.** Example: research synthesis with agents on academic
  literature, industry reports, patents, and news; one agent's finding in the
  store can redirect another's investigation. No coordinator means no single
  point of failure; the system continues if one agent stops.
- **Where it struggles.** Duplicate work and contradictory paths; less
  predictable outcomes. Reactive loops (agents keep responding to each other
  without converging) burn tokens. Duplicate work and concurrent writes have
  known fixes (locking, versioning, partitioning); loops need explicit
  termination: a time budget, a no-new-findings threshold over N cycles, or a
  judge agent.

## Choosing and evolving between patterns

Decision axes: how long workers keep context; how predictable the workflow is;
whether agents need each other's findings; whether work flows as events or
accumulates as knowledge.

- **Orchestrator-subagent vs. agent teams.** Short focused subtasks with clear
  outputs (code review) versus sustained multi-step work where accumulated
  context matters (migration).
- **Orchestrator-subagent vs. message bus.** Known fixed sequence versus a
  workflow that emerges from events. When orchestrator conditionals multiply, a
  bus makes routing explicit.
- **Agent teams vs. shared state.** Separate partitions combined at the end
  versus collaborative work where findings flow between agents in real time.
- **Message bus vs. shared state.** Stage-by-stage pipeline where each event
  triggers the next versus knowledge that accumulates. Shared state is
  decentralized and removes single points of failure; the bus keeps a central
  router.

## Getting started

- Production systems often combine patterns: for example orchestrator-subagent
  overall with shared state for one collaborative subtask, or a message bus that
  routes events to agent-team-style workers.
- Situation-to-pattern table:
  - Quality-critical output with explicit criteria: generator-verifier.
  - Clear decomposition, bounded subtasks: orchestrator-subagent.
  - Parallel, independent, long-running work: agent teams.
  - Event-driven pipeline, growing ecosystem: message bus.
  - Collaborative research, shared discoveries: shared state.
  - No single point of failure required: shared state.
- Recommendation: start with orchestrator-subagent (widest coverage, least
  overhead) and evolve as specific needs appear. Follow-up posts with production
  implementations are promised.

## Acknowledgements

Written by Cara Phillips with the contributors listed above.
