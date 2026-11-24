---
title: "Anthropic: Building agents — when to fold subagents into your main agent loop"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Diane Sarkis (Anthropic)
date: 2026-10-22
source_url: https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop
source_path: raw/anthropic-fold-subagents-into-main-loop.md
models: [claude-opus-5-5, claude-fable-5-1]
as_of: 2026-11-24
tags: [orchestration, subagents, single-agent, skills, tool-search, evals, migration]
---

# Anthropic: Building agents — when to fold subagents into your main agent loop

> **Note (checked 2026-11-24).** Claude Fable 5.1, one of the two models in `models:`, is now legacy; the current Fable model is Claude Fable 5.2 (see [[anthropic-prompting-claude-fable-5-2]]). Opus 5.5 is still current.

> Anthropic's Applied AI guidance on moving enterprise agents from an orchestrator with many subagents to one agent loop that loads skills and tools on demand, with a staged, eval-gated migration path.

## Summary

Anthropic published this article on claude.com on 2026-10-22. Diane Sarkis wrote it. The post says that Anthropic's Applied AI team compared designs across several enterprise deployments. In those comparisons, one agent with skills often beat two other designs on quality: a single prompt for everything, and an orchestrator with subagents. The single agent also often had lower cost and latency per task. The post does not publish the comparison data.

The post keeps subagents for three cases. The first case is measurable quality loss from context bloat in one loop. The second case is parallel tasks that need fresh, disposable context windows. The third case is a single agent that picks tools badly or holds conflicting instructions. Outside these cases, the post calls a subagent per team an org-chart copy ("Conway's law").

The proposed fix is progressive disclosure. The agent sees short skill and tool descriptions and loads the full content only when it needs it. The post then gives a staged migration: build evals, call subagents as tools, then fold subagents into skills and tools one at a time.

## Key points

- **Five failure modes in large organizations.** The post names context management, subagent sprawl (hundreds of overlapping subagents with no owner), "the Frankenprompt" (each team adds a rule), local evals that nobody owns, and latency. (see [[agent-orchestration]], [[multi-agent-economics]])
- **Three reasons for one loop.** Shared context lets the agent connect earlier results. Progressive disclosure removes the old reason to split, which was context bloat. Current models need less structure from the harness. (see [[context-engineering]], [[agent-skills]])
- **Target loop design.** One model and one context window run an open-ended tool loop. The harness sets turn budgets, cost budgets, and write gates. The model writes its plan on turn one and revises it, because the planner is also the executor. (see [[agent-harness]])
- **Where things go.** Ordering and domain procedure go into skills. Hard limits, such as validation and approval gates, go into tools. Code still loads cheap, almost-always-relevant context, such as entity resolution. (see [[tool-design]])
- **Tools grouped by user intent.** The post says tool choice tends to degrade past 30–50 tool definitions in the system prompt. It recommends tool search with deferred loading. (see [[tool-design]])
- **Permissions inside tools.** Each tool checks the calling user's access and returns a refusal that the model can read. One loop then serves users with different access levels. (see [[agent-identity-and-access]])
- **Evals gate every fold.** A central team owns one end-to-end eval set. Each skill-owning team ships a small eval set. Ten golden examples are enough to start. (see [[agent-evals]])
- **Check flipped tasks, not only the score.** In a sample support agent, a fold cut latency but broke a passing task. The break appeared in one run out of two, so the post says to run each task more than once.
- **Ownership model.** One small central team owns the system prompt and end-to-end quality. Domain teams own skills and tools, with one DRI per team. (see [[human-agent-teams]])

## Notable claims & data

- One customer measured its single agent loop at roughly 2x faster runtime than its multi-agent harness.
- One company's customer-facing agent had a dozen specialist subagents. Those subagents made a consistent brand voice hard to keep and added latency.
- For a typical over-built design, reviewers said most of the need fits in one clear system prompt, 4–5 thin data tools, and strict output guardrails.
- Anthropic cut [[claude-code]]'s system prompt for more advanced models by over 80%. Part of the cut came from progressive disclosure of skills and tools. This matches [[anthropic-new-rules-context-engineering-claude-5]].
- Model-specific claims, as of 2026-11-24: thinking cannot be turned off on Opus 5.5 or Fable 5.1. The post says models from Opus 4.5 onward handle far more in one loop than teams expected. Opus 4.5 is a historical marker here, so this page does not scope to it.
- The post names a migration kit and Claude API skills: `/claude-api build-eval`, `/claude-api prompt-audit`, `/claude-api hillclimb`, and `/claude-api cost-optimize`. It also names `/skill-creator` and `/skill-doctor` for skill upkeep.
- Knowledge bases belong behind a search or lookup tool, or inside a skill as reference files. The post says code should not paste reference material into prompts.

## Entities

[[anthropic]], [[claude]], [[claude-code]].

## Concepts

[[agent-orchestration]], [[multi-agent-economics]], [[agent-skills]], [[tool-design]], [[context-engineering]], [[agent-harness]], [[agent-evals]], [[agent-instructions]], [[agent-identity-and-access]], [[guardrails]], [[model-context-protocol]].

## Connections

- Agrees with "start with a single agent" in [[anthropic-building-multi-agent-systems]] and with the "when subagents hurt" list in [[anthropic-subagents-in-claude-code]].
- Uses the same "telephone game" term and the same context-centric split as [[anthropic-building-multi-agent-systems]].
- Gives the simplest-pattern rule from [[anthropic-multi-agent-coordination-patterns]] (generator-verifier, orchestrator-subagent).
- Keeps subagents for research-style parallel work, as in [[anthropic-eng-multi-agent-research-system]].
- Tool search and deferred loading: [[anthropic-eng-advanced-tool-use]].
