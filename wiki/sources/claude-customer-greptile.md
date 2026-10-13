---
title: "Anthropic customer story: Greptile (agentic code review on the Agent SDK)"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com customer stories)
date: "accessed 2026-10-12"
source_url: https://claude.com/customers/greptile
source_path: raw/claude-customer-greptile.md
tags: [case-study, code-review, claude-agent-sdk, hooks, subagents, prompt-caching]
---

# Anthropic customer story: Greptile (agentic code review on the Agent SDK)

> Vendor-published case study of Greptile moving its code-review agent from a fixed flowchart to multi-hop investigation on the [[claude-agent-sdk]].

## Summary

Anthropic publishes this story on claude.com; the page has no date (accessed 2026-10-12). All results are self-reported by Greptile (Daksh Gupta, CEO) through Anthropic. Greptile says it runs Opus 4.5. Greptile had built specialized review tools, but its orchestration forced them into a fixed sequence, so findings from one step could not steer the next. A 10-engineer team chose the [[claude-agent-sdk]] over a homegrown harness to spend time on domain tools; Gupta argues models and harnesses are coupled. The agent now picks its next investigation step, uses a memory sub-agent, and relies on hooks to guarantee coverage.

## Key points

- **Buy the harness, build the tools.** A small team put its effort into specialized tools (codebase context, similar-function search, git history) rather than loop infrastructure. (see [[agent-harness]], [[tool-design]])
- **Model–harness coupling** was a stated reason to use the model vendor's SDK. (see [[agent-harness]])
- **Multi-hop investigation.** The agent follows leads: git history, commit → original PR, comparison with similar functions. (see [[agents-vs-workflows]])
- **Hooks for determinism.** Hooks ensure every file in a PR is examined, a coverage guarantee the model alone does not give. (see [[agent-steering]], [[guardrails]])
- **Memory sub-agent.** One sub-agent retrieves team standards, learned codebase quirks, and instruction files (claude.md, cursor rules). (see [[agent-orchestration]], [[context-engineering]])
- **Evidence-backed findings.** In NVIDIA's PhysicsNeMo, the agent defended a disputed precision bug with similar functions and git history; the author agreed.

## Notable claims & data

Self-reported: ~90% cache hit rate; 1M issues caught per month; 2,000+ organizations; over a billion lines reviewed per month.

## Entities

[[anthropic]], [[claude]], [[claude-agent-sdk]], [[claude-code]]

## Concepts

[[agent-harness]], [[tool-design]], [[agent-steering]], [[guardrails]], [[agents-vs-workflows]], [[context-engineering]]

## Connections

Other review agents: [[openai-codex-code-review-rules]], [[anthropic-coderabbit-agent-orchestration]]. Same harness decision: [[claude-customer-caylent]]. Hooks: [[anthropic-configure-hooks]], [[anthropic-steering-claude-code]].
