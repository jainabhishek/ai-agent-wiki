# How monday.com transformed its platform into an agent-first product where humans and agents collaborate — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/how-monday-com-transformed-its-platform-into-an-agent-first-product-where-humans-and-agents-collaborate
> Publisher: Anthropic (claude.com articles) · Date: 2026-08-20
> Captured: 2026-10-12 via curl (condensed).

Page labels: Category Best practices · Product Claude Enterprise · Author Aleksandra Todorova · Reading time 10 min. Speakers: Daniel Lereya (chief product and technology officer, monday.com), Orly Stern Izhaki (VP of Product, AI Works Platform, monday.com), Patti Stevens (director of strategy, Cooke). No model version is named. All figures are self-reported by monday.com and its customer through Anthropic.

Intro: monday.com serves 250,000+ companies. After hitting a ceiling with add-on AI features, it rebuilt the platform around Claude as a human-agent collaboration product. Subtitle: two months and five million agent interactions after launch, five lessons.

## Hitting the "AI dust" ceiling

- Phase one: embed AI into the original platform, culminating in an internal "AI month" in May 2025 (four weeks of shipping AI features company-wide).
- Adoption was strong but plateaued. Izhaki calls it "AI dust": automations sprinkled on existing workflows (summarize text, categorize information) that did not change the value proposition or create sustained usage.
- Shift from adding AI features to building AI natively; Izhaki: adopting AI features differs from becoming an AI company.
- Reframe: from a work-management tool to a place where people and agents work together. The mandate came from the top; each team translated it into product choices and built its own agents.
- Result: the product rebuilt around humans and agents using existing context, workflows, boards, permissions, and governance. Since the May 2026 launch, customers had 5M+ agent interactions on the platform.

## Agents as teammates

- Each agent gets access permissions and restrictions, a name, and an avatar; colleagues assign it work via triggers and mentions.
- Rationale: enterprises often stall at an AI chat running parallel to where work happens; embedding agents in workflows and treating them like colleagues made agentic AI concrete.
- Mapped jobs (table, four workflows):
  - IT, ticket to resolution: Intake & Triage Agent (classify, auto-resolve common requests, escalate with context); Knowledge Agent (detect KB gaps, draft articles); Incident Agent (detect incidents, open war rooms, trigger post-mortems).
  - HR, job post to hire: Resume Screener (score, surface top candidates, send rejections); Interview Scheduler; Hiring Coordinator (keeps stakeholders updated so a human stays in the loop); Feedback Manager (collect structured interviewer feedback).
  - Marketing, competitive intelligence: Competitive Intelligence Agent (monitor, categorize signals, alerts, weekly briefings); Battlecard Agent (update battlecards on approved signals, notify sales).
  - Executive office, chief of staff as a service: Operator Agent (meetings, briefings, decisions → tracked tasks, priorities); Org Health Agent (revenue risks, cost leaks, failing initiatives); Strategy Consultant Agent (growth opportunities, action plans).

## Four ways to run Claude in monday

1. monday Agents: build custom agents with prompts and choose Claude as the model; the agent gets a name, face, and board presence for assignment.
2. Bring Your Own Agent (BYOA): Claude Managed Agents join the platform; an agent one person built becomes a teammate the team can mention and assign.
3. Pre-built Agents in the monday Agents Store: Claude plugins turned into specialized teammates (e.g. legal or finance plugins run as agents in team workflows).
4. Claude Coding integration: connect Claude in the monday dashboard, plan and assign agent tasks; Claude Managed Agents executes in the customer's own environment; results land back on the ticket before handoff to the next agent or a human reviewer.

## From brief to landing page without leaving the board

- Marketer and content lead shape a brief on one board item (goal, audience, key message, channels).
- A Strategist Agent (monday Agents) turns it into a structured brief: objective, messaging pillars, channel breakdown, success metrics.
- A Landing Page Builder (Claude Managed Agents, customer environment) generates a variant of an existing landing page; output lands back on the item.
- A Brand Reviewer (Claude Managed Agent) checks brand guidelines and legal standards and flags items for humans.
- The marketing manager makes one decision: publish or refine.

## A family business at the AI frontier

- Cooke (family seafood company, founded 1985, Blacks Harbour, New Brunswick; 16 countries) runs project delivery, resource management, and contract management on Claude and monday.
- PMs use Claude to turn approved charters into initial project plans, generate status reports, and surface risks/issues into monday RAID logs across ~200 active and proposed projects. Claude automates reporting and data prep for lifecycle workflows across 130 contracts.

## What monday.com learned

1. The mental model is harder to change than the technology: moving from improving the current product responsibly to rebuilding it for a different future took longer than the technical work.
2. Small teams move faster when everything changes at once (direction, UX, tech, pricing, trust model, definition of good); small teams with clear ownership and fast decision rights kept the detail that stakeholder layers lose.
3. Adoption depends on trust as much as capability: governance, permissions, transparency, and reliability decide whether agents leave pilots.
4. Capability needs matching infrastructure: agents do better grounded in live project data, team history, and structured workflows; monday invested in monday DB so the backend handles agent volume, speed, and complexity.
5. Build on what already works: the rebuild extends the existing promise (people team up for outcomes) to a new kind of team member.
