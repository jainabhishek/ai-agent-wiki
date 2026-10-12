---
title: "OpenAI: Shell + Skills + Compaction — Tips for Long-Running Agents"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Charlie Guo (OpenAI)
date: 2026-02-11
source_url: https://developers.openai.com/blog/skills-shell-tips
source_path: raw/openai-shell-skills-compaction.md
tags: [skills, shell, compaction, responses-api, long-running-agents, network-security]
---

# OpenAI: Shell + Skills + Compaction — Tips for Long-Running Agents

> OpenAI's launch-adjacent guide to three Responses API primitives — skills,
> the hosted shell tool, and server-side compaction — with ten practical tips
> and three build patterns, including production numbers from Glean.

## Summary

[[openai]] presents skills (aligned with the Agent Skills open standard), an
upgraded shell tool (OpenAI-hosted container with controlled internet access,
or a local shell you run), and server-side compaction (automatic, in-stream
when context crosses a threshold; or explicit via `/responses/compact`). The
division of labour: skills encode the *how*, shell executes the *do*,
compaction keeps long runs coherent. Tips cover writing skill descriptions as
routing logic with negative examples, placing templates inside skills, reusing
containers and `previous_response_id`, forcing determinism by naming the
skill, treating skills plus open networking as an exfiltration risk, using
`/mnt/data` as the artifact boundary, two-layer network allowlists, and
`domain_secrets`. Date from page byline: 2026-02-11.

## Key points

- **Descriptions are routing logic:** say when to use, when not to, and
  outputs/success criteria. See [[agent-skills]].
- **Negative examples fix misfires:** adding skills can initially *reduce*
  correct triggering; "don't call this skill when…" cases recover it.
- **Templates inside skills** cost nothing until invoked; Glean reports
  quality and latency gains. See [[context-engineering]].
- **Plan for long runs:** reuse the container, pass `previous_response_id`,
  use compaction by default rather than as a fallback.
- **Determinism lever:** instruct "Use the `<skill name>` skill" for
  production contracts.
- **Containment:** skills + open network = high exfiltration risk. Default:
  skills allowed, shell allowed, network only with a minimal per-request
  allowlist. Org allowlist caps request `network_policy` (out-of-org domains
  error). `domain_secrets` injects credentials via a sidecar; the model sees
  placeholders like `$API_KEY`. See [[guardrails]].
- **Same API local and hosted:** local mode returns `shell_call_output` for
  each `shell_call`; the Agents SDK accepts a custom shell executor. Start
  local, move hosted, keep skills identical. See [[openai-agents-sdk]].
- **Patterns:** A install → fetch → write artifact (`/mnt/data/report.md`);
  B skills + shell for repeatable workflows; C skills as enterprise workflow
  carriers.

## Entities

[[openai]], [[openai-agents-sdk]], [[openai-codex]], [[openai-agents-api]]

## Concepts

[[agent-skills]], [[context-engineering]], [[guardrails]], [[agent-harness]],
[[tool-design]]

## Notable claims & data

- Glean: skill-based routing first dropped triggering about 20% in targeted
  evals; recovered after negative examples and edge cases were added.
- Glean Salesforce skill: eval accuracy 73% → 85%; time-to-first-token −18.1%.
- Skills are framed as "living SOPs" that close an accuracy gap between single
  tool calls and multi-tool orchestration (Pattern C).
- No contradiction with existing pages. The skills metadata model (`name`,
  `description`, `path` exposed first) matches [[agent-skills]].

## Connections

Compare Anthropic's cache-safe compaction in
[[anthropic-prompt-caching-is-everything]] and context strategies in
[[anthropic-eng-context-engineering]]. Skill-authoring advice parallels
[[anthropic-lessons-building-claude-code-skills]] and
[[anthropic-eng-agent-skills]]. Skill testing is covered in
[[openai-testing-agent-skills-with-evals]]; repo use in
[[openai-skills-for-oss-maintenance]].
