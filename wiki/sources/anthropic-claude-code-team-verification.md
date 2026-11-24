---
title: "Anthropic: How the Claude Code Team Thinks About Verification"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Addy Osmani (Anthropic)
date: 2026-11-16
source_url: https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/
source_path: raw/anthropic-claude-code-team-verification.md
tags: [verification, testing, e2e-tests, property-tests, differential-tests, code-review, claude-code, skills, hooks]
---

# Anthropic: How the Claude Code Team Thinks About Verification

> The [[claude-code]] team's account of which tests let a coding agent verify its
> own work, and the rules the team uses to keep its verifiers and reviewers
> honest.

## Summary

Published 2026-11-16 on the claude.dev blog ("Engineering") by Addy Osmani of
[[anthropic]]. It follows [[anthropic-solving-code-review]], which Osmani co-wrote. The post
names no model. The thesis is that verification loops set how much work you can
delegate. Without them a person can run one or two Claude sessions, because the
person checks everything. With them a person can run dozens or hundreds. The
first half recommends three test types: end-to-end tests, property tests, and
differential tests. The second half lists the Claude Code team's own practices.
The central rules are to run the change end to end through a `verify` skill, to
keep checks out of reach of the change they judge, to start a new gate in observe
mode, to grade the reviewers against real bugs, and to turn misses into rules.

## Key points

### Why verification
- Claude writes and reviews about 90% of the Claude Code team's code.
- In internal tests on structured file generation, a separate grader that checks
  the work against a rubric raised task success by up to 10 points over a
  standard prompting loop. The largest gains were on the hardest problems.
- Agents generate tests, benchmarks, and specs cheaply, and the result runs as
  software with few extra tokens.
- If an agent keeps failing the same test, add a hook or a more explicit
  `CLAUDE.md` rule.

### Three test types
- **Failure modes for any test.** Flaky tests teach the agent to rerun instead of
  fix. Slow tests make the agent run fewer tests, so failures are harder to
  pinpoint. Run heavy tests before the commit.
- **End-to-end tests first.** If you pick one type, pick end-to-end. An agent can
  pass unit tests and still break the feature; an end-to-end test is hard to
  fool. Give the agent a skill that boots, drives, and inspects the app (CDP,
  simulators, API harnesses). A feature map with paths, shortcuts, selectors, and
  expected results serves as a rubric.
- **Property tests.** State a property that must hold and let a library
  (fast-check, Hypothesis, proptest) generate thousands of inputs. Properties:
  round-trip encoding, invariants, idempotency, and equivalence with a naive
  implementation. Generated inputs do not share the bias of the agent that wrote
  the code.
- **Differential tests.** For migrations, run the old and new systems on the same
  random or production-sampled inputs. Normalize irrelevant differences and keep
  a list of approved changes.

### The Claude Code team's practices
- **Run the change.** The team ranks an end-to-end run of the app above tests. Claude
  uses the Chrome extension for web, an iOS or Android MCP for mobile, computer
  use for desktop, or a local run for backend work. Put a skill named `verify`
  in `.claude/skills/`, near the code it tests. Claude uses it before each
  commit. Make it fast and reliable; it is the smoke-test harness.
- **Escalate after three rounds.** Claude fixes failing checks itself; a check
  that still fails after three rounds goes to a human.
- **Owners write checks.** A check that pulls in a reviewer states why.
- **Diff-triggered reliability checklist.** 39 items, each with a trigger
  readable from a diff, a check, and the incidents or PRs behind it. Claude runs
  only the items whose trigger matches, usually 3 to 10. Example item: "--resume
  loads old transcripts".
- **One reviewer, several rounds.** Tune the primary reviewer with a
  `REVIEW.md` instead of adding a second, more expensive reviewer. Each round
  gets context from earlier rounds and past failures.
- **Keep checks out of the change's reach.** Code Review takes `REVIEW.md`
  from the base or default branch and ignores the PR's copy. A review covers one
  commit; a pass on an out-of-date commit means nothing.
- **Cheap checks first.** Claude runs tests, build, and linter before it opens a
  PR. Enforce this with a hook on finish or a `/goal` of a passing suite.
