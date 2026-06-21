---
title: Claude
type: entity
subtype: product
created: 2026-06-21
updated: 2026-06-21
tags: [anthropic, model, llm]
---

# Claude

> Anthropic's family of large language models (e.g. Sonnet 4.5, Opus 4.5) — the
> reasoning engine that the agent harnesses and surfaces in this wiki are built
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
  vs. Opus 4.5 removing it. (see [[anthropic-evolution-of-agentic-surfaces]])

## Relationships

- Built by [[anthropic]]; powers [[claude-code]], [[claude-agent-sdk]],
  [[claude-managed-agents]].

## Appears in

- [[harnessing-claudes-intelligence]]
- [[anthropic-evolution-of-agentic-surfaces]]

## Contradictions / open questions

- _None recorded._
