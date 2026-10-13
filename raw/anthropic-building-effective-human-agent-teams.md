# Building effective human-agent teams — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/building-effective-human-agent-teams
> Publisher: Anthropic (claude.com articles) · Date: 2026-06-24
> Captured: 2026-10-12 via curl (condensed).

Page labels: Category Perspectives · Product Claude Tag · Reading time 16 min. Written by Kristen Swanson (Anthropic Education team), with contributions from Matt Bell, Erik Olesund, Hasnain Lakhani, Shale Craig, Nolan Caudill, Mike Schiraldi, Aleks Todorova, Molly Vorwerck. No model version is named. Based on several months of internal testing at Anthropic.

Intro: AI use has been "single-player" (one human, one agent, individual tasks) across chat, terminal, IDE, spreadsheets, decks. Tools like Claude Tag make it "multiplayer": humans and agents share a workspace and a team's goals; humans set strategy, Claude executes.

## What are multiplayer agents?

- Defined here as AI models that work with many humans at once. Like other agents they have memory and skills; unlike them they have their own credentials and live where work happens (at Anthropic, Slack).
- Required capabilities: (1) persistent memory, to remember goals and tune execution; (2) credentials not tied to humans, to operate inside predictable guardrails; (3) ongoing broad access to information, to learn how the org works and act toward team goals.
- These are the technical foundation; teams also need shared norms.

## Lesson 1: Work in public and give agents broad context

- Agents build understanding only from text the team makes searchable (Slack, code, docs, meeting notes). Private DMs, hallway talk, and restricted docs give no context. If it is not written and accessible, it does not exist for the agent.
- Anthropic uses a few clearly defined security boundaries applied to whole Slack workspaces, meeting-transcript stores, and doc libraries, instead of per-item sharing decisions. Within a boundary, context flows to every teammate, human or AI. This also removes decision fatigue about per-item sharing.
- Benefits: agents that read meeting decisions do not propose deprioritized work; agents that see other teams' specs suggest proven patterns; agents read far more than humans and surface missed work.
- Practices: choose a handful of company security boundaries and match workspace and document-sharing settings to them; default new channels to org-public and make decisions land in channels, docs, and notes; write artifacts and notes so agents can find them (agents are now a primary consumer of docs); give agents the tools and information for their job.
- Private needs remain: DM @Claude in Claude Tag, or use Claude.ai / Claude Cowork with personal MCP connectors, which keep the conversation private.

## Lesson 2: Every human and agent get a defined role with the right tools for the job

- One roster, one set of artifacts, one workspace. Agents have own credentials, skills, tool access. Roles differ (e.g. one owns data analysis, one enforces the design standard, one runs research synthesis).
- At kickoff, humans chat with agents to assign roles. An agent may spin up other agents so tasks go to agents with the right memory and access. Tool examples: BigQuery for data analysis; Playwright MCP for QA.
- Humans hold the roles only humans can hold, so human judgment covers the most important decisions. Without clear roles, people run fleets of personal AIs on the side, duplicating work and fracturing context. Example: one multiplayer agent tracks metrics once for everyone.
- Practices: an agreed task set (who does what); humans and agents in the same threads so anyone can pick up; right tools for each; written descriptions of agent roles and scopes.
- Figure: Claude agents share codebase maintenance (triaging feedback, planning, writing code, reviewing, reporting status), each on its own schedule; people set goals and review.
- An Anthropic engineering team made rosters of human and agent roles. Lessons: roles show where responsibility sits; skill files that define an agent's role make specialization easy and let others stand up the same agent type; add agents for new areas as complexity grows (e.g. a release-manager agent).

## Lesson 3: Set a north star to make agents more proactive

- The most important agents propose new projects, usually once a team with rich context and clear roles adds a north star: an ambitious goal that helps choose tasks.
- Humans always set the north star, grounded in mission and business goals, write it down, share it with agents, and choose which agents may proactively suggest workstreams (not all have the skills or trust).
- Example: an internal tools team with the north star "make product onboarding more helpful"; an agent proposed copy changes to onboarding error messages, which measurably raised onboarding success the next week.
- Practices: humans debate and document the north star; share it and name the agents allowed to propose workstreams; protect high-fidelity human calendar time for the most important work.

## Lesson 4: Build trust over time

- Grant autonomy in proportion to demonstrated reliability, then expand deliberately. Engineers have dispatched agents to fix 500 bugs independently, but did not start there.
- Like onboarding a colleague: many feedback cycles to externalize tacit knowledge; experiment with tasks to learn capability, goal phrasing, needed skill files, effective prompts. Retest as models change: prompts may need rewording, and old guardrails may constrain a smarter model.
- The best long-running agents have many ways to verify work before a human sees it: code has tests; technical docs can use rubrics and style guides. One agent doing and another checking is called the "Doer-Verifier" agent harness.
- Practices: review agent work manually at first and design verification checklists; tell the agent to use a verifier agent; build in reflection on misses; track per task type which agents have earned autonomy and expand scope after repeated success.
- Example: an engineering leader with a large backlog used one set of agents to read every item, check ownership, and score complexity of unowned items; another set filtered to medium/low complexity and wrote code changes. Humans first reviewed every agent decision and marked those needing human input; then taught agents to surface those decisions directly, keeping a human on hard tradeoffs. A weekly agent report included "lessons & missteps". Over time agents got more complex changes.
- Once independent, agents were coached to treat human attention as scarce: batch questions into one pass, restate key context, limit items per human. Some teams have an agent whose only role is to batch and escalate the most important communication; others cap agent work per day so human review stays sustainable and humans keep their skills.

## Questions to ask

- Is the information and access humans and agents need public and searchable?
- Can you write the team roster (humans and agents) and what each owns?
- Does every member have the right tools?
- Do you have rubrics or tests to verify key work products?
- Is there a clear north star?

## Moving forward

- None of these patterns are new for humans: north star, clear roles, documentation, a shared quality bar, room to learn from mistakes. Agents make skipping them costlier. Teams that apply the fundamentals most deliberately get the most from agents.
- Closing pointer: build multiplayer agents with agent teams in Claude Code or with Claude Tag.
