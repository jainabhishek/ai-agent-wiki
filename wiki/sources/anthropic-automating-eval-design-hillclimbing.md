---
title: "Anthropic: Automating Eval Design and Hillclimbing with Claude"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Lance Martin (Anthropic, claude.dev blog)
date: 2026-09-28
source_url: https://claude.dev/blog/automating-eval-design-and-hillclimbing/
source_path: raw/anthropic-automating-eval-design-hillclimbing.md
tags: [evals, hillclimbing, overfitting, llm-as-judge, prompt-optimization, cost-optimization, claude-api-skill]
---

# Anthropic: Automating Eval Design and Hillclimbing with Claude

> Anthropic's principles for building evals you can trust, and for hillclimbing
> against them without overfitting. The principles are packaged as the
> `/claude-api build-eval` and `/claude-api hillclimb` commands in the
> `claude-api` skill that ships with [[claude-code]].

## Summary

The post has two halves. **Eval design** names four properties of a good eval: (1)
tasks mirror production; (2) scores rise with stronger models and more thinking;
(3) passable headroom remains at the frontier, not explained by impossible or
ambiguous tasks; (4) run-to-run variance is low. It adds a warning against
**adversarial sampling**. **Hillclimbing** says where iterative optimization works:
on surfaces that are cheap to change, where the score change is attributable to
the edit, and where the objective is well scoped. Its main risk is
**overfitting**, where the eval "leaks" into the harness. The two skill commands
implement these principles as guided, approval-gated workflows. Two worked
examples follow: one cuts cost to about 1/5, and one raises a skill's eval score
from 66% to about 88%. See [[agent-evals]].

## Key points

### Eval design
- **Mirror production, not convenience.** Do not pick tasks because they are easy
  to generate or easy to grade.
- **Sanity check with a model and effort ladder.** If bigger models or higher
  effort do not score better, suspect ambiguous tasks or a miscalibrated grader.
- **Headroom.** The best model at maximum effort should score well below 100%.
  A task that fails on every replicate signals an impossible or ambiguous task,
  not headroom. A good task is one where two domain experts would agree, and where
  every graded criterion is stated in the task.
- **Variance sources**: ambiguous tasks, nondeterministic graders, inconsistent
  configuration (for example, effort not applied), and environment leakage
  (leftover files or git history from a prior trial).
- **Adversarial sampling is a trap.** Capability is jagged. Choosing cases because
  *today's model fails them* measures that model's "failure fingerprint", not what
  is intrinsically hard. Include a case only when a human can say why it is hard.
  Draw cases from production failures, bug reports, and tickets. Pure user-traffic
  sampling may skew easy, because users try what they expect to work.

### build-eval workflow
- **Input sourcing order**: production transcripts (after a retention and
  sensitive-data check), then bug reports and tickets, then 5–10 hand-written
  cases, then cases synthesized from the codebase and anchored in real examples.
  The user confirms all inputs on a generated review page.
- **Cheapest grader that fits.** Use programmatic checks (exact match, a fixed
  label set, a JSON schema, tests) for constrained outputs. Use LLM-as-judge for
  open-ended outputs, with a rubric of *checkable claims, not a 1-to-5 scale*.
  Against a baseline, use blind pairwise comparison in random order. The judge
  model must differ from the model under test.
- **Validate the grader before believing it.** Claude grades a few cases and asks
  the user whether they would score any differently. "Scoring failures are among
  the most common ways an evaluation is misconfigured."
- **Diagnostics during the baseline run**: run the grader twice on the same output
  (does the verdict change?), check plumbing (timeouts, API errors, truncation, so
  infrastructure noise is not mistaken for model variance), and check headroom (a
  baseline at about 95% or higher triggers a warning to optimize cost or latency
  instead).
- **Outputs**: cases, grader, runner, and one JSONL line plus one transcript per
  case. The skill also prints a confidence interval and writes a static local
  results page.

### Hillclimbing
- **Where it works**: cheap, revertible text surfaces such as prompts and skills.
  Open-ended harness code edits work less well. Skill triggering is a model case,
  because the trigger rate is directly coupled to the skill description being
  edited. **Cost at parity** is a strong objective even on a saturated eval.
- **Overfitting via harness leakage.** Example: the eval rewards OCR, so the
  hillclimber adds an OCR tool that rarely helps production. Mitigations: (1) split
  the cases into train and test, where "train up, test flat" is the overfitting
  signal; (2) the hillclimber may read failing transcripts but must never paste
  failure content into the prompt; (3) keep answers structurally out of the
  model's reach, because reward hacking happens.
