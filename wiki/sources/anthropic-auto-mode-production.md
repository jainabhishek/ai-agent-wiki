---
title: "Anthropic: Running Auto Mode in Production"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Molly Vorwerck (Anthropic, claude.com articles)
date: 2026-08-07
source_url: https://claude.com/resources/articles/auto-mode-in-production
source_path: raw/anthropic-auto-mode-production.md
tags: [case-study, guardrails, permissions, claude-code, long-running-agents]
---

# Anthropic: Running Auto Mode in Production

> Anthropic-published customer stories (Nuro, Gusto, Garner Health) on how teams
> run Claude Code auto mode, and where they still switch back to manual review.

## Summary

Molly Vorwerck (Anthropic, 2026-08-07) published this alongside the default
switch in [[anthropic-auto-mode-default]]. Results are self-reported by Anthropic
and the three customers. Headline claim: Claude works 9x longer between
interruptions than under the previous default, across all [[claude-code]] usage
(no method or baseline is given). The transferable content is how each team
pairs auto mode with other controls and which work it keeps out of auto mode.
See [[guardrails]].

## Key points

- **Keep a manual tier for high-stakes work.** Nuro switches to interactive mode
  for work that affects other teams; Gusto switches to accept-edits for
  Terraform, AWS, and live-API POSTs and checks each tool call.
- **Layer auto mode on other controls.** Nuro adds deny rules (recursive
  deletes) and skills. Gusto routes MCP traffic through a governed proxy with
  tool guards and prompt inspection, so scopes are set before auto mode runs.
- **Customize the boundary.** Garner Health blocks auto-approval of actions that
  message people (Slack, email); IP-sensitive teams tuned the classifier's
  injected prompts.
- **Precursor pattern.** Before auto mode, a Nuro engineer built a hook that sent
  each pending action to a small model, auto-approved about 90%, and routed the
  rest to Slack for human review.
- **Long unattended runs.** Nuro research agents hill-climb eval metrics
  overnight (one 10 p.m.–5 a.m. run produced three PRs). Garner's SDLC plugin
  has agents run "antagonistic research" on their own assumptions before
  implementing.
- **Advice (Garner):** build controls, telemetry, and standard workflows before
  scaling.

## Entities

[[anthropic]], [[claude-code]]

## Concepts

[[guardrails]], [[agent-steering]], [[agent-skills]],
[[model-context-protocol]], [[agent-harness]]

## Notable claims & data

- Gusto: about 10% of transcripts since mid-May 2026 included an auto mode
  denial; one engineer ran 2,425 sessions since December.
- Garner Health: 550 employees; about two hours a week per person encouraged for
  automation.
- **New versus [[anthropic-eng-claude-code-auto-mode]]:** the 9x
  interruption figure, customer deployment patterns, and the classifier-prompt
  tuning by customers. No classifier error rates appear here, so no figure
  conflicts with that page.

## Connections

- Launch and safety evidence: [[anthropic-auto-mode-default]].
- Design: [[anthropic-eng-claude-code-auto-mode]]; sandbox layer:
  [[anthropic-eng-how-we-contain-claude]].
- Deterministic hooks and deny rules: [[anthropic-steering-claude-code]],
  [[anthropic-configure-hooks]].
