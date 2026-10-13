---
title: "Claude customer story: Twilio PM builds a self-learning Feature Factory with Claude Code"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com customer stories); interviewee Michael Carpenter (Twilio)
date: accessed 2026-10-12 (no date on page)
source_url: https://claude.com/customers/twilio-qa
source_path: raw/claude-customer-twilio.md
tags: [case-study, claude-code, subagents, hooks, autonomy, risk-tiers, stall-detection, mcp]
---

# Claude customer story: Twilio PM builds a self-learning Feature Factory with Claude Code

> Q&A case study: one product manager builds a subagent pipeline with hooks,
> skills, a four-tier risk model, and staged autonomy on Claude Code.

## Summary

Anthropic published this Q&A on its claude.com customer-stories site; the page
has no date (accessed 2026-10-12). All results are self-reported by Twilio's
Michael Carpenter via Anthropic and are not independently verified. The page
gives two durations for the project: "over 51 days" in the intro and "1,000+
commits over 90 days" later. Carpenter built the "Feature Factory" on
[[claude-code]]: a pipeline of subagents (architect, spec, test generation,
development, review, documentation) whose output is a Claude Code plugin with
425 MCP tools for Twilio APIs.

## Key points

- **Knowledge capture as a flywheel.** A plain learnings file failed within four
  sessions. Hooks that write suggestions to a file Claude reads, auto-cleared on
  doc update, replaced it. Principle: capture must cost less effort than the
  discipline it replaces. See [[agent-steering]].
- **Four-tier risk model, set before business logic:** autonomous read-only;
  guarded (rate-limited test SMS); human approval (deploy, webhooks, buying
  numbers); never autonomous (delete, force-push, skip hooks). "CLI is for
  humans. MCP is for agents." See [[guardrails]].
- **Prompt fixes over infrastructure.** Friction events (wrong tool, skipped
  phase, misdiagnosis) were fixed by a 40-line markdown file with named tools,
  "do not skip live call phases", and per-phase retry budgets — not by a queue
  runner or retry logic.
- **Staged autonomy.** 23 design decisions over 40 days: from approval gates
  after every phase (six per feature) to headless runs by day 45.
- **Stall detection by pattern, not turn limits:** same tool + same input three
  times = stall; alternating calls = oscillation; no file changes = idle. Then
  safety floors on budgets, sandbox mode, and phase retry that keeps partial
  progress. See [[agent-harness]].
- **Silent tool failure.** The MCP server failed for 35 days (the post also calls them "35 sessions") (spawn, EOF, no
  error); work continued without tools. Fix was 53 lines of TypeScript. A
  boundary-failure example for [[boundary-contracts]] and [[model-context-protocol]].
- **Build-then-evaluate managed infrastructure.** He built memory and
  "dreaming" locally to evaluate [[claude-managed-agents]] from first-hand
  cost and latency data.

## Connections

Applies the mechanisms in [[anthropic-steering-claude-code]] and
[[anthropic-configure-hooks]]; staged autonomy parallels
[[anthropic-auto-mode-production]] and [[anthropic-eng-effective-harnesses-long-running-agents]].
Entities: [[anthropic]], [[claude-code]], [[claude-managed-agents]].
