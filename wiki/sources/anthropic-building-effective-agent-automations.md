---
title: "Anthropic: Building Effective Agent Automations"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Lance Martin and CJ Avilla (Anthropic, claude.dev blog)
date: 2026-10-08
source_url: https://claude.dev/blog/building-effective-agent-automations/
source_path: raw/anthropic-building-effective-agent-automations.md
tags: [agents, automation, claude-managed-agents, scheduled-agents, memory, guardrails, credentials, idempotency]
---

# Anthropic: Building Effective Agent Automations

> A reference implementation of a scheduled, unattended "daily brief" agent on
> [[claude-managed-agents]], organized around the failure modes that make
> background automations silently wrong: lost source access, stale memory,
> duplicate or phantom posts, and time-zone bugs.

## Summary

The post builds an agent that reads Slack channels and GitHub pull requests on a
cron schedule, tracks what changed since the last run, and posts a brief to one
Slack channel. It splits the automation into six components: **sources,
destination, agent, schedule, memory, guardrails**. Each component is a
declarative file (`agent.md`, `deployment.md`, `environment.yaml`, two memory-store
YAMLs, `vault.yaml`) that the `ant apply` CLI turns into Claude API resources. The
agent is a versioned configuration (model, system prompt, tools); a separate
**deployment** binds agent, environment, schedule, vault, memory stores, budget,
and the first message of each run. Every scheduled firing starts a fresh session
in a fresh sandbox. The main content is a set of state-management and
least-privilege rules, condensed by the authors into six rules (see Key points).
See [[agent-harness]], [[guardrails]], [[agent-identity-and-access]], [[context-engineering]].

## Key points

- **Bookmarks, not time windows** (Sources). A fixed window such as "the last 24
  hours" leaves gaps on late runs and repeats on early runs. The agent writes the
  newest-item timestamp per source to `bookmarks.json`. The next run reads from
  there, so its window adapts.
- **A failed read is not a quiet day.** If an MCP server is down or its token has
  expired, the run starts without those tools and the agent would report "nothing
  new". Rules: keep that source's bookmark unchanged, write the brief from the other
  sources, and name the unreadable source in one closing line. (Fail-loud at the
  agent level; compare [[boundary-contracts]].)
- **Confirm before recording** (Destination). The post counts as sent only when
  Slack returns `"ok": true` and a message `ts`. The agent first checks the channel
  for today's title, to avoid duplicates. Ledger and bookmarks update only after
  confirmation. An unclear result is recorded as "maybe posted" and nothing else
  changes. A run record moves through the states posting → posted / maybe posted.
- **Re-verify right before acting** (Agent, run step 5). The world changes between
  read and post. The agent re-checks each item's live source: resolved items are
  dropped, changed items are fixed, and items it cannot confirm are cut. The stated
  rationale: one stale "still waiting on you" line costs more trust than ten
  missing items. Links are copied from source link fields, never built by hand.
- **Brevity by explicit inclusion bar** (run step 4). An item needs a same-day
  action or must change an imminent decision. A count is not an item. Open items
  already in the ledger carry forward as one marked line.
- **Dates in the reader's time zone.** The `timezone` field sets when the run
  fires. The first message separately tells the agent which zone to use for date
  arithmetic. This prevents the agent from calling this morning "yesterday".
- **Two memory stores** mounted at `/mnt/memory/`: `preferences` (user-owned,
  `read_only` to the agent) and `state` (agent-owned, `read_write`: bookmarks,
  `ledger.md` keyed by stable IDs, `runs/<date>.md`, proposed preference changes,
  per-source behavior notes). Preferences are re-read every run, never baked into
  the prompt. If the agent cannot read the preferences, it stops rather than
  running on defaults. See [[context-engineering]].
- **Credentials outside the sandbox.** Vault credentials never enter the sandbox.
  MCP calls go through an external proxy that matches the credential by server URL.
  Shell calls see only a placeholder (`$SLACK_BOT_TOKEN`). The platform injects the
  real token on egress, and only to allowlisted hosts.
- **Guardrails sized to injection risk.** The agent reads text written by others,
  so the authors limit what a followed injection could do: a read-only GitHub token,
  a read-only preferences store, and a host allowlist. A planted instruction can
  still alter the brief, including through the agent's own notes, but it cannot
  write to GitHub or change the user's rules. Slack is the stated exception (one
  token reads and posts). See [[guardrails]].
- **No human in the loop.** MCP tools ask for approval by default, and nobody is
  present to give it. The GitHub toolset is therefore set to `always_allow`, which
  is safe only because the token is read-only. The bash tool runs without approval
  by default.
- **Spend cap from real runs.** Start at 3–5x a normal run's cost and tighten. A
  capped run *pauses* (`budget_reached`) rather than failing, so a cap that is too
  low looks like a quiet brief.

## Notable claims & data

- The model in the example `agent.md` is `claude-sonnet-5-5`. The toolset is
  `agent_toolset_20260401` with `web_search` and `web_fetch` disabled.
- The schedule is cron `"32 7 * * 1-5"` with timezone `America/New_York`.
- The budget is `max_list_cost.amount` as a string in cents (`"500"` = $5.00), and
  every run gets the full amount.
- Manual test run: `ant beta:deployments run --deployment-id <id>`.

## Entities

[[anthropic]], [[claude-managed-agents]], [[claude-code]], [[claude]]

## Concepts

[[agent-harness]], [[guardrails]], [[context-engineering]], [[agent-design-principles]],
[[boundary-contracts]], [[tool-design]]

## Connections

- This is a concrete deployment pattern for [[claude-managed-agents]]. The
  vault/proxy credential model and sandbox egress likely overlap with
  [[anthropic-eng-how-we-contain-claude]] and
  [[anthropic-eng-scaling-managed-agents]].
- The external state files (bookmarks, ledger, run records) that survive fresh
  sessions are the same move as the progress file in
  [[anthropic-eng-effective-harnesses-long-running-agents]]. Memory lives in files
  the agent reads each run, not in the prompt.
- Read-only scoping as the defense against prompt injection matches the
  layered-defense framing in [[guardrails]] and the least-privilege tooling advice
  in [[anthropic-eng-writing-tools-for-agents]].
- A sibling post from the same series:
  [[anthropic-automating-eval-design-hillclimbing]], also by Lance Martin, which
  uses the same `claude-api` skill as its onboarding path.

## Contradictions / open questions

- _None recorded._ The post does not say how the agent detects that an MCP server
  failed to load (the "session logs an error" path). It is open whether the agent
  sees that error or infers the failure from missing tools.
