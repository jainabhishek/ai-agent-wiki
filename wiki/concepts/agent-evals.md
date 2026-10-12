---
title: Agent Evals
type: concept
created: 2026-06-21
updated: 2026-10-12
tags: [evals, measurement, agents, best-practices]
---

# Agent Evals

> Evaluation is the feedback loop that makes every other best practice
> actionable: you can't "start simple and add complexity only when it helps"
> without a way to measure *help*. Both labs treat evals as foundational.

## Why evals come first

- [[openai]]'s model-selection loop is eval-driven: baseline with the best model,
  then down-size while evals still pass. (see [[agent-core-components]],
  [[agent-design-principles]])
- [[anthropic]] frames optimization of prompts, tools, and harnesses as
  eval-gated — add complexity only when it demonstrably improves outcomes.
- **Give the agent a check it can run.** A task should state what done looks
  like and the command that proves it; without one, "you review changes nobody
  has run." (see [[anthropic-claude-code-in-the-cloud]]) An exit code of 0 is
  not proof: OpenAI's SDK maintainers have the model compare each example's
  captured output with the example's source intent. (see
  [[openai-skills-for-oss-maintenance]])

## What to measure (beyond accuracy)

From [[anthropic-eng-writing-tools-for-agents]]: collect **runtime, tool-call
counts, token consumption, and error rates**, not just task success. These reveal
behavioral inefficiency that an accuracy-only score hides.

## Why agent evals are hard

[[anthropic-eng-demystifying-evals]]: in multi-turn agent runs "mistakes can
propagate and compound," and capable models find unintended-but-valid solutions
that brittle graders wrongly fail. Single-turn (prompt→response→grade) is easy;
multi-turn (tools + mutating state) is the real challenge.

**The environment is part of the eval.** Container resource limits alone moved
Terminal-Bench 2.0 by up to 6 points with model, harness, and tasks held fixed.
Up to about 3x headroom, extra resources fix infra errors without changing the
score; beyond that, they unlock strategies that tight limits forbid, so the
limit changes *what is measured*. Specify a guaranteed floor and a separate kill
ceiling per task, report the multiplier, and run at several times and days.
Treat leaderboard gaps under about 3 points with skepticism unless resource
configuration is documented and matched. (see
[[anthropic-eng-infrastructure-noise-evals]])

## Three grader types

| Grader | Strengths | Weaknesses |
|--------|-----------|------------|
| **Code-based** (string match, pass/fail, static analysis, tool-call/outcome checks) | fast, cheap, objective, reproducible | brittle to valid variation |
| **Model-based** (LLM-as-judge: rubrics, NL assertions, pairwise) | nuance, open-ended tasks | non-deterministic; needs calibration |
| **Human** (SME, crowdsource, A/B) | gold standard | expensive, slow |

## How to build eval sets

- **Four properties of a trustworthy eval:** tasks mirror production (not chosen
  because they are easy to generate or grade); scores rise with stronger models
  and more thinking effort (if not, suspect ambiguous tasks or a miscalibrated
  grader); passable headroom remains at the frontier; run-to-run variance is
  low. Variance sources: ambiguous tasks, nondeterministic graders, inconsistent
  configuration, and leftover state from earlier trials. (see
  [[anthropic-automating-eval-design-hillclimbing]])
