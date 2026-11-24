---
title: "Anthropic: Which Claude model should you build with? Fable, Opus, Sonnet, or Haiku"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Addy Osmani (Anthropic)
date: 2026-11-09
source_url: https://claude.dev/blog/which-claude-model-should-you-build-with/
source_path: raw/anthropic-which-claude-model-to-build-with.md
models: [claude-fable-5-2, claude-mythos-5-2, claude-opus-5-5, claude-sonnet-5-5, claude-haiku-5-5]
as_of: 2026-11-24
tags: [model-selection, model-specific, cost-per-task, effort, pricing, subagents, advisor-tool, migration, claude-code]
---

# Anthropic: Which Claude model should you build with? Fable, Opus, Sonnet, or Haiku

> Anthropic's November 2026 model-choice playbook for the Fable 5.2 / Opus 5.5 /
> Sonnet 5.5 / Haiku 5.5 lineup. It covers which model to start on per task, list
> prices, how to mix models, and the API differences to test before you switch.

## Summary

Published 2026-11-09 on the claude.dev blog ("Playbooks") by Addy Osmani of
[[anthropic]]. The post names four generally available models: Claude Haiku 5.5,
Sonnet 5.5, Opus 5.5, and Fable 5.2. It names Claude Mythos 5.2 as the most
capable model for cybersecurity and life-sciences research, available through
verification programs. No API model ID strings appear in the body. The `models:`
list follows the naming convention. All prices, defaults, and compatibility rules
on this page are for these five models.

The main advice is to start most work on **Opus 5.5 at `medium`**, not on the most
capable model. The post gives these reasons. Opus 5.5 is the [[claude-code]]
default. It costs half as much per token as Fable 5.2. Effort is a finer dial than
model choice. You move down to Sonnet 5.5 or Haiku 5.5 for scoped or high-volume
work. You move up to Fable 5.2 for the hardest technical work, for long unattended
runs, or when Opus 5.5 at `high` falls short. The unit of comparison is cost per
finished task, measured on your own work. See [[multi-agent-economics]] and
[[agent-evals]].

## Key points

### Starting points by task
- Opus 5.5 at `medium`: everyday engineering, multi-PR features, computer use and
  vision-heavy loops, and "not sure yet".
- Sonnet 5.5: chat (`low`/`medium`), well-scoped coding, everyday documents,
  slides, and spreadsheets, and repeated agent tasks. A clear spec alone does not
  qualify a task for Sonnet; migrations and performance work can still need Opus or
  Fable.
- Haiku 5.5: classification, routing, and extraction, plus subagents whose mistakes
  are cheap to spot.
- Fable 5.2 (`medium`, then `high`): major refactors and migrations, architecture
  planning, leading many subagents, deep research, and quantitative analysis.

### Effort before model
- Try one effort level up or down before you switch models. Past `high`, one more
  level can cost as much as the next model, so test the bigger model at lower
  effort. Effort does not add knowledge or skill.
- Escalation order when a model falls short: (1) give it a way to verify its own
  work, (2) raise effort one level, (3) move up a model at a lower effort level.
  See [[agent-verification]].
- Run low and re-run failures high: Opus 5.5 at `low` with failures re-run at
  `high` passed about 97% for about $0.17 per task. All tasks at `high` passed 95.3%
  for $0.29.

### Prices (per million tokens, Claude API list)

| | Input / output | Cache read |
|---|---|---|
| Haiku 5.5 | $0.10 / $0.50 (≤100K prompt); $0.50 / $2.50 (>100K) | $0.01 / $0.05 |
| Sonnet 5.5 | $2 / $10 | $0.10 |
| Opus 5.5 | $4 / $20 | $0.20 |
| Fable 5.2 | $8 / $40 | $0.20 |

All four have a 1M context window and 128K max output. Fast mode is on Opus 5.5 and
Fable 5.2 only. Default API effort: Haiku `medium`, Sonnet `high` (`medium` in Claude
Code), Opus `medium`, Fable `high` (`medium` in Claude Code). Because Fable and Opus
share a cache-read price, on long cache-heavy runs the 2x gap shows only on uncached
input and output.

### Mixing models
- **Switch at a natural break.** The cache belongs to the model that wrote it. Before
  a switch, compact or start from a short summary.
- **Thinking-block readability** (Claude API and Google-managed Google Cloud): Opus
  5.5 reads Sonnet 5.5 and Haiku 5.5 blocks. Sonnet 5.5 reads Haiku 5.5 blocks.
  Fable 5.2 reads Opus, Sonnet, and Haiku 5.5 blocks. Fable 5.1 reads Opus 5.5
  blocks. A model never reads the blocks of a model above it. Unreadable blocks are
  dropped silently. A move away from Fable 5.2 always drops its reasoning.
- **Subagents on smaller models** via `model: haiku` / `model: sonnet` or
  `CLAUDE_CODE_SUBAGENT_MODEL`. Keep code edits and judgment on the main model. The
  built-in Explore subagent now runs on the session's model (capped at Opus on the
  API). Define your own `Explore` with `model: haiku` to keep it cheap. The `haiku`
  alias resolves to Haiku 5.5 on the Anthropic API (Claude Code ≥ v2.1.293). On
  Bedrock, Google Cloud, Foundry, and Claude Platform on AWS it still resolves to
  Haiku 4.5. `opusplan` puts edits on Sonnet, so measure it first.
- **Advisor tool (beta).** The platform cost guide found that none of four pairings
  clearly beat the executor alone. An Opus 5.5 executor with a Fable 5.1 advisor
  scored +1.7 points for about 2.1x the cost ($2.92 per attempt, 90.1%). Measure the
  consult rate first. A Fable 5.2 executor accepts only a Fable 5.2 or Mythos 5.2
  advisor.
