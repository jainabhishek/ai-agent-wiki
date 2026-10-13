---
title: "Anthropic customer story: Dust (tool-call depth and prompt caching)"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com customer stories)
date: "accessed 2026-10-12"
source_url: https://claude.com/customers/dust
source_path: raw/claude-customer-dust.md
tags: [case-study, prompt-caching, tool-use, mcp, agent-platform, cost]
---

# Anthropic customer story: Dust (tool-call depth and prompt caching)

> Vendor-published case study of Dust, a no-code agent platform, on raising its per-run tool-call limit and restructuring prompt caching into tiers.

## Summary

Anthropic publishes this story on claude.com; the page has no date (accessed 2026-10-12). All results are self-reported by Dust through Anthropic. No model versions are named. Dust lets customers choose the model per agent; it gives each model its own prompting and context strategy behind one interface. Two engineering changes carry the story. First, Dust's old tool-call defaults (three per run, maximum eight) truncated results once models could chain more steps, so it redesigned the loop to allow up to 24. Second, longer runs raised token cost, so Dust built a three-tier prompt cache with Anthropic's Applied AI team.

## Key points

- **Tiered cache by scope and lifetime.** Globally shared instructions cached for one hour; workspace context and per-user context on shorter windows. Cache reads rose from ~30% to 65% of input tokens. (see [[context-engineering]], [[anthropic-prompt-caching-is-everything]])
- **Revisit harness limits as models improve.** Tool-call caps sized for weaker models truncated results; the loop now allows 24 calls. (see [[agent-harness]])
- **Per-model prompting behind a model picker.** Each model gets its own prompt and context strategy. (see [[prompt-tuning-axes]])
- **MCP both ways.** Dust is an MCP client (one interface to any tool) and an MCP server (exposes its agents and context). (see [[model-context-protocol]])
- **Governance in the platform.** Permission-aware retrieval, role-based access, and audit logs keep each agent within its user's clearance. (see [[guardrails]])
- **Sub-agent research.** Deep Research agents orchestrate sub-agents for 10+ minutes per report. (see [[agent-orchestration]])

## Notable claims & data

Self-reported: input spend −22%; overall model spend −18–19% (~$10K/day); tool-call depth 4–5 → 8+ steps "with no engineering changes" (the same page also describes the loop redesign); sources per research task 5 → 14; 300,000+ agents deployed; 70% average weekly active usage; AI-written code at Dust ~30% (early 2025) → 60–90%.

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[context-engineering]], [[agent-harness]], [[model-context-protocol]], [[prompt-tuning-axes]], [[guardrails]], [[agent-orchestration]]

## Connections

Cache-design principles: [[anthropic-prompt-caching-is-everything]]. Another ~90% cache-hit report: [[claude-customer-greptile]]. Agent platforms for non-engineers: [[claude-customer-n8n]], [[anthropic-cresta-agent-builder]].
