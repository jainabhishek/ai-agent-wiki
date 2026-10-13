---
title: "Anthropic: How Claude Code Works in Large Codebases"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic Applied AI team
date: 2026-05-14
source_url: https://claude.com/resources/articles/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start
source_path: raw/anthropic-claude-code-large-codebases.md
tags: [claude-code, large-codebases, context-engineering, harness, lsp, adoption]
---

# Anthropic: How Claude Code Works in Large Codebases

> First article of Anthropic's "Claude Code at scale" series: how Claude Code
> navigates monorepos and legacy estates, the order in which to build its
> extension layer, and the organizational setup that made deployments succeed.

## Summary

Anthropic (2026-05-14), drawing on Applied AI deployments. [[claude-code]]
navigates by **agentic search** (file system traversal, grep, following
references) on the live code, with no central index. The article contrasts this
with RAG embedding pipelines that lag active codebases and return renamed or
deleted code without warning. The tradeoff is that agentic search needs good
starting context, so codebase setup matters. "The harness matters as much as the
model": five extension points built in order — `CLAUDE.md`, hooks, skills,
plugins, MCP servers — plus LSP integrations and subagents. Three patterns from
successful deployments: make the codebase navigable, re-review configuration as
models improve, and assign ownership for Claude Code configuration.

## Key points

- **Build order matters**: `CLAUDE.md` first, then hooks, skills, plugins, MCP.
  A common mistake is building MCP connections before the basics work.
- **Hooks for self-improvement**: a stop hook proposes `CLAUDE.md` updates from
  the session; a start hook loads team/module context; lint/format by hook is more
  consistent than by instruction. See [[agent-steering]].
- **Path-scoped skills** (e.g. a payments team's deploy skill bound to its
  directory) keep expertise out of unrelated sessions. See [[agent-skills]].
- **LSP over grep**: symbol-level navigation avoids thousands of grep hits and
  wrong same-named symbols; called one of the highest-value investments for
  multi-language codebases (one company deployed LSP org-wide for C/C++ before
  rollout). See [[tool-design]], [[context-engineering]].
- **Subagents split exploration from editing**: a read-only subagent maps a
  subsystem to a file, then the main agent edits. See [[agent-orchestration]].
- **Navigability**: lean, layered `CLAUDE.md` (root = pointers and gotchas);
  start Claude in a subdirectory (it walks up and loads every `CLAUDE.md`);
  per-subdirectory test/lint commands; committed `permissions.deny` rules in
  `.claude/settings.json` to exclude generated and third-party code; a root
  markdown codebase map when directories do not explain themselves.
- **Configuration decays with model upgrades**: a rule forcing single-file
  refactors hampers a newer model; a hook enforcing `p4 edit` became redundant
  when Claude Code added native Perforce mode. Review configuration every three
  to six months and after major model releases. See [[agent-harness]].
- **Ownership**: fastest rollouts had tooling built before broad access; owners
  sit in developer experience; an emerging "agent manager" role (hybrid
  PM/engineer); minimum is a DRI for settings, permissions, plugin marketplace,
  and `CLAUDE.md` conventions. Regulated orgs start with approved skills,
  required review, limited access, and a cross-functional working group.

## Entities

[[anthropic]], [[claude-code]]

## Concepts

[[context-engineering]], [[agent-harness]], [[agent-steering]], [[agent-skills]],
[[agent-orchestration]], [[model-context-protocol]], [[tool-design]]

## Notable claims & data

- Claude Code is said to perform better than teams expect in C, C++, C#, Java,
  and PHP, "particularly as of recent model releases" (as of 2026-05-14).
- Stated limits: codebases with hundreds of thousands of folders and millions of
  files, non-git version control, game engines with large binaries, and
  non-engineer contributors need extra work.

## Connections

Extends [[anthropic-steering-claude-code]] and
[[anthropic-eng-claude-code-best-practices]]; the agentic-search-over-RAG claim
repeats [[anthropic-seeing-like-an-agent]] and the Grep-over-vector-store history
on [[claude-code]]. Configuration decay is the same co-evolution point as
[[harnessing-claudes-intelligence]]. Related: [[anthropic-onboarding-claude-code-legacy-codebase]],
[[anthropic-ai-native-sdlc-playbook]], [[anthropic-subagents-in-claude-code]].
