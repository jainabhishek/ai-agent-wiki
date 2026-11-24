---
title: "Anthropic: How the Claude Code Team Does Code Review"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Addy Osmani, Morgan Westlee Lunt, and Qing Wang (Anthropic)
date: 2026-10-15
source_url: https://claude.dev/blog/solving-code-review-at-anthropic/
source_path: raw/anthropic-solving-code-review.md
tags: [code-review, verification, human-in-the-loop, risk-tiers, agent-evals, claude-code, sdlc]
---

# Anthropic: How the Claude Code Team Does Code Review

> How the [[claude-code]] team reviews code when Claude writes about 90% of it:
> layered checks with rollback beneath them, human approval scaled by risk, an eval built from past
> incidents, and changes that make agent-on-agent review converge.

## Summary

Published 2026-10-15 on the claude.dev blog ("Engineering") by Addy Osmani,
Morgan Westlee Lunt, and Qing Wang of [[anthropic]]. The URL slug is
`solving-code-review-at-anthropic`, but the page headline is "How the Claude Code
team does code review". The post names no model. The team's goal is the least
human review time that does not raise reverts or incidents. Most reading moved to
machines, and review became continuous instead of a gate at the end. The body
numbers seven steps: verification before the PR, AI review, a blocking security
review, blocking CI, human approval scaled by risk, a merge queue with flags and
staged release, and fast rollback. Fig B instead counts six layers with fast
rollback beneath them, and Figs A and B place CI before AI review. The reviewer is scored daily against an eval
built from past incidents. The team cut review rounds after it found that agent
authors and agent reviewers did not converge.

## Key points

### Scale and goal
- Claude writes about 90% of Claude Code's code. From June to September, merged
  PRs to Claude Code more than doubled, and the share reverted fell by more than
  40%.
- In Anthropic's monorepo, changes landing per day rose from about 2,500 (May) to
  more than 30,000 (September).
- Code review has two jobs: find issues before they ship, and spread codebase
  understanding. The post calls "did a human read the code?" an imprecise proxy
  for "what could go wrong, and which check should catch it?".
- Goal: most PRs merge with at most one human in the loop, who can be the author.
  Metrics: human approvals per PR (median and p95), human comments, and time a PR
  waits on a person. Revert and incident rates are the guardrail.

### The layers (the body's seven numbered steps)
1. **Verified before review.** Claude runs something (tests, a build, a
   screenshot compared with the design) and shows the output. A fresh-context
   subagent reviews the diff. Boris Cherny estimates that a way to verify makes
   the result 2–3x better. Repeated reviewer flags are fixed at the source: a
   skill, a lint rule, `CLAUDE.md`, or `REVIEW.md`. A good `REVIEW.md` is short,
   says what failure looks like in that repo, caps nits, lists paths to skip,
   requires file-and-line evidence, and asks for a summary that starts with a
   count.
2. **AI review on every PR.** Code Review for Claude Code is generally available
   on Team and Enterprise plans; `/code-review` is a lighter local version. At
   the research-preview launch, internal PRs with substantive comments rose from
   16% to 54%. Repos are set to Quick, Standard, or Deep. Several agents hunt
   bugs in parallel, a separate group votes on each finding, and only findings
   with enough agreement are posted. Style-only findings are dropped (A/B
   tested). Tags: Important, Nit, Pre-existing. Every finding must be fixed or
   resolved with a reason.
3. **Blocking security review.** No merge while any bug or security finding is
   open; a fixing commit clears the finding.
4. **Blocking CI.** Lint, types, tests on every platform, build. The PR template
   asks how the change was tested and how to undo it; the requesting person
   signs off.
5. **Human approval by risk.** Low risk (docs, copy, flagged additive changes):
   no human once checks are green. Medium (ordinary changes; caching, the
   auto-updater, system prompts): one person. High: two people. A classifier
   assigns the tier from what changed, not from who wrote it, and a second classifier can
   add a person. Owner-listed sensitive paths and CI workflow files always need a
   person. Only trusted authors get the lighter paths. An agent's approval never
   counts as a person's. The person who prompted an agent-written PR counts as a
   required reviewer. An approval covers one commit.
6. **Merge queue, flags, staged release.** Checks rerun on main with the change
   applied. New behavior goes behind a flag to employees first, then to the
   latest channel, then stable.
7. **Fast detection and rollback.** Flags can be switched off with no deploy; a weekly
   on-call rotation; incident reviews ask which layer should have caught it.
   There are no circuit breakers yet that tighten approval when revert or
   incident numbers rise; engineers want them before more zero-human merges.

