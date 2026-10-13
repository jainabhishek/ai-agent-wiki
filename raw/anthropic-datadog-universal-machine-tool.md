# How Datadog built a "universal machine tool" for Claude Code — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/how-datadog-built-a-universal-machine-tool-for-claude-code
> Publisher: Anthropic (claude.com articles) · Date: 2026-07-21
> Captured: 2026-10-12 via curl (HTML downloaded, text extracted locally; condensed).

Author: Michael Segner. Category: Best practices. Product: Claude Code. Reading
time 4 min. Customer case study; claims are Datadog's own, reported by Anthropic.
Main speaker quoted: Sesh Nalla, VP of engineering, Datadog. The page links a
recorded session with a live demo (not captured).

## Agents, mechanization, and industrialization
- All Datadog engineers use AI coding tools for production code; Claude Code
  drives at least two-thirds of that.
- Four categories of work:
  - Targeted changes: dozens of hard bug fixes, performance optimizations,
    bridges to existing services.
  - Large refactors: a custom protobuf parser refactored in three days; a metrics
    control rewritten from FoundationDB to Postgres in under three months.
  - Replacing large parts: new sharding algorithms, autoscaling redesigns.
  - Building entire systems: replacing MongoDB with Postgres, BYOC control
    planes, ingestion pipelines from scratch.
- Moving along this map, work got more complex to generate and more ambiguous to
  verify.

## The flow problem
- Flow used to be a direct link between intent and code. With agents, engineers
  shape the work: what the agent sees, its tools, what success means, how failure
  is detected. Nalla likens it to everyone being promoted "three levels up".
- With approaches like Claude Managed Agents, sessions run longer, sometimes
  days. Each agent invents its own tools, glue code, conventions; humans must
  bridge agent execution and tools designed for humans.
- Machine tools (jigs, fixtures, gauges, mills) made parts precise, repeatable,
  composable, inspectable, replaceable — the breakthrough of industrialization.
  Temper is Datadog's attempt at a universal machine tool for agentic systems:
  the smallest kernel agents need to build what they need safely and precisely.

## The road to Temper
- Path ran through three projects; each exposed the next bottleneck:
  - **Courier** (2024): distributed queuing system, one year to build by hand.
    Hard part was making component interactions observable, testable,
    verifiable; used formal modeling and simulation, with extra rigor where
    mistakes would be expensive or hard to reverse.
  - **BitsEvolve** (September 2025): closed-loop evolutionary optimization
    harness. A council of models generates code variants; a cascade of
    benchmarks, tests, and production observability selects survivors.
    Bottleneck: the feedback loop/environment.
  - **Helix**: a Kafka-comparable streaming service, mostly built by Claude Code
    with one human steering; functional in a few days; in shadowing, 2x to 5x
    cheaper opportunities seen. Production hardening took much longer and more
    people and is still rolling out. New bottleneck: humans coordinating shipping
    through human-designed tools.
- Need: a verified, policy-driven runtime where agents build their own tools —
  Temper.

## Temper
- The gap between what agents generate and what passes verification is where
  failures accumulate; wrapping an agent around a traditional codebase treats it
  as a throughput problem without closing the gap.
- Temper inverts this: agents produce **specifications**, not application code.
  The kernel verifies each spec through four layers of analysis and deploys the
  system it describes. The spec is both the proven artifact and the executed
  artifact, so there is no drift between verified and running.
- Agent iterates with Temper to make something work, then makes it repeatable,
  checkable, reusable — a "software factory" around the codebase.
- Each capability is described by three contracts:
  - Behavior: states, transitions, preconditions, safety properties.
  - Data contract: entity types, properties, supported actions, published in
    machine-parseable form so an agent can discover the full API without docs.
  - Authorization: default-deny, scope-based approval; denials recorded as
    pending decisions a human can approve and hot-load into the policy engine.
- Four independent verification layers before the kernel loads a spec:
  1. Symbolic reasoning: proves each guard satisfiable and each invariant
     inductive.
  2. Exhaustive state exploration: visits every reachable state.
  3. Deterministic simulation: runs the actual production code path with seeded
     fault injection (drops, delays, reordering, crashes), so failures reproduce
     exactly under the same seed.
  4. Randomized property testing: about a thousand pseudorandom action sequences,
     shrinking any violation to a minimal counterexample.
- On a small spec, the whole cascade runs in well under a second.

## The dark factory for Helix
- "Dark factory" (term popularized by Simon Willison): agents keep working with
  no humans on the virtual factory floor. Temper's three roles in Helix's:
  1. Agent control plane for managed agents: sessions, roles, work queues,
     lifecycle.
  2. Tool-builder layer: agents bridge SDLC tooling (Git, CI, deployment) with
     small Temper apps.
  3. Helix control API: lifecycle surface around the data plane.
- Nalla: much software is control logic around database APIs (state, mutation
  policies, lifecycle transitions, integrations), so Temper could be general.

## Why not just build a CRUD app?
- Claude Code builds CRUD apps well, but control logic is scattered across
  routes, DB constraints, service code, background jobs, docs; the state machine
  is implicit.
- Temper makes the state machine explicit: the agent emits a precise description;
  compilation happens outside the LLM (like handing Rust to the Rust compiler);
  the transition table is data; agents can change it dynamically and hot-reload
  it under policy without going through CI.

## Where this is going
- Each artifact should be small enough to fit in your head — how high-assurance
  software (aviation, finance) has long been built; agents make that rigor
  affordable for general software.
- Nalla speculates software built this way could be grown and evolved through
  feedback, selection, adaptation.

## Best practices from the Datadog team
- Real bottleneck: assume verification, not generation. Invest in closing the
  generated-vs-proven gap rather than more throughput.
- What the agent should emit: specs for control logic (not code), proof-carrying
  output for arbitrary code. Keep compilation and proof outside the LLM, in a
  deterministic kernel, so the verified artifact is the running artifact.
- Make control logic explicit: pull the state machine out of routes, services,
  jobs into a transition table (data) an agent can read, modify, hot-reload under
  policy.
- Keep every generated artifact small enough for a human to reason about.
