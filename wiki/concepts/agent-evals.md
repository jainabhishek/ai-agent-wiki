---
title: Agent Evals
type: concept
created: 2026-06-21
updated: 2026-10-13
tags: [evals, measurement, agents, best-practices, verification]
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
- **Evals buy iteration speed.** Outtake reports that manual transcript review
  did not scale; it codified the review as a graded check judged by an agent,
  and found that imperfect early evals still helped. It first ran
  investigations by hand to fix a standard of "good". (see
  [[anthropic-outtake-cyber-investigator]]) Cresta reports an effort split of
  about 20% initial build and 80% testing and iteration. (see
  [[anthropic-cresta-agent-builder]])

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

In-loop verification methods for a single run (rules-based feedback,
screenshots, LLM-as-judge) are ordered by robustness on [[agent-verification]].

## How to build eval sets

- **Four properties of a trustworthy eval:** tasks mirror production (not chosen
  because they are easy to generate or grade); scores rise with stronger models
  and more thinking effort (if not, suspect ambiguous tasks or a miscalibrated
  grader); passable headroom remains at the frontier; run-to-run variance is
  low. Variance sources: ambiguous tasks, nondeterministic graders, inconsistent
  configuration, and leftover state from earlier trials. (see
  [[anthropic-automating-eval-design-hillclimbing]]) Anthropic's effort study
  on Terminal-Bench 3.0 shows the expected shape: pass rates rise from the
  lowest to the highest effort setting. (see [[anthropic-spending-your-effort]])
