---
title: "Anthropic: Using Claude Code — Spending Your Effort"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Thariq Shihipar (Anthropic)
date: 2026-09-25
source_url: https://claude.dev/blog/spending-your-effort/
source_path: raw/anthropic-spending-your-effort.md
models: [claude-opus-5-5, claude-fable-5-1]
as_of: 2026-10-12
tags: [claude-code, effort, reasoning-depth, verification, terminal-bench, evals, best-practices]
---

# Anthropic: Using Claude Code — Spending Your Effort

> An Anthropic engineer's account of what the effort setting changes in
> [[claude-code]]. It draws on three hands-on builds and on Terminal-Bench 3.0
> results, and it ends with a per-level rule of thumb.

## Summary

Published 2026-09-25 on the claude.dev blog ("Engineering") by Thariq Shihipar of
[[anthropic]]. The post is guidance, not a model-scoped prompting page. Its evidence
is tied to specific models and a date. The hands-on builds and the worked benchmark
examples ran on Claude Opus 5.5. The Terminal-Bench 3.0 charts cover Opus 5.5,
Fable 5.1, Opus 5, and Fable 5. The per-category chart and the failure-kind chart
show only Fable 5.1, Opus 5, and Fable 5. The runs are internal, with 5 attempts per
task; the footnote lists further caveats.

The post defines effort as a hint of how much compute to spend, related to how hard
the user thinks the task is. Higher effort means more independent judgment and more
verification, not a different approach. The central finding is that higher effort
pays off on tasks with many hidden edge cases. It reduces failures from missed edge
cases but does not fix failures from a wrong approach. The value of effort varies by
domain: it is largest in security and hardware and smallest in media and operations.

## Key points

- **Effort trades user-in-the-loop time for autonomy.** On an underspecified build
  (a fitness tracker), low effort produced a log and a graph in 1.5 minutes. Max
  effort produced a fuller app in 67 minutes and made more choices on the user's
  behalf. With a detailed spec, outputs at all levels were alike (low 16 minutes, max
  79 minutes). A good spec narrows what effort changes.
- **The author's per-phase loop:** (1) Claude interviews the user about the spec;
  (2) Claude implements at low effort; (3) the user reviews and iterates at low;
  (4) Claude verifies and tests at high effort. Effort is set per phase, not per
  session.
- **What higher effort changes in practice:**
  - `html-js-filter`: Fable 5.1 went from 1/5 at low to 5/5 at xhigh. The high-effort
    run reviewed its own draft adversarially, read the parser's source, ran a standard
    XSS test suite, and wrote a fuzzer.
  - Opus 5.5 at higher effort reproduced bugs before editing, tested against
    reference or brute-force implementations, and tried other data-prep methods.
    Results: `mvcc-lsm-compaction` 0/5 → 4/5, `cli-2ph-simplex` 0/5 → 5/5, and
    `gsea-proteomics` 0/5 → 4/5.
- **Failure-kind data (Fable 5.1, 370 attempts):** passes rose from 140 at low to 214
  at max. The count for "bug its tests missed" fell from 40 to 14. The count for
  "picked the wrong reading" rose from 25 to 47. The failure kinds are labeled by a
  model judge and are approximate.
- **Per-domain gain (Fable 5.1, pass rate from the pooled low settings to the pooled
  top settings):** security 64% → 87%, hardware 34% → 75%, ML 54% → 73%, science
  41% → 61%, software 43% → 56%, media 18% → 30%, operations 12% → 22%.
- **Effort curves (Fig A):** Opus 5.5 ranges from 36.6% at low to 65.7% at max.
  Opus 5.5 at high (58.9%) matches Fable 5.1 at max (58.0%) on about half the tokens.
  Opus 5.5 ran about three weeks after the other models, with a 128k response cap.
- **Rule of thumb:** low for brainstorming, sketches, and easy changes. Medium for
  most feature work. High where verification or edge cases matter, such as a bug in a
  brownfield codebase. Max for fully autonomous hard problems, such as an end-to-end
  build or a vulnerability hunt. The post gives no rule for xhigh. Use `/effort` to
  change the level mid-conversation.
- **Without a user in the loop, effort substitutes for clarification.** At high
  effort the model explores other interpretations that a user might have settled with
  one question.

## Entities

[[anthropic]], [[claude-code]], [[claude]]

## Concepts

[[prompt-tuning-axes]], [[agent-evals]], [[agent-steering]], [[agent-harness]]

## Notable claims & data

- The post uses **Terminal-Bench 3.0** (70 tasks, GPU tasks excluded). Do not
  conflate it with the **Terminal-Bench 4.0** scores in
  [[anthropic-opus-5-5-long-coding-sessions]].
- The chart data maps numeric internal effort values to named levels differently
  for each model. For example, "medium" is 20 on Opus 5 but 15 on Fable 5.1. This is
  concrete support for the rule that level names do not port across models.
- Footnote caveats: production safety interventions were off for Fable 5.1, and
  security tasks ran without internet access. The counts do not match the public
  leaderboard or the launch post.
- The opening claim is that effort changes no longer break the prompt cache in
  Claude Code on the newest models. [[anthropic-what-a-task-costs-opus-5-5]] limits
  this to API-key and subscription access.

## Connections

The companion post from the same day is [[anthropic-what-a-task-costs-opus-5-5]],
which prices effort and gives an Opus 5.5 level ladder. Its advice to "give the
model a way to check its work before raising effort" complements this post's
"verify at high". Effort defaults and calibration are in
[[anthropic-prompting-claude-opus-5-5]] and
[[anthropic-prompting-claude-fable-5-1]]. The "start smart, tune effort" framing is
in [[anthropic-choosing-claude-model]]. Verification as a separate phase matches
[[anthropic-verification-loops-with-skills]]. The cache claim updates
[[anthropic-claude-code-session-cost]].
