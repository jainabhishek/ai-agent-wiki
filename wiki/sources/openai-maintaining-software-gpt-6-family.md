---
title: "OpenAI: Maintaining software with the GPT-6 family"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Rodrigo Roim (OpenAI Core Experimentation team)
date: 2026-10-14
source_url: https://developers.openai.com/blog/maintaining-software-with-the-gpt-6-family
source_path: raw/openai-maintaining-software-gpt-6-family.md
models: [gpt-6-astra, gpt-6.1-sol]
as_of: 2026-11-24
status: legacy
superseded_by: [openai-prompting-gpt-6-2]
tags: [openai, codex, gpt-6, model-specific, maintenance, dead-code, feature-flags, cost, case-study]
---

# OpenAI: Maintaining software with the GPT-6 family

> **Legacy (checked 2026-11-24).** OpenAI's models overview (checked 2026-11-24) lists GPT-6.2 Astra, GPT-6.2 Sol, GPT-6.1 Terra, and GPT-6 Luna as current; GPT-6 Astra and GPT-6.1 Sol moved to "More models". The cost comparison below stays true of those models; the method (compare settings by cost per validated finding) does not depend on them. For the current models, see [[openai-prompting-gpt-6-2]].

> OpenAI Developers blog case study: one OpenAI team used Codex with GPT-6 Astra
> and GPT-6.1 Sol to remove dead code and stale experiments, and compared the
> cost per finding of the two models.

## Summary

The author's team builds OpenAI's experimentation software. Faster building
with coding agents also raised the team's maintenance load. The post reports
three maintenance workflows in [[openai-codex]]: dead-code removal, stale
experiment cleanup, and CI and test fixes. It reports a cost comparison between
`gpt-6-astra` and `gpt-6.1-sol` on one cleanup task.

The common method is short, broad prompts plus evidence gathering, small draft
PRs, and human review. The model writes the next, larger prompt from the review
feedback. The closing advice is to start with one small task, compare models
and effort levels on it, then widen the scope in steps.

GPT-5.6 Sol appears only as the earlier baseline. All results are
self-reported.

## Key points

### Dead code
- Earlier approach: static analysis tied to runtime logging. It still caused
  incidents (reflection, and code paths kept on purpose to mitigate future
  incidents).
- With GPT-5.6 Sol, the author gave Codex an area plus validation criteria, and
  the model wrote the analysis. With GPT-6 Astra, a short, informal, ambiguous
  prompt worked. Astra chose its own evidence: past PRs, Slack threads, project
  trackers, and production profiling tables that showed lines were never
  reached. It explained each deletion.
- Five engineers, part-time over two weeks: more than 1,400 merged PRs and over
  800k deleted lines. Reviews went to the teams that own each project.

### Stale experiments
- Harder than dead code: flag-gated code can still run in production.
- The author asked Astra to write the first prompt. The prompt names
  safeguards: verify live flag config, check git history and overlapping PRs,
  keep killswitches and operational safeguards, and open one small draft PR per
  cleanup.
- After review, Astra turned the review comments into a whole-repo `/goal`
  prompt. That prompt asks for a prioritized report (with CPU cost from
  production telemetry) grouped into parallel workstreams by owner and file,
  and it forbids changes to live configs or services.
- Judgment example: Astra found a test-override flag that caused large CPU
  fan-out. It did not remove the flag, because the flag was marked "Permanent"
  in the flag console. It raised the flag for human review. The team then
  removed it, for an estimated 0.42% CPU saving in the main affected service.

### Model and effort comparison (one task, author-validated findings)

| Model / effort | API cost | Findings | Cost per finding |
|---|---|---|---|
| GPT-6 Astra Ultra | $109.06 | 142 | $0.77 |
| GPT-6.1 Sol Ultra | $15.12 | 131 | $0.12 |
| GPT-6.1 Sol Medium | $5.27 | 86 | $0.06 |

- Scope: subdirectories with over 6,000 files and 1M lines (Python,
  TypeScript, Go, Rust). Costs include research subagents and the follow-up
  turns that Codex ran by itself.
- GPT-6.1 Sol Ultra: 92% of Astra's findings at 14% of the cost.
- Most Ultra-vs-Ultra gaps were constant flags used as dependencies of other
  flags: Astra found them, GPT-6.1 Sol did not. The team writes prompt
  corrections for such gaps, and revisits them at each model release because
  new models can make them obsolete.

### Other prompts and results
- Flaky tests: a `/goal` prompt that fixes clear, simple cases and opens PRs.
- `AGENTS.md` A/B: replay one past session prompt with and without one suspect
  instruction, from the same snapshot and model, and compare quality, tool
  calls, tokens, runtime, and cost.
- CI load: rank ideas by estimated CI minutes saved per day. Result: about 30
  PRs; median CI time from about 10 to 4.5 minutes; p90 from 12.5 to 6 minutes.
  One added mock cut a 63-test suite from 592.6 s to 29.8 s.
- The author suggests starting these at GPT-6.1 Sol Medium and raising effort
  for broader audits.

## Entities

[[openai]], [[openai-codex]]

## Concepts

[[human-agent-teams]], [[agent-harness]], [[agent-instructions]],
[[multi-agent-economics]], [[agent-evals]], [[agent-verification]],
[[guardrails]], [[prompt-tuning-axes]]

## Notable claims & data

- More than 1,400 merged maintenance PRs that started from GPT-6 proposals;
  over 800k lines deleted in the dead-code push.
- One container image went from 3.31GB to 1.72GB (48% smaller); about 400
  visual snapshot variants were removed from a test suite.
- Some proposals added more complexity than their benefit justified, so
  prioritization and measurement stayed in the workflow.
- The cost table counts "findings" that the author reviewed and validated. The
  post does not give false-positive counts or reviewer time.

## Connections

- Dead-code and stale-flag cleanup is a concrete case of the "garbage-collection
  agents" practice in [[agent-harness]] (from [[openai-harness-engineering]]).
- "Start small, review, and expand" matches earned autonomy per task type in
  [[human-agent-teams]].
- Cost per validated finding is an instance of the "cost per accepted outcome"
  rule in [[multi-agent-economics]].
- Re-tuning prompts at each model release continues
  [[openai-rethinking-skills-prompts-gpt-6-astra]] and the pruning rule in
  [[agent-instructions]]. The `AGENTS.md` replay prompt is a small eval in the
  sense of [[agent-evals]].
- Model roles match [[openai-practical-guide-building-with-gpt-6]]: Astra for
  the hardest reasoning, GPT-6.1 Sol for cheaper coding work.
- Flagging the "Permanent" flag for review instead of deleting it fits the
  Astra caution described in [[openai-prompting-gpt-6-astra]].

## Contradictions / open questions

- The post labels effort levels "Ultra" and "Medium". The API effort values
  recorded in [[openai-prompting-gpt-6-astra]] for GPT-6.1 Sol are `low`,
  `medium`, `high`, `xhigh`, and `max`. [[openai-practical-guide-building-with-gpt-6]]
  lists Low, Medium, High, and Extra high / Max. Neither names "Ultra". It may
  be a Codex label for one of those levels, or a newer level. Open as of
  2026-11-24.
