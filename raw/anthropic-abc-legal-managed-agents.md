# How ABC Legal turned every employee into a builder with Claude Managed Agents — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/how-abc-legal-turned-every-employee-into-a-builder-with-claude-managed-agents
> Publisher: Anthropic (claude.com articles) · Date: 2026-08-17
> Captured: 2026-10-12 via curl (condensed).

Customer story. Category: Best practices. Product: Claude Enterprise. Reading
time 16 min. Subject: Brandon Fuller, CTO of ABC Legal (U.S. legal document
delivery: service of process, eFiling, appearance counsel). All figures are
self-reported by ABC Legal.

## Intro
- Claude Enterprise rolled out to 1,100 employees earlier in 2026; teams began
  building automations with connectors on their own.
- Early agents ran as scheduled tasks on individual desktops. Fuller wanted
  agents that are versioned, observable, and always on, with one view of what
  exists, what it costs, and whether it ran.
- Deployed Claude Managed Agents: one deployment structure, shared workspaces,
  single audit and billing surface, cloud-hosted always-on agents.
- As of July 2026: 50+ Managed Agents in production; up to ~50% lower cost for
  the human tasks some agents cover (before heavy optimization); ~310
  employees across all departments using Claude daily.

## From enthusiasm to engineering: treating every agent like software
- Every agent defined as code. Fuller's view: an agent is structured text
  (prompt plus configuration), so it can live in a repo for review.
- Prompt, tool list, schedule, credentials, and memory live in config files in
  git. Changes only via an approved pull request, giving version history,
  review, rollback, audit trail.
- A one-week starter kit: two templates in dedicated git repos.
  - Event-driven agents (start when something happens, e.g. a new job, a court
    returns a document).
  - Scheduled agents (hourly, daily, weekly).
- Per-agent folder: JSON config, Markdown system prompt, deployment scripts,
  operational docs. Merge to main auto-deploys.
- Builder flow: clone repo, copy template, describe the agent to Claude Code,
  receive config, prompt, credential store, and memory.

## Bridging the technical divide
- The 15-person steering committee (finance, marketing, operations,
  development; none software developers) cloned the repo and built Managed
  Agents with Claude Code.
- Rationale: routing every agent through the dev team would cap company speed.
  Safe because builders fill in config and a prompt; Managed Agents supplies
  the runtime.
- Fuller had to explain what a pull request is.
- Within a week all 15 had working agents; they trained their teams. Within a
  month, ~50+ agents. Each agent has a name, an owner, one job.

## An agent for most stages of the legal document process
- AI Code Reviewer: reviews every PR across four codebases with multi-model
  analysis (security bugs, performance regressions, committed credentials).
  Engineers wait for it before merging.
- EvidenceChain Delivery Agent: pulls a database report of matching jobs,
  fetches each PDF from EvidenceChain.com with a browser built into the Managed
  Agent, delivers daily to a customer FTP server. Built in about an hour by an
  account manager with no automation experience.
- eFiling Rejection Diagnoser: triggers on a court rejection, reads job
  details, checks court rules, posts a diagnosis to Slack in about a minute
  (previously hours).
- Job-verification agent: checks each incoming job against court websites in a
  browser (case filed, hearing on the stated date), adjusts the job, flags
  jurisdictions, courts, and statute-of-limitations timeframes.
- Attorney Coverage Agent: checks attorney availability, emails them, reads
  replies on availability and pricing for a coordinator to confirm.
- Finance: AR-remittance agent parses a remittance email, builds a NetSuite
  payment-application file, posts to Slack for one-click approval, then
  imports; a daily agent gives a capitalize-or-expense verdict per engineering
  ticket.
- Marketing: Google Ads analyst posts a weekly recommendation.
- Operations: review agent "Charvis" checks completed service jobs; ~98%
  agreement with the compliance team.
- Service-Overdue-Nudger: tier-1 backlog pass; drafts tiered daily outreach
  for human approval.

## Making the agents smarter: harvest, tune, repeat
- Agents post actions and recommendations to Slack; people reply in threads and
  react with emoji. Example: "Hank", a code review agent, posts each review with
  PR name and counts to a shared channel.
- Most agents are single-task runners with no graded output. For agents that
  collect graded feedback, a three-role architecture: separate agents sharing
  one workspace, environment, and credential vault, on different schedules.
  - Initial Agent: does the work in real time; records an audit trail.
  - Harvester: hourly or daily; turns Slack thread replies and emoji reactions
    into labeled data points.
  - Tuner: weekly; proposes a prompt or config change (not model weights) as a
    draft PR. A human reviews and merges.
- "Deliveries-as-code" at Docketly (50-person sister company): ~145 delivery
  rulesets, each a YAML file in git. Four-agent loop: weekly verdict to Slack;
  Harvester labels reactions; Tuner opens a PR on the YAML; a fourth agent
  pushes the merged config to the production database, executing only
  human-approved changes. An emoji flag on a mis-routed delivery can become a
  merged routing change within the week. Review is the only manual step.

## Why Claude Managed Agents
- Criteria: versioning, observable sessions, workspace billing, model
  selection, memory primitives, MCP wiring, no infrastructure to babysit.
- Split: Anthropic owns execution loop, sessions, memory, console, models. ABC
  Legal owns prompt, tool list, trigger logic, audit trail, outcome feedback
  loop.
- Capabilities that mattered at scale:
  - Versioning: each push creates a new agent version with optimistic locking;
    easy rollback.
  - Model flexibility: Sonnet default; Haiku for high-volume, fast tasks; Opus
    when deeper reasoning justifies cost. Model swap is a one-line change.
  - MCP wiring and credential vaults: ABC Legal's own platform (100+ tools),
    Metabase, Slack (human in the loop), Atlassian.
  - Scheduled deployments: cron via Bitbucket Pipelines (repo access, secrets,
    billing already handled).
- AI spend tracked by vendor, tool, team, use case. Spend rose in spring, fell
  from July while usage grew.
- Cost stance: push spend to vertical operational agents with measurable
  return; keep horizontal chat broad but cost-controlled.
- Most agents start human-in-the-loop: recommendation stored in the job and
  shown as an accept/reject banner, or posted to Slack. Responses form a labeled
  dataset feeding the harvester-tuner loop, evals, and cross-model benchmarks.
  When an agent matches or beats humans on its task, it moves to automation
  mode and stays under the same measurement.
- Metric: efficiency ratio (value delivered vs run cost). Each agent reports
  its value per run in hours and dollars to a data warehouse. Agents follow a
  J-curve: negative early on larger models, positive after evals, cheaper
  models, and token trimming.

## Best practices for deploying a fleet of agents
- Think of everything as code (prompts, schemas, dispatch rules, notification
  templates, business config).
- Start with humans in the loop; agents earn autonomy by consistent agreement
  with human decisions.
- Use the PR as the control surface: make a decision look like a pull request.
- Invest in the feedback loop (harvester-tuner; improvement without
  retraining).
- Skip the scheduled-tasks detour: ABC Legal built scheduled tasks and local
  routines first because Managed Agents was newly in beta; Fuller now advises
  going straight to Managed Agents.
- Expect the git hurdle, not the AI hurdle: business users learning clone and
  PRs was the hard part.
- Not every task deserves an agent: judge value over cost.

## What's next
- In flight: service photo reviewer, PagerDuty triage agent, daily KPI digest,
  more Tuner loops. Looking for more "X-as-code" candidates (notification
  templates, event routing rules, dispatch logic).
