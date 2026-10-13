---
title: "Anthropic: How Anthropic's cybersecurity team built a threat detection platform with Claude Code (CLUE)"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com articles); subject Jackie Bow
date: 2026-05-12
source_url: https://claude.com/resources/articles/how-anthropic-uses-claude-cybersecurity
source_path: raw/anthropic-cybersecurity-triage-agents.md
tags: [case-study, security, alert-triage, multi-agent, claude-code, internal-context]
---

# Anthropic: How Anthropic's cybersecurity team built a threat detection platform with Claude Code (CLUE)

> Internal case study: Anthropic's Detection Platform Engineering team built CLUE, a Claude-based alert triage and investigation platform. The team gives the agent boundaries on tools and data and leaves the investigation strategy open.

## Summary

Anthropic published this internal case study on claude.com on 2026-05-12. Its subject is Jackie Bow, technical lead of Detection Platform Engineering. All figures are self-reported. A page footnote says the results came from Claude Sonnet and Opus models; it does not give versions. CLUE ("Claude Looks Up Evidence") is a natural-language detection-and-response interface. It connects Claude to internal systems through tool use. The team built it with Claude Code: a proof of concept in a day, and design plus implementation within a week.

## Key points

- **First-pass triage with internal context.** CLUE Triage enriches each alert from Slack, internal docs, code repos, and data warehouses before a human sees it. It assigns one of four dispositions (false positive, true positive, malicious, expected behavior) and a confidence score. Internal context is the differentiator over external security platforms. (see [[context-engineering]])
- **Orchestrator plus parallel sub-agents.** CLUE Investigate turns natural-language questions into SQL. An orchestrator sends queries to sub-agents that run in parallel, then synthesizes a summary. (see [[agent-orchestration]])
- **Boundaries, not playbooks.** The team rejected the SOAR-era instinct to define every step. Given tools and a goal, Claude took investigation paths the team would not have prescribed, and some found missed context. The rule: constrain which tools and data the agent can use, and leave the strategy open. (see [[agents-vs-workflows]])
- **Non-determinism as a feature.** The same alert may be investigated differently on different days. The team is testing parallel investigation strategies and comparing the results.
- **Transcripts as memory and audit.** The team stores every investigation transcript. The transcripts make every investigation auditable and form a knowledge base that Claude can query.
- **Accuracy is still unmeasured.** The team tracks disagreements with analysts but has no complete feedback loop yet. (see [[agent-evals]])

## Notable claims & data

- Self-reported: the false-positive share fell from about 1 in 3 alerts to 7%. Over 30 days CLUE automated ~12,000 queries and ~27,000 tool calls, an estimated 1,870 hours (234 person-days). The team claims 5–10x time savings over manual triage. An average investigation uses 25 tool calls and ~11 queries and takes 3–4 minutes. A contractor-access governance review fell from half a day to minutes.

## Connections

Same team's broader program: [[anthropic-securing-ai-native-sdlc]], [[anthropic-ciso-guide-agentic-ai]]. A Zero Trust framing of model-first alert triage: [[anthropic-zero-trust-for-ai-agents]]. Comparable production security agents: [[claude-customer-esentire]], [[anthropic-outtake-cyber-investigator]], [[anthropic-comcast-booz-allen-exploit-chains]].