- **Hillclimb loop.** The user picks the editable surfaces: system prompt, skills
  or instruction files, tool descriptions, model / effort / API parameters, and
  harness code. The user also picks the objective, and the skill makes a random
  train/test split. Before round 1, the skill checks that eval noise is smaller
  than the smallest improvement worth acting on. Each round proposes **one patch**
  aimed at the root cause, big enough to exceed noise ("rewrite the section", not
  "reword a line"). The skill keeps the patch only if train *and* test improve. It
  reverts on regression or on "train up, test flat".
- **Stall handling.** After 2–3 flat rounds, a *reflection* step makes no edit. It
  sorts every remaining train failure by cause, to expose ambiguous cases, harness
  errors, or variance. Only legitimate failures feed later rounds.
- **Exit.** The skill leaves the code at the best version on the test set and
  reports test vs baseline with confidence intervals. If the gain is within noise,
  it recommends against merging.

## Notable claims & data

- **Cost example** (internal customer-support benchmark, 44 tickets: 30 search and
  14 held out):
  - Baseline: Opus 4.8 at default (high) effort scored 74.4% at 4.6¢ per ticket.
  - A prompt audit removed mandatory tool-call rituals, a scratchpad step, and
    contradictory rules.
  - Opus 5.5 at low effort scored 87.8% at 1.9¢. Part of the saving is pricing:
    Opus 5.5 input/output tokens cost 20% less than Opus 4.8's, and cache reads
    60% less.
  - Sonnet 5 at low effort scored 88.9% at about 1¢. The post says "Sonnet 5",
    not Sonnet 5.5.
  - Routing rules and a refund-cap cross-reference brought it to 98.9% at about the
    same cost.
  - Held-out result: **90.5% vs 78.6%** for the original setup, at about **1/5 the
    cost**.
- **Performance example** (`claude-api` skill, eval derived from Anthropic docs;
  the hillclimber had access to the docs and SDKs):
  - Baseline: 66%.
  - Adding coverage for eight missing features raised it to 74%.
  - Fixing the C# and Java type tables raised it to 77%.
  - A reflection step found that Claude wrote *older API shapes from trained
    priors* even though the skill content was present. A "remembered form → current
    form" table near the top of the skill raised the score to 80%. Examples in the
    table: fixed-budget extended thinking → adaptive thinking; old web search and
    web fetch tool versions → current versions.
  - Fixing flawed tasks and graders, plus further skill edits, raised it to about
    88%. In one case, a grader's instructions contradicted the docs, and testing
    the real API showed the docs were right.
- The stale-prior finding is a durable skill-authoring lesson. Content that is
  present can still lose to the model's training priors unless the skill
  explicitly maps old forms to new ones, near the top of the skill.

## Entities

[[anthropic]], [[claude-code]], [[claude]]

## Concepts

[[agent-evals]], [[agent-skills]], [[agent-harness]], [[prompt-tuning-axes]],
[[agent-design-principles]], [[boundary-contracts]]

## Connections

- This is an operational follow-on to [[anthropic-eng-demystifying-evals]]. It
  shares two points with that page: expert agreement as the test of a good task,
  and that saturation gives no signal. It adds the model/effort-ladder sanity check
  and the train/test discipline for optimization.
- The plumbing diagnostic overlaps with [[anthropic-eng-infrastructure-noise-evals]].
- The skill-triggering eval example connects to [[agent-skills]] and
  [[anthropic-lessons-building-claude-code-skills]].
- The "remove mandatory tool-call rituals and scratchpad steps" prompt audit is the
  same subtraction theme as [[anthropic-prompting-claude-opus-5]] and
  [[harnessing-claudes-intelligence]].
- The finding that the docs were right and the grader was wrong is a small instance
  of [[boundary-contracts]]: the real API settled the question, not the author's
  assumption.
- Sibling post by the same author: [[anthropic-building-effective-agent-automations]].

## Contradictions / open questions

- **Tension with [[agent-evals]] ("Saturation — target weaknesses").** This post
  warns that choosing cases because the current model fails them measures that
  model's failure fingerprint. It says hard cases should be chosen by human
  judgment of difficulty. "Target weaknesses" on the concept page should be
  qualified accordingly.
- **Refinement of [[agent-evals]] ("paste eval transcripts back into the model").**
  This post allows the optimizer to *read* failing transcripts. It forbids pasting
  failure content into the prompt that is being optimized, because that overfits.
  This is a sharpening, not a reversal.
