---
title: "Anthropic: Lessons from Building Claude Code — How We Use Skills"
type: source
created: 2026-06-21
updated: 2026-06-21
author: Anthropic (Claude blog)
date: 2026-06-03
source_url: https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills
source_path: raw/anthropic-lessons-building-claude-code-skills.md
tags: [agents, skills, claude-code, best-practices]
---

# Anthropic: Lessons from Building Claude Code — How We Use Skills

> What Anthropic learned running hundreds of skills internally: skills aren't
> "just markdown" — they're folders of instructions, scripts, and resources, and
> their value compounds through gotchas and iteration.

## Summary

A field report on [[agent-skills]]: nine categories in active use and a set of
authoring principles. The highest-leverage content is **gotchas** — captured
failure points that push Claude out of its default behavior. See [[agent-skills]].

## Key points

- **Nine categories**: library/API reference, product verification (highest
  quality impact), data fetch/analysis, business-process automation, scaffolding,
  code quality/review, CI/CD, runbooks, infra ops.
- **Authoring principles**: avoid restating the obvious; build gotchas sections;
  progressive disclosure; avoid railroading; thoughtful setup (config.json);
  **write descriptions for models, not humans**; help Claude remember
  (append-only logs / JSON / SQLite); store scripts so Claude composes; on-demand
  hooks.
- **Distribution**: repo `./.claude/skills` for teams; internal plugin
  marketplaces for orgs; validate in sandboxes before promoting.
- **Measure** usage via PreToolUse hooks to find popular/under-triggering skills.

## Concepts

[[agent-skills]], [[context-engineering]], [[agent-design-principles]],
[[agent-steering]]

## Entities

[[anthropic]], [[claude-code]]

## Notable claims & data

- "Write descriptions for models, not humans" — the description field is what the
  model scans to decide whether to trigger the skill. Mirrors OpenAI's
  tool-clarity finding in [[tool-design]].
- Skills "improve iteratively — most began as a few lines and a single gotcha."
  Reinforces start-simple in [[agent-design-principles]].

## Connections

Deep-dive on the **skills** mechanism introduced in
[[anthropic-steering-claude-code]]; operationalizes "let Claude manage context"
from [[harnessing-claudes-intelligence]].
