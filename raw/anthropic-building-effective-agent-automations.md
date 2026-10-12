# Building effective agent automations — Anthropic (claude.dev blog) (raw capture)

> Source: https://claude.dev/blog/building-effective-agent-automations/
> Publisher: Anthropic (claude.dev blog) · Date: 2026-10-08
> Authors: Lance Martin and CJ Avilla. Category: Agents. Subtitle: a reference
> implementation walkthrough with common failure modes.
> Captured: 2026-10-12 via curl + local HTML-to-text (condensed, paraphrased).

## Intro

Anthropic uses simple scheduled agent automations internally: they run on a
schedule, gather context in the background, and proactively report what matters.
Two named failure modes: an automation silently loses access to a source, or it
does not follow the user's preferences. The post walks through a reference
implementation on Claude Managed Agents (beta) that reads custom sources (Slack,
GitHub repos) on a schedule, tracks what changed since the last run, and posts a
brief (to Slack).

## Get the code

- Interactive setup in Claude Code: `/claude-api managed-agents-onboard <post URL>`
  (the `claude-api` skill configures the agent following the post).
- Prerequisites: a Slack app (created from a manifest) and a GitHub token.
- Files in `daily-brief/`:
  - `agent.md` — model, tools, instructions
  - `deployment.md` — schedule, time zone, budget, input message
  - `environment.yaml` — network allowlist
  - `memory_store_preferences.yaml` — user preferences
  - `memory_store_state.yaml` — agent's bookmarks, ledger, notes, run records
  - `vault.yaml` — vault holding credentials
  - `claude-lock.json` — resource IDs written by `ant apply`
  - `slack/manifest.yaml` — one bot app
- `ant apply` (ant CLI) reads the files, creates resources in the Claude API
  workspace, and records IDs in `claude-lock.json`. Once configured, runs execute
  on Anthropic infrastructure; nothing stays running locally.

## Overview — six components

1. Sources — named list of places to read.
2. Destination — exactly one place the agent may write.
3. Agent — model, tools, run steps (`agent.md`).
4. Schedule — cron.
5. Memory — user preferences plus the agent's own memory.
6. Guardrails — read-only access wherever the agent only reads; a spending cap per run.

## Sources

Default sources: Slack channels and GitHub pull requests, listed in the
`preferences` file; template is extensible.

### Give the agent its own, scoped credentials

Credentials live in Managed Agents vaults; the agent references them but real
values stay outside the sandbox where Claude's code runs.
- MCP servers (GitHub): MCP tool calls go through a proxy running outside the
  sandbox; the proxy picks the vault credential whose URL matches the server's.
- Shell (Slack): the agent calls the Slack API with `curl` via the bash tool. The
  sandbox holds only an opaque placeholder `$SLACK_BOT_TOKEN`; the platform swaps in
  the real token as the request leaves the sandbox, only for allowed hosts.
- Create vault: `ant apply vault.yaml`. Add each credential with the TypeScript SDK:
  `client.beta.vaults.credentials.create(vaultId, {...})` with `display_name`,
  `auth.type: "environment_variable"`, `secret_name`, `secret_value`,
  `networking: { type: "limited", allowed_hosts: ["slack.com"] }`,
  `injection_location: { header: true }`.
- Attach the vault by copying its ID into `vault_ids` in `deployment.md`.

### Read from where you left off

Anti-pattern: a fixed window such as "the last 24 hours" — a late run leaves a gap,
an early run repeats items. Instead, a bookmark per source: at end of run the agent
writes the newest-item timestamp per source to `bookmarks.json` (e.g.
`"slack": "2026-09-14T13:02:11Z"`). The next run's window stretches/shrinks to
cover everything since. Bookmarks live in the `state` memory store — a folder of
text files mounted into each run's sandbox at `/mnt/memory/` and persisted between
runs; the agent uses ordinary file tools on it, guided by `agent.md`.

### Don't mistake a failed read for a quiet day

If an MCP server is down or its token expired, the run still starts without that
server's tools; the session logs an error but the agent sees nothing and reports
"nothing new". Three rules in `agent.md`: on source failure, keep that source's
bookmark unchanged; write the brief from the other sources; end the brief with one
line naming the unreadable source (e.g. pull requests unavailable this run).

## Destination

One Slack channel, a dated post per run, sent via bash/curl to
`https://slack.com/api/chat.postMessage` using the same bot token used for reading.
No approval step: the built-in bash tool runs without approval by default and
`slack.com` is on the environment allowlist.

### Confirm the post landed before recording it

After a confirmed post the agent updates its ledger and bookmarks. Mismatch risks:
recording a post that never landed (bookmarks advance, items never reported) or
re-posting when unsure (duplicate brief). Three rules: (1) search the channel's
recent messages for today's title and skip if already present; (2) count as sent
only if Slack returns `"ok": true` and a message `ts`; (3) update ledger and
bookmarks only after that confirmation. If unclear, mark the run "maybe posted" and
change nothing else. Run record in memory store at `runs/<date>.md`: marked
"posting" before the post, then "posted" with message ID, or "maybe posted".

## Agent

