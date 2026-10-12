# Codex as a platform: build on the open agent harness — OpenAI (Developers blog) (raw capture)

> Source: https://developers.openai.com/blog/codex-as-a-platform
> Publisher: OpenAI (Developers blog) · Date: 2026-08-19 (page byline "Aug 19, 2026"; category tag "Codex")
> Authors: Nicolas Bonamy, Derrick Choi
> Subtitle: build Codex into the products and workflows users already know.
> Captured: 2026-10-12 via curl of the .md endpoint plus the HTML page for the byline (condensed and paraphrased).
> Date note: an earlier reading reported "2026-07-07" as page metadata. In the fetched HTML that string occurs only inside a linked URL (a GitHub changelog post slug, `2026-07-07-codex-as-agent-provider-...`). It is not the publication date. The byline date 2026-08-19 is used.

## (Intro)

- Most people know Codex via the App, CLI, or IDE Extension; these are a few of the ways to use one underlying system.
- The open-source Codex harness (github.com/openai/codex) powers all of them. It helps models gather context, reason, use tools, stay inside configured boundaries, request approval, and carry work forward.
- Instead of moving every team's work into a general coding assistant, bring the agent into purpose-built software: engineering workflows, ops dashboards, security investigations, support consoles, team-specific internal apps.

## The reusable part is the agent loop

- An agent needs more than prompt + model response: understand the task, keep context over time, inspect information, call tools, show progress, handle failures, request human approval, return a result. That surrounding execution system is the harness.
- Evidence that harness design matters: on ARC-AGI-3, retained reasoning plus context compaction raised GPT-5.6 Sol's score from **13.3% to 38.3%** and cut output tokens **sixfold**.
- The Codex harness manages conversation state, streams execution, uses tools, enforces configured sandbox and approval policies, carries work across turns.
- **Codex app-server** exposes these through a documented client protocol: create threads, start turns, receive events, handle approval requests.
- Recommendation: start with Codex rather than inventing a new runtime, then decide what the surrounding app owns.

## An open harness developers can inspect and adapt

- Open source lets you inspect the layer between app and model and adapt the integration.
- What developers control: (1) the interface — keep existing dashboards, editors, queues, maps, records, approval flows instead of a generic chat window; (2) context and tools — expose the systems/data/actions for the workflow, including application-owned MCP services; (3) operational boundaries — the host app decides where the agent runs, which files/tools it can access, which actions need approval, how work is observed, how results return to the system of record.
- Open-source components: Codex CLI, app-server, official Codex SDK (listed in an open-source components guide).
- The open-source layer is the harness and integration surface; model access and managed services stay separate.

## Choose the right integration layer

- Script, CI job, one-off background task → `codex exec` (non-interactive mode): bounded workflow, structured output.
- App code that starts, resumes, or streams Codex tasks → official Codex SDK.
- Agent as part of the product → Codex app-server: connect to a local Codex process, keep conversations open, stream events, interrupt work, expose tools, respond to approval requests. SDK simplifies common flows; app-server gives direct control of lifecycle and UX.

## Build software around the workflow

- The opportunity is not re-skinning the Codex app but building software that matches how a team works. Examples: security analyst (investigation queue, alerts, affected services, approval before opening a remediation ticket); support engineer (account history, logs, internal docs, draft reply); product team (moving an issue to "ready" on a board kicks off a scoped implementation).
- The interface tells the agent what the user is looking at, supplies tools, and gives the user a review surface.
- Figure 1: the application owns product context, business rules, consent, and tools (MCP); app-server provides the agent loop and sandboxed execution.

## Example: Relay

- Relay: OpenAI's sample ops app on Codex app-server. Agent sits beside a fictional shipment dashboard, uses application-owned MCP tools, and requires human approval before a shipment is rebooked.
- The user does not write a prompt: they select a shipment and click an action such as **Compare recovery**. The app supplies context; Codex fetches current sample data; the agent explains options; consequential writes need approval.
- After a tool changes a record, the app refreshes its business view. Harness handles loop, state, streamed activity, tool interaction; the product keeps its dashboard, records, controls.
- Uses fictional seeded data; pattern generalizes to incident response, account operations, research workflows.

## What developers are building

- GitHub and JetBrains: Codex inside existing IDE workflows (linked GitHub changelog dated 2026-07-07).
- Cisco: Codex SDK in App Builder inside Cisco Cloud Control.
- Thrive Holdings and Crete: Codex in a tax-preparation workflow using practitioner feedback; pilot processed **7,000 returns** and cut preparation time by **about a third**.
- Pattern applies beyond engineering: support, operations, security triage, sales research, marketing. The app provides context, tools, approvals; Codex provides the agent loop.

## Build beyond the obvious

- Essential context often lives in a dashboard, timeline, map, document, or system record; these views are how people understand work and stay in control.
- Goal: make those interfaces more capable with an agent that investigates, proposes a next step, and takes an approved action — not replace them with a universal chat box.
- Starting point: the open-source Codex repo, then `codex exec` (non-interactive jobs), Codex SDK (programmatic workflows), or app-server (persistent conversations, streamed events, approval handling).
