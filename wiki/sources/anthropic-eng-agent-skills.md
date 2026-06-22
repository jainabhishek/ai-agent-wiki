---
title: "Anthropic (Eng): Equipping Agents for the Real World with Agent Skills"
type: source
created: 2026-06-21
updated: 2026-06-21
author: Anthropic Engineering
date: 2025
source_url: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
source_path: raw/anthropic-eng-agent-skills.md
tags: [skills, agents, progressive-disclosure, composability, primary-source]
---

# Anthropic (Eng): Equipping Agents for the Real World with Agent Skills

> The architectural primary source for [[agent-skills]]: the `SKILL.md` format,
> three-level progressive disclosure, bundled executable code, and the
> composability thesis — skills work across Claude.ai, Claude Code, the Agent SDK,
> and the Developer Platform.

## Summary

Agent Skills are "organized folders of instructions, scripts, and resources that
agents discover and load dynamically." They specialize a general agent via
reusable modules — "capturing and sharing procedural knowledge." Deepens
[[agent-skills]].

## Key points

- **SKILL.md + frontmatter**: mandatory `name` and `description`; frontmatter
  loads into the system prompt at startup so the agent recognizes relevant skills
  cheaply.
- **Three-level progressive disclosure**: (1) names/descriptions in system prompt
  → (2) full SKILL.md on relevance → (3) bundled files (reference.md, forms.md)
  only when the scenario needs them. Requires a filesystem + code execution. See
  [[context-engineering]].
- **Bundled executable code**: skills can ship code the agent runs as tools at its
  discretion — deterministic ops without loading code into context. See
  [[tool-design]].
- **Composability**: reusable modules instead of fragmented per-use-case agents.
- **Authoring**: evaluation-driven development; split large SKILL.md; iterate from
  observed usage; co-author with Claude. (see [[agent-evals]])
- **Security**: install from trusted sources; audit dependencies, bundled
  resources, and instructions pointing at untrusted networks. (see [[guardrails]])

## Concepts

[[agent-skills]], [[context-engineering]], [[tool-design]], [[agent-evals]],
[[guardrails]], [[agent-steering]]

## Entities

[[anthropic]], [[claude]], [[claude-code]], [[claude-agent-sdk]]

## Notable claims & data

- Supported across Claude.ai, [[claude-code]], the [[claude-agent-sdk]], and the
  Claude Developer Platform — skills are a cross-surface primitive, not a
  Claude Code feature.
- The PDF skill bundles `reference.md` + `forms.md` as a worked progressive-
  disclosure example.

## Connections

The engineering-architecture companion to the practitioner lessons in
[[anthropic-lessons-building-claude-code-skills]]; the progressive-disclosure
mechanism is the same one central to [[context-engineering]].
