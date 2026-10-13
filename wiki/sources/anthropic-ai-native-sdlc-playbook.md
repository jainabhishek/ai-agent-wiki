---
title: "Anthropic: The AI-Native SDLC Playbook"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Louis Claxton (Anthropic Applied AI)
date: 2026-08-21
source_url: https://claude.com/resources/articles/the-ai-native-sdlc-playbook
source_path: raw/anthropic-ai-native-sdlc-playbook.md
tags: [sdlc, governance, claude-code, hooks, skills, evals, ci-cd, enterprise]
---

# Anthropic: The AI-Native SDLC Playbook

> A stage-by-stage playbook (plan, design, build, test, deploy, maintain) for
> rebuilding the software lifecycle around agentic coding while keeping
> governance, with concrete config files, gates, and metrics per "play".

## Summary

Anthropic Applied AI guide (2026-08-21). Thesis: once agents make the build stage
fast, the bottleneck moves to the human-speed stages around it (plan,
review/test, deploy), line-by-line review stops matching reality, and governance
by committee gets expensive. The AI-native SDLC keeps the old control objectives
but enforces them as the agent acts, and turns the linear flow into a **loop of
committed artifacts**: `intent.md` → `spec.md` → `plan.md` → diff and tests → PR
with review findings → incident record → new `intent.md`. Each accepted artifact
triggers the next stage; the commit chain is the audit trail. Each "play" lists
prerequisites, infrastructure, steps, governance (what is enforced, evidence,
logging, approver), and leading/lagging indicators. Uses [[claude-code]] plan
mode, auto mode, `CLAUDE.md`, skills, hooks, subagents, worktrees, `claude -p` in
CI, managed settings, Claude Security, and Claude Tag.

## Key points

- **Plan/Design**: the originator writes `intent.md` with Claude (problem,
  outcome, affected systems, constraints, open questions); a non-interactive job
  on its merge produces `spec.md` with org policy skills loaded and concerns
  flagged. A human product owner accepts each artifact.
- **Build**: plan mode by default, `plan.md` committed and kept in sync with the
  diff; auto mode becomes the default for routine, well-tested, small-blast-radius
  work once guardrails mature. Name one source of truth per artifact when legacy
  tools (Jira, ServiceNow) exist; linkage (record ID ↔ commit SHA) is the minimum.
- **Skill vs hook**: a skill is an **advisory** control (makes compliance
  likely); a hook is the **deterministic** layer behind it. Policies that must
  always hold need both. Build hooks must be fast and file-scoped; human-approval
  hooks belong at deploy gates, not in build, or a person sits on the critical
  path of every parallel session. See [[agent-steering]], [[guardrails]].
- **`CLAUDE.md` rule**: a mistake made twice goes into `CLAUDE.md`; keep it under
  a page. See [[agent-instructions]].
- **Parallel sessions vs subagents**: worktree-isolated sessions raise tasks in
  flight; subagents (e.g. a report-only verifier) keep each session focused.
  Ceiling = what one person can review. See [[agent-orchestration]].
- **Feedback loop**: one-command checks with quantified targets; failing test
  first for bug fixes; a hook blocks test-file edits during fixes so the agent
  cannot weaken its own check. See [[agent-evals]].
- **Evals as configuration CI**: 20–50 real tasks; run on schedule and on any
  change to `CLAUDE.md`, skills, or hooks; gate config changes on pass rate; each
  incident becomes an eval.
- **Deploy**: identical AI review passes on every PR via `REVIEW.md`
  (bugs/security/compliance, severity definitions, nit cap); the authoring agent
  cannot approve (separation of duties); hooks express approval gates; agent acts
  up to the production gate and never past it; deploy/rollback exposed as
  per-environment MCP tools; rollback is the most rehearsed path.
- **Managed settings worked example** for regulated enterprises: deny/allow
  lists, no bypass mode, sandbox that fails closed with a domain allowlist and
  credential-file/env denial, managed-only hooks/MCP/marketplaces, minimum
  version floor. Tool-level denies do not stop shell egress; the OS sandbox does.
- **Maintain**: deterministic detection (rolling mean/σ with Western Electric
  rules) invokes Claude only on breach; tiers in `bands.yaml` (1σ log, 2σ
  read-only diagnosis, 3σ PR or pre-approved runbook); findings re-enter as
  `intent.md`. Scheduled model-based security scans treat findings the same way.

## Entities

[[anthropic]], [[claude-code]], [[claude]], [[claude-agent-sdk]]

## Concepts

[[agent-steering]], [[guardrails]], [[agent-evals]], [[agent-instructions]],
[[agent-skills]], [[agent-orchestration]], [[workflow-patterns]],
[[agent-harness]], [[model-context-protocol]]

## Notable claims & data

- Example managed settings pin `requiredMinimumVersion` "2.1.193"; values are
  illustrative and the article says to tailor, not copy.
- Claude Security (public beta, Claude Enterprise) runs scheduled scans on
  Claude Mythos 5 with validated findings and confidence ratings, billed at
  Mythos 5 rates — product details as of 2026-08-21.
- Managed Code Review is described as a research preview; Claude Design as beta;
  Claude Tag as public beta in Slack.

## Connections

Expands [[anthropic-steering-claude-code]] and
[[anthropic-eng-claude-code-best-practices]] to the whole lifecycle; sandbox and
permission rationale matches [[anthropic-eng-claude-code-sandboxing]] and
[[anthropic-eng-claude-code-auto-mode]]. Companion posts:
[[anthropic-securing-ai-native-sdlc]], [[anthropic-ai-ci-cd-on-call]],
[[anthropic-ai-code-modernization]], [[anthropic-running-ai-native-engineering-org]].
OpenAI's comparable view: [[openai-harness-engineering]].
