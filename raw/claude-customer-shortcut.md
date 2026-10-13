# How Shortcut uses Opus 4.6 to tackle complex spreadsheet work for enterprises — Anthropic (claude.com customer stories) (raw capture)

> Source: https://claude.com/customers/shortcut
> Publisher: Anthropic (claude.com customer stories) · Date: none on page (accessed 2026-10-12)
> Captured: 2026-10-12 via curl (HTML converted to text locally, then condensed).

Page metadata: Industry: software. Company size: small. Product: Claude Platform. Location: North America. Spokesperson: Nico Christie, co-founder, Fundamental Research Labs (leads Shortcut).

## Headline numbers (self-reported)

- 100,000+ users; scaled from a consumer app to 1,000+ companies.
- Internal benchmark 7.29 → 8.08 out of 10 after swapping to Opus 4.6 with no prompt changes.

## Company

Fundamental Research Labs, a two-year-old lab building "more human-like AI". First product Shortcut: an AI spreadsheet tool across Excel, Google Sheets, and a standalone web/desktop app.

## Results list

- Benchmark 7.29 → 8.08/10 with Opus 4.6, no prompt changes.
- Almost half a trillion tokens processed in January 2026.
- 100,000+ users at 1,000+ companies (consumers, ad agencies, hedge funds, management consultancies).
- Users report saving multiple hours a day on financial model buildouts, data extraction, formula auditing.
- Multi-agent architecture runs 10+ Claude subagents at once on multi-sheet workbooks.

## The challenge

A financial model can hold hundreds of thousands of related cells across sheets and lacks the scaffolding coding agents enjoy. Tasks: data extraction from documents, formula creation across linked cells, error detection, auditing. They built a benchmark of realistic, hard Excel problems with verifiably correct answers. At launch the best models scored 4–5.5/10; with other providers, Christie reported tasks failing roughly 70% of the time.

## Selecting Claude

- After testing providers on the benchmark, Claude is the only production model.
- Key factor: little adaptation needed. Other models required rounds of prompt engineering for model-specific behavior; swapping in Opus needed none. Christie: very little Claude-specific prompting.
- Opus 4.6 (released February) moved the score 7.29 → 8.08. Christie: hard tasks became doable, medium easy, easy saturated.

## Multi-agent architecture

- Auditing a complex workbook spawns multiple Claude subagents to explore sheets in parallel, like Claude Code; a ten-sheet model might use 6–10 agents, each checking one tab for errors, structural issues, and missing data, reporting findings to a main agent.
- Before changes, a planning mode: Claude reviews the workbook, identifies issues, asks clarifying questions. After the plan is approved, execution goes to a fresh Claude agent to keep execution context clean.

## Looking ahead

Each model upgrade brought gains without engineering work; roadmap tracks Claude's capability. Christie cites about a billion Excel users and two billion spreadsheet users as the target market.
