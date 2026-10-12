---
title: "Anthropic (Eng): The \"think\" Tool"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (Engineering blog; no individual byline)
date: 2025-03-20
source_url: https://www.anthropic.com/engineering/claude-think-tool
source_path: raw/anthropic-eng-think-tool.md
tags: [tool-design, reasoning, extended-thinking, tau-bench, swe-bench, prompting, primary-source]
---

# Anthropic (Eng): The "think" Tool

> March 2025 post on a no-op `think` tool that gives Claude a scratchpad between
> tool calls. Its results were measured on Claude 3.7 Sonnet. Anthropic added a
> December 2025 note that recommends built-in extended thinking instead in most
> cases.

## Summary

**Dates.** The page shows "Published Mar 20, 2025" and an "Extended thinking
update" banner dated Dec 15, 2025. This page uses 2025-03-20 as the source date
and records the banner as a later revision.

The `think` tool does nothing except log its single `thought` string argument.
In March 2025, extended thinking ran only before the response started. The
think tool let Claude stop mid-response, between tool calls, and reason about
new tool results, policy rules, and missing information. The post tests it on
τ-bench (customer-service agents with policies, measured by pass^k) and
SWE-bench. The findings depend on the models tested: the results are for
**Claude 3.7 Sonnet**. A footnote reports gains for **Claude 3.5 Sonnet (New)**
with the same configuration. Readers should not assume the numbers transfer to
current models.

**Current status.** The Dec 15, 2025 banner says extended thinking has improved
and Anthropic recommends it "instead of a dedicated think tool in most cases",
with similar benefits and better integration and performance. The current
Claude Platform docs (checked 2026-10-12) do not mention a think tool on the
extended thinking, thinking, or thinking-in-tool-workflows pages. They document
**interleaved thinking**, which is thinking between tool calls within one
assistant turn. That is the built-in form of what the think tool simulated.
Adaptive thinking (Claude 4.6 and later) interleaves automatically. Manual
extended thinking returns a 400 error on Claude 4.7 and later models. No
Anthropic page found says the think tool is still recommended for current
models. See [[tool-design]] and [[prompt-tuning-axes]].

## Key points

- **Definition:** tool `think` with one required string input `thought`. The
  description says it fetches no information and changes nothing; it only
  appends the thought to a log.
- **Use it for:** analysis of tool output (with possible backtracking),
  policy-heavy environments, and costly sequential decisions.
- **Do not use it for:** non-sequential tool calls (one call or parallel calls)
  or simple instruction following. It costs prompt and output tokens.
- **Prompting matters on hard domains.** The tool with a system-prompt section
  of domain-specific worked examples beat the bare tool on the airline domain.
  The bare tool was enough on the easier retail domain.
- **Put long guidance in the system prompt**, not in the tool description.
- **Consistency:** gains held through pass^5, which Anthropic reads as better
  handling of edge cases.

## Entities

[[anthropic]], [[claude]]

## Concepts

[[tool-design]], [[prompt-tuning-axes]], [[agent-instructions]],
[[agent-evals]], [[agent-harness]]

## Notable claims & data

All figures are for Claude 3.7 Sonnet, March 2025.

- τ-bench airline, pass^1: think tool plus optimized prompt 0.570 vs. baseline
  0.370 (54% relative), per the prose. The post's table gives 0.584 vs. 0.332.
  Extended thinking 0.412; bare think tool 0.404. At pass^5: 0.340 vs. 0.100.
- τ-bench retail, pass^1: bare think tool 0.812, baseline 0.783, extended
  thinking 0.770. At pass^5: 0.626 vs. 0.583 (extended thinking 0.548).
- SWE-bench: a think tool contributed to a 0.623 state-of-the-art score. The
  isolated effect was +1.6% (n=30 with, n=144 without; Welch t(38.89) = 6.71,
  p < .001, d = 1.47).
- Extended thinking performed about the same as the unprompted think tool on
  airline, and below baseline on retail.

## Connections

- An early "give the model room to reason after tool results" pattern. Model
  features later absorbed it as interleaved and adaptive thinking. Current
  per-model thinking guidance lives in [[anthropic-prompting-claude-sonnet-5]]
  (adaptive thinking on by default, manual budgets removed) and
  [[anthropic-prompting-claude-sonnet-5-5]] (`between_tools` thinking setting
  for notes between tool calls).
- Tool-description practice: complements
  [[anthropic-eng-writing-tools-for-agents]] and
  [[anthropic-eng-advanced-tool-use]]. Its finding that long guidance works
  better in the system prompt than in the tool description is in tension with
  [[anthropic-new-rules-context-engineering-claude-5]]. That post keeps
  tool-usage guidance only in the tool description, so the two posts disagree
  for current models.
- pass^k as a consistency metric links to [[anthropic-eng-demystifying-evals]]
  and [[agent-evals]].
- The same era's "think" < "ultrathink" keyword budgets in Claude Code appear in
  [[anthropic-eng-claude-code-best-practices]]. Both are superseded by adaptive
  thinking and effort.
