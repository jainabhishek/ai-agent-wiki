---
title: "Anthropic: Building verification loops in Claude Code with skills"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Delba de Oliveira (Anthropic, Claude Code team)
date: 2026-07-22
source_url: https://claude.com/resources/articles/building-verification-loops-in-claude-code-with-skills
source_path: raw/anthropic-verification-loops-with-skills.md
tags: [claude-code, agent-skills, verification, feedback-loop, best-practices, ci]
---

# Anthropic: Building verification loops in Claude Code with skills

> A short Claude Code guide on turning the manual checks a developer repeats
> after each agent change into skills, and on choosing where each check runs:
> standalone, embedded, chained, or on every PR.

## Summary

Published on claude.com articles (Anthropic) on 2026-07-22 by a Claude Code team
member. The article frames an agentic coding session as a loop of gather
context, take action, verify results. [[claude-code]] already verifies against
deterministic signals (type checkers, linters, tests, runtime errors). The
article defines a **verification loop** as a repeating cycle in which the agent
checks its own work and fixes failures before it moves on. The remaining manual
checks become verification loops when the developer writes them as
[[agent-skills]]. The article lists built-in options, explains how to write a
check, and gives four placements for a check with the trade-off of each. It is
product guidance, not per-model prompting advice, so it carries no `models:`
scope.

## Key points

- **Built-in loops**: the `/verify` skill (build, run, observe); the toolchain
  (put exact build and test commands in `CLAUDE.md`); Code Review (research
  preview, managed multi-agent PR review, closable with an `@claude` comment);
  GitHub Actions running a verification skill on each push or PR; a
  spec-validation skill against a markdown spec; rubrics in
  [[claude-managed-agents]] (beta), graded by a separate grader agent.
- **What to capture**: the corrections you repeat on every feature. Write them in
  plain English for a day-one teammate. Checks can be deterministic and
  project-specific, e.g. reject a migration that drops a column without a
  backfill step.
- **How to package**: the `skill-creator` plugin interviews you, or you write
  `.claude/skills/<name>/SKILL.md` by hand. The example `verify-log-hygiene`
  skill restricts tools with `allowed-tools: [Read, Edit, Grep]`, reports each
  violation as `file:line`, then fixes it.
- **Four placements**:
  - *Standalone*: invoked on purpose, for cross-cutting checks (security scan,
    accessibility audit, license headers). Running it after every change is the
    signal to embed or chain it.
  - *Embedded*: a one-line step appended to the producing skill (e.g. run eslint
    after scaffolding a component). Only for skills you can edit, not built-in
    or plugin-managed skills that updates overwrite.
  - *Chained*: a skill invokes the next at its end. The Claude Code team chains
    `/code-review` → `/simplify` → `/verify` → a custom `/design` skill against
    `DESIGN.md`. A wrapper skill adds checks to a skill you cannot modify.
    Chains trade flexibility for automation and can raise token spend.
  - *On every PR*: the same skills and rubrics gate every teammate's change.
    Wait until the chain is stable, because each tweak is then team-visible.
- **Six-step process**: pick the most frequent manual follow-up; try `/verify`
  first; write the procedure; make it a skill; confirm it runs on a new task;
  then experiment with chaining.

## Entities

[[anthropic]], [[claude-code]], [[claude-managed-agents]]

## Concepts

[[agent-skills]], [[agent-evals]], [[agent-harness]], [[agent-steering]],
[[guardrails]]

## Notable claims & data

- "Embedded only works on skills you can edit" — the edit-ownership constraint
  decides embed versus chain. This is a durable design rule.
- Chained verification can increase token spend; the article advises testing a
  chain before broad deployment. No figures are given.
- The verifier for rubric-based outcomes is a separate grader agent, which
  matches the separate-verifier pattern in [[agent-evals]] and
  [[anthropic-harness-for-every-task]].

## Connections

Follows the loop framing of [[anthropic-getting-started-with-loops]]. Extends
the skill mechanism in [[anthropic-steering-claude-code]] and the
product-verification skill category in [[anthropic-lessons-building-claude-code-skills]].
The "make a skill mandatory" pattern in [[openai-skills-for-oss-maintenance]]
(an `AGENTS.md` rule requires the verification skill) is the OpenAI-side
analogue of the embedded and chained placements. Skill authoring details are in
[[anthropic-complete-guide-building-skills]] and
[[anthropic-improving-skill-creator]]. Deterministic lifecycle enforcement
belongs to hooks instead; see [[anthropic-configure-hooks]].
