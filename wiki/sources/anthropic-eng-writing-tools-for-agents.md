---
title: "Anthropic (Eng): Writing Effective Tools for Agents"
type: source
created: 2026-06-21
updated: 2026-06-21
author: Anthropic Engineering
date: 2025
source_url: https://www.anthropic.com/engineering/writing-tools-for-agents
source_path: raw/anthropic-eng-writing-tools-for-agents.md
tags: [tools, agents, best-practices, evals, primary-source]
---

# Anthropic (Eng): Writing Effective Tools for Agents

> The primary-source deep dive on tool design — and the meta-move of using agents
> themselves to evaluate and improve their tools. Deepens [[tool-design]].

## Summary

Tools are the agent–environment contract. Pick high-impact tools (not wrappers
over every API), consolidate and namespace them, return high-signal context, be
token-efficient, write onboarding-quality descriptions, and **evaluate with the
agent in the loop**. (see [[tool-design]])

## Key points

- **Choose the right tools:** "more tools don't always lead to better outcomes."
  Prefer `search_contacts` over `list_contacts`; consolidate (`schedule_event`
  finds availability *and* books).
- **Namespacing:** common prefixes by service/resource; prefix vs suffix has
  measurable eval effects.
- **Meaningful context:** semantic over technical (`name` not `uuid`); add a
  `response_format` (`concise`/`detailed`) parameter.
- **Token efficiency:** pagination, filtering, truncation with helpful messages;
  actionable errors.
- **Descriptions:** onboarding-quality; unambiguous params (`user_id` not `user`);
  "even small refinements... can yield dramatic improvements."
- **Evaluate with agents:** realistic multi-call tasks; metrics beyond accuracy
  (runtime, tool-call count, tokens, errors); paste transcripts into Claude to
  auto-optimize tools. (see [[agent-evals]])

## Concepts

[[tool-design]], [[agent-evals]], [[context-engineering]], [[agent-design-principles]]

## Entities

[[anthropic]], [[claude]]

## Notable claims & data

- The **human clarity test** restated: if a human can't pick the right tool, an
  agent can't either — same principle as [[anthropic-eng-context-engineering]].
- Using agents to refine their own tools operationalizes OpenAI's
  evaluator–optimizer / eval loop ideas (see [[workflow-patterns]], [[agent-evals]]).

## Connections

The Anthropic-side primary source for [[tool-design]], complementing OpenAI's tool
taxonomy in [[openai-practical-guide-to-building-agents]]. Tool-eval advice feeds
[[agent-evals]].
