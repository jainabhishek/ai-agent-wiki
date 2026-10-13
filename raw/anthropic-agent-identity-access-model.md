# Agent identity in Claude Tag: a new access model for autonomous, team-wide AI — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/agent-identity-access-model
> Publisher: Anthropic (claude.com articles) · Date: 2026-06-24
> Captured: 2026-10-12 via WebFetch (condensed).

Author: Noah Zweben, member of technical staff on the Claude Code team. The page
also shows 2026-10-06 to 2026-10-08 in "Related articles"; those dates belong to
other articles.

## Intro (no heading)

- Agents work best when they reach the same tools, documents, and context as
  their human teammates.
- In a single-user assistant the agent acts with the user's own accounts. In a
  multiplayer setting such as Claude Tag (Claude in Slack), Claude uses
  workspace-level tools instead.
- Claude needs admin-configured accounts tied to the workspace. Anthropic calls
  this model "agent identity".

## Why "act as the user" breaks down

- Autonomy is growing: the post cites task length doubling about every four
  months; agents schedule their own work and react to events after the
  requester has logged off.
- In a shared channel, no single person's permissions are clearly the right
  ones. Agent identity lets admins define what the agent can do separately from
  the humans present, and tracks what it does.

### Claude acts as itself
- Claude has its own account in each system: posts in Slack as the Claude app,
  opens pull requests as the Claude GitHub App, queries the warehouse through an
  admin-provisioned service account.
- No personal credentials are involved, so a shared channel cannot be used to
  reach someone's private documents.

### Inheriting permissions
- Admins set a workspace-wide baseline identity (connections and skills); every
  channel inherits it by default.
- Per-channel overrides: for example GitHub plus warehouse access for an
  engineering channel, or a CRM connection limited to one private channel.
- Admins also configure: repository access (read and write scope); connectors,
  where different API keys for the same service carry different permission
  levels (read-only warehouse in general channels, write access in a private
  data-team channel); skills and plugins; standing instructions and context per
  channel.
- Revoking an identity cuts Claude's access everywhere it was used; simpler than
  auditing individual user accounts.

## How the agent identity model works

The question changes from "what can this user do?" to "what can this agent do in
this compartment?". This departs from per-user access control lists: a channel
member without direct repo access can still ask Claude to read the repo if the
channel grants it.

### How identity boundaries work
- Each private channel gets its own identity. Public channels share one
  workspace-level identity.
- Access and memory are isolated per channel; what Claude learns in a private
  channel does not surface elsewhere.
- By default anyone in a channel can tag Claude. Admins can scope a channel's
  profile to its least-privileged member.
- On Enterprise plans, role-based access control (RBAC) can restrict which
  members may invoke Claude at all.

### Broad default access to tools and context
- Value grows with each connected system, because Claude combines context
  across them (Slack threads, Drive docs, tracker tickets, warehouse queries).
- Recommended rollout: baseline profile in a few channels, review the audit
  trail, then widen access one deliberate grant at a time.
- Broad, low-risk integrations run in shared channels under agent identity;
  personal or team-specific tools stay in DMs.
- Admins can disable Claude Tag in specific channels or restrict it to certain
  users through RBAC.

### Direct messages
- DMs run under the individual user's claude.ai account: their connectors,
  their credentials, their name on results.
- DMs suit email drafts or software only that person is licensed for.

### Security and audit
- Connection credentials are stored separately, mapped to the channel's
  identity, and injected at the network boundary at request time.
- Outbound traffic to hosts the admin has not allowed is blocked.
- Routines, memory writes, and network calls made with agent credentials are
  logged. Because Claude uses its own service accounts, its actions also appear
  in each connected system's own logs.

## What's next

- Planned: just-in-time credential grants — a user approves one sensitive action
  without widening the agent's standing scope.
- Planned: an identity-aware overlay — Claude acts only when both the channel
  profile and the requesting user's own permissions allow it.
