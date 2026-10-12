---
title: "Anthropic: Building a C compiler with a team of parallel Claudes"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Nicholas Carlini (Anthropic Engineering blog)
date: 2026-02-05
source_url: https://www.anthropic.com/engineering/building-c-compiler
source_path: raw/anthropic-eng-building-c-compiler.md
tags: [multi-agent, long-running-agents, harness, coding, verification, economics, case-study]
---

# Anthropic: Building a C compiler with a team of parallel Claudes

> A case study in which 16 parallel Claude Opus 4.6 agents, with no orchestrator
> and no human in the loop, wrote a 100,000-line Rust C compiler that builds
> Linux 6.9 — and in which the verifier, not the coordination scheme, did most of
> the work.

## Summary

Nicholas Carlini (Anthropic Safeguards) ran "agent teams": many [[claude]]
instances working on one shared git repository with no active human
intervention. The run used Claude Opus 4.6 and was published on 2026-02-05;
the author treats the task as a capability benchmark that he had run across the
Claude 4 series (earlier Opus 4 models barely produced a working compiler; Opus
4.5 passed large test suites but could not compile large real projects). Over
about 2,000 [[claude-code]] sessions in two weeks, 16 agents consumed 2 billion
input and 140 million output tokens, just under $20,000, and produced a
clean-room compiler (no internet, Rust standard library only) that builds a
bootable Linux 6.9 on x86, ARM, and RISC-V and passes 99% of most compiler test
suites. The harness is minimal: each agent runs `claude
--dangerously-skip-permissions -p` in an infinite loop inside its own Docker
container, and coordination is only lock files in `current_tasks/` plus git
push and merge. There is no orchestrator agent, no inter-agent messaging, and no
high-level goal process. The author's main lesson is that effort belongs in the
environment: a nearly perfect verifier, test output designed for a model's
context, and work that is split so agents do not collide. See
[[agent-harness]], [[agent-orchestration]], [[multi-agent-economics]].

## Key points

- **Loop harness for autonomy.** Interactive scaffolds stop to ask for input;
  an outer `while true` loop restarts a fresh session from `AGENT_PROMPT.md`
  after each one ends. Run it in a container. (Enabling long-running Claudes)
- **Coordination by lock file and git.** An agent claims a task by writing
  `current_tasks/<task>.txt`; git rejects a duplicate claim. The agent pulls,
  merges, pushes, and deletes the lock. Merge conflicts are frequent and Claude
  resolves them. Agents pick the "next most obvious" problem. (Running Claude in
  parallel)
- **The verifier must be nearly perfect.** An autonomous agent solves whatever
  the tests define, so wrong tests mean the wrong problem gets solved. When new
  features started to break old ones, a CI gate that blocks regressing commits
  fixed it. (Write extremely high-quality tests)
- **Design test output for the model.** Print a few lines and log the rest;
  put `ERROR` and the reason on one grep-able line; pre-compute summary
  statistics. Counter "time blindness" with a default `--fast` mode that runs a
  1% or 10% sample, deterministic per agent and random across VMs. Tell agents
  to keep READMEs and progress files current, because each starts with no
  context. (Put yourself in Claude's shoes) See [[context-engineering]].
- **Parallelism needs partitionable work.** Many failing tests parallelize
  trivially. Compiling the Linux kernel is one monolithic task, so all 16 agents
  hit the same bug and overwrote each other. A GCC known-good oracle restored
  parallelism: compile a random subset with Claude's compiler and the rest with
  GCC, then narrow the failing subset. Delta debugging handled file pairs that
  failed only together. (Make parallelism easy)
- **Specialist roles** run beside the main workers: de-duplicate code, speed up
  the compiler, improve emitted code, critique design as a Rust expert, write
  docs. (Multiple agent roles)
- **Ceiling.** Late in the run, new features and fixes often broke existing
  ones, and the author could not fix several limitations. (Evaluation)

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[agent-harness]], [[agent-orchestration]], [[multi-agent-economics]],
[[agent-evals]], [[context-engineering]], [[workflow-patterns]],
[[guardrails]]

## Notable claims & data

- 16 agents; ~2,000 sessions; 2 weeks; 2B input + 140M output tokens; just under
  $20,000; 100,000 lines of Rust.
- Builds QEMU, FFmpeg, SQLite, postgres, redis; 99% on most compiler test
  suites including the GCC torture suite; runs Doom.
- Limitations: calls GCC for 16-bit real-mode x86 (its 16-bit output exceeds
  60 KB against Linux's 32 KB limit); uses GCC's assembler and linker; not a
  drop-in replacement; output with all optimizations on is slower than GCC with
  all optimizations off; Rust quality below expert level.
- Risk stated by the author: with autonomous agents it is easy to see tests
  pass and assume the job is done, "when this is rarely the case".
- The harness used `--dangerously-skip-permissions`; the author's only
  containment advice is to run it in a container. See [[guardrails]].

## Connections

- **Versus [[cursor-agent-swarm-model-economics]].** Both are large multi-agent
  coding runs, but their architectures are opposite. Cursor needed planner
  agents, decision records, neutral merge resolution, and a custom VCS to stop
  conflicts and churn. Carlini used plain git, lock files, and no planner, and
  relied on a near-perfect external verifier (test suites, then a GCC oracle).
  Cursor's main cost lever was worker-model routing; here a single model did
  everything, and the effective lever was verifier and test-harness quality.
  The dollar figures ($20,000 here; $1,339–$10,565 per Cursor configuration)
  come from different tasks, models, and accounting and are not comparable.
  See [[multi-agent-economics]].
- **Partitionability.** The Linux kernel stall gives direct evidence for the
  open question in [[agent-orchestration]]: the boundary for multi-agent coding
  is task partitionability plus harness support. This run is also a replication
  on an ordinary git repository, which that page lists as open.
- **Shared-context warning.** [[anthropic-eng-multi-agent-research-system]] says
  multi-agent systems fit poorly when agents must share context, such as most
  coding. Here agents shared only the repository, READMEs, and progress files,
  which worked once the verifier split the work.
- **Long-running harness lineage.** Extends
  [[anthropic-eng-effective-harnesses-long-running-agents]] (progress files,
  fresh sessions that re-orient from git) from one agent to many, and parallels
  the verifier emphasis in [[anthropic-eng-harness-design-long-running-apps]].
