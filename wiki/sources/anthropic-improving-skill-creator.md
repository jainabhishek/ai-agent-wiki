---
title: "Anthropic: Improving skill-creator — test, measure, and refine Agent Skills"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com articles)
date: 2026-03-03
source_url: https://claude.com/resources/articles/improving-skill-creator-test-measure-and-refine-agent-skills
source_path: raw/anthropic-improving-skill-creator.md
tags: [skills, evals, benchmarking, trigger-tuning, skill-authoring]
---

# Anthropic: Improving skill-creator — test, measure, and refine Agent Skills

> Announcement of eval, benchmark, parallel-run, blind A/B, and description-tuning features in Anthropic's skill-creator, with a two-type model of skills that says what each test is for.

## Summary

Published 2026-03-03 on claude.com; no model version is named. Anthropic observes that most skill authors are subject-matter experts, not engineers. They could not tell whether a skill still worked on a new model, triggered correctly, or improved after an edit. skill-creator now writes evals, runs them, and benchmarks results without code. It is available in Claude.ai, Cowork, as a Claude Code plugin, and in the repo. The post splits skills into **capability uplift** (the base model cannot do the task, or not consistently) and **encoded preference** (the model can do each step; the skill sequences them per a team's process). The two types need tests for different reasons.

## Key points

- **Why test each type.** Capability uplift skills may become unnecessary as models improve; if the base model passes the evals *without* the skill, the skill is obsolete, not broken. Encoded preference skills last longer but are only as good as their fidelity to the real workflow. (see [[agent-skills]], [[agent-evals]])
- **Evals catch model-change regressions.** Run them against each new model before the team notices drift. Example: evals isolated the PDF skill's failure on non-fillable forms; the fix anchors placement to extracted text coordinates.
- **Benchmark mode** tracks eval pass rate, elapsed time, and token usage. Results stay local and can feed a dashboard or CI.
- **Isolated parallel runs.** Each eval runs in a separate agent with a clean context, so runs do not contaminate each other. (see [[agent-orchestration]])
- **Blind comparators.** Comparator agents judge skill v1 vs v2, or skill vs no skill, without knowing which is which.
- **Description tuning.** skill-creator tests the description against sample prompts and proposes edits that cut false positives and false negatives. Reported: better triggering on 5 of 6 public document-creation skills.
- **Outlook.** The post predicts that skill and specification may merge: evals already describe the "what", and a description of the outcome may later be enough as the skill.

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[agent-skills]], [[agent-evals]], [[agent-orchestration]]

## Connections

Supersedes the Jan 2026 statement in [[anthropic-complete-guide-building-skills]] that skill-creator does not run automated tests. Eval and hillclimb method: [[anthropic-automating-eval-design-hillclimbing]]. OpenAI's equivalent: [[openai-testing-agent-skills-with-evals]]. Eval fundamentals: [[anthropic-eng-demystifying-evals]].
