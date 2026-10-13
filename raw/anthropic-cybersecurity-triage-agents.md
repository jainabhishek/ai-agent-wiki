# How Anthropic's cybersecurity team built a threat detection platform with Claude Code — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/how-anthropic-uses-claude-cybersecurity
> Publisher: Anthropic (claude.com articles) · Date: 2026-05-12
> Captured: 2026-10-12 via curl (condensed).

Category: Best practices, Perspectives. Product: Claude Code. Reading time 12 min. Subject: Jackie Bow, technical lead, Detection Platform Engineering, Anthropic. Internal case study published by Anthropic; figures are self-reported. Page footnote: results were generated with Claude Sonnet and Opus models. Condensed paraphrase.

## Context

- Detection Platform Engineering does defensive security: detect threats, respond to possible breaches, monitor for suspicious activity, triage alerts, investigate anomalies.
- Anthropic's Responsible Scaling Policy ties releases to security commitments, so this team helps decide what the company can ship.
- Bow's long-held goal: tools that use the context that matters (Slack conversations, internal docs, institutional knowledge), not just logs and alerts.

## The problem: Drowning in data and alerts

- An analyst jumps between five or six tools, each with its own query language and mental model. Simple investigations take hours; complex ones take days.
- Analysts' attention drops after many alerts per day.
- Team asked: what drains energy, what is repetitive, what blocks impactful work? Answers: alert triage eating hours, manual correlation across disconnected systems, constant context switching.
- Bow: the team cannot scale with the company without something like Claude.

## The solution: Claude Looks Up Evidence (CLUE)

- CLUE is a detection-and-response platform with a natural-language interface on Claude, connected to internal systems via tool use — not another dashboard.
- Built with Claude Code over several months alongside normal work: proof of concept in a day; design docs, development steps, and implementation within a week. Claude Code acted as design partner.
- Turning point: asking Claude Code to add a UI button; it implemented it at once, better than Bow would have.

### CLUE Triage

- First-pass triage before a human sees an alert. Claude uses tools to enrich each alert with context from Slack, internal docs, code repositories, and data warehouses.
- Assigns a disposition: false positive, true positive, malicious, or expected behavior; plus a confidence score per alert so analysts know where to focus.
- Rationale: alerts arrive as isolated signals (failed login, unusual API call, config change); internal context (who the user is, what they were doing, team patterns) turns them into signal.

### CLUE Investigate

- Analysts query all security-critical logs in natural language (e.g., failed logins for a system over the past day); Claude writes and runs the SQL. Bow: Claude writes more precise queries than humans.
- Agentic loop: an orchestrator issues commands to sub-agents that run queries in parallel, gather findings, and synthesize an investigation summary. Hours of manual correlation become 3–4 minutes.
- Averages per investigation: 25 tool calls and nearly 11 queries.
- Differentiator is internal context: check Slack for planned maintenance, query the warehouse for baseline behavior, read repos to learn what a service does.

### Data governance review

- Demo: did three contractors access documents they should not have over two months? Normally at least half a day (access logs, permissions cross-reference, document classifications). With CLUE: Claude plans, writes verbose queries, and finishes in minutes with a summary, recommendations, and every query visible.

## Measuring the impact

- **Fewer false positives:** before CLUE Triage about 1 in 3 alerts were false positives; now 7%.
- **Broader coverage:** lower-confidence signals used to go unexamined; now every incoming alert is enriched, and batch processing handles thousands of signals.
- **Time savings:** over 30 days, about 12,000 queries and 27,000 tool calls automated — an estimated 1,870 hours (234 person-days) of manual work; 5–10x time savings vs manual triage.
- **Still learning to measure accuracy:** the team reviews dispositions and tracks disagreements but is still building feedback loops to learn how often Claude catches what analysts miss and vice versa. Every investigation transcript is auditable.

## Where we're headed: letting Claude investigate like Claude

- "Bitter lesson" framing: encoding human-specific reasoning underperforms giving models general capability and letting them find their own approach.
- Early debate on how much to constrain investigation paths. SOAR-era instinct: playbooks, every step defined, deterministic. Observation: given tools and a goal rather than a fixed sequence, Claude often took paths the team would not have prescribed, sometimes surfacing missed context.
- Principle: set boundaries (which tools, which data) and leave the strategy open.
- Next steps:
  - **Reactive to proactive:** continuous hunting for patterns that match no written rule, or behaviors normal individually but unusual in aggregate.
  - **Learning from itself:** every investigation transcript is stored; the corpus becomes a knowledge base Claude can query for how past investigations unfolded (organizational memory).
  - **Embracing non-determinism:** the same alert may be investigated differently on different days; a second path may find what the first missed. Experimenting with running several investigation strategies in parallel and comparing results.
- Bow: past tools encoded how humans investigate; next-generation tools should let models find better approaches.
