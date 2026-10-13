# Dust enables agents to go deeper at lower cost with Claude — Anthropic (claude.com customer stories) (raw capture)

> Source: https://claude.com/customers/dust
> Publisher: Anthropic (claude.com customer stories) · Date: none on page (accessed 2026-10-12)
> Captured: 2026-10-12 via curl (condensed).

Page labels: Case study | Claude Platform, Claude Code. Industry: software. Company size: startup. Location: Europe. Main speaker: Stanislas Polu, co-founder and CTO. All figures are self-reported by Dust through Anthropic.

## Headline figures
- About $10K/day saved on model spend after prompt-caching work (18% cut in overall model spend; body says 18–19%).
- Cache reads rose from 30% to 65% of input tokens; input spend down 22%.
- Autonomous tool-calling depth rose from 4–5 to 8+ steps per agent run, "with no engineering changes".
- Execution loop redesigned to allow up to 24 tool calls per run.
- Deep Research workflows run 10+ minutes across data warehouses, web, and internal sources.
- MCP integration layer, with Dust as both MCP client and server.

Context: Dust is a multiplayer platform for human-agent collaboration; model-agnostic agents connected to company knowledge and tools, which read from and write back to the stack (CRM updates, reports, workflows) without code. Customers include Datadog, Vanta, and 1Password; 300,000+ agents deployed.

## The challenge
- Dust's premise: "AI operators" (RevOps leads, chiefs of staff, support managers), not always engineers, build the most useful agents. Agents must act reliably across company systems; Polu ties time savings to trust.

## The solution
- Model choice: customers pick the model per agent from a dropdown. Dust reports Claude stood out on instruction following, nuanced writing, and reliable tool use. As Claude improved, sources consulted per research task grew from five to fourteen.
- Platform layers: LLM picker (automatic router coming), retrieval pipeline over 100+ data sources, sub-agent delegation framework, no-code agent builder; governance via permission-aware retrieval, role-based access, audit logs. Each model gets its own prompting and context strategy under the interface.
- Tool-call limits: earlier models gave truncated or unreliable results after a few tool calls. Old defaults were three tools per run, maximum eight; the model hit the limit and truncated results. Loop redesigned for up to 24 tool calls per run.
- Deep Research agents orchestrate sub-agents for 10+ minutes per report. Longer runs raised token use.
- Prompt caching, designed with Anthropic's Applied AI team: three tiers — globally shared instructions cached for one hour; workspace context and per-user context on shorter windows.
- MCP: as client, agents reach any compatible tool through one interface; as server, Dust exposes its agents and context to other MCP-aware systems.

## The outcome
- Cache reads ~30% → 65% of input tokens; input spend −22%; total model spend −18–19%, about $10K/day.
- Average 70% weekly active usage across customer organizations.
- Internally, Claude Code is used as a coding partner, as a GitHub Action reviewing PRs, and to turn scoped tasks into review-ready PRs. One engineer built a skill that pulls company context from Dust mid-session. AI-written code went from about 30% in early 2025 to 60–90% now, depending on the engineer, in weeks.
- Polu: the engineer's role shifts to directing, reviewing, and orchestrating AI output.

Note: one quote is attributed to "Paul" rather than Polu on the page; likely a typo.
