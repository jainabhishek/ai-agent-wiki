# Agents you can coach: how Asana builds human-agent teams with Claude — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/agents-you-can-coach-how-asana-builds-human-agent-teams-with-claude
> Publisher: Anthropic (claude.com articles) · Date: 2026-09-29
> Captured: 2026-10-12 via curl (condensed).

Page labels: Category Best practices, Perspectives · Product Claude Platform · Authors Aleksandra Todorova, Kristen Swanson · Reading time 15 min. Main speaker: Arnab Bose, Chief Product Officer, Asana. No model version is named. Claims are Asana's, reported through Anthropic.

Third post in a series on human-agent teams (first: Anthropic's multiplayer lessons, "Building effective human agent teams"; second: how Slack turns workplace conversation into agent context). This one covers agents that operate on the same platform where teams work.

Background: Asana's Work Graph model maps tasks, projects, goals, and conversations as a web of relationships with owners, contributors, and dependencies. Asana chose to have agents work inside this same model rather than build a new AI-specific context structure: agents have roles, get assigned tasks, read/write messages, and appear in activity feeds, with extra safeguards on access and sharing. Asana calls its agents "AI teammates". Claude powers complex tasks.

## Think through and structure your work before agents act on it

- Claude is the default AI tool for Asana employees, connected to Google Drive, Slack, and Asana.
- Pattern: a person takes unstructured inputs (an idea, Slack thread, Zoom recording, Databricks report, Google Doc), talks them through with Claude, then puts the result into Asana projects and tasks. Agents then act on that structure using the three capabilities from the series' first post: persistent memory, own credentials, shared context.
- Practice: start with your own ideas; debate with Claude until next steps are clear; log actionable items to the Work Graph.

## Give every agent a role and the tools and access it needs

- Humans design their teams; each employee gets a list of recommended agents.
- Agents are built around roles: content writer, insights analyst, project manager, work intake specialist, campaign analyst, campaign coordinator. Each has pre-built skills (from Asana research into how customers do that work) and integrations (e.g. HubSpot, a document drive).
- Each agent has a profile page: name, purpose, who can use it, admins, instructions, skills, integrations, permissions. Access can be scoped to specific projects, documents, or apps.
- Additional safeguard: per Asana, an agent's effective access is bounded by the permissions of the person who triggers it. This lets agents read broad public content while limiting leakage of what they learned in private contexts.
- Practice: define the role (purpose, instructions, owned jobs) before creating the agent, like a new hire's first quarter; scope access (projects, documents, apps, actions); name users and admins separately — many users, a small named group of governors.

## Separate working with an agent from training it

- Shared memory: an agent retains information from previous instructions, and many users reuse it.
- Role restriction: anyone can give feedback on a task, but only admins and editors can commit feedback to permanent memory, or undo/delete it. Other users' feedback applies only to the current task.
- Example: the communications team owns voice and tone, so it administers the writing agent; the CPO can draft with it but cannot change its behavior. One or two experts per team configure skills, behavior, and memory; everyone else benefits.
- Practice: decide who trains and who works with each agent (subject-matter experts build); match editors to the team that owns the standard the agent applies; build memory as you work (ask it to remember decisions, delete stale ones).

## Keep the agent's work where everyone can see it

- When a task is assigned to an AI teammate, everyone with access sees that an agent is doing it. The agent posts its research plan and steps; others can comment and steer.
- Example: the CPO @-mentioned an agent on a briefing-document task to factor in an earlier talk track; a short request sufficed because the material was already in the Work Graph. A communications colleague saw the exchange and iterated with the agent in parallel.
- Bose's argument: a fluent individual can get good output from a one-on-one agent, but reviewers then cannot see the prompt or the back-and-forth and cannot align on disagreements. On a shared task the request, pushback, and output sit together, and reviewers can revise the instructions.
- Practice: bring agents in where the team reviews work; make agent work visibly agent work; let reviewers coach the agent.

## Three jobs Asana has handed to agents

### Answering product questions from a Slack channel
- Sellers and customer-success staff ask launch questions in a shared Slack channel. Previously the same questions repeated and experts were @-mentioned each time; a static knowledge base did not work because answers are nuanced and change.
- Now an Asana app turns each question into an Asana task; an agent picks it up. If approved guidance exists, it replies with source links. If no approved answer exists and it is a product gap, it creates a task in the product team's intake project. If the same question recurs, it creates a task for enablement to update training and docs. Topic clusters signal where enablement should focus.

### Briefing executives on at-risk renewals
- The Chief Customer Officer (Josh Abdulla) used to rely on a manual weekly at-risk renewals briefing synthesized from CSM updates across thousands of customers; it was tedious and reactive.
- The "At-Risk Renewal" AI teammate reads every at-risk renewal task (CSM updates, status notes, comments) and generates a daily digest in three buckets: positive momentum, negative momentum, recommended follow-ups. Global view first, then by region. Pushed each morning to the CCO, CRO, and every regional CS leader.
- Leaders ask follow-ups in the shared space and coach the agent to remember things, so the report improves each run. Bose's point: an individual could generate such a report alone, but a shared agent gives standardization, a shared workspace, and compounding improvement.

### Planning engineering cycles with Command
- Running automated coding loops (feedback → synthesis → coding agents → PRs) on Asana's own product bloated cycles and delayed releases. Bose: code generation is no longer the bottleneck; planning, decision-making, and refinement are.
- Engineering now runs on Command by Asana. A team space holds 10–12 engineers on one product. Agents fill the team's unplanned board with tickets from customer feedback and a Slack feedback channel. People decide what enters the cycle. Command predicts cycle completion with optimistic, balanced, and conservative estimates.
- Tickets can go to a person or a coding agent. Managers ask in chat why a release is off track and which tradeoffs would recover it. All of it is exposed via Asana's MCP server, so executives can ask Claude without opening Command.
- Closing principle from Bose: one shared context for humans and agents, a distinct identity per agent so contributions and access can be audited, and a durable record of what agents learn.
