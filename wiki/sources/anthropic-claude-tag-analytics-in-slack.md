---
title: "Anthropic: Self-service data analytics in Slack with Claude Tag"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Clement Peng, Lily Zhao (Anthropic Data Science and Data Engineering)
date: 2026-08-13
source_url: https://claude.com/resources/articles/self-service-data-analytics-in-slack-how-anthropic-deploys-claude-tag-for-ad-hoc-questions
source_path: raw/anthropic-claude-tag-analytics-in-slack.md
tags: [case-study, data-analytics, claude-tag, slack, skills, permissions, observability]
---

# Anthropic: Self-service data analytics in Slack with Claude Tag

> Anthropic's data team on deploying its governed analytics agent to the whole company in Slack: live-refreshed skills, a deliberately scoped service account, and per-answer telemetry.

## Summary

Anthropic published this internal case study on claude.com on 2026-08-13. All figures are self-reported by Anthropic, and no model version is named. The post follows an earlier post that reached ~95% accuracy with a governed semantic layer, skill files, and an eval suite in Claude Code. This post covers distribution of the same agent to non-analysts through Claude Tag in Slack. The authors give five deployment lessons (distribution, permissions, freshness, and observability), three usage patterns, and an ordered setup checklist.

## Key points

- **Skills are served content.** Claude Tag's runtime mounts the data repo's `skills/` directory and re-reads it on every conversation. Data models change several times a day, and a stale skill produces confident wrong answers that a Slack user cannot sanity-check. (see [[agent-skills]], [[context-engineering]])
- **Method skills, not only a knowledge skill.** A table-map skill alone gave correct numbers without insight. The team added runbook skills for forecasting (including when to refuse on short or noisy series), cohorts, funnels, charting, and analytical writing.
- **Context outside the warehouse.** An internal knowledge index (incidents, flag flips, threads) explains why a metric moved. The authors call it the highest-leverage addition after the warehouse.
- **A shared service account is a shared read replica.** Anyone who can mention the bot inherits the bot's access, and there is no per-user row-level security. Five controls apply: (1) scope the account to governed tables only; (2) classify PII per column, with Claude flagging candidates and a human applying the label through lineage, and give the account no PII clearance; (3) document the connection and authentication path in the skill, so the agent fails cleanly; (4) treat channel membership as an access grant that the data team owns; (5) label every query with the surface, the conversation, and the user, for audit and cost tracking. (see [[agent-identity-and-access]], [[tool-design]])
- **Instrument every answer.** Log the loaded skill versions, 👍/👎 reactions and corrections, and data-quality warnings (also shown in the answer footer). The routed-through-governed-layer adoption rate was the most actionable metric, because a dip signalled skill drift or a new question class. (see [[agent-evals]])
- **Order of setup:** permissions, then distribution and a freshness check, then telemetry from day one, then the knowledge index, then analytics skills driven by real questions.

## Notable claims & data

Self-reported: ~95% accuracy (prior post); in one channel over a month, Claude Tag answered more than 75% of questions unprompted, typically within 1–2 minutes; a dashboard caching bug was fixed across dozens of dashboards in under an hour; a missing usage segment went from question to drafted PR in 90 seconds. Example conversations on the page are labelled fictional recreations.

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[agent-skills]], [[context-engineering]], [[guardrails]], [[agent-identity-and-access]], [[tool-design]], [[agent-evals]], [[human-agent-teams]].

## Connections

Prior post: [[anthropic-self-service-data-analytics]]. The same Claude Tag pattern for CI incidents: [[anthropic-ai-ci-cd-on-call]]. Team norms: [[anthropic-building-effective-human-agent-teams]]. Scheduled loops: [[anthropic-getting-started-with-loops]]. Comparable vendor data agent: [[openai-in-house-data-agent]].
