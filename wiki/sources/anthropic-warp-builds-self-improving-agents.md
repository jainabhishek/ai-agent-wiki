---
title: "Anthropic: How Warp builds self-improving agents on Claude"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Michael Segner (Anthropic, claude.com articles)
date: 2026-08-26
source_url: https://claude.com/resources/articles/how-warp-builds-self-improving-agents-on-claude
source_path: raw/anthropic-warp-builds-self-improving-agents.md
tags: [case-study, agent-skills, feedback-loop, self-improvement, human-in-the-loop, code-review]
---

# Anthropic: How Warp builds self-improving agents on Claude

> A customer case study: Warp turns human feedback on agent output into reviewed
> edits to the agent's skill file, through a scheduled "improver" agent.

## Summary

Anthropic published this case study on claude.com articles on 2026-08-26, in a
startup series. All results and company figures are self-reported by Warp and
Anthropic. Warp's internal code review agent produced unhelpful comments.
Prompt rewrites and `AGENTS.md` edits helped only partly. Warp's diagnosis:
feedback given to an agent disappears when the session ends. The fix is a
two-skill loop. A **base skill** holds domain instructions. Humans comment on
the agent's output. A scheduled **improver skill** compares agent output with
human responses and opens a PR with the smallest edit to the base skill. A human
merges the PR, and the next run inherits it. No model name is given.

## Key points

- **Architecture**: base skill (per task) + human feedback + improver skill
  (on a schedule, not per task). The skill edit is a normal PR, so the existing
  code-review workflow is the approval gate. See [[agent-skills]].
- **Worked example (issue triage)**: a GitHub Action runs a triage agent on each
  new issue. The agent missed the `ready to spec` label. A maintainer commented
  with what and why. The improver runs in Warp's Oz orchestration platform. It
  runs a Python script bundled with the skill to pull issues with feedback into
  a JSON summary, then opens a PR that changes the label rule. The PR
  description names the triggering signals.
- **Authoring tips**: write principles, not rules; explain the why; capture
  feedback where people already work, with no extra step; keep skills small with
  progressive disclosure; prefer detailed domain-expert feedback over binary
  thumbs; invest in the improver, which is reusable across agents.
- **Skills vs memory**: skills are procedural, stable, and changed on purpose.
  Memory is written by the agent at inference time and changes constantly.
- **Guarding the loop**: assume some feedback is wrong. Let the agent
  sanity-check it, filter whose input counts, and keep a human at the filtering
  or final-review stage. In verifiable domains, build the verification harness
  first. Otherwise use golden-output evals and restrict feedback to domain
  experts. Feed global metrics (time to merge, contributor count, cost) to the
  improver; roll out crawl-walk-run.
- **Scale (self-reported)**: the pattern runs across Warp's open-source repo
  with separate spec-writing, review, and triage agents; hundreds of
  contributors and thousands of code reviews.

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[agent-skills]], [[agent-evals]], [[guardrails]], [[agent-harness]],
[[context-engineering]], [[human-agent-teams]].

## Notable claims & data

- Company figures (self-reported): $73M raised; 800K monthly developers; 56% of
  the Fortune 500; 10M Claude Code sessions inside Warp to date, 400K+ per week;
  40M Warp Agent conversations.
- An 80%-correct first-pass prompt is described as still noisy for recurring
  tasks.
- No before/after quality metric for the code review or triage agents is given.

## Connections

The same feedback-to-skill loop appears in
[[anthropic-abc-legal-managed-agents]] (harvester-tuner loop) and
[[openai-self-improving-tax-agents-codex]]. The skills-vs-memory distinction
complements [[anthropic-building-agents-with-skills]] and
[[anthropic-complete-guide-building-skills]]. Bundled deterministic scripts
inside a skill match the advice in [[openai-skills-for-oss-maintenance]]. Human
approval of each skill edit is a guardrail of the kind in [[guardrails]].
