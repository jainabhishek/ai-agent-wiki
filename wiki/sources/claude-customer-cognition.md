---
title: "Anthropic customer Q&A: Cognition (Devin)"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com customer stories)
date: "accessed 2026-10-12"
source_url: https://claude.com/customers/cognition
source_path: raw/claude-customer-cognition.md
tags: [case-study, coding-agents, long-horizon, evals, harness, model-migration]
---

# Anthropic customer Q&A: Cognition (Devin)

> Vendor-published interview with Cognition's CEO and CPO on what an autonomous coding agent (Devin) needs from a model and from the harness around it.

## Summary

Anthropic publishes this Q&A on claude.com; the page has no date (accessed 2026-10-12). All claims are self-reported by Cognition (Scott Wu, CEO; Walden Yan, CPO) through Anthropic. The headline figure — a 3.5x rise in merged PRs per week — is tied to a model the page calls "Claude Sonnet 3.6" and dates to 2024, so it describes a model generation long since superseded. Cognition routes work across several models. It says autonomous agents face a higher bar than code completion: users under-specify tasks, so the agent must clarify and infer intent, and it must stay on track over long trajectories. The durable content is about harness engineering and model-swap evaluation, not the model comparison.

## Key points

- **Trajectory monitoring.** Cognition invests in detecting when an agent drifts off course and steering it back. Before recent frontier models, the main failure was inconsistency over long contexts. (see [[agent-harness]], [[guardrails]])
- **Harness is tuned per model.** Changing which model handles which part of the workflow forces changes to prompts, tool definitions, context management, trajectory monitoring, and guardrails. About 50–70 engineers work on that integration surface. (see [[agent-harness]], [[prompt-tuning-axes]])
- **Component evals gate model swaps.** Separate evals for file-edit mechanics, locating the right files for an issue, and end-to-end engineer tasks; a long eval set guards against regressing product behaviors when a new model goes in. A strictly better model is swapped on day one. (see [[agent-evals]])
- **Success metric is a merged PR** for a well-scoped ticket.
- **Self-verification artifact.** Devin can send a screen recording showing it clicked through its own fix.
- **Sandbox readiness is a hard problem.** VM sandboxing has been rebuilt many times; the difficulty is having latest code, dependencies, and repos ready, not only spin-up.

## Notable claims & data

Self-reported: 3.5x merged PRs/week after Sonnet 3.6 (2024); Devin usage up at least 7x "since late last year" (undated page, so the window is unclear); Cognition engineers reportedly no longer type code.

## Entities

[[anthropic]], [[claude]]

## Concepts

[[agent-harness]], [[agent-evals]], [[prompt-tuning-axes]], [[guardrails]], [[model-context-protocol]]

## Connections

Model-evaluation practice parallels [[anthropic-cursor-evaluates-models]] and [[anthropic-jetbrains-evaluates-fable-5]]. Long-horizon coding agents: [[anthropic-eng-effective-harnesses-long-running-agents]], [[openai-run-long-horizon-tasks-codex]].
