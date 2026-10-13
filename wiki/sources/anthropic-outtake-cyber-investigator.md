---
title: "Anthropic: How Outtake built a cyber investigator on Claude"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Michael Segner (Anthropic, claude.com articles)
date: 2026-07-22
source_url: https://claude.com/resources/articles/how-outtake-built-a-cyber-investigator-on-claude
source_path: raw/anthropic-outtake-cyber-investigator.md
tags: [case-study, long-running-agents, harness, evals, security, prompt-injection, claude-agent-sdk]
---

# Anthropic: How Outtake built a cyber investigator on Claude

> Case study of a long-running security investigation agent: prototype in
> Claude Code, move to the Agent SDK, move must-do steps from the prompt into the
> harness, and use evals mainly to speed iteration.

## Summary

Published by Anthropic on claude.com (2026-07-22, Michael Segner); results are
self-reported by Outtake. The Recon Agent follows an impersonation (for example
a cloned login page) to the attacker's wider infrastructure, maps it as a graph,
and writes an actor profile and timeline. It reads, writes, and runs code and
interacts with malicious pages. Sessions run a median of 16 minutes and up to
two hours. The model version is not named.

## Key points

- **Define "good" first.** Engineers ran investigations by hand to set a fixed
  standard before automating.
- **Prototype, then graduate.** [[claude-code]] validated the design; the
  [[claude-agent-sdk]] gave control of memory, context, and filesystem without
  rebuilding the loop. Skills carried over.
- **Constrain orchestration, free judgment.** Hard-code the always-do steps at
  the orchestration layer; leave low-level judgment to the agent.
- **Prompts are suggestions.** In long runs, prompt rules are eventually ignored;
  move invariants into harness guardrails, which also frees context.
- **Filesystem plus bash** gives memory that survives compaction and lets the
  agent work around failing tools.
- **Evals for speed.** Manual transcript review does not scale; codify it as a
  graded check and let an agent judge. Imperfect early evals still help.
- **Self-improvement loop.** The agent reports missing tools; a separate coding
  agent writes the tool and a test scenario; a human judges only the outcome.
- **Assume hijack.** A "blastbox" sandbox hides internals; a trust checkpoint
  scores each internet resource before the agent touches it.

## Notable claims & data

- Median session 16 min; longest 2 h. 20M+ potential attacks scanned in 2025;
  ARR 6x and customers 10x+ year over year (company figures).

## Connections

[[anthropic]], [[claude-code]], [[claude-agent-sdk]]. Concepts:
[[agent-harness]], [[guardrails]], [[agent-steering]], [[agent-evals]],
[[context-engineering]], [[tool-design]]. Related sources:
[[anthropic-steering-claude-code]] (authority of steering methods),
[[anthropic-building-agents-claude-agent-sdk]],
[[anthropic-eng-effective-harnesses-long-running-agents]],
[[anthropic-cybersecurity-triage-agents]], [[anthropic-warp-builds-self-improving-agents]],
[[anthropic-prompt-injection-defenses-browser]].
