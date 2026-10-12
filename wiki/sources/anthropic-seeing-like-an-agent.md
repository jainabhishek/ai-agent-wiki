---
title: "Anthropic: Seeing Like an Agent — How We Design Tools in Claude Code"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Thariq Shihipar (Anthropic, Claude Code)
date: 2026-04-10
source_url: https://claude.dev/blog/seeing-like-an-agent/
source_path: raw/anthropic-seeing-like-an-agent.md
tags: [tool-design, claude-code, elicitation, progressive-disclosure, subagents, harness]
---

# Anthropic: Seeing Like an Agent — How We Design Tools in Claude Code

> Case studies from the [[claude-code]] team on when to add, change, or remove
> an agent tool, built on the habit of reading model outputs to learn what the
> model can actually do ("seeing like an agent").

## Summary

The post treats tool design as matching tools to the model's real abilities,
learned by experiment and reading outputs. Four case studies: (1)
**AskUserQuestion** — after two failed attempts (a questions parameter on
ExitPlanTool confused the model; a parsed markdown format was unreliable), a
dedicated blocking question tool with structured options worked; (2)
**TodoWrite → Task tool** — todo lists plus reminders every 5 turns helped
early models, but constrained later ones; tasks with dependencies shared
across subagents replaced them as models (Opus 4.5) got better at subagents;
(3) **search** — a pre-indexed RAG vector store was replaced by a Grep tool so
Claude builds its own context, with skills adding progressive disclosure; (4)
**Claude Code Guide** — a docs-search subagent added self-knowledge without a
new tool. Claude Code has about 20 tools and a high bar for adding more.
Source date: 2026-04-10 byline.

## Key points

- **General vs. specialized** is the central question (one bash/code tool vs.
  ~50 tools); the answer depends on the model, goal, and environment. See
  [[tool-design]].
- **Structure beats format instructions** for UI-bound output: the dedicated
  tool gave guaranteed options and composability (Agent SDK, skills) where a
  prompt-specified markdown format did not. (raw: Attempts 1–3)
- **Tools must be retired as models improve:** reminders and rigid todos
  became a constraint; old tools can limit new models. Support a small set of
  models with similar capability profiles. (raw: tasks & todos)
- **Let the agent find context:** Grep over RAG; skills enable recursive
  nested search. See [[context-engineering]], [[agent-skills]].
- **Add capability without adding tools:** progressive disclosure via skills
  or a subagent (Claude Code Guide) that searches in its own context and
  returns only the answer. See [[agent-orchestration]].
- Each new tool is one more choice for the model, so the bar is high.

## Entities

[[anthropic]], [[claude-code]], [[claude]], [[claude-agent-sdk]]

## Concepts

[[tool-design]], [[context-engineering]], [[agent-skills]],
[[agent-orchestration]], [[agent-harness]], [[agent-design-principles]]

## Notable claims & data

- Claude Code has about 20 tools. (raw: Claude Code Guide agent)
- Early TodoWrite design injected system reminders every 5 turns. (raw: tasks
  & todos)
- Over about a year Claude went from not building its own context to nested
  multi-layer file search. (raw: search interface)
- Consistent with the existing [[tool-design]] preference for general-purpose
  tools the model already knows; no contradiction found. Adds the explicit
  point that tool sets should shrink or change as models improve, which aligns
  with the "delete scaffolding" corollary in [[harnessing-claudes-intelligence]].

## Connections

Companion to [[anthropic-prompt-caching-is-everything]] (same author; plan
mode as tools). Extends [[anthropic-eng-writing-tools-for-agents]] with
production case studies, and [[anthropic-eng-agent-skills]] on progressive
disclosure. Compare OpenAI's skill-routing advice in
[[openai-shell-skills-compaction]].
