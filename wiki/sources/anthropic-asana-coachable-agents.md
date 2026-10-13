---
title: "Anthropic: Agents you can coach — how Asana builds human-agent teams with Claude"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Aleksandra Todorova, Kristen Swanson (Anthropic)
date: 2026-09-29
source_url: https://claude.com/resources/articles/agents-you-can-coach-how-asana-builds-human-agent-teams-with-claude
source_path: raw/anthropic-asana-coachable-agents.md
tags: [case-study, human-agent-teams, agent-memory, permissions, governance, mcp]
---

# Anthropic: Agents you can coach — how Asana builds human-agent teams with Claude

> Vendor-published interview with Asana's CPO on running "AI teammates" inside Asana's Work Graph: scoped roles, access bounded by the person who triggers the agent, and memory that only named editors can change.

## Summary

Anthropic published this case study on claude.com on 2026-09-29. It is the third post in Anthropic's human-agent-teams series. The claims are Asana's own (CPO Arnab Bose), reported through Anthropic, and no model version is named. Asana chose to put agents inside its existing Work Graph model instead of building a separate context structure for AI. In that model, agents have roles, receive task assignments, post messages, and appear in activity feeds. The post gives four practices and three internal deployments.

## Key points

- **Structure before agents act.** People talk unstructured inputs through with Claude, then log actionable items as projects and tasks that agents can pick up. (see [[context-engineering]])
- **Role-first agent design.** The team defines the purpose, instructions, and owned jobs before it builds an agent. Each agent has a profile page that lists its users, admins, skills, integrations, and permissions. (see [[agent-instructions]])
- **Access bounded by the triggering user.** Per Asana, an agent's effective access never exceeds the permissions of the person who invokes it. This limits leakage of what the agent learned in private contexts. (see [[guardrails]])
- **Use is separate from training.** Anyone can give task-level feedback. Only admins and editors can commit feedback to the agent's shared permanent memory, or delete it. The team that owns the standard, for example brand voice, administers the agent.
- **Agent work is visible.** The agent posts its plan and steps on the shared task, so reviewers can coach the agent and revise the instructions, not only the output.
- **Planning is the new bottleneck.** Automated feedback-to-PR coding loops bloated Asana's cycles. In Command, agents fill an unplanned board and people decide what enters a cycle. Command exposes this data through Asana's MCP server. (see [[model-context-protocol]])

## Notable claims & data

Self-reported, no metrics. Deployments: (1) a Slack product-question channel where each question becomes a task, and the agent answers from approved guidance, files a product-gap task, or flags recurring questions to enablement; (2) a daily at-risk-renewal digest in three buckets (positive momentum, negative momentum, recommended follow-ups), pushed to the CCO, the CRO, and regional leaders; (3) Command team spaces of 10–12 engineers with optimistic, balanced, and conservative completion estimates.

## Entities

[[anthropic]], [[claude]]

## Concepts

[[guardrails]], [[context-engineering]], [[agent-instructions]], [[model-context-protocol]]

## Connections

Series: [[anthropic-building-effective-human-agent-teams]] (part 1) and [[anthropic-slack-human-agent-teams]] (part 2). Agent identity and access: [[anthropic-agent-identity-access-model]]. Similar platform rebuild: [[anthropic-monday-agent-first-platform]].
