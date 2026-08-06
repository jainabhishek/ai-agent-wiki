---
title: "Anthropic: Prompting Claude Sonnet 5"
type: source
created: 2026-08-06
updated: 2026-08-06
author: Anthropic
date: accessed 2026-08-06
source_url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5
source_path: raw/anthropic-prompting-claude-sonnet-5.md
models: [claude-sonnet-5]
as_of: 2026-08-06
tags: [prompting, model-specific, anthropic, sonnet-5]
---

# Anthropic: Prompting Claude Sonnet 5

> Anthropic's model-specific prompting page for Claude Sonnet 5 — effort
> calibration, adaptive-thinking defaults, literal instruction following, and
> design defaults.

## Summary

Claude Sonnet 5 is positioned for coding and agentic tasks and "performs well out
of the box on existing Claude Sonnet 4.6 prompts." The page's distinctive theme is
**literalism**: the model interprets prompts more exactly than its predecessor,
which raises precision but breaks prompts that relied on the model generalizing an
instruction beyond its stated scope. A second theme is that several API levers
present on Sonnet 4.6 have been removed, so behavior previously controlled by
parameters must now be controlled by prompt. See [[prompt-tuning-axes]].

## Key points

### More literal instruction following
Sonnet 5 "does not silently generalize an instruction from one item to another,
and it does not infer requests you didn't make," particularly at lower effort.
Anthropic frames this as an upside for "API use cases with carefully tuned prompts,
structured extraction, and pipelines where you want predictable behavior." Where
an instruction should apply broadly, the scope must be stated — e.g. "Apply this
formatting to every section, not just the first one."

### Effort and thinking depth
Effort defaults to `high` (unchanged from Sonnet 4.6); `xhigh` is recommended for
the hardest coding and agentic work. Anthropic gives a cross-model mapping for
migration: **Sonnet 5 at `medium` ≈ Sonnet 4.6 at `high`**, and **Sonnet 5 at
`high` ≈ Sonnet 4.6 at `max`** — and advises benchmarking by observed thinking
length rather than by effort name. The model "respects effort levels strictly,
especially at the low end," scoping work to exactly what was asked at `low` and
`medium`, with some risk of under-thinking on moderately complex tasks at `low`.
The stated fix is to raise effort rather than to prompt around it.

### Adaptive thinking is on by default
A behavioral change from Sonnet 4.6, where the same requests ran without thinking.
Manual extended thinking (`thinking: {type: "enabled", budget_tokens: N}`) is
**removed and returns a 400 error**. Because `max_tokens` is a hard limit on
thinking *plus* response text, budgets tuned for Sonnet 4.6 need revisiting — a
tight budget can yield a response that is almost entirely thinking followed by a
truncated answer and `stop_reason: "max_tokens"`.

### New tokenizer
Sonnet 5 produces approximately **30% more tokens for the same text** than Sonnet
4.6, compounding the `max_tokens` problem above.

### Sampling parameters removed
Setting `temperature`, `top_p`, or `top_k` to a non-default value returns a 400
error — new for Sonnet-class models. Tone and stylistic variety must be steered by
system prompt instead.

### Tool use triggering
More agentic than Sonnet 4.6 by default, reaching for tools and running
self-verification loops more readily. With thinking disabled it is *less* likely
to reach for tools, so tool-dependent workloads running thinking-off need an
explicit nudge. Effort is also a tool-use lever: `high`/`xhigh` show
"substantially more tool usage in agentic search and coding."

### Progress updates
Interim-status scaffolding ("After every 3 tool calls, summarize progress") should
be removed — the model now provides regular, higher-quality updates natively.

### Design and frontend defaults
The model "may settle into a consistent default visual style on open-ended
frontend and design briefs." Generic negative instructions ("don't use that color,"
"make it clean and minimal") shift it to a *different fixed palette* rather than
producing variety. Two approaches work: specify a concrete alternative in detail,
or have the model propose several visual directions and let the user pick. The
propose-options approach is explicitly recommended as the way to get run-to-run
variety **because `temperature` is no longer available**.

### Code review harnesses
A harness tuned for an earlier model may show *lower recall* on Sonnet 5, which
Anthropic attributes to a harness effect rather than a capability regression: given
"only report high-severity issues" or "don't nitpick," the model investigates just
as thoroughly, finds the bugs, then declines to report findings below the stated
bar. Precision rises while measured recall falls. The recommended fix is to
separate finding from filtering — instruct the model that its job at the finding
stage is coverage, and rank or filter downstream.

### Computer use
Supports `computer_20251124`, up to 2576px / 3.75MP. Internal testing puts 1080p at
a good performance/cost balance; 720p or 1366×768 are lower-cost options.

## Notable claims & data

- Effort-level intelligence is not comparable across model generations under the
  same name — hence the explicit `medium`↔`high` and `high`↔`max` mapping.
- ~30% token inflation from the new tokenizer for identical text.
- Positive examples of desired communication style outperform negative
  instructions — stated here and echoed on [[anthropic-prompting-claude-opus-5]].

## Entities

[[anthropic]], [[claude]]

## Concepts

[[prompt-tuning-axes]], [[agent-instructions]], [[agent-evals]],
[[tool-design]], [[context-engineering]]

## Connections

The code-review literalism finding matches the same failure mode documented on
[[anthropic-prompting-claude-opus-5]], suggesting it is a 5-generation trait rather
than a per-model quirk. Sibling: [[anthropic-prompting-claude-fable-5]].

## Contradictions / open questions

- _None recorded._
