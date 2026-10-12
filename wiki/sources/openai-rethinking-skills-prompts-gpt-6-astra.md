---
title: "OpenAI: Rethinking skills and prompts for GPT-6 Astra"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Eric Provencher (OpenAI)
date: 2026-09-11
source_url: https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
source_path: raw/openai-rethinking-skills-prompts-gpt-6-astra.md
models: [gpt-6-astra]
as_of: 2026-10-12
tags: [prompting, model-specific, openai, gpt-6, skills, agents-md, codex]
---

# OpenAI: Rethinking skills and prompts for GPT-6 Astra

> OpenAI Developers blog post on auditing skills, `AGENTS.md`, and task prompts
> when moving a coding agent to GPT-6 Astra.

## Summary

The post argues that instructions accumulated to steer earlier models now hurt
GPT-6 Astra. It covers three instruction surfaces: skills, `AGENTS.md`, and task
prompts. The post is written about `gpt-6-astra` only. It mentions Sol and Luna
only to warn that guidance written for them may over-constrain Astra.

Date: the page byline says Sep 11, 2026. One secondary source gave Sep 5; the
byline is used.

## Key points

### Skills
- [[openai-codex]] loads each skill's name and description into context. With
  too many skills, Codex **shortens descriptions to fit**, and skill selection
  gets worse.
- Contradictory or over-broad descriptions make the model load irrelevant
  instructions. The `$skill-creator` skill was updated to counter this.
- Three rules: (1) keep descriptions minimal but explicit about when to use;
  (2) use progressive disclosure — the root skill file is a small router to
  supporting docs and scripts; (3) replace step-by-step "recipes" with less
  specific guidance, because the model now handles ambiguity.
- Repository skills are read by other contributors' agents on other models.
  Write for the set of models that will read them. See [[agent-skills]].

### AGENTS.md
- Remove "read these docs before every edit" rules. Point to each doc for the
  situation where it applies instead. See [[agent-instructions]].
- Remove "remember to run tests" encouragement: Astra tests unprompted.
- Use `AGENTS.md` to pre-authorize known-safe workflows (example: a local test
  suite with disposable fixtures and no production access).

### Decision boundaries
- Strong "ask first" language written for earlier models can make Astra stop
  where the user wanted it to continue. The author says Astra has better
  judgment about safety, and recommends softening such language.

### Persistence
- Astra may return after a first implementation with work left. Define
  completion up front (run, inspect, fix). A mandatory review stop after the
  first implementation pulls the model toward stopping early.

## Notable claims & data

- Codex truncates skill descriptions when many skills are installed (no
  threshold given).
- No metrics are given; the post is qualitative.

## Entities

[[openai]], [[openai-codex]]

## Concepts

[[agent-skills]], [[agent-instructions]], [[context-engineering]],
[[prompt-tuning-axes]], [[guardrails]]

## Connections

Applies the Astra behaviors documented in [[openai-prompting-gpt-6-astra]]
(instruction sensitivity, tentative stopping, over-testing) to skills and
`AGENTS.md`. The progressive-disclosure rule matches
[[anthropic-eng-agent-skills]]. The "prune instructions per model release" theme
continues [[openai-prompt-guidance-gpt-5-6]].

## Contradictions / open questions

- The post says Astra "will not perform tasks unless it knows it is safe" and
  that users should trust it. [[guardrails]] recommends gating high-risk
  actions with tool-risk ratings and human-in-the-loop escalation. The post does not say to
  remove external controls, only to soften prompt wording; record as a tension,
  not a contradiction.
