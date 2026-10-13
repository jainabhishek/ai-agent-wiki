---
title: "Anthropic: A Field Guide to Claude Fable 5 — Finding Your Unknowns"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Thariq Shihipar (Anthropic)
date: 2026-07-06
source_url: https://claude.com/resources/articles/a-field-guide-to-claude-fable-finding-your-unknowns
source_path: raw/anthropic-fable-field-guide-unknowns.md
tags: [claude-code, agentic-coding, planning, workflow, human-in-the-loop, best-practices]
---

# Anthropic: A Field Guide to Claude Fable 5 — Finding Your Unknowns

> A workflow guide for [[claude-code]] that treats the gap between what the user
> specifies and what the task needs ("unknowns") as the main limit on agent output
> quality, with patterns to surface unknowns before, during, and after implementation.

## Summary

Published 2026-07-06 on claude.com articles by Thariq Shihipar of [[anthropic]]. The
post is framed around Claude Fable 5, which the author calls the first model whose
work quality is limited by the user's ability to clarify unknowns. Fable 5 is now a
legacy model (see [[anthropic-prompting-claude-fable-5]]). The patterns themselves are presented as a general way of working, so
this page carries no `models:` scope. Readers should treat the opening model claim as
dated to July 2026.

The author splits a problem into four categories: known knowns (what the prompt
says), known unknowns, unknown knowns (obvious criteria one recognizes only on
sight), and unknown unknowns. Too-specific instructions make Claude follow a path
even when a pivot is better. Too-vague instructions make Claude fill gaps with
generic best practice. The fix is to tell Claude your starting point and use it as a
thought partner to find unknowns early, when they are cheap.

## Key points

- **Pre-implementation patterns.**
  - *Blind spot pass*: ask Claude to find and explain your "unknown unknowns" in
    an unfamiliar codebase area or domain. State who you are and what you know.
  - *Brainstorms and prototypes*: surface unknown knowns with throwaway HTML mocks
    or several divergent design directions before wiring real code. Spec changes
    found late can force very different code that an agent finds hard to revert.
  - *Interviews*: Claude asks one question at a time, prioritizing questions whose
    answers would change the architecture.
  - *References*: point Claude at source code (even in another language) as the
    richest spec. The author ranks code above diagrams or screenshots.
  - *Implementation plan*: lead with what is most likely to change (data models,
    type interfaces, UX flows); put mechanical refactoring last.
- **During implementation.** Implement in a fresh session seeded with the planning
  artifacts (spec, prototype). Have Claude keep `implementation-notes.md` and log
  forced deviations under "Deviations", choosing the conservative option.
- **Post implementation.** Build pitch and explainer artifacts for reviewers. Ask
  for an HTML report with a quiz on the change; the author merges only after
  passing it.
- **Worked example.** The Fable launch video was edited end-to-end in Claude Code
  (Whisper-style transcription, ffmpeg cuts, a Remotion prototype). The author
  then asked Claude to teach color grading after realizing he had no quality bar.

## Entities

[[anthropic]], [[claude-code]], [[claude]]

## Concepts

[[context-engineering]], [[agent-instructions]], [[agent-steering]],
[[agent-design-principles]]

## Notable claims & data

- The known/unknown 2x2 and the claim that "reducing and planning for your
  unknowns" is the core skill of agentic coding.
- Plan in one session, implement in a fresh one with artifacts passed in: a
  context-reset pattern consistent with [[context-engineering]].
- The post points to [[anthropic-new-rules-context-engineering-claude-5]] for the
  context side of Fable-generation models.

## Connections

Same author as [[anthropic-claude-code-session-management]]. Complements
[[anthropic-eng-claude-code-best-practices]] (explore, plan, code) and
[[anthropic-unreasonable-effectiveness-of-html]] (HTML artifacts for plans,
mocks, and reports). The interview and plan-review steps parallel the
human-in-the-loop patterns in [[anthropic-getting-most-out-of-opus-5-5]].
