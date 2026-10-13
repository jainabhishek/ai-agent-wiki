---
title: "Anthropic: How ABC Legal turned every employee into a builder with Claude Managed Agents"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Anthropic (claude.com articles)
date: 2026-08-17
source_url: https://claude.com/resources/articles/how-abc-legal-turned-every-employee-into-a-builder-with-claude-managed-agents
source_path: raw/anthropic-abc-legal-managed-agents.md
tags: [case-study, managed-agents, agents-as-code, human-in-the-loop, feedback-loop, agent-fleet]
---

# Anthropic: How ABC Legal turned every employee into a builder with Claude Managed Agents

> Customer story (case study) on running a fleet of 50+ agents as code on
> Claude Managed Agents, built mostly by non-developers.

## Summary

Published by [[anthropic]] on 2026-08-17. All figures are self-reported by ABC
Legal, a U.S. legal document delivery company, as of July 2026. CTO Brandon
Fuller moved desktop scheduled tasks onto [[claude-managed-agents]]. Each agent
is defined as code in git and changes only through an approved pull request.
Non-developers built agents from templates with [[claude-code]]. Agents start
with a human in the loop. A harvester-tuner loop turns Slack feedback into
pull requests that change prompts and config. Reported results: 50+ agents in
production; up to ~50% lower cost on some covered tasks; ~310 daily users; one
review agent at ~98% agreement with the compliance team.

## Key points

- **Agents as code.** Prompt, tool list, schedule, credentials, and memory live
  as config files in git. Each agent folder holds a JSON config, a Markdown
  system prompt, deploy scripts, and ops docs. A merge to main deploys the
  agent. Two templates exist: event-driven and scheduled.
- **The pull request is the control surface.** Every change gets review,
  version history, rollback, and an audit trail. The stated rule: make a
  decision look like a pull request.
- **Earned autonomy.** Each agent first posts recommendations, as a banner or
  in Slack. It moves to automation mode only after it matches or beats humans
  on that task. It stays under the same measurement after the move. See
  [[guardrails]].
- **Harvester-tuner loop.** Three agents share one workspace and credential
  vault. The Initial Agent does the work. The Harvester (hourly or daily) turns
  thread replies and emoji reactions into labels. The Tuner (weekly) drafts a
  prompt or config change as a PR, and a human merges it. Improvement happens
  without retraining. At Docketly, about 145 YAML routing rulesets are tuned
  this way. A fourth agent applies only merged changes.
- **Responsibility split.** The platform owns the loop, sessions, memory,
  console, and models. ABC Legal owns the prompt, tools, triggers, audit
  trail, and outcome feedback. See [[agent-harness]].
- **Model tiering.** Sonnet is the default, Haiku is for high-volume work, and
  Opus is for deep reasoning. A model swap is a one-line config change.
- **Economics.** Each agent reports its value per run (hours and dollars)
  against its cost. Agents follow a J-curve: they lose money while new, then
  pay off after evals, cheaper models, and token trimming. The case study
  states that not every task deserves an agent.
- **The main hurdle was git, not AI.** Business users had to learn clone and
  pull-request workflows.

## Concepts

[[human-agent-teams]]

## Connections

- Same production pattern as [[anthropic-building-effective-agent-automations]]
  and [[anthropic-eng-scaling-managed-agents]].
- The feedback loop resembles [[anthropic-warp-builds-self-improving-agents]]
  and [[openai-self-improving-tax-agents-codex]].
- Entities: [[claude-managed-agents]], [[claude-code]]. Concept: [[model-context-protocol]].
