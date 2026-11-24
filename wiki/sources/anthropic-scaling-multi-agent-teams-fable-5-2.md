---
title: "Anthropic: Safely scaling multi-agent teams with Claude Fable 5.2"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Barry Zhang, Tianyi Peng, Elle Najt, Keller Scholl, Lance Martin (Anthropic)
date: 2026-11-09
source_url: https://claude.dev/blog/safely-scaling-multi-agent-teams-with-fable-5-2/
source_path: raw/anthropic-scaling-multi-agent-teams-fable-5-2.md
models: [claude-fable-5-2]
as_of: 2026-11-24
tags: [multi-agent, orchestration, sandboxing, monitoring, guardrails, long-horizon, formal-verification, lean, model-specific]
---

# Anthropic: Safely scaling multi-agent teams with Claude Fable 5.2

> A case study of 1,000 agents on an early Claude Fable 5.2. The team reproduced a
> Lean formalization of Fermat's Last Theorem with only Git, a shared Postgres
> database, and a lead/helper hierarchy. Sandboxing and two monitoring layers
> surrounded the team.

## Summary

Published 2026-11-09 on the claude.dev blog ("Agents"). The run used "an early
version" of Claude Fable 5.2. The September 2026 baseline used an internal research
model "roughly comparable to" Claude Fable 5.1. No API model ID appears in the post.
`models:` records `claude-fable-5-2` by naming convention. The result is for a
pre-release build and is not a measurement of the released model.

In the September baseline, a researcher and dozens of agents worked on Prove2Me, a
domain platform with a shared statement graph. That run took 11 days, about 6
billion output tokens, and 13 million lines of Lean. This run gave 1,000 agents
general tools only. Each agent had a no-network sandbox on its own VM, Lean and
Mathlib, its own Git branch with merge requests into main, and a shared Postgres
database. The only structure was one lead and 999 helpers. The team proved the
theorem in 28.7 hours. It used one-third of the output tokens, and its proof was
one-seventh the length. The post calls it a "toy experiment."

The coordination findings: the lead invented its own coordination schema (five SQL
tables) within 10 minutes. Control moved from top-down assignment to helpers who
pulled their own work. The hardest statement was solved through a self-grown task
tree of 2,418 tasks. The safety findings: no single layer is enough. Monitors that
can read chain of thought caught every sabotage attempt in red-team evaluations.
See [[agent-orchestration]], [[guardrails]], and [[multi-agent-economics]].

## Key points

### Harness
- General tools only: shell, file editor, Lean toolchain, Git branch and merge
  requests, and a shared SQL database. Anthropic chose SQL for its general
  organizing primitives, for transactions that handle concurrent writes from 1,000
  agents, and because Claude already knows it.
- A single shared machine failed at about 100 agents. More than half of the
  100-agent runs ran out of memory, disk, or CPU. So each agent got its own
  lightweight VM.
- The prompt held 60 statements with one-line descriptions, the tool list, and the
  roles. The harness sent the lead 19 automatic time-remaining reminders, each
  telling it to keep going.

### Safety layers
- **Sandboxing.** There was no messaging tool; agents coordinated only through the
  database and Git. Agents pushed only to their own branch, and a separate job did
  the merges. The database used an unprivileged role, a 5-second statement limit,
  and a 256 MiB write cap. A gateway pipe was the only network path. The gateway
  stamped each request with the agent's identity outside the sandbox. The kernel
  had no modules, kexec, raw memory access, or probes, and ran in lockdown mode. The
  user was unprivileged with sudo removed. Agent tools could not read or change the
  agent loop.
- **Real-time monitoring.** A prompted LLM classifier checks every tool call before
  it runs. A block stops the whole team until a person reviews it. In multi-agent
  sabotage evaluations that included decomposition attacks, monitors that saw CoT
  and inter-agent messages caught all attempts. Anthropic runs an action-only
  monitor in parallel, so that agent reasoning cannot persuade the monitor. This run
  used only the action-based monitor; the CoT monitor was added shortly after.
- **Offline monitoring.** It applies the same threat models with extra affordances,
  for example looking up other agents' actions.
