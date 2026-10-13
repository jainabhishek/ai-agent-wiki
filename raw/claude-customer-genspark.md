# Genspark's Super Agent orchestrates 150+ tools with Claude — Anthropic (claude.com customer stories) (raw capture)

> Source: https://claude.com/customers/genspark
> Publisher: Anthropic (claude.com customer stories) · Date: none on page (accessed 2026-10-12)
> Captured: 2026-10-12 via curl (condensed).

Page labels: Case study | Claude Platform. Industry: software. Company size: startup. Location: North America. Speaker: Kay Zhu, co-founder and CTO. All figures are self-reported by Genspark through Anthropic.

## Headline figures
- $250M ARR since pivoting to the Super Agent in early 2025. (The outcome section says "past $200 million in annualized revenue"; the page gives both numbers.)
- 150+ specialized tools orchestrated by Claude inside one agent.
- AI slides, spreadsheets, and documents produced through Claude-generated code.
- 100% of internal code written by AI.

Context: Genspark is an AI workspace where one prompt yields slides, spreadsheets, documents, posters, or websites for non-technical knowledge workers.

## The challenge: a rigid workflow
- Launched mid-2024 as AI search; expanded to parallel search and asynchronous deep research emailed after several minutes. Zhu: search must answer in 1–10 seconds, too short for meaningful work.
- Example: a user spent a week comparing credit cards with a search engine; the async agent reached the same conclusion in 15 minutes.
- Architecture was a directed graph of predefined workflow nodes: too rigid, broke on edge cases. Easy queries passed through more nodes than needed, while difficult queries got stuck at points the graph had no path around. Zhu notes search satisfaction has stayed near 80% for a decade because users ask harder questions as systems improve.

## The solution: an agent loop
- Zhu tested a ReAct-style loop (model picks each next step) against each new frontier model, roughly every three months, for two years. Repeated failures: infinite loops, repeating the same error, not recognizing when it had enough to stop.
- Early 2025, with Claude Sonnet 3.7: the model knew when to stop, which tools to call, and tried alternatives after a tool error. Error recovery was the missing piece; the product was rewritten around it.
- Super Agent is model-agnostic; different frontier models do different jobs. Claude's two roles: (1) the agent loop — per step choose among 150+ tools, gather more, backtrack, or summarize and return; for the hardest planning, Genspark fans out to several frontier models in parallel and uses Claude to reconcile their plans; (2) code generation behind slides, spreadsheets, and documents.
- Zhu's analogy: old system ran on rails (fast until derailed); the agent is a driver with GPS and a goal that routes around obstacles.
- Zhu: no moat except execution speed. About 50 engineers produce all code via AI tools; some built a "lights-out factory" automating issue creation, PR composition, code review, merging, testing. Zhu writes code in Claude Code plan mode.

## The outcome
- Growth past $200M annualized revenue; AI Workspace major versions on a ~2-month cadence (3.0 latest, 4.0 planned).
- Unplanned uses: a New York real-estate analyst builds investor decks in hours instead of weeks; Japanese seafood CEOs analyze demand and source leads; one user had the agent write his resignation.
- Zhu's 2026 expectations: effectively infinite context via scaffolding; agents running hours or days; orchestration models driving fleets of parallel sub-agents. Internal experiments on each.
- Billboard on US-101: a three-day work week. Goal: bring the Claude Code experience to all white-collar workers.