### Improving the reviewer
- **Incidents are the eval.** Past PRs that caused incidents (with fix-forwards
  and reverts) were confirmed by engineers who know the code. The reviewer runs
  against the set daily. A change to its prompts, tools, or model is kept only if
  the score rises.
- **Noise is measured by response.** Each comment is sorted by what the author
  did: fixed it, called it wrong, called the behavior intentional, or decided it
  did not matter. The reviewer also runs on known-clean PRs. The written priority
  is real bugs first, fewer rounds second.
- **Noise costs more with agent authors.** An agent fixes every nit, which adds a
  commit and a review round.
- **Review must converge.** One PR went through more than fifty overnight rounds.
  About 59% of repeat flags were code present since the first pass. Fixes: a
  three-round cap after which the reviewer asks the author to reconsider the
  approach; diff-only re-review after the first few passes; flag the bug class,
  not one line; no repeated findings. Results (internal PRs, before → after): pass
  after one round 65% → 78%; five or more rounds 8.9% → 1.5%; mean reviews to
  pass 2.08 → 1.32.
- Review agents also run nightly over existing code.

### Humans and team norms
- Humans keep: deciding whether to build it; risky code (billing, the
  auto-updater, CI workflows); architecture that sets a pattern; reading the
  evidence; owning the outcome.
- Shared understanding comes from asking Claude for an explainer of one slice of
  the code, sometimes as a visual artifact, and from working in open Slack
  channels. There is no formal process.
- "You land it, you own it": small, reversible changes; blast radius sets the
  bar; incident reviews look at the system, not the person.
- Raise a change of direction early in the thread, not as a blocking comment on a
  finished PR.

### Adoption checklist
- Before the PR: runnable checks in a short `CLAUDE.md`; formatter and linter
  hooks; local `/code-review` and `/security-review`; a `REVIEW.md`.
- On every PR: required CI; "Testing", "Risk", and "How to revert" in the
  template; an AI reviewer on one repo first; security review; all threads
  resolved; effort matched to risk; capped rounds.
- Approval: written risk tiers set from the change; trusted-author lists;
  CODEOWNERS and branch protection for auth, billing, CI and release workflows,
  and installers; no bot approval in a human slot; dismiss approvals on new
  commits.
- After merge: merge queue, flags, internal use, staged releases, one-step
  rollback; an incident eval rescored on every reviewer change.

## Entities

[[anthropic]], [[claude-code]], [[claude]]

## Concepts

[[agent-verification]], [[agent-evals]], [[guardrails]],
[[human-agent-teams]], [[agent-orchestration]], [[agent-instructions]],
[[agent-steering]], [[agent-skills]]

## Notable claims & data

- All figures are self-reported by Anthropic. The before/after review-round
  numbers come from Fig D; the post does not give the measurement window or PR
  counts.
- **Attribution of 16% → 54%:** [[anthropic-securing-ai-native-sdlc]] ties the
  rise to the rule that agents must prove each finding. This post ties it to the
  launch of the Code Review research preview. Both can be true if proof-writing
  was part of that launch; neither source says so.
- **Code Review status changed:** [[anthropic-ai-native-sdlc-playbook]] and
  [[anthropic-verification-loops-with-skills]] describe Code Review as a research
  preview. This post (2026-10-15) says it is generally available on Team and
  Enterprise plans.
- **Share of code written by Claude:** [[anthropic-agentic-coding-ci-test-impact]]
  reports 80% for Anthropic. This post reports about 90% for Claude Code. The
  scopes differ (company versus one team).
- **Agent approval:** Code Review posts findings, not approvals. The team's own
  repos let low-risk changes merge on automated checks alone.

## Connections

The follow-up post [[anthropic-claude-code-team-verification]] (by Addy Osmani)
goes deeper on verification. It attributes eval details to this post that the
capture of this post does not contain. The team norms extend
[[anthropic-running-ai-native-engineering-org]]. The CI layer links to
[[anthropic-agentic-coding-ci-test-impact]]. The parallel finders and risk-tiered
humans match [[anthropic-securing-ai-native-sdlc]]. The `REVIEW.md` practice
matches [[anthropic-ai-native-sdlc-playbook]] and parallels scoped `AGENTS.md`
review rules in [[openai-codex-code-review-rules]]. The review-skill chain is in
[[anthropic-verification-loops-with-skills]]. Asking Claude for an explainer
artifact links to [[anthropic-unreasonable-effectiveness-of-html]], which the
post cites; skills at scale are in
[[anthropic-lessons-building-claude-code-skills]]. Capped generator-verifier
loops are discussed in [[anthropic-multi-agent-coordination-patterns]].
