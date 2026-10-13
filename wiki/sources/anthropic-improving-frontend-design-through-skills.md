---
title: "Anthropic: Improving frontend design through Skills"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic Applied AI (Prithvi Rajasekaran, Justin Wei, Alexander Bricken), with Molly Vorwerck and Ryan Whitehead
date: 2025-11-12
source_url: https://claude.com/resources/articles/improving-frontend-design-through-skills
source_path: raw/anthropic-improving-frontend-design-through-skills.md
tags: [skills, frontend, prompting, distributional-convergence, artifacts, context-engineering]
---

# Anthropic: Improving frontend design through Skills

> A worked example of turning a domain prompt into an on-demand skill: Anthropic's frontend-aesthetics skill and the web-artifacts-builder skill.

## Summary

Published 2025-11-12 on claude.com; the post names no Claude model version, so its before/after examples reflect the late-2025 Claude models and are qualitative (screenshots, no metrics). The problem it names is **distributional convergence**: without direction, the model samples the safe center of web training data, which gives Inter fonts, purple-on-white gradients, and little motion. Claude is steerable, but frontend guidance in a system prompt would load into every unrelated request. A skill loads the guidance only when the task is frontend work. The post's general method for any domain with generic default output has four steps. First, identify the convergent defaults. Second, give concrete alternatives. Third, write at the right altitude. Fourth, package the result as a skill.

## Key points

- **Map aesthetics to code.** Effective guidance targets dimensions that become implementable code: typography, color/theme, motion, backgrounds. Write at the "right altitude": no exact hex codes, but not vague taste words either. (see [[agent-instructions]], [[anthropic-eng-context-engineering]])
- **Name the defaults to avoid.** The typography block bans named fonts and gives alternatives by category. It asks for weight extremes (100/200 vs 800/900) and size jumps of 3x+. A font mandate alone also improved other parts of the design.
- **Compact skill.** The combined `<frontend_aesthetics>` prompt is ~400 tokens. It explains the convergence problem, gives one directive per design vector, lists clichés to avoid, and ends with a reminder against converging on a new default (e.g. Space Grotesk). (see [[agent-skills]])
- **Skills over system prompt.** Domain context loads just-in-time, so unrelated tasks carry no frontend tokens. (see [[context-engineering]])
- **Scripts remove architectural limits.** `web-artifacts-builder` lets Claude build artifacts with React, Tailwind CSS, and shadcn/ui across many files. Its scripts scaffold the repo and then bundle the result into the single HTML file that artifacts require, using Parcel. Scripts for boilerplate cut tokens and raise reliability. (see [[tool-design]])
- **Latent capability.** The post's claim: models can do more than they show by default, and a skill can bring that capability out.

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[agent-skills]], [[context-engineering]], [[agent-instructions]], [[tool-design]]

## Connections

Cited as the example skill in [[anthropic-building-agents-with-skills]] and listed in [[anthropic-complete-guide-building-skills]]. HTML artifacts as output: [[anthropic-unreasonable-effectiveness-of-html]]. Skill authoring practice: [[anthropic-lessons-building-claude-code-skills]].
