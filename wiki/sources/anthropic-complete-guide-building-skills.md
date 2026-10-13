---
title: "Anthropic: The Complete Guide to Building Skills for Claude"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (guide PDF)
date: 2026-01-29
source_url: https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
source_path: raw/anthropic-complete-guide-building-skills.md
tags: [skills, skill-authoring, mcp, evals, troubleshooting, guide]
---

# Anthropic: The Complete Guide to Building Skills for Claude

> Anthropic's 33-page practitioner guide to planning, writing, testing, distributing, and debugging skills, with a dedicated track for MCP connector builders.

## Summary

The PDF has no date of its own; this page uses the landing-page byline (2026-01-29) on claude.com. The PDF's distribution chapter is headed "January 2026", which agrees. The guide defines a skill as a folder with a required `SKILL.md` (YAML frontmatter + Markdown) and optional `scripts/`, `references/`, and `assets/`. It states three design principles: three-level progressive disclosure, composability with other loaded skills, and portability across Claude.ai, Claude Code, and the API. For MCP builders it frames MCP as connectivity ("what Claude can do") and skills as knowledge ("how Claude should do it"). It names three skill categories: document and asset creation, workflow automation, and MCP enhancement. Its success targets are rough benchmarks that Anthropic says include some "vibes-based" judgment.

## Key points

- **Frontmatter rules.** File must be exactly `SKILL.md`; folder and `name` in kebab-case; no `README.md` inside the skill. `description` must state what the skill does and when to use it, under 1024 characters, no `<` or `>`. Optional fields: `license`, `compatibility` (1–500 chars), `metadata`, `allowed-tools`. "claude"/"anthropic" names are reserved, because frontmatter enters the system prompt and could inject instructions. (see [[agent-skills]], [[guardrails]])
- **Description formula.** What it does + when to use it + key capabilities, with phrases users actually say and file types. Bad: vague, no triggers, or too technical.
- **Instructions.** Specific commands over vague verbs; an error-handling section; explicit links to `references/`; critical rules at the top. For critical validations, bundle a script: "Code is deterministic; language interpretation isn't." (see [[agent-instructions]], [[tool-design]])
- **Iterate on one hard task first,** then extract the winning approach into a skill, then broaden test cases.
- **Three test types.** Triggering (obvious, paraphrased, unrelated), functional (Given/When/Then), and performance vs a no-skill baseline. Targets: trigger on 90% of relevant queries over 10–20 test queries; 0 failed API calls; rerun the same request 3–5 times for consistency. (see [[agent-evals]])
- **Trigger tuning.** Under-triggering → add detail and keywords to the description. Over-triggering → add negative triggers and narrow scope. Debug by asking Claude when it would use the skill.
- **Five patterns.** Sequential workflow orchestration (ordering, validation, rollback); multi-MCP coordination (phases, data passing); iterative refinement (validation script, stop criterion); context-aware tool selection (decision tree, explain the choice); domain-specific intelligence (compliance before action, audit trail). Framing: problem-first vs tool-first. (see [[workflow-patterns]], [[model-context-protocol]])
- **Context limits.** Keep `SKILL.md` under 5,000 words; review if more than 20–50 skills are enabled at once; consider skill "packs". (see [[context-engineering]])
- **Distribution (Jan 2026).** Upload a zip via Claude.ai settings or place in the Claude Code skills directory. Admins can deploy workspace-wide (since 2025-12-18). API: `/v1/skills` endpoint and the `container.skills` parameter on Messages API requests, which requires the Code Execution Tool beta. Works with the [[claude-agent-sdk]].

## Notable claims & data

- Illustrative baseline comparison (not a measurement): without skill 15 messages, 3 failed calls, 12,000 tokens; with skill 2 clarifying questions, 0 failures, 6,000 tokens.
- The guide says skill-creator "does not execute automated test suites or produce quantitative evaluation results." [[anthropic-improving-skill-creator]] (2026-03-03) later added evals, benchmark mode, and blind A/B comparators, so this limitation no longer holds.
- Internal inconsistency: Chapter 2 reserves names *containing* "claude"/"anthropic"; Reference B says names with that *prefix*. Reference B's "all optional fields" list omits `compatibility`.
- The guide says explicit "be thorough" encouragement works better in user prompts than in `SKILL.md`.

## Entities

[[anthropic]], [[claude]], [[claude-code]], [[claude-agent-sdk]]

## Concepts

[[agent-skills]], [[model-context-protocol]], [[agent-evals]], [[workflow-patterns]], [[context-engineering]], [[agent-instructions]], [[guardrails]]

## Connections

Architecture argument: [[anthropic-building-agents-with-skills]], [[anthropic-eng-agent-skills]]. Later tooling: [[anthropic-improving-skill-creator]]. Claude Code practice: [[anthropic-lessons-building-claude-code-skills]]. OpenAI's trigger-eval method (also 10–20 prompts): [[openai-testing-agent-skills-with-evals]]. MCP server side: [[anthropic-agents-production-systems-mcp]].
