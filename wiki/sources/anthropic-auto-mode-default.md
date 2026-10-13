---
title: "Anthropic: Auto Mode Is Now the Default in Claude Code"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Conner Phillippi et al. (Anthropic, claude.com articles)
date: 2026-08-07
source_url: https://claude.com/resources/articles/auto-mode-default-in-claude-code
source_path: raw/anthropic-auto-mode-default.md
tags: [case-study, guardrails, permissions, classifiers, prompt-injection, claude-code, evals]
---

# Anthropic: Auto Mode Is Now the Default in Claude Code

> Launch post that makes auto mode the default for Pro, Max, and Team, backed by
> new safety evidence: a human-vs-classifier study, a harm re-grading of real
> sessions, third-party red-teaming, and a cross-vendor prompt injection test.

## Summary

Anthropic published this on 2026-08-07 (author Conner Phillippi, with John
Hughes among contributors); new Pro, Max, and Team sessions start in auto mode
from 2026-08-14, while Enterprise, API, and cloud-platform stay opt-in. All
figures are Anthropic's own or from vendors it commissioned. The case: manual
approval is habitual (users approve 97% of prompts) and many users already
bypass it (49.5% have a Bash allow rule; 25% of interactive sessions start in
bypass mode). Against that baseline, auto mode blocked far more planted
dangerous commands than humans did. Model-dependent results are dated: the
prompt injection test ran 2026-07-17 on Claude Fable 5, Opus 5, Sonnet 5, and
GPT-5.6 Sol. See [[guardrails]], [[claude-code]].

## Key points

- **Human vs. classifier (n=1,053 testers).** One prompt per session hid a
  dangerous command: humans caught 13.6%, auto mode blocked 89%. Auto mode
  blocked 800 that humans approved; humans blocked 6 that auto mode allowed.
  Human catch rate fell from about 17% early to about 5% after 50+ prompts;
  auto mode stayed flat.
- **Harm re-grading (May–June 2026, opted-in accounts).** At severity 7+
  (production-level), 6.3% of manually approved sessions had an unrequested
  harmful action vs. 2.4% for auto mode.
- **Red-teaming (Apollo Research).** Hardening came mainly from more classifier
  context (repo visibility, git state, data-handling rules). Miss rate on
  synthetic attacks fell from 12% to 7%; Anthropic says 7% is not a real-world
  miss rate.
- **Prompt injection (Trajectory Labs, 72 scenarios × 10 = 720 attempts).** 0
  successes on Claude Fable 5, Opus 5, Sonnet 5 in auto mode; GPT-5.6 Sol 5.83%
  (Codex Auto-review) and 19.03% (Full Access); Claude in `bypassPermissions`
  0.09%. Caveats: unequal effort settings (Sol at max, Claude at high); first-party
  browser safeguards not tested; OpenAI shipped a new Auto-review the week
  before.
- **New safeguards:** hard deny on data exfiltration; data-sharing rules
  (secrets vs. confidential; public vs. private vs. trusted push destinations);
  git-status check before destructive git commands; API-side injection probe.
- **Admin controls:** `defaultMode` and `disableAutoMode` in managed settings;
  `Shift+Tab` switches modes in the CLI.

## What is new versus [[anthropic-eng-claude-code-auto-mode]]

- New evidence types: the 1,053-tester study, the severity re-grading, Apollo
  red-teaming, the Trajectory Labs cross-vendor test, allow-rule adoption stats,
  the 39% vs. 3% plan-vs-permission rejection gap, and the 25% more PRs claim.
- New features: hard denies, data-sharing rules, git status checks, default
  rollout, free classifier overhead, admin keys.
- Unchanged: 3 consecutive / 20 total denial fallback; broad
  code-execution allow rules set aside while auto mode is on; the input-layer
  injection probe.
- **Figures that differ:** approval rate **97%** here vs. **93%** on the
  engineering page (2026-03-25); a different time window is likely but not
  stated. Miss rates are not comparable: 12%→7% here is on Apollo's synthetic
  attack sets, while the engineering page reports 17% FNR on 52 real overeager
  actions and 5.7% on 1,000 synthetic exfiltration cases. This post does not
  name the classifier model (the engineering page says Sonnet 4.6).

## Entities

[[anthropic]], [[claude]], [[claude-code]], [[openai-codex]], [[openai]]

## Concepts

[[guardrails]], [[agent-evals]], [[agent-steering]], [[agent-harness]]

## Notable claims & data

- Incidents caught inside Anthropic: a report push to a public code-sharing
  site; a mass kill across about 2,000 pods with GPU job deletions; a request
  for read-only billing access that reached for an account-root admin role.
- Customer claims (self-reported): Gusto about 10% of sessions hit a denial;
  Garner Health rolled out to 550 employees via managed settings. Details in
  [[anthropic-auto-mode-production]].

## Connections

- Follows [[anthropic-eng-claude-code-auto-mode]] (design) and
  [[anthropic-eng-how-we-contain-claude]] (sandbox layer).
- Companion customer write-up: [[anthropic-auto-mode-production]].
- OpenAI-side context on the compared product:
  [[openai-running-codex-safely]].
