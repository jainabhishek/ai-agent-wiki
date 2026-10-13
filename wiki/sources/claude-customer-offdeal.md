---
title: "Claude customer story: OffDeal runs M&A advisory on one Claude agent"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com customer stories); spokesperson Ori Eldarov, OffDeal
date: "accessed 2026-10-12"
source_url: https://claude.com/customers/offdeal
source_path: raw/claude-customer-offdeal.md
tags: [case-study, claude-agent-sdk, agent-skills, context-engineering, long-running-agents, financial-services, agent-evals]
---

# Claude customer story: OffDeal runs M&A advisory on one Claude agent

> Vendor-published case study of an AI-native investment bank that replaced 12+
> fixed workflows with one Claude Agent SDK agent built from skills.

## Summary

Anthropic published this customer story on claude.com. The page shows no
publication date; the wiki records it as accessed 2026-10-12. All results are
self-reported by OffDeal through Anthropic. The page does not name a Claude
model version.

OffDeal ran a separate agentic workflow per task. Each broke when a problem fell
outside its predefined path or a procedure changed. Deals carry 100M+ tokens of
context, and stuffing it into a long-context model failed at the 1M-token
limit. OffDeal moved to the [[claude-agent-sdk]] and consolidated into one
general agent, "Archie", with 20+ data sources and modular skills. OffDeal
reports zero context-overflow failures and an internal eval rising from 25% to
60% from the SDK switch alone, then to 85% after MCP and prompt work.

## Key points

- **Context, not intelligence, was the bottleneck** (CEO's diagnosis). They
  treated deal research like traversing a large codebase and relied on the
  SDK's subagents and automatic compaction instead of custom compaction.
- **One general agent plus skills beats many fixed workflows** when procedures
  change often and problems fall outside predefined paths.
- **Skills encode expert method.** A buyer-sourcing skill runs up to 4 hours
  across about 10 banker techniques. OffDeal reports about $200 compute versus
  $12,000+ and over a week for analysts.
- **Domain experts author skills.** A banker, not an engineer, built a
  branded-deck skill (20 slide templates).
- **Eval design:** multi-part queries over real production data (10M–100M+
  tokens), graded against real deal outcomes with composite rubrics.
- **Same SDK in dev and prod** lets Claude Code prototypes ship almost
  overnight.

## Entities

[[anthropic]], [[claude]], [[claude-agent-sdk]], [[claude-code]]

## Concepts

[[agent-skills]], [[context-engineering]], [[agents-vs-workflows]],
[[agent-harness]], [[agent-evals]], [[model-context-protocol]]

## Notable claims & data

- Eval 25% → 60% (SDK swap) → 85% (MCP design and prompting); 12+ workflows to
  1 agent; 8 deals, $91M in year one with two bankers; deck time about 1 hour
  versus 30–40 hours (all self-reported).

## Connections

An instance of the "when to build an agent" triggers in
[[agents-vs-workflows]]: fixed workflows broke on exceptions and on frequent
procedure changes. Harness reuse matches
[[anthropic-building-agents-claude-agent-sdk]]; skill authoring by domain
experts parallels [[anthropic-building-agents-with-skills]].
