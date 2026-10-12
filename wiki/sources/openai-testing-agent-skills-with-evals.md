---
title: "OpenAI: Testing Agent Skills Systematically with Evals"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Dominik Kundel, Gabriel Chua (OpenAI)
date: 2026-01-22
source_url: https://developers.openai.com/blog/eval-skills
source_path: raw/openai-testing-agent-skills-with-evals.md
tags: [evals, skills, codex, deterministic-graders, rubric-grading, regression-testing]
---

# OpenAI: Testing Agent Skills Systematically with Evals

> A step-by-step method for evaluating a Codex skill: define success, write a
> small trigger/no-trigger prompt set, grade JSONL traces deterministically,
> then add a schema-constrained rubric pass.

## Summary

The post treats a skill as a prompt and evaluates it like one. An eval is a
prompt → a captured run (trace + artifacts) → a few checks → a score tracked
over time. Using a sample `setup-demo-app` skill (Vite + React + TypeScript +
Tailwind), it walks through: defining success as outcome, process, style, and
efficiency goals; bootstrapping with `$skill-creator`; manual runs to surface
triggering, environment, and execution assumptions; a 10–20 row CSV with
`should_trigger` including a negative control; deterministic graders over
`codex exec --json` event streams; and a read-only rubric pass with
`--output-schema`. Extensions add command counts, token budgets, build and
smoke checks, repo cleanliness, and permission regressions. Date from page
byline: 2026-01-22.

## Key points

- **Four goal types:** outcome, process (did the skill fire and follow the
  steps), style, efficiency (no thrashing). Keep must-pass checks few. See
  [[agent-evals]].
- **Trigger tests:** explicit, implicit, contextual, and negative-control
  prompts; the negative control catches false-positive invocation. See
  [[agent-skills]].
- **Grade the trace, not just the output:** `codex exec --json` emits JSONL
  events; check `item.*` events where `item.type` is `command_execution`.
- **Model grader with a schema:** a second read-only `codex exec` returns
  `overall_pass`, `score` (0–100), and per-check `{id, pass, notes}` via
  `--output-schema`; usable in CI through the Codex GitHub Action
  `codex-args`.
- **Least privilege:** `codex exec` sandboxes by default; use `--full-auto`
  only when writes are needed. See [[guardrails]].
- **Coverage grows from failures:** every manual fix becomes an eval row.

## Entities

[[openai]], [[openai-codex]]

## Concepts

[[agent-evals]], [[agent-skills]], [[guardrails]], [[boundary-contracts]]

## Notable claims & data

- 10–20 prompts per skill is enough to catch regressions early.
- Efficiency signals: `command_execution` counts; `usage.input_tokens` /
  `usage.output_tokens` from `turn.completed` events.
- Repo cleanliness check: `git status --porcelain` empty or allow-listed.
- Consistent with the code-based plus model-based grader taxonomy in
  [[anthropic-eng-demystifying-evals]]; no contradiction.

## Connections

Applies the general eval method of [[anthropic-eng-demystifying-evals]] to
skills specifically. Pairs with [[openai-shell-skills-compaction]] (Glean's
targeted trigger evals) and [[openai-skills-for-oss-maintenance]]. Related
Anthropic work: [[anthropic-automating-eval-design-hillclimbing]].
