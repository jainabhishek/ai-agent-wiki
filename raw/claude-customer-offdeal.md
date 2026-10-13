# OffDeal powers every stage of M&A advisory with one Claude-based agent — Anthropic (claude.com customer stories) (raw capture)

> Source: https://claude.com/customers/offdeal
> Publisher: Anthropic (claude.com customer stories) · Date: none on page (accessed 2026-10-12)
> Captured: 2026-10-12 via curl (HTML converted to text locally, then condensed).

Page metadata: Industry: financial services. Company size: small. Product: Claude Agent SDK, Claude Platform. Location: North America. Spokesperson: Ori Eldarov, CEO and founder.

## Headline numbers (self-reported)

- Internal eval accuracy 25% → 85% after migrating to the Claude Agent SDK and refining MCP design and prompting.
- 5–8 concurrent deals per banker, with AI working across every deal phase.

## Company

AI-native investment bank pairing bankers with engineers; sells founder-led businesses with $1–20M annual profit (largest segment by deal count, historically underserved). Eldarov: 5 engineers and 4 bankers.

## Results list

- Eval accuracy 25% → 85%.
- Failed API calls from context overflow dropped to zero overnight.
- 12+ independent agentic workflows consolidated into one general-purpose agent, "Archie".
- 5–8 concurrent deals per banker.
- Buyer-sourcing agent runs autonomously up to 4 hours across 10 sourcing methods.
- Each banker meets 2–3 new potential clients a day.
- First year: 8 deals, $91M transaction value, with two bankers.

## The challenge — context, not intelligence

- Before: one dedicated agentic workflow per workstream (seller lists, buyer lists, confidential investment memorandums, etc.). Each call was smart, but predefined solution paths failed on problems outside the instructions, and every SOP change broke a workflow.
- One deal can involve 100M+ tokens of relevant data (buyer profiles, past transactions, financials, market data). They had packed full context into a long-context model from another provider (preferring this over RAG for accuracy) until calls failed at the 1M-token limit.

## The solution — Claude Agent SDK for subagent orchestration

- They had explored custom compaction, auto-summarization, and structured note-taking. An early Agent SDK post led them to see deal research as like traversing a large codebase.
- The SDK's built-in context management (subagent orchestration, automatic compaction) let them stop building workarounds.
- Since December, nearly all AI workloads run in Archie, connected to 20+ data sources.
- Capabilities are modular "skills" Archie combines, instead of hardcoded workflows.
- Buyer sourcing: find 300–400 acquirers among millions of companies and tens of thousands of PE firms. Experienced bankers use about 10 approaches (past deal activity, website mandates, portfolio investments, etc.) and cross-feed them. Encoded as a buyer-sourcing skill; a long-running agent works up to 4 hours, cross-references, and recursively refines. Traditional cost: analyst team, more than a week, $12,000+. Agent: about $200 compute. Eldarov says it finds buyers a human team would be unlikely to find.
- Non-engineers author skills: a banker built a branded-presentation skill (fonts, margins, indentation, 20 slide templates) with no engineering. Hundreds of decks since; about 1 hour per deck versus 30–40 hours traditionally.

## The outcome

- Context overflow failures went to zero.
- Eval: switching to the SDK alone moved the score 25% → 60% ("a few lines of code"); MCP design and prompting later reached 85%. The eval scores Archie on complex multi-part M&A queries over real production data (10M to 100M+ tokens of deal context), graded against actual deal outcomes and human-verified data; the score is a composite of qualitative and quantitative rubrics, not pass/fail.
- 5–8 concurrent deals and 2–3 new client meetings per banker per day. First year: 8 deals, $91M, team of two; a deal typically takes 9–12 months. In 2026, average deal size rose from $11M to over $20M.
- Prototypes built in Claude Code reach production almost overnight because both run on the same SDK.
- Plans: buy-side advisory, capital raises, debt origination.
