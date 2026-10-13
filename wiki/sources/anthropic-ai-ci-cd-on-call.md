---
title: "Anthropic: Claude on call — Claude Tag as first responder for CI/CD failures"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Sachin Malhotra (Anthropic), with Michael Segner
date: 2026-08-18
source_url: https://claude.com/resources/articles/ai-ci-cd-on-call
source_path: raw/anthropic-ai-ci-cd-on-call.md
tags: [case-study, incident-response, ci-cd, claude-tag, slack, orchestration, agent-memory, skills]
---

# Anthropic: Claude on call — Claude Tag as first responder for CI/CD failures

> Anthropic's CI team describes its internal on-call agent: Claude Tag in the on-call Slack channel, with skill files, a self-appended lessons log, and orchestrator/executor subagents for triage.

## Summary

Anthropic published this internal case study on claude.com on 2026-08-18. All results are self-reported by Anthropic about its own CI team, and no model version is named. The on-call agent has four parts: memory, connections and access, schedules, and instructions. Claude Tag provides memory across the on-call Slack channel, real-time reaction to channel events, and natural-language scheduled routines. Claude Tag runs as its own service account with Datadog and Grafana access. Standing instructions are markdown skills in a GitHub repository. The post walks through detection, triage, resolution, and verification/handoff, and links a public setup kit.

## Key points

- **Deterministic alerting, mixed escalation.** Alert rules stay deterministic. Claude reads every alert against criteria in a root `oncall.md` and decides page-now or log-to-`lessons.md` (example rule: error rate > 2% for > 5 min outside a deploy window). Claude also proposes rule tuning from a new service's first days of data. (see [[guardrails]], [[workflow-patterns]])
- **Orchestrator plus executors for triage.** An orchestration agent spawns executor subagents, one per source of truth (Grafana, logs, PagerDuty, GitHub, Kubernetes, Slack), all via MCP connectors. The orchestrator merges findings into a SITREP. (see [[agent-orchestration]], [[model-context-protocol]])
- **Skills captured from a live incident.** The author built a 617-line investigation skill for one bug class by debugging turn by turn with Claude, then asking Claude to write the skill. (see [[agent-skills]])
- **Self-appended lessons log.** Claude appends each resolved incident to `lessons.md` and reads it at the start of every investigation. Recurring patterns get promoted into the skill. (see [[context-engineering]], [[agent-steering]])
- **Multiplayer triage.** Humans steer or add hypotheses in the same Slack thread while Claude investigates.
- **Gated resolution.** Most fixes arrive as PRs that the on-call reviews and merges. Progressive flag rollout runs as a separate Claude Code agent with the author's permissions.
- **Status-report taste is human work.** The `ci-weather` report format took several iterations, because readability depends on team taste.

## Notable claims & data

Self-reported: first SITREP in every recent incident that had one, typically within 15 minutes; median 14 minutes to first evidence-grounded analysis; fastest root cause in 4 minutes; setup took "hours, not days"; engineers ship 8x as much code per quarter as in 2021–2025. Quality gates are unchanged: a named human owner per PR, approval to merge, and the same CI gates.

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[agent-orchestration]], [[agent-skills]], [[context-engineering]], [[agent-steering]], [[model-context-protocol]], [[guardrails]], [[workflow-patterns]]

## Connections

Companion to [[anthropic-agentic-coding-ci-test-impact]] (agentic CI test selection) and [[anthropic-ai-native-sdlc-playbook]]. Same Claude Tag deployment pattern for data questions: [[anthropic-claude-tag-analytics-in-slack]]. Multiplayer-agent norms: [[anthropic-building-effective-human-agent-teams]]. Scheduled automations: [[anthropic-building-effective-agent-automations]], [[anthropic-getting-started-with-loops]].
