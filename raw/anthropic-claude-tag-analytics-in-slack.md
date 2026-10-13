# Self-service data analytics in Slack: how Anthropic deploys Claude Tag for ad-hoc questions — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/self-service-data-analytics-in-slack-how-anthropic-deploys-claude-tag-for-ad-hoc-questions
> Publisher: Anthropic (claude.com articles) · Date: 2026-08-13
> Captured: 2026-10-12 via curl (condensed).

Page labels: Category Best practices · Product Claude Tag · Authors Clement Peng, Lily Zhao (Anthropic Data Science and Data Engineering), contributions from Josh Cherry and Michael Segner · Reading time 2 min (as labelled). No model version is named. Figures are self-reported by Anthropic about internal use. Example conversations on the page are labelled fictional recreations.

Context: a previous post described ~95% accuracy on data-analytics questions via (1) a governed semantic layer, (2) skill files encoding analytical conventions, (3) an evaluation suite — focused on Claude Code for data scientists. This post covers deploying that foundation to the rest of the company via Claude Tag (public beta) as a Slack data-analytics agent anyone can ask, backed by the same governed definitions.

## Best practices for deploying a data analytics agent in Slack

Accuracy and deployment to non-analysts are different problems. Five learnings, on distribution, permissions, freshness, and observability.

### Refresh skills as often as you refresh your data models
- A skill is a markdown file of natural-language instructions plus files Claude can reference.
- Key architectural decision: treat skill files as served content, refreshed continuously, not shipped once.
- Data models change several times a day (renamed column, corrected metric, deprecated table). A stale skill gives a confidently wrong answer. In Slack the asker lacks surrounding context (no dashboard, trend lines) to sanity-check a single number, so they tend to accept it.
- Implementation: Claude Tag's runtime mounts the data repo's `skills/` directory and re-reads it on every conversation; skills are plain markdown on disk.

### Give the agent skills beyond knowing what to query
- First attempt: a single "knowledge skill" (which tables, how the semantic layer is organized). Gave correct numbers but not useful insight.
- Askers pose open-ended questions ("what's driving this dip?", month-end forecast, "show as a funnel"), which need analyst method, not just data location.
- Added analytics/runbook skills: Forecasting (when/how to fit a simple trend, seasonality assumptions, when to refuse because the series is too short or noisy); Cohort and retention (standard definitions, leadership retention-curve template, gotchas like left-censoring and survivorship); Funnel analysis (canonical stage definitions); Charting (chart type per question, palettes, table vs plot); Analytical writing (TL;DR first, number, mechanism, caveat; hedging matched to confidence).
- These conventions usually live in someone's head; writing them as skills makes Claude apply them consistently.

### Connect to business context, not just the warehouse
- "Why did sign-ups drop on Tuesday?" is often answered by Slack threads, incident trackers, release notes, docs — not the data model.
- Claude Tag is wired to an internal knowledge index cataloguing documents, discussions, and events. On a metric move, it searches for contemporaneous context (incident, flag flip, competitor news).
- Example answer shape: sign-ups fell 12% Tuesday; a payment-service incident was open 9–11am; the dip concentrates in the affected region.
- After the warehouse, a knowledge graph / internal search / incident and changelog feeds is called the highest-leverage addition. Claude Tag can also read key Slack channels.

### Permission the service account deliberately
- Claude Tag queries the warehouse as a service account, not as the asking human. Right design (no per-user warehouse credentials), but anyone who can mention the bot has the bot's data access; no per-user row-level security.
- Five measures (described as easy to get wrong, hard to undo):
  1. Scope the service account to governed data only: semantic-layer output tables and curated marts; no raw event streams, staging schemas, or personal sandboxes. Out-of-boundary questions get an explicit "can't" rather than a guess.
  2. Classify PII at column level and deny the service account clearance. A data catalog with column-level lineage; Claude scans new columns and flags likely PII for human review; a human applies the classification in metadata; lineage propagates labels downstream. With no PII clearance, warehouse column-level controls make those columns unreadable to the agent.
  3. Document the connection path in the skill: how the agent connects (CLI, direct API, or MCP server) and how auth works for each. Lets the agent fail cleanly and explain its constraints instead of silently querying the wrong project or relaying an auth prompt.
  4. Treat Claude's channel membership as an access grant: adding Claude Tag to a channel grants its members read access to what the agent can query. A data-team member adds Claude; the data team owns the channel list.
  5. Label every query with surface, conversation, and requesting user (where Slack provides it). Not enforcement — cost attribution and audit (e.g. who triggered a 4 TB scan).
- Posture: the authors treat the Slack agent as a read-only copy of the governed warehouse that everyone in the channel shares, and they scope its access on that basis.

### Instrument every answer
- Correctness cannot be eyeballed. One structured event per question: which skill files loaded and their version; 👍/👎 reaction or correction reply; open data-quality warnings on touched tables (also shown in the answer footer).
- Two views: adoption (share of agent queries routed through the governed layer vs ad hoc SQL, by surface and domain) and correctness (👎 and correction rate by domain) — the online accuracy proxy between eval runs.
- Adoption was the most actionable metric: a dip for a domain almost always meant skill drift or a new question class the semantic layer does not cover.

## How this accelerates self-service analytics adoption

### Claude Tag threads become the new meeting
- Best threads have several people adding context while Claude does legwork. Example: slow revenue dashboard → Claude finds query results not cached plus a bug in result delivery → owner fixes cache, splits bug off → dozens of dashboards affected → Claude writes the caching fix, a data-team member reviews, all fixed in under an hour.
- Open threads let readers learn without a written summary and let anyone contribute. Keep the agent in shared channels and work in threads, not DMs, as a reviewable record.

### Claude Tag handles repetitive tasks
- Ask Claude to create loops on a schedule or on anomalies. Examples: Proactive readouts before weekly standup; Test monitoring several times a day during launches/experiments (caught settings changed mid-experiment); Observability (pipeline failure → investigate, draft fix, ping on-call; unexpected KPI move → check explanations like holiday effects or upstream changes); Triage of a data-questions channel (answer, investigate deeper, or bring in a human).
- Claude can propose loops: ask it what repetitive jobs it has seen in your channels.

### Stepping in when needed
- Claude can be made proactive in chosen channels. In one data channel over a month, Claude Tag answered more than 75% of posted questions, typically within a minute or two, without being called.
- Example: in 90 seconds Claude explained a dashboard's data definition, confirmed a new usage segment was missing, proposed a fix, and drafted a PR; a data scientist approved; Claude merged and refreshed the dashboard.

## Getting started

Order matters:
1. Permissions first: decide service-account reads before writing agent code; widening later is easier than clawing back.
2. Distribution second: choose mounted repo or skills-over-MCP; verify freshness end to end (change a skill, confirm pickup within your SLA).
3. Telemetry from day one; old conversations cannot be instrumented retroactively.
4. Knowledge index when the data path is stable (warehouse answers what; docs and incident feeds answer why).
5. Analytics skills last: build the data-access skill first, then let real questions show which analyst skills are needed.
