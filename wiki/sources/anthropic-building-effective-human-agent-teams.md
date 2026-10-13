---
title: "Anthropic: Building effective human-agent teams"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Kristen Swanson (Anthropic Education team)
date: 2026-06-24
source_url: https://claude.com/resources/articles/building-effective-human-agent-teams
source_path: raw/anthropic-building-effective-human-agent-teams.md
tags: [human-agent-teams, multiplayer-agents, claude-tag, verification, autonomy, organizational-practice]
---

# Anthropic: Building effective human-agent teams

> Anthropic's guidance on "multiplayer agents": agents that serve a whole team in shared channels, with four team norms learned from several months of internal use.

## Summary

Anthropic published this perspective piece on claude.com on 2026-06-24. It is the first post in a series on human-agent teams, and it names no model version. The post defines multiplayer agents as models that work with many humans at once and live where the work happens (Slack at Anthropic). Multiplayer agents need three capabilities: persistent memory, credentials not tied to a human, and ongoing broad access to information. The post then gives four lessons. Its closing claim: these are old human-team habits, and agents only make skipping them more costly.

## Key points

- **Lesson 1: work in public.** Agents know only what is written and searchable. Anthropic sets a few workspace-level security boundaries and lets context flow freely inside each boundary, instead of making per-item sharing decisions. New channels default to org-public, and teams write meeting notes and artifacts for agents as primary readers. Private work goes through DMs or personal MCP connectors. (see [[context-engineering]], [[guardrails]])
- **Lesson 2: one roster with defined roles.** Each human and agent has a written role, a scope, and the right tools. Skill files define agent roles, so others can stand up the same agent type. Without roles, people run side fleets of personal AIs that duplicate work and fragment context. (see [[agent-skills]], [[human-agent-teams]])
- **Lesson 3: a human-set north star.** Humans write the north star and name which agents may propose new workstreams.
- **Lesson 4: earn autonomy per task type.** Grant autonomy in proportion to demonstrated reliability, and track autonomy per task type. Review agent work manually at first. Retest as models change, because old guardrails can constrain a stronger model. (see [[agent-design-principles]])
- **Verification before human review.** The best long-running agents check their own work with tests, rubrics, and style guides. A "Doer-Verifier" harness gives one agent the task and a second agent the check. (see [[agent-harness]], [[agent-verification]])
- **Human attention is the scarce resource.** Agents batch questions, restate key context, and limit the items each human sees. Some teams set daily caps on agent output so that human review stays sustainable.

## Notable claims & data

- Engineers have sent agents to fix 500 bugs independently. They started with full human review of every agent decision.
- Backlog example: one set of agents scored the complexity of unowned items, and a second set coded the medium- and low-complexity items. A weekly "lessons & missteps" report helped the team expand agent scope over time.
- An agent proposed changes to onboarding error-message copy, which "measurably" raised onboarding success the next week (no number given).

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[context-engineering]], [[agent-orchestration]], [[human-agent-teams]], [[agent-skills]], [[agent-harness]], [[agent-evals]], [[guardrails]], [[agent-design-principles]]

## Connections

Series continues in [[anthropic-slack-human-agent-teams]] and [[anthropic-asana-coachable-agents]]. Applied examples: [[anthropic-ai-ci-cd-on-call]], [[anthropic-claude-tag-analytics-in-slack]], [[anthropic-monday-agent-first-platform]]. The verifier idea parallels [[anthropic-harness-for-every-task]] and [[anthropic-eng-effective-harnesses-long-running-agents]].
