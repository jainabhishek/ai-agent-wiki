---
title: "Claude customer story: Office Hours with Spotify on asynchronous coding"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com customer stories); Boris Cherny (Anthropic) interviewing Niklas Gustavsson (Spotify)
date: "accessed 2026-10-12"
source_url: https://claude.com/customers/spotify-boris-office-hours
source_path: raw/claude-customer-spotify-boris-office-hours.md
tags: [case-study, claude-code, claude-agent-sdk, background-agents, verification, code-migration, developer-productivity]
---

# Claude customer story: Office Hours with Spotify on asynchronous coding

> Vendor-published interview on how Spotify runs background coding agents at
> scale, built on fleet-wide migration tooling and strong test automation.

## Summary

Anthropic published this "Office Hours with Boris Cherny" transcript on
claude.com. The page shows no publication date; the wiki records it as accessed
2026-10-12. Internal references (Opus 4.5 "back in November/December")
suggest early 2026. All figures are self-reported by Spotify in conversation
with Anthropic's Claude Code lead.

Spotify's fleet-management system had merged millions of PRs from deterministic
migration scripts. It hit a ceiling because code's API surface made each script
balloon with edge cases. LLMs, first with an LLM judge and decomposition, became
"Honk": the [[claude-agent-sdk]] in a Kubernetes pod with internal tools and CI
verification on Linux and macOS. Spotify reports 73% of PRs AI-authored, a 75%+
rise in PR frequency, and neutral quality metrics, across 2,900 engineers.

## Key points

- **Remove scaffolding the model outgrows.** A judge raised PR success from
  about 20–30% to 80% early on. Spotify later removed it once models and the
  harness improved.
- **Verification is the core of closed-loop agents.** The agent can run CI on
  Linux and macOS, and the iOS simulator. Cherny calls under-investing in the
  verification loop a common mistake.
- **Auto-merge forced strong tests, which now enable agents.** Owning teams
  no longer see most automated PRs, so tests had to carry quality.
- **Standardization helps agents.** Claude copies patterns from nearby code;
  inconsistent code confuses it.
- **Tool access widened over time:** from a trusted allowlist to user-added
  internal tools in Honk V2.
- **Encode quality in instructions** (skills, CLAUDE.md) to go faster without
  losing quality (Cherny).
- **Workflow:** 5–10 Claude Code sessions over git worktrees; 20M+ line
  monorepo works after CLAUDE.md iteration.

## Entities

[[anthropic]], [[claude-code]], [[claude-agent-sdk]], [[claude]]

## Concepts

[[agent-harness]], [[agent-evals]], [[agent-steering]], [[guardrails]],
[[agent-orchestration]]

## Notable claims & data

- 73% AI-authored PRs; 75%+ PR frequency gain; 2,900 engineers; about 4,500
  deploys a day; idea to production in about an hour (all self-reported).
- The 20–30% → 80% judge effect is the speaker's recollection.

## Connections

Judge removal is an instance of harness–model co-evolution in [[agent-harness]]
and [[anthropic-eng-harness-design-long-running-apps]]. The verification
emphasis matches [[anthropic-verification-loops-with-skills]] and
[[anthropic-eng-claude-code-best-practices]]. Migration-at-scale parallels
[[anthropic-ai-code-modernization]].