- **Bulk delegation.** An Opus 5.5 lead with up to 25 Sonnet 5.5 workers, over about
  22M tokens of code, cost about a third less than Opus 5.5 alone at about the same
  score. Skip this for dependent chains or for work that fits in one context window.
  See [[agent-orchestration]] and [[claude-managed-agents]].

### Compatibility checks before migrating
- Fable 5.2 preserved thinking applies to every API account. An edited prefix
  returns 400 unless you opt in to dropping blocks. No change is needed via Claude
  Code, the [[claude-agent-sdk]], or Managed Agents.
- Opus 5.5 and Fable 5.2 always think. Sonnet 5.5 has `between_tools`. Haiku 5.5
  can turn thinking off at `high` or below. Read content blocks by type.
- `tool_choice` `any`/`tool` returns 400 on Sonnet 5.5, Opus 5.5, and Fable 5.2. Use
  `auto` plus `strict: true` plus a prompt line instead.
- Computer use works only through `computer_toolset_20260801`.
- Haiku 4.5 → 5.5: effort replaces `budget_tokens`. Non-default sampling parameters
  and a final assistant turn both return 400.
- Safety fallbacks in Claude Code: cyber → Opus 4.8, biology → Opus 5 (Fable 5.2
  keeps Fable 5.1's fallbacks).
- For multi-model systems, build every request for the strictest model, and let
  code, not a model, apply simple routing rules.

### Measure on your own work
Sample real tasks with outcome checks. Run each candidate at two or three effort
levels in separate sessions (no shared cache). Plot score against spend. Keep a
multi-model setup only if it beats every single-model point. Shadow-run the winner
before cutover. See [[agent-evals]].

## Notable claims & data

- Terminal-Bench 3.0: Fable 5.1 at `max` scored 58.0%; Opus 5.5 at `high` scored
  58.9% on half the tokens (cited from [[anthropic-spending-your-effort]]).
- FrontierCode 2.0: Fable 5.2 at `high` scored 45.3% and Opus 5.5 at `max` scored
  45.5%. Fable cost roughly half as much per task.
- SWE-bench Pro, Opus 5.5 compared with `high`: `medium` scored about 2.5 points
  lower at about 70% of the cost. `low` scored about 8 points lower at about a third
  of the cost. `xhigh` scored about 1.4 points higher at 2.5x the cost.
- On one 20-problem search benchmark, two problems carried 43% of the spend.
- Fable 5.2 output is up to 30% faster than Fable 5.1. Sonnet 5.5 is 30% faster
  than Sonnet 5.
- A cache read costs about $0.03 per turn at 150K context and about $0.004 at 20K
  (cited from [[anthropic-what-a-task-costs-opus-5-5]]).

## Entities

[[anthropic]], [[claude]], [[claude-code]], [[claude-agent-sdk]],
[[claude-managed-agents]]

## Concepts

[[multi-agent-economics]], [[agent-orchestration]], [[agent-evals]],
[[agent-verification]], [[prompt-tuning-axes]], [[context-engineering]],
[[agent-harness]], [[tool-design]]

## Connections

- Updates [[anthropic-choosing-claude-model]] (2026-07-24) for the November 2026
  lineup. Both posts judge by cost per task, treat effort as a second dial, and say
  to test on your own evals. They differ on the starting model (see Contradictions).
- Same author and cost model as [[anthropic-what-a-task-costs-opus-5-5]]. Both say
  small models must not do code edits, and both flag `opusplan` for measurement.
- The advisor section revisits [[anthropic-advisor-strategy]] with a more cautious
  result.
- Per-model prompting: [[anthropic-prompting-claude-fable-5-2]],
  [[anthropic-prompting-claude-opus-5-5]],
  [[anthropic-prompting-claude-sonnet-5-5]],
  [[anthropic-prompting-claude-haiku-5-5]]. Sonnet launch details:
  [[anthropic-building-with-sonnet-5-5]].
- Effort data: [[anthropic-spending-your-effort]].

## Contradictions / open questions

- **Starting model.** [[anthropic-choosing-claude-model]] says to start with the
  most intelligent generally available model and tune with effort ("start smart").
  This post says to "start most work on Opus 5.5 at its default effort level,
  medium."
  Opus 5.5 is not the most capable GA model in this lineup. The newer post (2026-11-09)
  supersedes the older one (2026-07-24) for the current lineup.
- **Sonnet 5.5 cache-read price.** [[anthropic-building-with-sonnet-5-5]] says
  "Cache read: $0.20 for both models" and "A cache read costs a tenth of the input
  price." This post says Sonnet 5.5 cache reads cost $0.10. That is one-twentieth of
  input, the same ratio as Opus 5.5. The post gives no change date. Verify against
  the pricing docs.
- **Who reads Sonnet 5.5 thinking blocks.** [[anthropic-building-with-sonnet-5-5]]
  says "No other model can read Sonnet 5.5's blocks." This post says Opus 5.5 and
  Fable 5.2 both read Sonnet 5.5's blocks. This may be a later platform change
  (Fable 5.2 did not exist at the earlier date). Verify against the preserved-thinking
  docs.
- **Explore subagent model.** [[claude-code]] and
  [[anthropic-prompt-caching-is-everything]] describe Haiku-based Explore agents. This
  post says that in current Claude Code, Explore runs on the session's model. The
  difference is a product change over time, so the older pages need an "as of" note.
- The advisor caution ("none clearly beat its executor alone") is weaker than the
  results in [[anthropic-advisor-strategy]] and [[anthropic-choosing-claude-model]]
  (Sonnet 5 with a Fable 5 advisor scored within 10% of Fable 5 at 63% of the price).
  The models and benchmarks differ, so the numbers do not contradict each other
  directly.
