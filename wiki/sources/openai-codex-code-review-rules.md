---
title: "OpenAI: Custom Code Review Rules for Codex"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Hari Srikanth (OpenAI Developers blog)
date: 2026-07-20
source_url: https://developers.openai.com/blog/custom-code-review-rules-for-codex
source_path: raw/openai-codex-code-review-rules.md
tags: [openai, codex, code-review, agents-md, evals, instructions]
---

# OpenAI: Custom Code Review Rules for Codex

> How Codex Code Review reads scoped repository rules from `AGENTS.md`, with eval
> results and rules for writing review guidance that finds real issues without
> noise.

## Summary

[[openai-codex]] Code Review can apply custom repository rules written in
`AGENTS.md` and cite the rule in each finding. The motivation is volume: weekly
PR volume at [[openai]] more than doubled since Q4, so review became the
bottleneck. Some invariants are invisible in a diff. The worked example renames
the experimental notification `rawResponseItem/completed`, which compiles but
breaks Codex Cloud listeners. A breaking-change rule in the Codex repo's
`AGENTS.md` catches it. An eval suite showed rule-guided review recovered 98%
of required custom findings vs 58.3% for the baseline control. The post names no
model.

## Key points

- **Rules live next to the code.** Repo-wide rules go in the root `AGENTS.md`;
  service rules go in a nested `AGENTS.md`. Review applies only the rules that
  cover the changed files. See [[agent-instructions]].
- **Write each rule as an invariant plus a safe path.** Name the risk and the
  alternative, for example "keep the name or add a backward-compatible event".
- **Include only consequential, non-obvious rules.** If removing a rule would
  not change the review, delete it. Describe outcomes, not function names.
  Prune rules that keep producing noise.
- **Use rules for judgment, CI for mechanics.** Keep formatting and
  deterministic checks in tests and linters.
- **Four eval axes:** coverage (busy diffs, competing rules), restraint (clean
  changes and valid exceptions stay quiet), retention (ordinary bugs still
  caught), and actionability (finding names guidance, location, priority). See
  [[agent-evals]].
- **Three-change test per rule:** one change that should trigger the rule, one
  safe counterexample, and one unrelated change. Request a review with
  `@codex review`.
- Broad instructions created noise. Small, scoped rule sets worked best.
- Code Review is an extra reviewer. Tests, branch protection, and required
  approvals remain the hard enforcement. See [[guardrails]].

## Entities

[[openai]], [[openai-codex]]

## Concepts

[[agent-instructions]], [[agent-evals]], [[guardrails]], [[agent-steering]],
[[boundary-contracts]]

## Notable claims & data

- 98% vs 58.3% recovery of required custom findings (primary suite; known
  violations plus safe counterexamples). Suite size and model not disclosed.
- Weekly PR volume at OpenAI more than doubled since Q4 (chart only).
- The `rawResponseItem/*` rule was added to protect Codex Cloud consumers
  (openai/codex PR #29086).

## Connections

- Applies the "keep `AGENTS.md` small, highest-value rules first" guidance in
  [[openai-skills-for-oss-maintenance]] and the pointer-not-blanket-rule advice
  in [[openai-rethinking-skills-prompts-gpt-6-astra]] to review rather than
  authoring.
- The positive/negative/unrelated test set mirrors the trigger evals in
  [[openai-testing-agent-skills-with-evals]].
- The renamed-field example is an integration-surface boundary bug of the kind
  described in [[boundary-contracts]]: it compiles, and only a recorded contract
  or rule catches it.
