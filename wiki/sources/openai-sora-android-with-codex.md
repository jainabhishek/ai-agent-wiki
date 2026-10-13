---
title: "OpenAI (Eng): How We Used Codex to Build Sora for Android in 28 Days"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Patrick Hum, RJ Marsan (OpenAI)
date: 2025-12-12
source_url: https://openai.com/index/shipping-sora-for-android-with-codex/
source_path: raw/openai-sora-android-with-codex.md
tags: [case-study, codex, coding-agent, planning, agents-md, parallel-sessions]
---

# OpenAI (Eng): How We Used Codex to Build Sora for Android in 28 Days

> Case study published by OpenAI (2025-12-12) on four engineers shipping the
> Sora Android app with Codex. All figures are self-reported. A later banner on
> the page says the Sora product was discontinued as of 2026-04-26.

## Summary

From 2025-10-08 to 2025-11-05, four engineers working with an early
GPT-5.1-Codex took Sora for Android from prototype to global launch. They used
about 5 billion tokens and estimate that Codex wrote about 85% of the code.
They report an internal build in 18 days, public launch 10 days later, and a
99.9% crash-free rate. The team treated [[openai-codex]] like a new senior hire.
Codex was strong at reading code, writing broad tests, applying CI feedback,
reviewing code, and running in parallel. It was weak at inferring unstated
architecture, at long-term design judgment, and at experiential checks: it
could not see the app run. The findings depend on the late-2025 model.

## Key points

- **Hand-build the foundation and a few representative features.** Humans set
  architecture, modules, dependency injection, navigation, authentication, and
  networking. Prompts that point Codex at an existing screen as the pattern
  worked. Prompts with little context, or "port the iOS app", did not.
- **Plan before code.** Codex first summarizes how the relevant code works.
  Humans correct that summary, then the two co-write a mini design doc. Codex
  then executes it step by step. For tasks larger than the context window, save
  the plan to a file so other instances can reuse it. Reviews check the code
  against the plan.
- **`AGENTS.md` for persistent guidance.** Codex keeps many `AGENTS.md` files
  in the repo, for example "always run `./gradlew detektFix` before
  committing". A user-level `~/.codex/AGENTS.md` maps local repositories.
- **Brooks' Law applies to agent sessions.** Parallel sessions moved the
  bottleneck from writing code to human decisions, review, and integration.
  Each added session adds coordination overhead.
- **Cross-platform by translation.** With the iOS, backend, and Android repos
  in one environment, Codex translated Swift logic to Kotlin inside the Android
  architecture. The lesson: concrete examples beat descriptions.

## Concepts

[[human-agent-teams]]

## Connections

- The plan-file practice matches [[openai-run-long-horizon-tasks-codex]].
  Example-first context matches [[context-engineering]].
- The human-review bottleneck from parallel sessions is the problem that
  [[openai-symphony-codex-orchestration]] (April 2026) addresses by moving
  supervision to the ticket level. It also matches "human attention is the
  scarce resource" in [[anthropic-building-effective-human-agent-teams]].
- This post says Codex could not see the app run. The later Symphony post
  reports that OpenAI added end-to-end tests and Chrome DevTools app driving to
  its harness. Read these as a dated evolution of the harness, not a conflict.
  Compare "verify like a human user" in [[agent-harness]].
- On parallelism limits, see [[agent-orchestration]].
