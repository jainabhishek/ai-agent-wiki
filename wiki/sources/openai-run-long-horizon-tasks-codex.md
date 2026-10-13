---
title: "OpenAI: Run Long Horizon Tasks with Codex"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Derrick Choi (OpenAI Developers blog)
date: 2026-02-23
source_url: https://developers.openai.com/blog/run-long-horizon-tasks-with-codex
source_path: raw/openai-run-long-horizon-tasks-codex.md
tags: [openai, codex, long-horizon, durable-state, verification, agent-loop, case-study]
---

# OpenAI: Run Long Horizon Tasks with Codex

> A single-run experiment in which Codex built a design tool from a blank repo
> over about 25 hours, and the four-file "durable project memory" setup the
> author credits for keeping the run coherent.

## Summary

Derrick Choi of [[openai]] gave [[openai-codex]] a blank repository, full
access, and a spec for a design tool, running **GPT-5.3-Codex at "Extra High"
reasoning**. The run lasted about 25 hours, used about 13M tokens, and produced
about 30k lines of code. The author calls it an experiment, not a production
rollout. He credits four Markdown files that the agent rereads (spec, plan,
runbook, status log) and verification after every milestone. The post frames
the trend as **time horizon** rather than one-shot intelligence, citing METR's
~7-month doubling time. **Model dependence:** the result is for GPT-5.3-Codex
as of 2026-02-23. The wiki's current OpenAI pages cover the GPT-5.6 and GPT-6
generation ([[openai-prompting-gpt-6-astra]]), so the specific durations and
token counts are dated. The file-based method does not depend on the model.

## Key points

- **Durable project memory (four files).** `Prompt.md` freezes the target
  (goals, non-goals, hard constraints, deliverables, "done when"). `plans.md`
  holds milestones sized for one loop, acceptance criteria and validation
  commands per milestone, a stop-and-fix rule, decision notes, and intended
  architecture. `implement.md` is the runbook (plan is source of truth, validate
  after each milestone, keep diffs scoped, update docs). `documentation.md` is
  the status and audit log (status, decisions, run/demo commands, known issues).
  See [[context-engineering]].
- **Agent loop over prompt.** Plan → edit → run tools → observe → repair →
  update docs → repeat. The loop gives real feedback, externalized state, and
  steerability. See [[agent-harness]].
- **Harness supplies structure.** Codex models do better on Codex surfaces
  because the harness gives repo metadata, file tree, diffs, command outputs,
  and a "done when" routine. See [[agent-harness]].
- **Verification at each milestone.** Lint, typecheck, tests, build, and export
  commands ran after milestones, with failures repaired before moving on. See
  [[agent-evals]] and [[agent-steering]].
- **Mid-run steering.** GPT-5.3-Codex is claimed to accept course corrections
  without losing progress. Native plan mode is toggled with `/plan`.
- **Codex app features:** parallel project threads, Skills, Automations, Git
  worktrees for isolated, reviewable runs. See [[agent-skills]].

## Entities

[[openai]], [[openai-codex]], [[cursor]]

## Concepts

[[context-engineering]], [[agent-harness]], [[agent-steering]],
[[agent-evals]], [[agent-skills]], [[agent-instructions]]

## Notable claims & data

- ~25 h uninterrupted, ~13M tokens, ~30k LOC; ten feature areas built (canvas
  editing, live collaboration, inspector, layers, snapping, history, replay and
  branching, prototype mode, comments, export to JSON and React + Tailwind).
- Output was "not perfect or production-ready" per the author; quality was not
  independently measured. One run, one task, no comparison baseline.
- METR: task length that frontier agents finish at ~50% and 80% reliability
  doubles roughly every 7 months (cited, not reproduced here).
- Quotes [[cursor]]'s "Scaling agents" post saying OpenAI models drift less on
  extended autonomous work. This is a vendor-quoted third-party claim.

## Connections

- Same file-based state pattern as the progress file and feature list in
  [[anthropic-eng-effective-harnesses-long-running-agents]] and the per-run
  notebook in [[openai-automating-repetitive-work-codex]].
- Milestone validation with a stop-and-fix rule matches the verifier-as-steering
  idea in [[anthropic-eng-harness-design-long-running-apps]] and
  [[anthropic-eng-building-c-compiler]].
- Long-run continuity on the API side: [[openai-shell-skills-compaction]].
- Multi-agent counterpart for long runs: [[cursor-agent-swarm-model-economics]].