- **Observe mode for new gates.** Each commit carries a stamp of how it was
  verified, including "none". A commit gate can block a commit if the session "did
  not contain /code-review or /verify" (the post's wording; it does not say
  whether one of the two is enough). It has three modes: off, observe (log
  only), and enforce. A commit message can explain a skipped verification. After
  two blocks in a session, the next commit passes so Claude does not get stuck.
- **Review the reviewers.** Track reverted merges, changes a maintainer rejected
  before merge, and a size-matched set of clean changes. The formal eval (attributed by the post to
  [[anthropic-solving-code-review]]; see Notable claims) recreates each repo at review time and
  scores only findings that match a one-sentence answer key. Merged, stable
  changes are the control, and the tuning set is separate from the test set.
  Recall is measured at three stages (raw findings, after verification, final
  review) to see where bugs are lost. Severity tags are Important, Nit, and
  Pre-existing. Recall is tuned until the next gain would overfit the eval.
- **Turn misses into rules.** A candidate rule mined from review comments and
  reverts must appear in at least two PRs and be visible in a diff. Three agents
  try to disprove it, and a human approves it in a PR. A replay of three bug
  finders against a known-incident PR counts the bug as detectable if two find
  it; a miss on a small diff becomes a `REVIEW.md` rule.
- **Flaky tests.** Skips, inserted sleeps, and retry-until-green are off limits.
  When Claude finds no root cause, the test is removed and the reason recorded.
- **Prune.** Test suites, verification steps, and `.md` rule files are tidied
  on a routine.

## Entities

[[anthropic]], [[claude-code]], [[claude]], [[claude-managed-agents]] (the
grader figure links to its launch post)

## Concepts

[[agent-verification]], [[agent-evals]], [[guardrails]], [[agent-skills]],
[[agent-steering]], [[agent-instructions]], [[human-agent-teams]],
[[agent-harness]]

## Notable claims & data

- Up to 10 points of task success from a separate rubric grader (internal test,
  structured file generation). The post gives no baseline or task count.
- **Tension with [[anthropic-securing-ai-native-sdlc]]:** the wiki summarizes
  that post as recommending many narrow reviewers instead of one mega-prompt. This post says a second,
  more expensive reviewer on top of the primary is often worse than tuning the
  primary. The two can fit: Code Review itself runs several parallel finders plus
  voters, so the advice may be against stacking review *layers*, not against
  parallel finders inside one reviewer.
- **Tension with [[anthropic-building-agents-claude-agent-sdk]]:** that post
  ranks rules-based checks (lint, types) first by robustness. This post says that
  if you pick one test type, pick end-to-end, and that running the app matters
  more than tests. The axes differ (robustness of a signal versus coverage of the
  feature).
- **Corroborates [[anthropic-ai-native-sdlc-playbook]]:** both keep the agent
  from editing the check that judges it. The playbook blocks test-file edits with
  a hook; this post reads `REVIEW.md` from the base branch.
- **Eval details not found in the cited post.** This post says the earlier code
  review post described the repo recreation, the one-sentence answer key, the
  tuning/test split, and three-stage recall. The 2026-11-24 capture of
  [[anthropic-solving-code-review]] has only the incident set, expert
  confirmation, the daily run, and the clean-PR control. The page may have
  changed, or the details may come from another post.
- The three-round escalation matches the three-round review cap in
  [[anthropic-solving-code-review]].

## Connections

This post builds on [[anthropic-solving-code-review]]; Addy Osmani wrote this
post and co-wrote that one. The `verify` skill and the chain of review skills are
described in [[anthropic-verification-loops-with-skills]], which the post links.
The rule to give the agent a runnable check repeats
[[anthropic-eng-claude-code-best-practices]] and
[[anthropic-claude-code-in-the-cloud]]. The `/goal` stop condition is in
[[anthropic-getting-started-with-loops]]. Differential tests for migrations match
the certificates in [[anthropic-ai-code-modernization]]. Turning misses into
rules parallels OpenAI's scoped review rules in
[[openai-codex-code-review-rules]] and the write-back loop in
[[anthropic-securing-ai-native-sdlc]]. Hook mechanics are in
[[anthropic-configure-hooks]].