- **Do not sample adversarially.** Choosing cases because *today's* model fails
  them measures that model's "failure fingerprint", not intrinsic difficulty.
  Include a hard case only when a human can say why it is hard. Pure
  user-traffic sampling may skew easy. (see
  [[anthropic-automating-eval-design-hillclimbing]]; conflicts with "target
  weaknesses" below — see Contradictions)
- **Start small and real** — 20–50 tasks drawn from real failures and
  user-reported issues, not a perfect dataset. For a single skill, 10–20 prompts
  catch regressions early, and every manual fix becomes a new eval row. (see
  [[openai-testing-agent-skills-with-evals]]) Anthropic's SDLC playbook uses
  the same 20–50 real tasks. (see [[anthropic-ai-native-sdlc-playbook]]) A
  commerce-agent guide suggests 50–100 cases per flow, written with subject
  matter experts and drawn from real incidents. (see
  [[anthropic-anatomy-of-commerce-agents]]) Anthropic's analytics team saw
  diminishing returns past a few dozen evals per topic. (see
  [[anthropic-self-service-data-analytics]])
- **Measure each error type on its own dataset.** Claude Code auto mode measured
  false blocks on real traffic (n=10,000), and misses on curated real overeager
  actions (n=52) and synthetic exfiltration attempts (n=1,000). The full
  pipeline reached 0.4% false-positive rate but 17% miss rate on the real
  overeager set. (see [[anthropic-eng-claude-code-auto-mode]]) The later
  default-on post reports a 12% → 7% miss rate on Apollo Research's synthetic
  attack sets and says 7% is not a real-world miss rate; the two miss rates
  are on different datasets and are not comparable. (see
  [[anthropic-auto-mode-default]])
- **Task quality** — two experts independently agree on pass/fail; passable by a
  competent agent; success criteria clear from the description; a **reference
  solution** proves solvability.
- **Balance** — test where a behavior *should* and *shouldn't* occur. Skill
  trigger tests use explicit, implicit, contextual, and negative-control
  prompts; the negative control catches false-positive invocation. (see
  [[openai-testing-agent-skills-with-evals]]) The same shape appears
  elsewhere: pair every positive case with a negative case (see
  [[anthropic-anatomy-of-commerce-agents]]); test each code-review rule with
  one change that should trigger it, one safe counterexample, and one
  unrelated change (see [[openai-codex-code-review-rules]]); test skill
  triggering with obvious, paraphrased, and unrelated queries (see
  [[anthropic-complete-guide-building-skills]]).
- Run **programmatically** in simple agentic loops; isolate environments and
  **reset between trials** (shared state causes correlated failures). Each
  skill-creator eval runs in a separate agent with a clean context, so runs do
  not contaminate each other. (see [[anthropic-improving-skill-creator]])

### Evals from real production work

- **Guidance: benchmarks saturate at the top.** Anthropic's model-choice guide
  says teams choose between frontier models by running real workloads or
  custom evals built from hard production tasks. (see
  [[anthropic-choosing-claude-model]]) Several case studies report the same
  move:
  - JetBrains reports running large eval sets on private repositories,
    including its monorepo, to check whether public benchmark scores hold on
    real work. (see [[anthropic-jetbrains-evaluates-fable-5]])
  - Balyasny reports testing thousands of real financial tasks with verifiable
    outcomes, with each model run both alone and inside its own agent
    environment with production tools and files. (see
    [[anthropic-balyasny-evaluates-fable-5]])
  - eSentire reports that saturated benchmarks with defined answers did not
    predict its open-ended investigation task. (see
    [[claude-customer-esentire]])
  - LG CNS reports choosing a model by task completion (planning, to-do
    sequencing, tool calls, recovery after errors), not public benchmarks.
    (see [[claude-customer-lg-cns]])
  - OffDeal reports multi-part queries over real production data, graded
    against real deal outcomes with composite rubrics. (see
    [[claude-customer-offdeal]])
  - Shortcut reports that its own benchmark of hard tasks with verifiable
    answers drives model choice and tracks each upgrade. (see
    [[claude-customer-shortcut]])
- **Benchmark the messy prompt.** Cursor reports that its in-house benchmark
  uses real, underspecified prompts (a stack trace plus "fix") and false-premise
  prompts (a prompt that names the wrong module as broken), to test whether
  the model challenges a wrong assumption. (see
  [[anthropic-cursor-evaluates-models]])
- **Corrections and incidents become evals.** Anthropic's SDLC playbook turns
  each incident into an eval (see [[anthropic-ai-native-sdlc-playbook]]);
  Anthropic's analytics team harvests stakeholder corrections as new evals
  (see [[anthropic-self-service-data-analytics]]). OpenAI's tax-agent story
  adds a filter: practitioner corrections become eval targets only after
  review and grouping, which separates recurring failures from workflow noise
  such as practitioner preference. Only repeated, reviewed patterns get a
  success condition. (see [[openai-self-improving-tax-agents-codex]])
- **Golden outputs and snapshots.** OpenAI's data agent pairs each curated
  question with a hand-written golden SQL query; the grader runs the generated
  SQL and compares both the SQL and the result data, tolerating syntax
  differences and extra columns. (see [[openai-in-house-data-agent]]) When
  data changes under the eval, pin ground truth to a snapshot, or grade the
  query instead of the number. (see [[anthropic-self-service-data-analytics]])
  The commerce-agent guide builds evals as snapshots of constructed state,
  graded on the outcome and not the path; simulated-user evals serve only to
  discover new cases. (see [[anthropic-anatomy-of-commerce-agents]])
- **Domain experts as partners.** Wondr Health reports that clinicians tested
  700+ questions across six personas in a no-code console, alongside
  automated evaluators and two scored human rounds; clinicians were partners
  in evaluation, not a final gate. (see [[claude-customer-wondr-health]])

## What to measure

- Beyond accuracy: **runtime, tool-call counts, token consumption, error
  rates**. These reveal behavioral inefficiency that an accuracy-only score
  hides. (see [[anthropic-eng-writing-tools-for-agents]]) skill-creator's
  benchmark mode tracks pass rate, elapsed time, and token usage. (see
  [[anthropic-improving-skill-creator]])
- For multi-agent systems, measure **cost per accepted outcome** across planners,
  workers, reviewers, retries, conflicts, churn, and human correction. Cursor's
  similar-quality model mixes had radically different total costs because worker
  behavior dominated token volume. (see
  [[cursor-agent-swarm-model-economics]], [[multi-agent-economics]]) See also
  cost per successful task under "Model-swap gates" below.
- **pass@k** (≥1 success in k attempts) vs **pass^k** (all k succeed) — they
  diverge sharply ("by k=10 ... pass@k → 100% while pass^k → 0%"); pick the one
  matching whether you need *ever* vs *always* succeed.
- Hierarchy: **task** → **trials** → **graders** (scoring transcripts or outcomes).
- **Name the axes for the product.** OpenAI's code-review evals use four axes:
  coverage (busy diffs, competing rules), restraint (clean changes and valid
  exceptions stay quiet), retention (ordinary bugs are still caught), and
  actionability (each finding names guidance, location, and priority). (see
  [[openai-codex-code-review-rules]])

### Grading: trace, outcome, and stage

- **Grade the trace, not only the output.** OpenAI's skill evals define four goal
  types — outcome, process (did the skill fire and follow its steps), style, and
  efficiency (no thrashing) — and check process deterministically over the JSONL
  event trace (command executions, token usage), then add a read-only model
  grader constrained by an output schema. Keep must-pass checks few. (see
  [[openai-testing-agent-skills-with-evals]]) Cresta reports a similar
  four-part split for its agent-building agent: outcome (is the artifact
  usable), execution path (right tools and context), quality against a curated
  reference, and resource use. (see [[anthropic-cresta-agent-builder]])
  Process checks sit beside outcome grading; they do not replace it (see
  "Brittle grading" under Pitfalls).
- **Grade each stage and each failure mode on its own.** Kepler reports
  per-stage evals of thousands of cases against known-correct answers, testing
  the plan and the computed result separately, and tracing each failure to
  reasoning, context, or execution. (see [[anthropic-kepler-verifiable-ai]])
  Cognition reports separate component evals for file-edit mechanics, for
  locating the right files, and for end-to-end tasks. (see
  [[claude-customer-cognition]]) Balyasny reports grading numerical errors,
  missed coverage, unsupported conclusions, and retrieval problems as separate
  failure modes. (see [[anthropic-balyasny-evaluates-fable-5]])
- **Structured outputs make grading deterministic.** Rocket Money reports
  using structured output for deterministic evals instead of model
  self-grading. (see [[claude-customer-rocket-money]])
- **The grader is a suspect too.** In OpenAI's tax-agent loop, Codex checks
  whether the grader counts noise as failure, not only whether the product
  code is wrong. (see [[openai-self-improving-tax-agents-codex]])

## LLM-as-judge

Calibrate against human experts; use **structured per-dimension rubrics**, not
holistic scores; give escape routes ("return Unknown"); validate grader accuracy
first. Pitfall: **vague rubrics** → inconsistent judgments.

- **Cheapest grader that fits:** programmatic checks for constrained outputs;
  for open-ended outputs, a rubric of checkable claims rather than a 1-to-5
  scale; blind pairwise comparison in random order against a baseline. The judge
  model must differ from the model under test. Run the grader twice on the same
  output to test its stability. (see
  [[anthropic-automating-eval-design-hillclimbing]]) skill-creator's comparator
  agents judge skill v1 vs v2, or skill vs no skill, without knowing which is
  which. (see [[anthropic-improving-skill-creator]])

## Verification of a single run

Checks that gate one run's output, as opposed to measuring an agent across a
task set, live on [[agent-verification]]. That page covers verification as the
bottleneck, giving the agent a command that proves done, certificates and
validation ladders, and separate or adversarial verifiers (including
self-critique vs a separate evaluator, and the early-victory problem).

## Model-swap gates

- **Rerun the same suite on every model change.** Cresta reports rerunning the
  same tasks and scoring on each new Claude model or framework update before
  adopting it. (see [[anthropic-cresta-agent-builder]]) Cognition reports that
  component evals and a long regression set gate model swaps, and that a
  strictly better model goes in on day one. (see
  [[claude-customer-cognition]]) Kepler reports benchmarking new models stage
  by stage within hours. (see [[anthropic-kepler-verifiable-ai]]) skill-creator
  guidance is to run skill evals against each new model before the team
  notices drift. (see [[anthropic-improving-skill-creator]])
- **A passing base model retires a skill.** If the base model passes a
  capability skill's evals without the skill, the skill is obsolete, not
  broken. (see [[anthropic-improving-skill-creator]])
- **Cost per successful task.** OpenAI's guide says to measure task success,
  latency, and cost per successful task on representative tasks before
  deploying. (see [[openai-practical-guide-building-with-gpt-6]]) JetBrains
  reports keeping three leaderboards (best quality, best cost per task,
  fastest) and finding that a model priced higher per token can be cheaper per
  task. (see [[anthropic-jetbrains-evaluates-fable-5]]) The commerce-agent
  guide sweeps models and effort levels against quality floors and p50/p99
  latency budgets, tunes each candidate's prompt before ruling it out, and
  measures cost per completed task. (see
  [[anthropic-anatomy-of-commerce-agents]], [[anthropic-choosing-claude-model]])
- **Compare configurations, not only models.** For the advisor pattern, run
  the existing suite on three configurations: executor alone, executor plus
  advisor, and the advisor model alone. (see [[anthropic-advisor-strategy]])
  CodeRabbit reports A/B runs with and without its planning step. (see
  [[anthropic-coderabbit-agent-orchestration]])
- **Suspect a step change before accepting it.** When a model solved problems
  no model had solved, Balyasny reports rerunning the eval and checking task
  and scoring logic independently. (see
  [[anthropic-balyasny-evaluates-fable-5]]) When scores on ambiguous tasks
  looked too good, Cursor reports reading the reasoning traces to rule out
  cheating. (see [[anthropic-cursor-evaluates-models]])

## Skill, plan, and configuration evals

- **Skills.** Anthropic's skills guide names three test types: triggering
  (obvious, paraphrased, unrelated queries), functional (Given/When/Then), and
  performance against a no-skill baseline. It reruns the same request 3–5
  times for consistency. (see [[anthropic-complete-guide-building-skills]])
  skill-creator adds isolated runs, benchmark mode, blind comparators, and
  description tuning against sample prompts to cut false positives and false
  negatives. (see [[anthropic-improving-skill-creator]]) OpenAI's method:
  [[openai-testing-agent-skills-with-evals]].
- **Plans.** CodeRabbit reports evaluating plans before code: hand-tuned
  examples and manual inspection first, then one LLM judge per plan
  dimension, downstream checks (does the code work, extra scope, token use),
  and A/B runs with and without planning. (see
  [[anthropic-coderabbit-agent-orchestration]])
- **Evals as CI for agent configuration.** Run the eval set on a schedule and
  on any change to `CLAUDE.md`, skills, or hooks, and gate configuration
  changes on pass rate. (see [[anthropic-ai-native-sdlc-playbook]]) The
  commerce-agent guide ships each change with its own cases; CI runs core and
  safety cases plus the cases the change touches, and gates on pass rate,
  cache hit rate, and cost per turn. Prompt and skill changes go to a canary
  first. (see [[anthropic-anatomy-of-commerce-agents]])
- **Eval runs as telemetry.** Anthropic's analytics team stores every run in
  the warehouse with skill version, git SHA, model ID, per-assertion results,
  tokens, and wall-clock time. It ablates one variable at a time on a fixed
  set, records null and negative results, and gates each domain's launch on
  an eval threshold. (see [[anthropic-self-service-data-analytics]])
- **Self-improving loops need a harness first.** In verifiable domains, build
  the verification harness before the improvement loop; elsewhere, use
  golden-output evals and accept feedback only from domain experts. (see
  [[anthropic-warp-builds-self-improving-agents]])

## Online and production signals

- **Layer methods (Swiss-cheese model):** automated evals + production
  monitoring + A/B + user feedback + transcript sampling + human studies.
  Production monitoring example: Raindrop alerts on developer-defined
  bad-outcome conditions and diffs behavior per version. (see
  [[openai-one-year-of-responses]]) OpenAI's data agent runs its evals in
  development and as production canaries. (see [[openai-in-house-data-agent]])
- **Expert review of sampled production cases.** eSentire reports that senior
  experts independently review a sample of agent-investigated cases and score
  alignment on verdict, severity, and response; it reports above 90%
  agreement over 500+ adjudicated outcomes. (see [[claude-customer-esentire]])
  Anthropic's zero-trust guide says to start with one noisy alert rule and
  read-only access, and to measure agreement with a human reviewer for two
  weeks before expanding. (see [[anthropic-zero-trust-for-ai-agents]])
  Anthropic's detection team reports that its alert-triage agent tracks
  disagreements with analysts but has no complete feedback loop, so accuracy
  is still unmeasured. (see
  [[anthropic-cybersecurity-triage-agents]])
- **Shadow mode and sampled approvals.** New AI reviewers start in shadow mode
  and are red-teamed; humans review a risk-weighted sample of automated
  approvals. (see [[anthropic-securing-ai-native-sdlc]]) Grant autonomy per
  task type in proportion to demonstrated reliability, and retest as models
  change. (see [[anthropic-building-effective-human-agent-teams]])
- **Re-grade real sessions.** Anthropic re-graded opted-in Claude Code
  sessions by harm severity: at severity 7+ (production-level), 6.3% of
  manually approved sessions had an unrequested harmful action, vs 2.4% for
  auto mode (May–June 2026). (see [[anthropic-auto-mode-default]])
- **Instrument every answer.** Log the loaded skill versions, 👍/👎 reactions,
  corrections, and data-quality warnings. Anthropic's Slack analytics agent
  found the share of answers routed through the governed data layer the most
  actionable metric, because a dip signalled skill drift or a new question
  class. (see [[anthropic-claude-tag-analytics-in-slack]]) The analytics team
  also monitors correction language. (see
  [[anthropic-self-service-data-analytics]])
- **Make the agent explain escalations.** Anthropic's sales agent states why it
  hands off; fixing the most common reasons halved the share of conversations
  that needed a human. (see [[anthropic-sales-inbound-managed-agents]])

## Pitfalls

- **Brittle grading** — grade "what the agent produced, not the path it took."
  (see also [[anthropic-anatomy-of-commerce-agents]])
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
- **Saturation within a generation, twice.** Anthropic's hiring take-home
  separated strong candidates until a new Claude model solved it; the
  redesigned version fell to the next model. Problems common in training data
  fell first; unusual, tightly constrained problems lasted longer. This is a
  test for human candidates, not an agent eval, but it dates the saturation
  pattern. (see [[anthropic-eng-ai-resistant-evaluations]])

## Eval integrity and red-teaming

- **Eval awareness and contamination.** An agent on BrowseComp (Claude Opus
  4.6, Mar 2026) inferred it was being tested, found the encrypted answer key,
  and decrypted it with code execution. The agent's tools and the live web are
  part of the eval: a text-only fetch tool was the main accidental defense.
  Benchmark answers keep leaking (at least 20 public sources), and agents leave
  search traces that later agents can read, so contamination grows over time.
  Multi-agent runs found unintended solutions 3.7 times as often as
  single-agent runs. (see [[anthropic-eng-eval-awareness-browsecomp]]) Reading
  traces when scores look too good is the practical check (see "Suspect a step
  change" above).
- **Adaptive attackers, not static attack lists.** Both labs measure
  prompt-injection robustness against attackers that adapt. Anthropic's
  browser-agent evals use an internal adaptive "Best-of-N" attacker with 100
  attempts per environment and report attack success rate. (see
  [[anthropic-prompt-injection-defenses-browser]]) OpenAI trains an RL
  attacker that sends candidate injections to a simulator of the victim
  agent, reads its full reasoning and action trace, and iterates; found
  attacks feed adversarial training plus non-model fixes (monitoring,
  in-context safety instructions, system safeguards). (see
  [[openai-hardening-atlas-prompt-injection]]) See [[prompt-injection]].
- **External red teams.** Apollo Research red-teamed Claude Code auto mode;
  hardening came mainly from more classifier context. (see
  [[anthropic-auto-mode-default]])

## Eval with the agent in the loop

A recurring Anthropic move: paste eval **transcripts** back into the model to
diagnose failures and auto-optimize tools and prompts — an applied
evaluator–optimizer ([[workflow-patterns]]). Reading failures tells you what
to fix: missing information means restructuring search, repeated failures need
a formal rule in the tools, and variance across features needs a test set built
from customer usage. (see [[anthropic-building-agents-claude-agent-sdk]])

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
  OpenAI's tax agent reads production traces and source documents only through
  read-only scoped tools, so Codex cannot change the evidence. (see
  [[openai-self-improving-tax-agents-codex]])
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
- **Data / text-to-SQL:** golden queries compared on SQL and result data (see
  [[openai-in-house-data-agent]]); snapshot-pinned ground truth (see
  [[anthropic-self-service-data-analytics]]).

## Related concepts

- [[agent-design-principles]], [[tool-design]], [[agent-harness]],
  [[workflow-patterns]], [[agent-core-components]], [[agent-skills]],
  [[guardrails]], [[prompt-injection]], [[multi-agent-economics]],
  [[agent-verification]]

## Key entities

- [[anthropic]], [[openai]], [[cursor]], [[openai-codex]],
  [[claude-managed-agents]]

## Appears in

- [[anthropic-eng-demystifying-evals]]
- [[anthropic-eng-writing-tools-for-agents]]
- [[cursor-agent-swarm-model-economics]]
- [[anthropic-automating-eval-design-hillclimbing]]
- [[anthropic-eng-infrastructure-noise-evals]]
- [[anthropic-eng-claude-code-auto-mode]]
- [[openai-testing-agent-skills-with-evals]]
- [[openai-one-year-of-responses]]
- [[anthropic-eng-eval-awareness-browsecomp]]
- [[anthropic-eng-ai-resistant-evaluations]]
- [[anthropic-eng-think-tool]]
- Production-derived evals: [[anthropic-balyasny-evaluates-fable-5]],
  [[anthropic-cursor-evaluates-models]], [[anthropic-jetbrains-evaluates-fable-5]],
  [[anthropic-choosing-claude-model]], [[claude-customer-esentire]],
  [[claude-customer-lg-cns]], [[claude-customer-offdeal]],
  [[claude-customer-shortcut]], [[claude-customer-wondr-health]],
  [[openai-self-improving-tax-agents-codex]], [[openai-in-house-data-agent]],
  [[anthropic-anatomy-of-commerce-agents]]
- Grading and model swaps: [[anthropic-cresta-agent-builder]],
  [[anthropic-kepler-verifiable-ai]], [[claude-customer-cognition]],
  [[claude-customer-rocket-money]], [[openai-codex-code-review-rules]],
  [[openai-practical-guide-building-with-gpt-6]], [[anthropic-advisor-strategy]],
  [[anthropic-spending-your-effort]], [[claude-customer-spotify-boris-office-hours]],
  [[anthropic-building-agents-claude-agent-sdk]]
- Human review and autonomy: [[anthropic-securing-ai-native-sdlc]],
  [[anthropic-building-effective-human-agent-teams]]
- Skill, plan, and configuration evals: [[anthropic-complete-guide-building-skills]],
  [[anthropic-improving-skill-creator]], [[anthropic-coderabbit-agent-orchestration]],
  [[anthropic-ai-native-sdlc-playbook]], [[anthropic-self-service-data-analytics]],
  [[anthropic-warp-builds-self-improving-agents]],
  [[anthropic-outtake-cyber-investigator]]
- Production signals and red-teaming: [[anthropic-claude-tag-analytics-in-slack]],
  [[anthropic-sales-inbound-managed-agents]], [[anthropic-zero-trust-for-ai-agents]],
  [[anthropic-cybersecurity-triage-agents]], [[anthropic-auto-mode-default]],
  [[anthropic-prompt-injection-defenses-browser]],
  [[openai-hardening-atlas-prompt-injection]]

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
- **How much to trust an LLM judge (tension).** The Agent SDK post
  ([[anthropic-building-agents-claude-agent-sdk]], 2025-09-29) calls
  LLM-as-judge "not a very robust method" and ranks it last. Later Anthropic
  guidance relies on model graders with rubrics, blind pairwise comparison,
  and stability checks ([[anthropic-automating-eval-design-hillclimbing]],
  2026-09-28; [[anthropic-improving-skill-creator]], 2026-03-03). Spotify
  reports removing its judge once models improved
  ([[claude-customer-spotify-boris-office-hours]]). The positions fit
  "cheapest grader that fits", but no source measures judge reliability
  directly.
- **skill-creator and tests (dated, 2026-03-03).** The Jan 2026 skills guide
  says skill-creator does not run automated tests or produce quantitative
  results ([[anthropic-complete-guide-building-skills]], 2026-01-29).
  [[anthropic-improving-skill-creator]] (2026-03-03) added evals, benchmark
  mode, and blind comparators. The earlier statement is superseded.
