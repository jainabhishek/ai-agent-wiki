---
title: "OpenAI (Eng): Harness engineering — leveraging Codex in an agent-first world"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Ryan Lopopolo (OpenAI)
date: 2026-02-11
source_url: https://openai.com/index/harness-engineering/
source_path: raw/openai-harness-engineering.md
tags: [openai, codex, agent-harness, harness-engineering, agents-md, context-engineering, architecture, linting, autonomy, primary-source]
---

# OpenAI (Eng): Harness engineering — leveraging Codex in an agent-first world

> OpenAI's account of building an internal product with zero hand-written
> code. The engineers' job became the environment around [[openai-codex]]:
> repository knowledge, legibility tools, mechanical architecture rules, and
> recurring cleanup agents.

## Summary

Over five months a small OpenAI team built and shipped an internal beta in
which Codex wrote every line: application code, tests, CI, docs,
observability, and tooling. The repository started empty in late August 2025;
the scaffold came from Codex CLI on **GPT-5**. All figures are self-reported
by OpenAI from one internal project: about 1M lines, about 1,500 merged PRs,
3.5 PRs per engineer per day with three engineers (rising as the team grew to
seven), and an estimated 1/10th of hand-coding time. The thesis: when the
agent fails, the fix is to add the missing capability to the environment and
make it legible and enforceable, never to "try harder". The post's own caveat:
the end-to-end autonomy depends on this repository's structure and tooling and
should not be assumed to generalize. See [[agent-harness]] and
[[context-engineering]].

## Key points

- **AGENTS.md as a table of contents.** One large `AGENTS.md` failed: it
  crowds context, makes everything "important", rots, and resists mechanical
  checks. The team uses a ~100-line `AGENTS.md` that points into a structured
  `docs/` directory (design docs, execution plans, product specs, generated
  schema, `llms.txt` references, quality and reliability docs), which is the
  **system of record**. See [[agent-instructions]], [[agent-steering]].
- **Plans are versioned artifacts.** Execution plans with progress and
  decision logs, completed plans, and a tech-debt tracker live in the repo.
- **Knowledge-base hygiene is enforced.** Linters and CI check that docs are
  current, cross-linked, and well-structured; a recurring **doc-gardening
  agent** opens PRs that fix stale docs.
- **If the agent cannot see it, it does not exist.** Slack threads, Google
  Docs, and tacit knowledge must move into the repo. Prefer "boring",
  composable dependencies the agent can model; sometimes reimplement a small
  helper rather than work around opaque library behavior.
- **Application legibility.** The app boots per git worktree; Chrome DevTools
  Protocol plus skills give DOM snapshots, screenshots, and navigation; an
  ephemeral per-worktree observability stack exposes logs (LogQL) and metrics
  (PromQL). Human QA capacity had become the bottleneck. See [[tool-placement]].
- **Enforce invariants, not implementations.** Each business domain has fixed
  layers (Types → Config → Repo → Service → Runtime → UI) with cross-cutting
  concerns entering only through Providers. Codex-written custom linters and
  structural tests enforce this, plus "taste invariants" (structured logging,
  naming, file-size limits). **Lint error messages carry remediation
  instructions** into the agent's context. See [[guardrails]].
- **Agent-to-agent review loop.** Codex reviews its own PR, requests more
  agent reviews locally and in the cloud, answers feedback, and iterates until
  agent reviewers are satisfied. Human review is optional.
- **Garbage collection for entropy.** Codex copies existing patterns, good or
  bad. Manual Friday cleanup (20% of the week) did not scale. The team encodes
  "golden principles" and runs recurring background Codex tasks that find
  deviations, update quality grades, and open small refactor PRs, most
  reviewable in under a minute.

## Entities

[[openai]], [[openai-codex]]

## Concepts

[[agent-harness]], [[context-engineering]], [[agent-instructions]],
[[agent-steering]], [[guardrails]], [[tool-design]], [[tool-placement]], [[agent-skills]],
[[agent-evals]], [[agent-design-principles]], [[human-agent-teams]].

## Notable claims & data

- Single Codex runs often work on one task for more than six hours.
- Merge philosophy: minimal blocking gates, short-lived PRs, flaky tests
  handled by re-runs. The author conditions this on agent throughput far
  exceeding human attention and calls it irresponsible in a low-throughput
  setting.
- From one prompt, Codex can reproduce a bug, record a video, fix it, verify
  by driving the app, open a PR, handle review and build failures, escalate
  only when judgment is needed, and merge.
- Agents also write evaluation harnesses, release tooling, and production
  dashboard definitions.

## Connections

- **Agrees with Anthropic on a short entry file.** The ~100-line map matches
  the <200-line `CLAUDE.md` advice in [[anthropic-steering-claude-code]] and
  progressive disclosure in [[context-engineering]].
- **Compare** the environment-first long-running patterns in
  [[anthropic-eng-effective-harnesses-long-running-agents]] (progress files,
  startup sequence, verify like a user) and the verifier-as-steering-wheel
  idea in [[anthropic-eng-building-c-compiler]].
- **Tension on merge gates.** [[anthropic-eng-building-c-compiler]] (cited on
  [[agent-harness]]) says a CI gate should block any commit that breaks
  existing tests. This post runs minimal blocking gates and re-runs flakes.
  The OpenAI rule is explicitly scoped to very high agent throughput, and it
  still relies on mechanical lints and structural tests; record it as a scoped
  difference, not a flat contradiction.
- Related OpenAI accounts of Codex at scale:
  [[openai-symphony-codex-orchestration]], [[openai-how-openai-uses-codex]],
  [[openai-run-long-horizon-tasks-codex]], [[openai-codex-code-review-rules]].
- The loop internals are in [[openai-unrolling-codex-agent-loop]]; the client
  protocol is in [[openai-codex-app-server-harness]].
