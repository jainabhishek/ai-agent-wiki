---
title: "Claude customer story: Shortcut spreadsheet agent on Opus 4.6"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com customer stories); spokesperson Nico Christie, Fundamental Research Labs
date: "accessed 2026-10-12"
source_url: https://claude.com/customers/shortcut
source_path: raw/claude-customer-shortcut.md
tags: [case-study, claude-platform, multi-agent, subagents, planning, spreadsheets, agent-evals]
---

# Claude customer story: Shortcut spreadsheet agent on Opus 4.6

> Vendor-published case study of an AI spreadsheet tool that audits workbooks
> with parallel per-sheet subagents and executes plans in a fresh agent.

## Summary

Anthropic published this customer story on claude.com. The page shows no
publication date; the wiki records it as accessed 2026-10-12. The page refers
to Opus 4.6's February release and January 2026 usage, so it likely dates from
early 2026. All results are self-reported by Fundamental Research Labs through
Anthropic. The headline finding is specific to Claude Opus 4.6: an internal
benchmark rose from 7.29 to 8.08 out of 10 with no prompt changes.

Shortcut works across Excel, Google Sheets, and its own app. The company built a
benchmark of hard Excel tasks with verifiable answers. At launch, the best
models scored 4–5.5 out of 10. To audit a workbook, Shortcut fans out one
subagent per sheet (6–10 for a ten-sheet model) that report to a main agent. It
then plans with the user and hands the approved plan to a fresh agent.

## Key points

- **Own benchmark with verifiable answers** drives model choice and tracks
  each upgrade.
- **Low model-specific prompting** was a selection factor. Other models needed
  rounds of prompt work; swapping Opus in needed none (company's claim).
- **Parallel per-sheet exploration subagents** gather context and report to a
  main agent, modeled on [[claude-code]].
- **Plan, approve, then execute in a fresh context.** Planning mode reviews
  and asks clarifying questions; a new agent executes so its context stays
  clean.
- **Model upgrades delivered gains without engineering work**, per the company.

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[agent-orchestration]], [[context-engineering]], [[agent-evals]],
[[agent-harness]]

## Notable claims & data

- 7.29 → 8.08/10 (Opus 4.6, no prompt changes); about 70% task failure with
  other providers early on; almost half a trillion tokens in January 2026;
  100,000+ users at 1,000+ companies (all self-reported).

## Connections

Fan-out exploration matches [[anthropic-eng-multi-agent-research-system]].
Fresh-context execution parallels the separate-instance advice in
[[agent-orchestration]].
