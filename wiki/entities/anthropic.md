---
title: Anthropic
type: entity
subtype: org
created: 2026-06-21
updated: 2026-10-12
tags: [anthropic, agents]
---

# Anthropic

> AI research and safety company; maker of the Claude family of models and
> publisher of practical engineering guidance on building agents.

## Overview

In the context of this wiki, Anthropic is the source of the engineering guide
[[anthropic-building-effective-agents]], which frames agentic systems as a
spectrum from **workflows** to **agents** and advocates simple, composable
patterns over heavy frameworks.

## Key facts

- Publishes engineering guidance emphasizing **simplicity, transparency, and a
  well-designed Agent-Computer Interface (ACI)**. (see [[anthropic-building-effective-agents]])
- Catalogs five reusable [[workflow-patterns]]. (see [[anthropic-building-effective-agents]])
- Maker of [[claude]] and the agent surfaces [[claude-code]],
  [[claude-agent-sdk]], and [[claude-managed-agents]].
- Advocates **harness–model co-evolution** and pruning scaffolding the model has
  outgrown. (see [[agent-harness]], [[harnessing-claudes-intelligence]])
- Treats [[agent-skills]] and [[agent-steering]] as core context-engineering
  mechanisms. (see [[anthropic-steering-claude-code]])
- Contains agents at the environment layer first (sandboxes, VMs, egress
  controls) and treats model-level defenses as a second layer. (see
  [[anthropic-eng-how-we-contain-claude]], [[guardrails]])
- Current model lineup as of 2026-10-12: Claude Fable 5.1, Opus 5.5, Sonnet
  5.5, and Haiku 5.5, each with its own prompting page. (see
  [[anthropic-prompting-claude-fable-5-1]],
  [[anthropic-prompting-claude-opus-5-5]],
  [[anthropic-prompting-claude-sonnet-5-5]],
  [[anthropic-prompting-claude-haiku-5-5]])
- Publishes developer guidance on `claude.dev/blog` (posts from April 2026 on)
  as well as the Engineering blog. (see [[anthropic-seeing-like-an-agent]],
  [[anthropic-building-effective-agent-automations]])

## Relationships

- Industry counterpart to [[openai]]; their published agent guidance largely
  agrees — see [[agent-building-best-practices-anthropic-vs-openai]].

## Appears in

- [[anthropic-building-effective-agents]]
- [[anthropic-steering-claude-code]]
- [[anthropic-lessons-building-claude-code-skills]]
- [[harnessing-claudes-intelligence]]
- [[anthropic-evolution-of-agentic-surfaces]]
- [[anthropic-eng-context-engineering]]
- [[anthropic-eng-writing-tools-for-agents]]
- [[anthropic-eng-effective-harnesses-long-running-agents]]
- [[anthropic-eng-demystifying-evals]]
- [[anthropic-eng-multi-agent-research-system]]
- [[anthropic-eng-agent-skills]]
- [[anthropic-prompting-claude-opus-5]] (legacy)
- [[anthropic-prompting-claude-sonnet-5]] (legacy)
- [[anthropic-prompting-claude-fable-5]] (legacy)
- [[anthropic-prompting-claude-opus-5-5]]
- [[anthropic-prompting-claude-sonnet-5-5]]
- [[anthropic-prompting-claude-haiku-5-5]]
- [[anthropic-prompting-claude-fable-5-1]]
- [[anthropic-eng-how-we-contain-claude]]
- [[anthropic-eng-scaling-managed-agents]]
- [[anthropic-eng-claude-code-auto-mode]]
- [[anthropic-eng-harness-design-long-running-apps]]
- [[anthropic-eng-infrastructure-noise-evals]]
- [[anthropic-eng-advanced-tool-use]]
- [[anthropic-eng-code-execution-with-mcp]]
- [[anthropic-new-rules-context-engineering-claude-5]]
- [[anthropic-harness-for-every-task]]
- [[anthropic-prompt-caching-is-everything]]
- [[anthropic-seeing-like-an-agent]]
- [[anthropic-building-effective-agent-automations]]
- [[anthropic-claude-code-in-the-cloud]]
- [[anthropic-automating-eval-design-hillclimbing]]
- [[anthropic-building-with-sonnet-5-5]]
- [[anthropic-getting-most-out-of-opus-5-5]]

## Contradictions / open questions

- _None recorded._