- Out of more than one million tool calls, none was blocked. In a replay against
  the CoT monitor, one call (a root-access check) came close.
- Monitoring assumes the model may be misaligned, because these runs use models that
  may not have finished the pre-release alignment assessment.

### Emergent coordination
- **Five tables in 10 minutes:** announce, assign, notes, subtasks, and landed.
- **Triage by verdict.** The lead put crews of 16–17 helpers on each statement, with
  a captain per crew. It asked every helper for a difficulty verdict. At about 27
  minutes it set aside the 47 statements judged infeasible and put crews of 46–139
  helpers on the other 10. All 10 were proved in about 70 minutes.
- **From push to pull.** By hour 5.6, 73 helpers had written 756 tasks, and only 16
  of those helpers were captains. By hour 3 the lead told free helpers "do not wait
  for me."
- **Task tree.** The lead put about 750 helpers on Langlands–Tunnell. The captain
  had estimated the odds of finishing at under 1%. The work grew into a tree of
  2,418 tasks, up to 10 levels deep. Each piece could assume the pieces beneath it,
  so hundreds of helpers worked in parallel. The statement was proved at hour 28.4,
  and the final theorem at hour 28.7.

### Conclusions stated by the authors
- Domain platforms such as Prove2Me still add efficiency (faster compiles, reuse of
  human results).
- Agents tend to give up and misjudge difficulty. Helpers called 47 of 60 statements
  infeasible, and the team proved most of them. Human encouragement at such points
  helps.
- Safety boundaries are what made the experiment acceptable to run, and the
  boundaries must keep pace with the scale of the work.

## Notable claims & data

- 1,000 agents; 28.7 hours; one-third of the baseline's output tokens; a proof
  one-seventh the length of the baseline proof.
- Baseline: 11 days, about 6B output tokens, 13M lines of Lean, a researcher plus
  dozens of agents.
- More than 1M tool calls with zero blocks.
- A single shared host failed at about 100 agents (more than half of runs stopped
  or restarted).
- 54 of 60 statements were counted at the end: five alternatives were no longer
  needed, and one statement was dropped.
- There was a restart from the last save near hour 18, with 12 more hours given.

## Entities

[[anthropic]], [[claude]]

## Concepts

[[agent-orchestration]], [[multi-agent-economics]], [[guardrails]],
[[agent-identity-and-access]], [[agent-harness]], [[agent-verification]],
[[agent-steering]], [[human-agent-teams]], [[agent-memory]], [[tool-design]]

## Connections

- Containment layers extend [[anthropic-eng-how-we-contain-claude]] and
  [[anthropic-eng-claude-code-sandboxing]] to a multi-agent team. Gateway-stamped
  identity connects to [[anthropic-agent-identity-access-model]] and
  [[anthropic-zero-trust-for-ai-agents]].
- Coordination through a shared store and Git, not messages, parallels
  [[anthropic-eng-building-c-compiler]] (parallel agents with Git locks) and the
  shared-state patterns in [[anthropic-multi-agent-coordination-patterns]] and
  [[anthropic-building-multi-agent-systems]].
- Large-swarm economics: [[cursor-agent-swarm-model-economics]],
  [[anthropic-which-claude-model-to-build-with]] (lead plus cheaper workers).
- Early-stopping and misjudged difficulty match the "Finish the whole task" section
  of [[anthropic-prompting-claude-fable-5-2]]. The 19 time reminders are a harness
  form of that nudge.
- Lead/orchestrator role: [[anthropic-prompting-claude-fable-5-2]] reports good
  results with Fable 5.2 as planner and orchestrator for other models.

## Contradictions / open questions

- The post says the team worked "without … steering from a researcher." The harness
  did send 19 automatic "keep going" reminders to the lead. So the run had no human
  steering, but it did have scripted encouragement.
- The comparison with the baseline mixes model and harness changes: an early Fable
  5.2 against a model comparable to Fable 5.1, and general tools against Prove2Me.
  This run also started with 47 proved lemmas taken from the baseline. The post does
  not separate the token and length gains by cause.
- The CoT monitor's detection rate comes from Anthropic's own sabotage evaluations,
  and that monitor was not used during this run.
