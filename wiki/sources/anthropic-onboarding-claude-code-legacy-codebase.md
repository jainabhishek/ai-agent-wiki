---
title: "Anthropic: Onboarding Claude Code Like a New Developer (MacCoss Lab, Skyline)"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com articles)
date: 2026-04-28
source_url: https://claude.com/resources/articles/onboarding-claude-code-like-a-new-developer-lessons-from-17-years-of-development
source_path: raw/anthropic-onboarding-claude-code-legacy-codebase.md
tags: [case-study, claude-code, legacy-code, agent-skills, mcp, context-engineering, open-source]
---

# Anthropic: Onboarding Claude Code Like a New Developer (MacCoss Lab, Skyline)

> Case study: a 17-year-old, 700,000-line C# scientific codebase onboards
> [[claude-code]] with the same method it uses for trainee developers — a
> versioned context repository plus skills and MCP servers.

## Summary

Published 2026-04-28 by [[anthropic]] on claude.com articles, with no individual
byline. The subject is Brendan MacLean, principal developer of Skyline at the
University of Washington's MacCoss Lab. The post describes him as a Claude Developer
Ambassador whose lab is in the Claude for Open Source program. A footnote discloses
that Anthropic co-founder Dario Amodei was once a member of the lab. All results are
self-reported by the lab and the publisher.

MacLean found browser chat unworkable for incremental changes because each session
started from zero. He then treated Claude like a trainee: a contained first project,
and better recorded context after each round. All AI context lives in a separate
repository, `pwiz-ai`, so it applies across branches and points in time.

## Key points (transferable design lessons)

- **CLAUDE.md is the lay of the land; skills hold the expertise.** The root
  `CLAUDE.md` covers environment setup and points to docs. Domain knowledge lives
  in [[agent-skills]].
- **"Reference do not embed."** Each skill points into a central documentation
  knowledge base instead of copying it, so skills stay light.
- **Explicit triggers for critical skills.** The `debugging` skill description says
  to always load it for bugs, failures, or unexpected behavior. The skill forces
  root-cause analysis before any fix, instead of "guess and test".
- **Context is a maintained artifact.** Plans and to-do lists do not persist;
  recorded context does. Version it and grow it like code. A separate context repo
  suits context that changes at a different speed than code; the same repo also works.
- **MCP where live data matters.** Claude wrote a C# MCP server to view screenshot
  diffs and a Python MCP server over test results, team email, and GitHub release
  tags (see [[model-context-protocol]]).

## Notable claims & data (self-reported)

- Codebase: 700,000+ lines of C#, 200,000+ automated nightly tests, in development
  since 2008.
- A year-long abandoned Files View feature was finished in two weeks with Claude
  Code; all final commits were co-authored by Claude.
- A test-management module frozen for three years got new features and CSS layout
  in under a day.
- Reproduction of 2,000+ tutorial screenshots is fully automated and nearly 100%
  reproducible. A daily Claude Code summary reports test failures, exceptions,
  and open support threads.

## Connections

A long-lived-codebase companion to [[anthropic-claude-code-large-codebases]] and
[[anthropic-eng-claude-code-best-practices]]. The skill-library lessons match
[[anthropic-lessons-building-claude-code-skills]] and
[[anthropic-complete-guide-building-skills]]. The context-as-artifact framing fits
[[context-engineering]].
