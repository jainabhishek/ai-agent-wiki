---
title: "Anthropic (Eng): Effective Context Engineering for AI Agents"
type: source
created: 2026-06-21
updated: 2026-06-21
author: Anthropic Engineering
date: 2025
source_url: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
source_path: raw/anthropic-eng-context-engineering.md
tags: [context-engineering, agents, best-practices, memory, primary-source]
---

# Anthropic (Eng): Effective Context Engineering for AI Agents

> The primary-source treatment behind the blog summaries: context engineering is
> "curating and maintaining the optimal set of tokens during inference." Its
> governing maxim — **find the smallest set of high-signal tokens that maximize
> the likelihood of your desired outcome.**

## Summary

Frames context as **finite and precious** because of **context rot** (recall
degrades as the window grows, from n² attention + sparse long-sequence training).
Covers system-prompt altitude, tool/example curation, just-in-time vs pre-loading
retrieval, and three long-horizon techniques. Deepens [[context-engineering]].

## Key points

- **System-prompt altitude:** between brittle (hardcoded if-else) and vague;
  organize with XML/Markdown sections; start minimal with the best model; "minimal
  does not necessarily mean short." (see [[agent-design-principles]], [[agent-steering]])
- **Tools:** information- + behavioral-efficiency; the **human clarity test**.
  (see [[tool-design]])
- **Examples:** curate diverse canonical examples; don't stuff edge cases.
- **Retrieval:** just-in-time (lightweight identifiers, load at runtime,
  progressive disclosure) vs pre-loading (embeddings; staleness risk); **hybrid
  recommended**; "do the simplest thing that works."
- **Long-horizon:** compaction; structured note-taking (agentic memory + the
  file-based memory tool); sub-agent architectures. (see [[agent-harness]],
  [[agent-orchestration]])

## Concepts

[[context-engineering]], [[tool-design]], [[agent-design-principles]],
[[agent-harness]], [[agent-orchestration]], [[agent-skills]]

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Notable claims & data

- **Context rot**: "as the number of tokens in the context window increases, the
  model's ability to accurately recall information from that context decreases."
- Sub-agents explore with tens of thousands of tokens but return ~1–2k-token
  summaries — the mechanism behind [[agent-orchestration]] sub-agents.

## Connections

Primary source behind [[harnessing-claudes-intelligence]] ("let Claude manage
context") and the basis for the [[context-engineering]] concept page. Compaction
+ note-taking + sub-agents map onto the long-running patterns in
[[anthropic-eng-effective-harnesses-long-running-agents]].
