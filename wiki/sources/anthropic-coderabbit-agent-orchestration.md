---
title: "Anthropic: How CodeRabbit Used Claude to Build an Agent Orchestration System"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com articles), no named author
date: 2026-05-27
source_url: https://claude.com/resources/articles/how-coderabbit-used-claude-to-build-an-agent-orchestration-system
source_path: raw/anthropic-coderabbit-agent-orchestration.md
tags: [case-study, planning, orchestration, model-routing, agent-evals, claude-code]
---

# Anthropic: How CodeRabbit Used Claude to Build an Agent Orchestration System

> Anthropic-published customer case study: CodeRabbit puts a multi-model
> planning layer in front of the coding agent so that unstated requirements
> surface before code is generated.

## Summary

Anthropic published this case study on 2026-05-27; all results are
self-reported by CodeRabbit (an AI code review company; about 2 million PRs
reviewed per week for 15,000+ customers). CodeRabbit found that the most common
failure in AI-generated PRs was code that worked technically but missed the
developer's intent, because developers leave shared context unstated and the
agent fills the gaps with plausible guesses. Its fix is a planning layer that
runs before [[claude-code]]: several [[claude]] models analyze the request,
surface assumptions, and produce a product requirements document (PRD) that
stakeholders validate. Claude Code then turns the PRD into a fine-grained
implementation plan. The post does not name model versions.

## Key points

- **Plan before code, at a level above Plan Mode.** The layer narrows the
  direction given to Claude Code; it does not replace Claude Code Plan Mode. The
  saved plan doubles as a decision record for rework prevention, intent checks,
  and onboarding.
- **Tiered model routing.** Opus runs the orchestration loop; Sonnet sequences
  planning steps; Haiku does narrow work (context distillation, targeted tool
  calls). Routing follows eval results on cost and latency. See
  [[agent-orchestration]], [[multi-agent-economics]].
- **Evals for plans, not only code.** Start with hand-tuned examples and manual
  inspection; then a library of LLM judges, one per plan dimension; downstream
  checks (does the code work, extra scope, token use); A/B runs with and without
  the planning step. See [[agent-evals]].
- **Plan granularity is a tuned variable.** Too granular goes stale as code
  changes; too high-level leaves room for harmful assumptions.
- **Pre-coding checklist:** target outcome and its measure, implicit
  assumptions, forgotten edge cases, how output is checked against intent.

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[agent-orchestration]], [[agent-evals]], [[multi-agent-economics]],
[[agent-instructions]], [[context-engineering]]

## Notable claims & data

- "Many issues" formerly found in code review are now caught at planning; no
  figure is given. Treat as a self-reported claim, not a measured rate.

## Connections

- Same intent-gap diagnosis as the spec-first advice in
  [[anthropic-eng-claude-code-best-practices]].
- Model-tier routing parallels [[anthropic-choosing-claude-model]] and the
  orchestrator/worker split in [[anthropic-eng-multi-agent-research-system]].
- Another planning-plus-review case study: [[claude-customer-greptile]].
