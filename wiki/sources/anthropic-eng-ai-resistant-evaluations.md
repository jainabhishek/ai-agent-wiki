---
title: "Anthropic: Designing AI-resistant technical evaluations"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Tristan Hume (Anthropic Engineering blog)
date: 2026-01-21
source_url: https://www.anthropic.com/engineering/AI-resistant-technical-evaluations
source_path: raw/anthropic-eng-ai-resistant-evaluations.md
tags: [evals, hiring, benchmarks, saturation, test-time-compute, case-study]
---

# Anthropic: Designing AI-resistant technical evaluations

> How Anthropic's performance-engineering hiring take-home was defeated by
> successive Claude models, and the redesigns that keep it measuring human
> skill when candidates may use AI.

## Summary

**Scope: this is a human-hiring evaluation, not an agent eval.** The post is
about a take-home test that measures job candidates who may use AI help. It
does not describe how to evaluate an agent. Its links to [[agent-evals]] are
indirect: it records how fast a fixed task saturates as models improve, which
task properties survive stronger models, and benchmark numbers for Claude models
on one optimization task under different harnesses and time budgets.

Tristan Hume's take-home (in use since early 2024, published 2026-01-21) asks
candidates to optimize a parallel tree traversal on a Python-simulated,
TPU-like accelerator (scratchpad memory, VLIW, SIMD, multicore), using a
Perfetto trace. About 1,000 candidates took it, and AI use is explicitly
allowed. Successive models defeated it. By May 2025, over half of candidates
would have scored better by delegating fully to Claude 3.7 Sonnet in
[[claude-code]]. Claude Opus 4 beat almost all humans within the 4-hour limit.
For version 2 the author used Opus 4 to find where it struggled, started the
new test there, and cut the limit to 2 hours. Claude Opus 4.5 then matched the
best human 2-hour score. A harder transposition problem fell to Opus 4.5 with
a longer thinking budget ("ultrathink"), because such problems are common in
training data. The surviving design is a set of Zachtronics-style puzzles in a
tiny, constrained instruction set, with no debugging tools provided. The
author's summary of the trade: the original worked because it resembled real
work; the replacement works because it simulates novel work.

## Key points

- **Design goals (v1):** longer horizon than live interviews; realistic
  environment; time for comprehension and tool building; AI allowed; many
  chances to score (no single-insight problems); wide score spread; no narrow
  domain knowledge; fun. (Design goals)
- **Saturation path:** v1 fell to Opus 4 (pre-release), v2 to Opus 4.5
  (pre-release). With unlimited time, the best humans still beat Claude.
  (Then Claude Opus 4 / 4.5 defeated it)
- **Redesign method for v2:** find where the current model starts to struggle,
  and make that the new starting point. (Then Claude Opus 4 defeated it)
- **Options rejected:** banning AI (hard to enforce, unlike the job); requiring
  candidates to "substantially beat Claude Code alone" (humans steering a fast
  model fall behind it, so watching may become the best strategy).
  (Considering the options)
- **Familiar problems fall first.** Bank-conflict-free transposition is common
  across platforms, so Claude drew on a large body of prior work. It also found
  an unintended whole-computation transpose that the author had to patch out.
  (Attempt 1)
- **Out-of-distribution survives.** Puzzles in a tiny, constrained ISA
  optimized for instruction count beat Opus 4.5. Tool building is part of the
  signal: the starter code only validates solutions. (Attempt 2)

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[agent-evals]], [[agent-harness]]

## Notable claims & data

Simulated clock cycles on the released original (lower is better):

| Cycles | Configuration |
|---|---|
| 2164 | Claude Opus 4, many hours in test-time compute harness |
| 1790 | Claude Opus 4.5, casual Claude Code session (≈ best human in 2 h) |
| 1579 | Claude Opus 4.5, 2 h in test-time compute harness |
| 1548 | Claude Sonnet 4.5, many more than 2 h of test-time compute |
| 1487 | Claude Opus 4.5, 11.5 h in harness (best at launch) |
| 1363 | Claude Opus 4.5, improved test-time compute harness, many hours |

- The same model (Opus 4.5) ranges from 1790 to 1363 cycles depending on
  harness and time budget. A "generic" harness improvement after launch raised
  the score. This is evidence that harness and compute are part of what a score
  measures. See [[agent-harness]].
- Opus 4.5 stopped at a perceived memory-bandwidth limit, as most humans do.
  Told the achievable cycle count, it found the trick. A target number changed
  the outcome.
- Earlier precedent: Claude 3 Opus and Claude 3.5 Sonnet beat parts 1 and 2 of
  a 2023 live-interview question.

## Connections

- **[[agent-evals]] saturation.** The post is a dated case of the "saturation"
  pitfall: a task that separated humans stopped separating them as models
  improved.
- **Tension with adversarial sampling.** The v2 method — start the test where
  the current model struggles — is the move that
  [[anthropic-automating-eval-design-hillclimbing]] warns against for agent evals,
  because it measures one model's "failure fingerprint". The aims differ: the
  hiring test wants to stay ahead of the model, while an agent eval wants to
  measure intrinsic difficulty. The v2 version still fell to the next model.
  This fits the warning, but it is one data point.
- **Harness changes the score.** Like [[anthropic-eng-infrastructure-noise-evals]],
  the cycles table shows configuration (harness, time, thinking budget) moving
  results for a fixed model and task.
- **Unintended solutions.** Opus 4.5's whole-computation transpose matches the
  "unintended but valid solution" pattern in [[anthropic-eng-demystifying-evals]]
  and the BrowseComp decryption in [[anthropic-eng-eval-awareness-browsecomp]].
