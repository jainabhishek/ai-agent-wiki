---
title: "Anthropic: Using Claude Code — The Unreasonable Effectiveness of HTML"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Thariq Shihipar (Anthropic, claude.dev blog; personal opinion piece)
date: 2026-05-20
source_url: https://claude.dev/blog/using-claude-code-the-unreasonable-effectiveness-of-html/
source_path: raw/anthropic-unreasonable-effectiveness-of-html.md
tags: [anthropic, claude-code, output-format, html, human-in-the-loop, playbook]
---

# Anthropic: Using Claude Code — The Unreasonable Effectiveness of HTML

> A Claude Code team member argues for HTML instead of Markdown as the format
> for agent outputs that humans must read, review, share, or edit through a UI.

## Summary

Thariq Shihipar of [[anthropic]]'s [[claude-code]] team says Markdown limits
agent-to-human output. Long Markdown files go unread, they cannot show rich
visuals, and they are hard to share. He now asks Claude for HTML files. The
article is labeled as the author's personal opinion. He gives five reasons:
information density (tables, CSS, SVG, scripts, interaction, canvases, images),
readability, link-based sharing, two-way interaction, and Claude Code's access
to files, MCP servers, the browser, and git history. He lists five use cases:
specs and exploration, code review, design prototypes, reports, and custom
editing interfaces. The FAQ answers the token-cost objection by pointing to
"the 1MM context window in Opus 4.7". **Model dependence:** that cost argument
is tied to Claude Opus 4.7 as of 2026-05-20, and the wiki treats Opus 4.7 as a
prior generation. The format argument does not depend on the model.

## Key points

- **Human-facing outputs, not agent state.** The case is about artifacts that a
  person reads or edits: specs, plans, PR explainers, reports, prototypes.
- **A web of files instead of one plan.** The author makes exploration files,
  mockups, and an implementation plan. A fresh session receives all of them to
  implement, and the verification agent reads them too. See
  [[context-engineering]] and [[agent-orchestration]].
- **Throwaway editors with an export.** Ask for a single-file UI for the data
  at hand, such as a ticket triage board, a flag-config form, or a prompt
  tuner. It must end with a "copy as JSON/prompt/diff" button that feeds the
  result back to Claude Code. See [[agent-steering]].
- **Staying in the loop.** The author says HTML made him engage with Claude's
  plans again after he had started skimming them. See [[agent-steering]].
- **No special setup.** Ask for "an HTML file" or "an HTML artifact". Build a
  skill once a pattern recurs. See [[agent-skills]].

## Entities

[[anthropic]], [[claude-code]], [[claude]]

## Concepts

[[agent-steering]], [[context-engineering]], [[agent-skills]],
[[agent-orchestration]]

## Notable claims & data

- The author rarely reads a Markdown file longer than about 100 lines.
- HTML costs more tokens than Markdown. The author argues that being read more
  outweighs the cost. No measurement is given.
- The author says he has stopped using Markdown for almost everything and calls
  himself an "HTML maximalist".

## Contradictions / open questions

- [[context-engineering]] recommends Markdown checklists and status files as
  agent working state. That does not conflict with this post. Those files are
  agent-read state, and this post concerns human-facing outputs. The open
  question is whether HTML plans work as well as Markdown when a later agent
  session must parse and update them.

## Connections

- Complements the human-review guidance in [[anthropic-steering-claude-code]]
  and [[anthropic-eng-claude-code-best-practices]].
- Contrast with [[openai-run-long-horizon-tasks-codex]], which keeps durable
  plan and status files in Markdown for the agent to reread.
