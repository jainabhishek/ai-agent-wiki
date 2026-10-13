---
title: "OpenAI (Eng): Building Self-Improving Tax Agents with Codex"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Aravind Srinivasan, Samay Shamdasani (Thrive Holdings); Arthur Fernandes Araujo, John de Wasseige (OpenAI)
date: 2026-05-27
source_url: https://openai.com/index/building-self-improving-tax-agents-with-codex/
source_path: raw/openai-self-improving-tax-agents-codex.md
tags: [case-study, evals, production-feedback, codex, self-improvement, domain-agents]
---

# OpenAI (Eng): Building Self-Improving Tax Agents with Codex

> Case study published by OpenAI (2026-05-27), co-written with Thrive Holdings.
> Practitioner corrections in a production tax agent become reviewed eval
> targets, which Codex then works against as bounded engineering tasks. All
> results are self-reported.

## Summary

OpenAI forward-deployed engineers and Thrive Holdings built "Tax AI" for
Crete's network of 30+ accounting firms. Tax AI prepared 7,000 returns in the
pilot season. The authors report that it cuts preparation time by about a
third, produces drafts up to 97% accurate, and raised the share of returns at
75% correct-field completion from about a quarter to 86% within six weeks.

The design has three pillars. Practitioners decide which errors matter. The
product records evidence from source document to extracted field (with
citations), to submission, to correction. A [[openai-codex]] loop then
investigates, fixes, and validates against targeted and regression evals, and
proposes a PR for engineer review.

## Key points

- **Corrections become evals only after review and grouping.** Field-level
  review rows hold the expected value, the predicted value, and whether the
  difference is actionable. Rows are grouped to separate recurring failures
  from workflow noise, such as practitioner preference or prior-year
  carry-forwards. Only repeated, reviewed patterns become eval targets with a
  success condition.
- **A bounded task environment.** Codex gets a writable worktree that holds
  `AGENTS.md`, a task folder (`task.yaml`, `EXEC_PLAN.md`, `RESULTS.md`), the
  scoped product code, targeted and regression eval suites, graders, and
  skills. Production traces and source documents come through read-only scoped
  tools, so Codex cannot change the evidence.
- **The grader is also a suspect.** Codex considers whether the grader counts
  noise as failure, not only whether the product code is wrong.
- **Ambiguous cases go to humans.** Evidence that is unclear or not safe to
  automate goes back to the product team. Engineers own architecture and
  shipping. Automation covers only the extraction and mapping layer.
- **The first domain is the expensive one.** Rental properties (Schedule E)
  took about six weeks of heavy engineering oversight to reach 90% precision
  and recall. The resulting conventions made Schedules C and A easier.

## Concepts

[[human-agent-teams]]

## Connections

- Production-to-eval loop: compare the eval-design guidance in [[agent-evals]],
  [[anthropic-automating-eval-design-hillclimbing]], and
  [[openai-testing-agent-skills-with-evals]].
- The authors say the loop builds on [[openai-harness-engineering]] and
  [[openai-symphony-codex-orchestration]]: legible tasks, scoped context, and
  validation in the environment. The `EXEC_PLAN.md` file matches the plan-file
  practice in [[openai-run-long-horizon-tasks-codex]].
- The read-only evidence boundary is an instance of sizing write access in
  [[guardrails]].
