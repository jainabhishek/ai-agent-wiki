---
title: OpenAI Codex
type: entity
subtype: product
created: 2026-10-12
updated: 2026-10-12
tags: [openai, codex, coding-agent, harness]
---

# OpenAI Codex

> OpenAI's coding agent, and the open-source agent harness behind it. The same
> harness runs the Codex app, CLI, IDE extension, and the [[openai-agents-api]].

## Overview

OpenAI presents the Codex harness as a reusable agent runtime, separate from any
one product. The host application owns the UI, context, tools, approvals, and the
system of record. The harness owns the agent loop. (see
[[openai-codex-as-a-platform]])

Most of OpenAI's 2026 guidance on skills, `AGENTS.md`, and long-running agents is
written against Codex. (see [[openai-shell-skills-compaction]],
[[openai-testing-agent-skills-with-evals]],
[[openai-skills-for-oss-maintenance]],
[[openai-rethinking-skills-prompts-gpt-6-astra]])

## Key facts

- The harness is open source at `github.com/openai/codex`. (see
  [[openai-codex-as-a-platform]])
- It has three integration layers: `codex exec` for scripts, the Codex SDK, and
  app-server. The app-server protocol covers threads, turns, events, and approval
  requests. (see [[openai-codex-as-a-platform]])
- OpenAI reports that harness settings alone (kept reasoning plus compaction)
  raised GPT-5.6 Sol on ARC-AGI-3 from 13.3% to 38.3%, with six times fewer
  output tokens. The figure comes from a separate OpenAI post that the wiki has
  not captured. (see [[openai-codex-as-a-platform]])
- When many skills are loaded, Codex shortens skill descriptions. This makes
  short, distinct descriptions matter. (see
  [[openai-rethinking-skills-prompts-gpt-6-astra]])
- Named features include persistent goals and automatic approval review. (see
  [[openai-automating-repetitive-work-codex]])
- OpenAI ships an `$openai-docs` skill for migrating prompts to GPT-6. (see
  [[openai-prompting-gpt-6-astra]])
- OpenAI uses Codex in CI and review for the [[openai-agents-sdk]] repositories.
  (see [[openai-skills-for-oss-maintenance]])

## Relationships

- Built by [[openai]]. Runs inside the [[openai-agents-api]].
- Plays the role for OpenAI that [[claude-code]] plays for [[anthropic]]: the
  first-party coding agent and the testbed for skills and harness guidance.

## Appears in

- [[openai-codex-as-a-platform]]
- [[openai-automating-repetitive-work-codex]]
- [[openai-rethinking-skills-prompts-gpt-6-astra]]
- [[openai-shell-skills-compaction]]
- [[openai-testing-agent-skills-with-evals]]
- [[openai-skills-for-oss-maintenance]]
- [[openai-private-mcp-servers]]

## Contradictions / open questions

- _None recorded._
