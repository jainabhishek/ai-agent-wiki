---
title: "Anthropic: The new rules of context engineering for Claude 5 generation models"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Thariq Shihipar (Anthropic, claude.dev blog)
date: 2026-07-24
source_url: https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/
source_path: raw/anthropic-new-rules-context-engineering-claude-5.md
tags: [context-engineering, claude-code, system-prompt, claude-md, skills, progressive-disclosure, tool-descriptions]
---

# Anthropic: The new rules of context engineering for Claude 5 generation models

Written for the Claude 5 generation (Jul 2026); check against current models before applying.

> Anthropic's account of cutting over 80% of Claude Code's system prompt for
> Claude 5-generation models with no measurable eval loss, and the six
> "then → now" shifts it draws for system prompts, CLAUDE.md, skills, tools, and
> references.

## Summary

Scope: the post states the cut was made "for models like Claude Opus 5 and
Claude Fable 5" and frames its guidance for the "Claude 5 generation". It names
no API model IDs, so this page carries no `models:` field.

Anthropic found it had been over-constraining [[claude-code]] through its system
prompt, CLAUDE.md files, and skills; transcripts showed the layers issuing
conflicting instructions in one request. For newer models it deleted many
worst-case guard rules and let the model rely on surrounding context and
judgement — removing over 80% of the system prompt with no measurable loss on
coding evals. Six earlier best practices are recast as myths: rules →
judgement; examples → interface design; everything upfront → progressive
disclosure; repetition → single tool descriptions; manual CLAUDE.md memory →
auto-memory; simple specs → rich references (HTML artifacts, test suites, code,
rubrics). The post then gives per-layer guidance and ships the practices in
`claude doctor` (`/doctor`). See [[context-engineering]] and [[agent-instructions]].

## Key points

- **Conflicting layers cost reasoning.** System prompt, skills, and user
  requests can clash; the model must spend effort reconciling them. Audit for
  over-constraint and conflicts.
- **Rules → judgement.** Replace blanket rules (e.g. no-comments defaults) with
  an instruction to match the surrounding code's comment density, naming, and
  idiom.
- **Examples → interfaces.** Usage examples narrow the model's exploration.
  Make parameters expressive instead: TodoWrite's ~9,100-character description
  became one line plus a `status` enum (`pending` / `in_progress` /
  `completed`) and one rule.
- **Progressive disclosure everywhere:** code-review and verification moved from
  the system prompt into skills; tools can be deferred and found via
  `ToolSearch`; CLAUDE.md / SKILL.md should be a tree of files, not a catch-all.
- **No repetition:** tool-usage guidance lives only in the tool description.
- **Auto-memory** replaces the `#`-hotkey CLAUDE.md memory habit.
- **Rich references:** prefer references in code (HTML mockup over prose or a
  screenshot); rubrics encode taste and drive verifier agents in dynamic
  workflows.
- **Per layer:** system prompt = product context (where harness builders should
  invest most); CLAUDE.md = brief purpose + codebase gotchas, nothing
  discoverable; skills = lightweight team-specific guides, split into files,
  tightly constrained only where it matters.

## Entities

[[anthropic]], [[claude-code]], [[claude]]

## Concepts

[[context-engineering]], [[agent-instructions]], [[agent-skills]],
[[tool-design]], [[agent-steering]], [[agent-harness]]

## Notable claims & data

- Over 80% of Claude Code's system prompt removed, no measurable loss on
  Anthropic's coding evals (Opus 5 / Fable 5 named as examples).
- TodoWrite description ~9,100 characters → one line (from a figure).
- **Contradicts earlier guidance:** "give usage examples" in tool descriptions
  ([[anthropic-building-effective-agents]]; strengthened by `input_examples`,
  72% → 90%, in [[anthropic-eng-advanced-tool-use]], Nov 2025). This post
  (Jul 2026) says examples constrain the newest models. Reads as
  model-generation dependent; flagged for [[tool-design]].
- Partly supersedes [[anthropic-steering-claude-code]]'s framing of CLAUDE.md as
  a memory store (auto-memory now does that).

## Connections

Applies the progressive-disclosure and "let Claude manage context" ideas of
[[anthropic-eng-context-engineering]] and [[harnessing-claudes-intelligence]] to
Claude Code's own prompt. Rubric-driven verifier agents are the dynamic
workflows of [[anthropic-harness-for-every-task]]. Deferred tools are the
Tool Search mechanism of [[anthropic-eng-advanced-tool-use]]. Points readers to
the Fable prompting guide ([[anthropic-prompting-claude-fable-5]]); companion to
[[anthropic-prompting-claude-opus-5]].
