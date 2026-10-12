---
title: Claude
type: entity
subtype: product
created: 2026-06-21
updated: 2026-10-12
tags: [anthropic, model, llm]
---

# Claude

> Anthropic's family of large language models (current as of 2026-10-12: Fable
> 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5) — the reasoning engine that the agent harnesses and surfaces in this wiki are built
> around.

## Overview

The model layer of [[agent-core-components]]. The ingested sources use Claude's
evolving capabilities as the reason to keep harnesses simple and prune scaffolding
the model has outgrown (see [[harnessing-claudes-intelligence]],
[[agent-harness]]).

## Key facts

- "Claude 3.5 Sonnet reached 49% on SWE-bench Verified with only a bash tool and a
  text editor tool." (see [[tool-design]], [[harnessing-claudes-intelligence]])
- Capability changes alter optimal harness design: Sonnet 4.5 "context anxiety"
  vs. Opus 4.5 removing it. (see [[anthropic-evolution-of-agentic-surfaces]],
  [[anthropic-eng-scaling-managed-agents]]) With Opus 4.6, a long-running app
  harness dropped its sprint structure and kept its planner. (see
  [[anthropic-eng-harness-design-long-running-apps]])
- **Model lineup (as of 2026-10-12).** Current models with Anthropic prompting
  pages: Claude Fable 5.1 (`claude-fable-5-1`; the page metadata also names
  Claude Mythos 5.1), Claude Opus 5.5 (`claude-opus-5-5`), Claude Sonnet 5.5
  (`claude-sonnet-5-5`), and Claude Haiku 5.5 (`claude-haiku-5-5`). (see
  [[anthropic-prompting-claude-fable-5-1]],
  [[anthropic-prompting-claude-opus-5-5]],
  [[anthropic-prompting-claude-sonnet-5-5]],
  [[anthropic-prompting-claude-haiku-5-5]]) Legacy: Claude Fable 5, Opus 5,
  Sonnet 5, and older; their prompting pages are marked `status: legacy`. (see
  [[anthropic-prompting-claude-fable-5]], [[anthropic-prompting-claude-opus-5]],
  [[anthropic-prompting-claude-sonnet-5]])
- Prompting guidance is a per-model contract: each current page says prompts
  for its predecessor (Opus 5, Sonnet 5, Fable 5; for Haiku 5.5, Claude Haiku
  4.5) "should perform well without changes", then lists behavioral
  differences. Per-model behaviors live on those source pages, not
  here. (see [[prompt-tuning-axes]])
- Positioning (vendor claims): Sonnet 5.5 for well-scoped everyday coding and
  repeated agent tasks; an Opus model for the hardest long-horizon work. In
  Claude Code the `default` model stays Opus 5.5. (see
  [[anthropic-building-with-sonnet-5-5]],
  [[anthropic-prompting-claude-sonnet-5-5]])

## Relationships

- Built by [[anthropic]]; powers [[claude-code]], [[claude-agent-sdk]],
  [[claude-managed-agents]].

## Appears in

- [[harnessing-claudes-intelligence]]
- [[anthropic-evolution-of-agentic-surfaces]]
- [[anthropic-eng-context-engineering]]
- [[anthropic-eng-writing-tools-for-agents]]
- [[anthropic-eng-demystifying-evals]]
- [[anthropic-eng-multi-agent-research-system]]
- [[anthropic-eng-agent-skills]]
- [[anthropic-eng-scaling-managed-agents]]
- [[anthropic-eng-harness-design-long-running-apps]]
- [[anthropic-prompting-claude-fable-5-1]]
- [[anthropic-prompting-claude-opus-5-5]]
- [[anthropic-prompting-claude-sonnet-5-5]]
- [[anthropic-prompting-claude-haiku-5-5]]
- [[anthropic-prompting-claude-fable-5]]
- [[anthropic-prompting-claude-opus-5]]
- [[anthropic-prompting-claude-sonnet-5]]
- [[anthropic-building-with-sonnet-5-5]]

## Contradictions / open questions

- _None recorded._
