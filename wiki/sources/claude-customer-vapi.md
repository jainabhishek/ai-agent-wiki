---
title: "Claude customer story: Vapi builds Composer, a voice-agent builder, on Claude"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com customer stories)
date: accessed 2026-10-12 (no date on page)
source_url: https://claude.com/customers/vapi
source_path: raw/claude-customer-vapi.md
tags: [case-study, claude-agent-sdk, tool-search, model-selection, context-engineering, voice-agents]
---

# Claude customer story: Vapi builds Composer, a voice-agent builder, on Claude

> Case study of a natural-language agent that configures voice agents through a
> 100+ tool catalog, chosen by live A/B tests of tool-calling reliability.

## Summary

Anthropic published this customer story on claude.com; the page has no date
(accessed 2026-10-12). Every metric is self-reported by Vapi via Anthropic and
is not independently verified. Vapi built Composer, an agent that builds and
configures voice agents through conversation. It runs on Claude through the
[[claude-agent-sdk]], with fallback between the direct Anthropic API and Amazon
Bedrock. Vapi went from a one-evening prototype to general availability in 2.5
months with five engineers. Model names are given only as Claude Opus, Sonnet,
and Haiku, with no versions.

## Key points

- **Model selection on live traffic.** Feature flags split production traffic
  between Claude and other providers' models. Vapi measured tool success rate,
  error classes, and user outcomes. Criteria order: function-calling
  reliability, consistency under tool orchestration, latency, then cost.
- **Prompt bloat fixed by modular architecture.** The v1 system prompt filled
  more than 50% of the context window before any user turn. A runtime router,
  shared chat kernel, and pluggable UI shell replaced it. New product surfaces
  dropped from ~700 to ~30 frontend lines. See [[context-engineering]].
- **Tool search over a large catalog.** 10+ skills and 100+ tools; only the tools
  relevant to the current turn load into context. See [[tool-design]].
- **Approve/deny on state-mutating actions.** Composer streams results and asks
  for approval only on actions that change state. See [[guardrails]].
- **Claimed gap grows with chain length.** Vapi says Claude's accuracy lead over
  tested models widens with longer tool chains and more specialized tools.
- **Claimed outcomes:** 2x to 10 call minutes, ~3x to 100 call minutes, 3x
  recovery after a failed first call.

## Connections

Same agent-builds-agents pattern as [[anthropic-cresta-agent-builder]]. Tool
search mechanism: [[anthropic-eng-advanced-tool-use]]. Entities: [[anthropic]],
[[claude]], [[claude-agent-sdk]].
