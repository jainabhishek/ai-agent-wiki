---
title: "Anthropic: How monday.com rebuilt its platform as an agent-first product"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Aleksandra Todorova (Anthropic)
date: 2026-08-20
source_url: https://claude.com/resources/articles/how-monday-com-transformed-its-platform-into-an-agent-first-product-where-humans-and-agents-collaborate
source_path: raw/anthropic-monday-agent-first-platform.md
tags: [case-study, human-agent-teams, agent-platform, managed-agents, product-strategy]
---

# Anthropic: How monday.com rebuilt its platform as an agent-first product

> Vendor-published case study of monday.com moving from bolt-on AI features to a platform where agents are assignable teammates, and five lessons from that move.

## Summary

Anthropic published this case study on claude.com on 2026-08-20. All figures are self-reported by monday.com and its customer Cooke through Anthropic, and no model version is named. monday.com first added AI features to its existing product, which culminated in an internal "AI month" in May 2025. Adoption then plateaued, and monday.com calls those features "AI dust": automations that did not change the product's core value. monday.com then rebuilt the platform around human-agent collaboration on its existing boards, permissions, and governance, and launched the rebuild in May 2026.

## Key points

- **Embed agents where work happens.** Each agent has a name, an avatar, permissions, and board presence, and people assign it work by triggers and mentions. monday.com's reason: enterprises stall when AI chat runs parallel to the real workflow. (see [[agent-design-principles]])
- **Four integration routes:** custom prompt-built monday Agents with Claude as the model; Bring Your Own Agent for [[claude-managed-agents]]; pre-built agents from Claude plugins; and a coding integration where Managed Agents run in the customer's environment and post results back to the ticket.
- **Multi-agent pipeline with one human decision.** A Strategist Agent structures the brief, a Landing Page Builder generates the page, and a Brand Reviewer checks brand and legal rules and flags issues. A human then makes one decision: publish or refine. (see [[workflow-patterns]], [[agent-orchestration]])
- **Lessons:** the mental model is harder to change than the technology; small teams with clear ownership move faster when everything shifts at once; adoption depends on trust (governance, permissions, transparency, reliability) as much as on capability; agents need grounding data and backend capacity (monday.com built monday DB for this); build on the existing product promise. (see [[guardrails]])

## Notable claims & data

Self-reported: 250,000+ customer companies; 5M+ agent interactions since the May 2026 launch (the subtitle places this two months after launch). Cooke uses Claude with monday.com across ~200 projects and 130 contracts for plans, status reports, and RAID-log risks.

## Entities

[[anthropic]], [[claude]], [[claude-managed-agents]]

## Concepts

[[agent-orchestration]], [[workflow-patterns]], [[guardrails]], [[agent-design-principles]], [[human-agent-teams]].

## Connections

Similar "agents inside the work platform" design: [[anthropic-asana-coachable-agents]]. Team norms: [[anthropic-building-effective-human-agent-teams]]. Managed Agents deployments: [[anthropic-abc-legal-managed-agents]], [[anthropic-eng-scaling-managed-agents]].
