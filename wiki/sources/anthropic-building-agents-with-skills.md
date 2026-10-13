---
title: "Anthropic: Building agents with Skills — equipping agents for specialized work"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com articles); Barry Zhang, Mahesh Murag, Keith Lazuka, Ryan Whitehead
date: 2026-01-22
source_url: https://claude.com/resources/articles/building-agents-with-skills-equipping-agents-for-specialized-work
source_path: raw/anthropic-building-agents-with-skills.md
tags: [skills, agent-architecture, progressive-disclosure, mcp, claude-code]
---

# Anthropic: Building agents with Skills — equipping agents for specialized work

> Anthropic's argument for one general code-driven agent plus a skills library, instead of a separate specialized agent per domain.

## Summary

The post (claude.com, 2026-01-22) says Anthropic "stopped building specialized agents" and builds skills instead. Its reasoning: code is a general interface for almost any digital work, so a general agent with bash and a filesystem (e.g. [[claude-code]]) covers many domains. What such an agent lacks is domain expertise. Skills supply that expertise as files: a folder with `SKILL.md`, supporting docs, and scripts. The post proposes a four-layer agent architecture: **agent loop** (reasons), **agent runtime** (executes code on a filesystem), **MCP servers** (connect to external systems), and **skills library** (guides with procedural knowledge). Each layer can change independently.

## Key points

- **Progressive disclosure with token sizes.** Only frontmatter metadata loads at start (~50 tokens per skill); the full `SKILL.md` loads when relevant (~500 tokens); reference files (2,000+ tokens) load only when needed. This lets one agent hold hundreds of skills. (see [[agent-skills]], [[context-engineering]])
- **Scripts as tools.** Code is self-documenting, modifiable, and need not sit in context, unlike fixed tool definitions. Example: Claude kept rewriting a slide-styling script, so it saved it as `apply_template.py` in the skill. (see [[tool-design]])
- **Files as the primitive.** Skills version in Git, share via Drive, and are authored by PMs, analysts, and domain experts as well as engineers; skill-creator gets a first skill working in under 30 minutes.
- **Ecosystem types.** Foundational (documents, spreadsheets, presentations), partner (K-Dense, Browserbase, Notion), enterprise (internal process and compliance).
- **Complexity is growing.** Status report writer ~100 lines; financial model builder ~800 lines; RNA-seq pipeline 2,500+ lines (HISAT2, StringTie, DESeq2).
- **Vertical deployment by skills.** Financial-services skills (DCF, comps, earnings, initiation coverage, due diligence, pitch materials) and life-sciences skills (scVI-tools, Nextflow, clinical-trial protocols, FHIR, prior authorization) on the same general agent.
- **Open standard.** Agent Skills is published as an open standard intended to be portable across platforms, like MCP.

## Entities

[[anthropic]], [[claude]], [[claude-code]], [[claude-agent-sdk]]

## Concepts

[[agent-skills]], [[agent-core-components]], [[context-engineering]], [[model-context-protocol]], [[tool-design]], [[agent-design-principles]]

## Connections

Engineering-blog counterpart: [[anthropic-eng-agent-skills]]. Authoring guide: [[anthropic-complete-guide-building-skills]]. MCP pairing: [[anthropic-agents-production-systems-mcp]]. Example skill: [[anthropic-improving-frontend-design-through-skills]]. Skills for verification: [[anthropic-verification-loops-with-skills]].