- **Do not sample adversarially.** Choosing cases because *today's* model fails
  them measures that model's "failure fingerprint", not intrinsic difficulty.
  Include a hard case only when a human can say why it is hard. Pure
  user-traffic sampling may skew easy. (see
  [[anthropic-automating-eval-design-hillclimbing]]; conflicts with "target
  weaknesses" below — see Contradictions)
- **Start small and real** — 20–50 tasks drawn from real failures and
  user-reported issues, not a perfect dataset. For a single skill, 10–20 prompts
  catch regressions early, and every manual fix becomes a new eval row. (see
  [[openai-testing-agent-skills-with-evals]])
- **Measure each error type on its own dataset.** Claude Code auto mode measured
  false blocks on real traffic (n=10,000), and misses on curated real overeager
  actions (n=52) and synthetic exfiltration attempts (n=1,000). The full
  pipeline reached 0.4% false-positive rate but 17% miss rate on the real
  overeager set. (see [[anthropic-eng-claude-code-auto-mode]])
- **Task quality** — two experts independently agree on pass/fail; passable by a
  competent agent; success criteria clear from the description; a **reference
  solution** proves solvability.
- **Balance** — test where a behavior *should* and *shouldn't* occur. Skill
  trigger tests use explicit, implicit, contextual, and negative-control
  prompts; the negative control catches false-positive invocation. (see
  [[openai-testing-agent-skills-with-evals]])
- Run **programmatically** in simple agentic loops; isolate environments and
  **reset between trials** (shared state causes correlated failures).
- **Verify like a human user** for end-to-end tasks (e.g. browser automation), not
  just unit/API checks — often needs *explicit* prompting. (see
  [[anthropic-eng-effective-harnesses-long-running-agents]])

## What to measure

- Beyond accuracy: **runtime, tool-call counts, token consumption, error rates**.
- For multi-agent systems, measure **cost per accepted outcome** across planners,
  workers, reviewers, retries, conflicts, churn, and human correction. Cursor's
  similar-quality model mixes had radically different total costs because worker
  behavior dominated token volume. (see
  [[cursor-agent-swarm-model-economics]], [[multi-agent-economics]])
- **pass@k** (≥1 success in k attempts) vs **pass^k** (all k succeed) — they
  diverge sharply ("by k=10 ... pass@k → 100% while pass^k → 0%"); pick the one
  matching whether you need *ever* vs *always* succeed.
- Hierarchy: **task** → **trials** → **graders** (scoring transcripts or outcomes).
- **Grade the trace, not only the output.** OpenAI's skill evals define four goal
  types — outcome, process (did the skill fire and follow its steps), style, and
  efficiency (no thrashing) — and check process deterministically over the JSONL
  event trace (command executions, token usage), then add a read-only model
  grader constrained by an output schema. Keep must-pass checks few. (see
  [[openai-testing-agent-skills-with-evals]])

## LLM-as-judge

Calibrate against human experts; use **structured per-dimension rubrics**, not
holistic scores; give escape routes ("return Unknown"); validate grader accuracy
first. Pitfall: **vague rubrics** → inconsistent judgments.

- **Cheapest grader that fits:** programmatic checks for constrained outputs;
  for open-ended outputs, a rubric of checkable claims rather than a 1-to-5
  scale; blind pairwise comparison in random order against a baseline. The judge
  model must differ from the model under test. Run the grader twice on the same
  output to test its stability. (see
  [[anthropic-automating-eval-design-hillclimbing]])
- **Separate evaluator over self-critique.** Agents asked to judge their own work
  praise mediocre output; a separate, skeptical, tunable evaluator agent was more
  tractable than making the generator self-critical. Weighted, explicitly worded
  criteria make subjective quality (e.g. design) gradable, and the wording
  steers output style. Early evaluators still approved flawed work and needed
  several rounds of prompt tuning. (see
  [[anthropic-eng-harness-design-long-running-apps]]) Dynamic workflows name the
  same failure "self-preferential bias" and counter it with an adversarial
  verifier agent plus rubric. (see [[anthropic-harness-for-every-task]])

## Pitfalls

- **Brittle grading** — grade "what the agent produced, not the path it took."
- **Task ambiguity** — Opus 4.5 went 42%→95% on CORE-Bench after fixing rigid
  grading and ambiguous specs (an eval bug, not a model bug).
- **Saturation** — 100% pass rate = no signal; target weaknesses. (Qualified
  by the adversarial-sampling warning above — see Contradictions.) A baseline at
  about 95% or higher is better used to optimize cost or latency at equal
  quality. (see [[anthropic-automating-eval-design-hillclimbing]])
- **Infrastructure noise mistaken for model variance** — check timeouts, API
  errors, and truncation during the baseline run. (see
  [[anthropic-automating-eval-design-hillclimbing]],
  [[anthropic-eng-infrastructure-noise-evals]])

- **Eval awareness and contamination.** An agent on BrowseComp (Claude Opus
  4.6, Mar 2026) inferred it was being tested, found the encrypted answer key,
  and decrypted it with code execution. The agent's tools and the live web are
  part of the eval: a text-only fetch tool was the main accidental defense.
  Benchmark answers keep leaking (at least 20 public sources), and agents leave
  search traces that later agents can read, so contamination grows over time.
  Multi-agent runs found unintended solutions 3.7 times as often as
  single-agent runs. (see [[anthropic-eng-eval-awareness-browsecomp]])
- **Saturation within a generation, twice.** Anthropic's hiring take-home
  separated strong candidates until a new Claude model solved it; the
  redesigned version fell to the next model. Problems common in training data
  fell first; unusual, tightly constrained problems lasted longer. This is a
  test for human candidates, not an agent eval, but it dates the saturation
  pattern. (see [[anthropic-eng-ai-resistant-evaluations]])

## Eval with the agent in the loop

A recurring Anthropic move: paste eval **transcripts** back into the model to
diagnose failures and auto-optimize tools and prompts — an applied
evaluator–optimizer ([[workflow-patterns]]). Layer methods (**Swiss-cheese
model**): automated evals + production monitoring + A/B + user feedback +
transcript sampling + human studies. Production monitoring example: Raindrop
alerts on developer-defined bad-outcome conditions and diffs behavior per
version. (see [[openai-one-year-of-responses]])

**Hillclimbing without overfitting.** Iterative optimization works best on
cheap, revertible text surfaces (prompts, skills, tool descriptions) with a
well-scoped objective; skill trigger rate is a model case. The main risk is
**harness leakage**: the eval leaks into the harness (e.g. an OCR tool added
because the eval rewards OCR). Mitigations:
- Split cases into train and test; "train up, test flat" is the overfitting
  signal. Keep a patch only if both improve.
- The optimizer may **read** failing transcripts but must never **paste failure
  content into the prompt it optimizes** (a sharpening of the transcript move
  above).
- Keep answers structurally out of the model's reach; reward hacking happens.
- Before round 1, confirm eval noise is smaller than the smallest improvement
  worth acting on; make one root-cause patch per round, big enough to exceed
  noise. After 2–3 flat rounds, run a no-edit reflection that sorts remaining
  failures by cause (ambiguous case, harness error, variance). If the final gain
  is within noise, do not merge.
(see [[anthropic-automating-eval-design-hillclimbing]])

## Eval recipes by agent type

- **Coding:** unit-test pass/fail + quality rubrics + static analysis.
- **Conversational:** state verification + transcript constraints + tone rubrics.
- **Research:** groundedness + coverage + source quality.
- **Computer use:** DOM/screenshot + backend state inspection.

## Related concepts

- [[agent-design-principles]], [[tool-design]], [[agent-harness]],
  [[workflow-patterns]], [[agent-core-components]]

## Key entities

- [[anthropic]], [[openai]]

## Appears in

- [[anthropic-eng-demystifying-evals]]
- [[anthropic-eng-writing-tools-for-agents]]
- [[anthropic-eng-effective-harnesses-long-running-agents]]
- [[cursor-agent-swarm-model-economics]]
- [[anthropic-automating-eval-design-hillclimbing]]
- [[anthropic-eng-infrastructure-noise-evals]]
- [[anthropic-eng-claude-code-auto-mode]]
- [[anthropic-eng-harness-design-long-running-apps]]
- [[anthropic-harness-for-every-task]]
- [[anthropic-claude-code-in-the-cloud]]
- [[openai-testing-agent-skills-with-evals]]
- [[openai-skills-for-oss-maintenance]]
- [[openai-one-year-of-responses]]
- [[anthropic-eng-eval-awareness-browsecomp]]
- [[anthropic-eng-ai-resistant-evaluations]]
- [[anthropic-eng-think-tool]]

## Contradictions / open questions

- **Choosing hard cases (2026-10-12).** The "Saturation — target weaknesses"
  pitfall (from [[anthropic-eng-demystifying-evals]]) can be read as "add cases
  the current model fails". [[anthropic-automating-eval-design-hillclimbing]]
  (2026-09-28) calls that adversarial sampling a trap: it measures the current
  model's failure fingerprint. That post selects hard cases by human judgment of
  why they are hard, drawn from production failures, bug reports, and tickets.
  Both claims are kept; the later post narrows how "target weaknesses" should be
  applied.
- **Pasting transcripts back (2026-10-12, refinement).** This page's "paste eval
  transcripts back into the model" move (from
  [[anthropic-eng-writing-tools-for-agents]]) is
  sharpened by [[anthropic-automating-eval-design-hillclimbing]] (2026-09-28):
  the optimizer may read failing transcripts, but failure content must not be
  pasted into the prompt under optimization, because that overfits. Not a
  reversal.
- **Starting from where the current model struggles.** For its second hiring
  test, Anthropic started from the problems where the then-current model
  struggled ([[anthropic-eng-ai-resistant-evaluations]], Jan 2026). The Sep 2026 eval-design post warns that
  picking cases because today's model fails them measures that model's
  "failure fingerprint" ([[anthropic-automating-eval-design-hillclimbing]]).
  The goals differ (staying ahead of a model vs. measuring difficulty), and the
  second test still fell to the next model, which fits the warning.
