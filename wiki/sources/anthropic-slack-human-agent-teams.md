---
title: "Anthropic: How Slack builds human-agent teams (Jaime DeLanghe interview)"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Anthropic (claude.com articles); interview with Jaime DeLanghe, CPO of Slack
date: 2026-08-19
source_url: https://claude.com/resources/articles/turning-conversation-into-knowledge-how-slack-builds-human-agent-teams
source_path: raw/anthropic-slack-human-agent-teams.md
tags: [case-study, human-agent-teams, slack, adoption, organizational-practice, context]
---

# Anthropic: How Slack builds human-agent teams (Jaime DeLanghe interview)

> Vendor-published interview with Slack's Chief Product Officer on running human-agent teams in shared channels: public-by-default context, handoff loops, and adoption by example.

## Summary

Anthropic published this on claude.com on 2026-08-19 as the second post in its series on human-agent teams (the first: [[anthropic-building-effective-human-agent-teams]]). It is an interview, not a technical guide. All practices and outcomes are self-reported by Slack; the post gives no metrics and names no model version. DeLanghe's thesis: the conversation around the work is the context agents need, so work should happen in channels that agents can read. Agents (Claude in Slack) do production work; humans review, decide, and hand work back.

## Key points

- **Agents see only what is visible.** Default channels to public; decisions in DMs or private threads are invisible to agents. A private channel is a blind spot for every agent that reports on it. (see [[context-engineering]])
- **Ask for the reasoning, not the record.** Use agents to reconstruct why a decision was made and how context changed since.
- **Handoff loop.** Agents draft, summarize, monitor, and prepare; a human reviews, decides, and redirects at the end of each loop. Example: an agent-built Monday briefing, workshop recap with escalations, meeting briefings. (see [[human-agent-teams]])
- **Shared channel as work queue.** Humans and agents triage in one channel; humans set priority. An emoji reaction adds an item that an agent picks up.
- **Clear agent roles.** Treat agents as coworkers with focus areas. Route routine transactional tasks (help-desk tickets, weekly metrics) to a general agent. Retire an agent whose purpose people cannot state.
- **Adoption spreads by example.** Salesforce's public "How I Slackbot" channel (thousands of members, her count); a Slack PM's "what I did and how" canvas was copied by other PMs.
- **Usage is not value.** Token usage and message counts show activity, not results; linking use to business outcomes still needs judgment.

## Entities

[[anthropic]], [[claude]]

## Concepts

[[context-engineering]], [[agent-orchestration]], [[human-agent-teams]], [[agent-design-principles]]

## Connections

Series companion: [[anthropic-building-effective-human-agent-teams]]. Claude in Slack for analytics: [[anthropic-claude-tag-analytics-in-slack]]. Organizational adoption: [[anthropic-running-ai-native-engineering-org]].
