---
title: "OpenAI: Using Skills to Accelerate OSS Maintenance"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Kazuhiro Sera (OpenAI)
date: 2026-03-09
source_url: https://developers.openai.com/blog/skills-agents-sdk
source_path: raw/openai-skills-for-oss-maintenance.md
tags: [skills, codex, agents-md, ci, code-review, release-engineering]
---

# OpenAI: Using Skills to Accelerate OSS Maintenance

> How OpenAI maintains the Python and TypeScript Agents SDK repos with Codex:
> repo-local skills, mandatory if/then rules in `AGENTS.md`, scripts for
> mechanics, model judgment for interpretation, and the Codex GitHub Action
> for CI.

## Summary

The [[openai-agents-sdk]] maintainers keep recurring workflows as skills in
`.agents/skills/` and make them mandatory through short if/then rules in
`AGENTS.md` (for example: run `$code-change-verification` when runtime code,
tests, examples, or build behavior change, and do not mark work complete until
it passes). Each skill has a narrow contract, clear trigger, and concrete
output. Skill `description` fields are written as routing contracts. Mechanics
(fixed-order verification commands, example runners, tag fetches) live in
`scripts/`; interpretation (comparing example logs with source intent, judging
release diffs) stays with the model. Release review defaults to "safe" and
blocks only on concrete evidence with an unblock checklist. Codex PR auto
review is the required path for routine correctness; humans decide among valid
design options. Date from page byline: 2026-03-09.

## Key points

- **Skill inventory:** Python — `code-change-verification`, `docs-sync`,
  `examples-auto-run`, `final-release-review`, `implementation-strategy`,
  `openai-knowledge`, `pr-draft-summary`, `test-coverage-improver`; JS adds
  `changeset-validation`, `integration-tests`, `pnpm-upgrade`. See
  [[agent-skills]].
- **AGENTS.md makes skills mandatory;** the skill defines "verified". Keep
  AGENTS.md small with highest-value rules first; it also holds public-API
  compatibility rules. See [[agent-instructions]], [[agent-steering]].
- **Descriptions route:** add *when* and *whether mandatory*, not only *what*;
  fix metadata before adding code.
- **Model vs. script split:** if the model rediscovers the same shell recipe,
  make it a script; scripts are tiny CLIs with deterministic stdout that fail
  loudly. See [[tool-design]], [[agent-design-principles]].
- **Model-judged integration tests:** runners capture per-example
  stdout/stderr; Codex compares each log with the example's source intent,
  since a zero exit code is insufficient. JS also tests published packages via
  local Verdaccio on Node.js, Bun, Deno, Cloudflare Workers, and Vite React.
- **Report-first skills** (`docs-sync`, `test-coverage-improver`) ask for
  approval before edits.
- **CI security:** limit triggers, sanitize untrusted PR/issue input, protect
  `OPENAI_API_KEY` (`drop-sudo` or unprivileged user), run Codex last. See
  [[guardrails]].
- **Review split:** Codex for bugs, regressions, missing tests; humans for API
  and architecture choices, compatibility and rollout, naming and release
  communication, cross-team alignment.

## Entities

[[openai]], [[openai-codex]], [[openai-agents-sdk]]

## Concepts

[[agent-skills]], [[agent-instructions]], [[agent-steering]], [[tool-design]],
[[guardrails]], [[agent-evals]], [[agent-verification]]

## Notable claims & data

- Merged PRs: 457 (1 Dec 2025 – 28 Feb 2026) vs. 316 in the prior three months
  (Python 182 → 226; TypeScript 134 → 231). Attributed by the author to
  skills, AGENTS.md, Actions, and Codex PR review together; no controlled
  comparison.
- Downloads (30-day windows as of 2026-03-06): ~14.7M PyPI, ~1.5M npm.
- Release-review example (openai-agents-python #2480): green overall with the
  Python 3.9 drop flagged moderate risk.
- Claim that Codex as the required reviewer for routine correctness is "safe
  enough in practice" is OpenAI's own assessment.
- No contradiction found; the AGENTS.md-as-mandatory-trigger pattern parallels
  CLAUDE.md guidance in [[anthropic-steering-claude-code]].

## Connections

Repo-scale application of [[openai-shell-skills-compaction]] and
[[openai-testing-agent-skills-with-evals]]. Compare Anthropic's skill guidance
in [[anthropic-lessons-building-claude-code-skills]] and steering taxonomy in
[[anthropic-steering-claude-code]]. Related: [[openai-automating-repetitive-work-codex]],
[[openai-codex-as-a-platform]].
