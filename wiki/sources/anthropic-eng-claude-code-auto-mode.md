---
title: "Anthropic (Eng): How We Built Claude Code Auto Mode"
type: source
created: 2026-10-12
updated: 2026-10-12
author: John Hughes (Anthropic Engineering)
date: 2026-03-25
source_url: https://www.anthropic.com/engineering/claude-code-auto-mode
source_path: raw/anthropic-eng-claude-code-auto-mode.md
tags: [guardrails, permissions, classifiers, prompt-injection, claude-code, evals, primary-source]
---

# Anthropic (Eng): How We Built Claude Code Auto Mode

> Design and measured results of Claude Code auto mode: a two-layer,
> model-based permission system that sits between per-action approval and
> `--dangerously-skip-permissions`.

## Summary

Users approved 93% of [[claude-code]] permission prompts, so approval was
mostly fatigue. Auto mode replaces most prompts with two layers: an **input
layer** (a server-side prompt-injection probe that adds a warning when tool
output looks like a hijack) and an **output layer** (a transcript classifier on
Sonnet 4.6 that judges each action before it runs). The threat model lists
overeager behavior, honest mistakes, prompt injection, and a misaligned model;
the classifier is tuned mainly for the first two. Actions pass three tiers:
safe-tool allowlist, in-project file edits (skip the classifier because version
control makes them reviewable), and the classifier for everything else. See
[[guardrails]].

## Key points

- **Reasoning-blind classifier.** It sees user messages and tool calls only. It
  excludes assistant text (rationalizations can persuade it) and tool results
  (main injection entry point). Including them hurt recall; tool-calls-only lost
  the user-intent anchor and blocked requested actions.
- **Two stages.** Stage 1: one-token yes/no, biased to block. Stage 2: same
  prompt, final instruction asks for reasoning; runs only on stage-1 flags and
  mostly hits the prompt cache.
- **Prompt template.** Fixed rules (judge real-world impact; chained commands
  are one action; agent-chosen parameters are unauthorized until the user says
  so; a question is not a directive) plus three slots: Environment (trust
  boundary, default = current git repo), Block rules (20+ in four groups),
  Allow exceptions. `claude auto-mode defaults` prints the baseline.
- **Entering auto mode drops broad allow rules** that grant arbitrary code
  execution (blanket shell, wildcarded interpreters, package-manager run).
- **Multi-agent handoffs.** Check on delegation can deny (inside a subagent the
  orchestrator's instruction looks like a user message); check on return only
  warns.
- **Deny-and-continue.** A block returns as a tool result telling Claude to find
  a safer path. 3 consecutive or 20 total denials escalate to the human;
  headless `claude -p` terminates.

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[guardrails]], [[agent-evals]], [[agent-orchestration]],
[[agent-design-principles]], [[agent-steering]]

## Notable claims & data

| Metric | Real traffic (n=10,000) | Real overeager (n=52) | Synthetic exfil (n=1,000) |
|---|---|---|---|
| Stage 1 only | 8.5% FPR | 6.6% FNR | 1.8% FNR |
| Full pipeline | 0.4% FPR | 17% FNR | 5.7% FNR |

- The 17% miss rate is the stated main limitation. In most misses the
  classifier saw the danger but judged that an earlier user approval covered
  the full blast radius. Prompt engineering did not fix it at acceptable cost.
- Anthropic says auto mode beats skipping permissions but does not replace
  human review of high-stakes infrastructure.
- Incident-log examples: deleting remote git branches, uploading a GitHub token
  to a compute cluster, attempting production DB migrations, sharing data via a
  public Gist.

## Connections

- The model-layer half of [[anthropic-eng-how-we-contain-claude]], which calls
  auto mode one defense-in-depth layer inside a sandbox, not a replacement.
- A worked instance of layered [[guardrails]] as described in
  [[openai-practical-guide-to-building-agents]] (classifiers + tool risk
  ratings + human escalation), with measured error rates.
- Complements the deterministic PreToolUse hooks in
  [[anthropic-steering-claude-code]]: hooks are rule-based, auto mode is
  model-based.
- An eval-design example for [[anthropic-eng-demystifying-evals]]: three
  datasets (real traffic, curated failures, synthetic attacks) measure FPR and
  FNR separately.