In Managed Agents an agent is a versioned configuration (model, system prompt,
tools); each run follows its run steps and stops. `agent.md` frontmatter:
`name: Daily brief`, `model: claude-sonnet-5-5`, `mcp_servers` with a url-type
`github` server at `https://api.githubcopilot.com/mcp/`; `tools`:
`agent_toolset_20260401` with `web_search` and `web_fetch` disabled, and an
`mcp_toolset` for github with `default_config.permission_policy.type: always_allow`.
Body: eight numbered run steps (full text in repo). MCP tools request approval by
default and nobody is present to grant it, hence `always_allow` — paired with a
read-only GitHub token.

### Keep the brief short

Run step 4 ("Decide"), paraphrased: an item earns a line only if the reader would
act on it today or it changes an imminent decision; when unsure, omit; most days a
few items, sometimes none; a count is not an item (link the blocked ones); an item
already in the ledger and still open is carried as one marked line ("still
waiting, day 3") not re-reported; closed items dropped silently; never revive a
topic the preferences file retired.

### Re-check anything still open right before posting

Run step 5 ("Verify"), paraphrased: just before posting, re-check each item's live
source — resolved: drop; changed: fix the line; unconfirmable: drop and list in the
run record's cuts. Rationale: one stale "still waiting on you" line costs more
trust than ten missing items, so assert or drop, never hedge. Every link is copied
from the source's own link field (PR `html_url`, Slack permalink), never built by
hand.

## Schedule

The agent is only configuration; a deployment runs it. The deployment names agent,
environment, and each run's first message, and holds schedule, vault, memory
stores, and budget. Each schedule firing starts a fresh agent session.
`deployment.md` frontmatter: `agent: ./agent.md`, `environment_id:
./environment.yaml`, `schedule: {type: cron, expression: "32 7 * * 1-5", timezone:
America/New_York}`, `vault_ids: [vlt_...]`, `resources:` the preferences store with
`access: read_only` (instruction: re-read every run, never write) and the state
store with `access: read_write` (bookmarks, ledger, notes, proposals, run records).
Body = first message: write today's brief; reader's time zone is America/New_York,
compute all dates there; follow run steps in order; edition title format
"Daily brief, <weekday> <month> <day>".
- Create: `ant apply deployment.md`. Manual test run:
  `ant beta:deployments run --deployment-id <id>`.

### Compute dates in your time zone

Common bug: the agent calls this morning "yesterday" because it computes dates in
the server's time zone. The `timezone` field sets firing time; the body's second
line tells the agent which zone to use for dates.

## Memory

Each run starts in a fresh sandbox with no memory; without memory feedback doesn't
stick, but stale memory misleads (reporting a resolved item as still waiting, or
dropping an open one as "already reported"). Two stores under `/mnt/memory/`:
- `preferences` (user-owned, read-only to agent): channels/repos, exclusions,
  length cap, destination, when to stop.
- `state` (agent-owned, read-write): bookmarks, ledger, per-run records, proposed
  changes to preferences, per-source behavior notes (e.g. a source returns only
  the newest 50 items).
`ant apply deployment.md` creates the preferences store but not its file; seed
`preferences.md` with `scripts/seed-preferences.sh` before first run.

### Re-read your preferences at the start of every run

Anti-pattern: baking a copy of preferences into the prompt — keeps applying rules
already changed. Read the file fresh each run; if unreadable, stop and say so
rather than running on defaults.

### Keep a ledger of what you've already reported, and report the change

`ledger.md` lists every reported item: date reported, source, a stable ID (Slack
message ts or PR number), last known status — so the brief doesn't repeat itself.
Example lines show a Slack thread, a PR "review blocked, day 2 (still waiting)",
and an escalation "owner named, in progress".

## Guardrails

### Limits on what it can do

The agent reads text written by others, which can act as instructions. Limit what
it could do if it followed them: GitHub token read-only, `preferences` store
read-only, environment reaches only allowlisted hosts. A planted instruction can
still alter the brief's content, including via the agent's between-run notes, but
cannot write to GitHub or edit the user's rules. Exception: Slack — the same token
posts, so invite the bot only to channels it must read or post in.

### Set the spending cap from real runs

Start the cap at 3–5x a normal run's cost; tighten with real data. A run hitting
the cap pauses rather than fails, so a too-low cap looks like a quiet brief. Cap =
`budget` in `deployment.md`; each run gets the full amount; on reaching it the run
pauses with stop reason `budget_reached`. Example: `budget: {type: limit,
max_list_cost: {amount: "500", currency: USD}}` — amount is a string in cents
("500" = $5.00).

## Getting started — six rules

1. Read each source from a bookmark, not a fixed time window.
2. Report a failed read as unreadable, never as a quiet day.
3. Re-check every item right before posting.
4. Count a post as sent only on Slack confirmation; then update bookmarks and ledger.
5. Re-read preferences every run, from a store the agent can't edit.
6. Read-only access wherever the agent only reads; cap per-run spend.

Run `claude update`, then `/claude-api managed-agents-onboard <post URL>`; the skill
reads the post, proposes a setup, writes files to an `agents/` folder, and creates
resources with `ant apply`. Treat as a starting point.
