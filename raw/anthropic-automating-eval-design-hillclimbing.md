# Automating eval design and hillclimbing with Claude — Anthropic (claude.dev blog) (raw capture)

> Source: https://claude.dev/blog/automating-eval-design-and-hillclimbing/
> Publisher: Anthropic (claude.dev blog) · Date: 2026-09-28
> Author: Lance Martin. Category: Playbooks. 12 min read.
> Captured: 2026-10-12 via curl + local HTML-to-text (condensed, paraphrased).

## Intro

Evals signal how an app or skill performs on specific tasks; designing them and
improving against them without self-deception is hard. Anthropic added guidance
for both to the `claude-api` skill: `/claude-api build-eval` builds an eval inside
the user's codebase; `/claude-api hillclimb` improves the application against it
one change at a time, with a held-out set to catch overfitting.

## Eval design

Four elements of a good eval (Figure 1):
- **Tasks mirror production.** Sample tasks from the setting where the capability
  will be used, not those easy to generate or grade.
- **Performance improves with stronger models and more thinking.** If larger models
  / higher effort don't score better, suspect ambiguous tasks or a miscalibrated grader.
- **"Passable" headroom at the frontier.** The strongest model at highest effort
  should be well below 100%, else changes can't be judged. The gap must not come
  from impossible/ambiguous tasks — a tell is a task that fails every run
  regardless of replicate count. Good task: two domain experts would reach the same
  verdict, and everything the grader checks is stated in the task.
- **Low run-to-run variance.** High variance usually means ambiguous tasks or a
  grader that gives different verdicts on identical output. Variance can hide in
  configuration (effort not applied consistently) and in the environment (leftover
  state from an earlier trial — a file, git history — can hand the agent the answer).
Figure 1 chart: score vs tokens spent, three model sizes × three effort settings
(illustrative).

### Adversarial sampling

Model capability is jagged. Picking cases because today's model fails them samples
the valleys of one model's capability surface (Figure 2), so the eval measures that
model's failure fingerprint rather than what is intrinsically hard or valuable.
Pick hard cases because a human judged them hard — be able to say why a task is
hard before including it. Include specific application failures from production
traffic, bug reports, tickets. But don't blindly trust user traffic: users try what
they expect to work, so a distribution drawn purely from traffic may skew easy.

## /claude-api build-eval

Claude interviews the user, builds the eval in the codebase, pausing for approval
at set points.

### Designing examples

Input sourcing order: (1) production transcripts, after asking about retention and
sensitive data; (2) bug reports and support tickets; (3) five to ten hand-written
cases; (4) cases synthesized from the codebase. Synthetic data is anchored in a few
real examples. Claude generates a simple page showing every input and waits for
confirmation (Figure 3: inputs for an e-mail router app).

### Validating the grader

Claude proposes the cheapest grader that fits the output:
- **Programmatic verification** when outputs are constrained: exact match, label
  from a fixed set, JSON matching a schema, passing tests.
- **LLM-as-judge** (default for open-ended outputs with clear quality criteria): a
  second model reads input, output, and a rubric written as checkable claims (not a
  1-to-5 scale), returns score + reasoning. With a baseline, the judge sees both
  outputs in random order, unlabeled, and picks the better. User picks the judge
  model; it should not be the model under test.
Claude grades a handful of cases and asks whether the user would score any
differently (Figure 4). Read a sample of scored transcripts before trusting the
evaluator; scoring failures are among the most common misconfigurations.
After grader validation the skill reports eval size (cases × repeats × model, and
approximate duration), runs the baseline, prints score with a confidence interval.
Outputs: cases, grader, runner, one JSON line and one full transcript per case, and
a plain page listing each case's score with a transcript link. Extra pages (e.g.
charts) on request; by default static local files that load nothing from the network.

### Diagnostic checks

During baseline runs:
- **Grader**: run the grader twice on the same output; report whether the verdict changed.
- **Plumbing**: check for timeouts, API errors, cut-off answers, so infrastructure
  noise isn't read as model variance.
- **Headroom**: if baseline ≥ ~95%, warn that hillclimbing should target cost or
  latency rather than quality.

## Hillclimbing

Hillclimbing tunes parameters such as effort or prompts that trade cost vs
performance. Where to apply it:
- **Cheap iteration**: the modified surface should be cheap to change and revert.
  Many internal/customer efforts target text (prompts, skills); open-ended harness
  modification can mean extensive code changes.
- **Attributable**: score changes must be attributable to the modified surface.
  Successful example: skill triggering — the metric (trigger rate) is directly
  coupled to the skill description being edited.
- **Well-scoped objective**: a common failure is an open-ended "improve
  performance" request without regard to headroom; near-saturated evals or poorly
  scoped surfaces (e.g. open-ended harness edits) tend to stall. Cost is a broadly
  strong objective: even on a saturated eval, ask Claude to cut cost at parity.

### Overfitting

Even a good eval rarely matches the production distribution, so overfitting yields
a system better on the eval than in production. The eval can "leak" into the
harness (code around the model: prompts, tools, the loop calling Claude). Example:
an eval task benefiting from OCR leads the hillclimber to add an OCR tool that
rarely helps production. More broadly, hillclimbing adds harness features for edge
cases in the chosen examples (Figure 5). Three mitigations:
- **Split the cases**: a train set the hillclimber may read and a never-seen test
  set. Train up while test is flat is a common overfitting warning.
- **Never paste failures into the prompt**: if the hillclimber reads failing
  transcripts, it must never paste failure content into the prompt.
- **Keep answers structurally out of the model's reach**: models sometimes "reward
  hack" by directly finding eval answers.

## /claude-api hillclimb

User chooses which surfaces Claude may change: system prompt; skills or instruction
files; tool descriptions; model choice, effort level, other API parameters; harness
code. Claude asks for the objective (performance, or cost while performance holds),
then randomly splits the eval set into train and test. For a cost goal it considers
common cost drivers: prompt caching, auditing the prompt for compatibility with the
selected model, choosing model and effort.
- Before round 1: check that eval noise (score movement by chance) is smaller than
  the smallest improvement worth acting on; if not, say so and suggest more
  repetitions or cases.
- Each round: read the previous round's train transcripts, propose one change as a
  patch, aimed at a change whose effect can exceed noise — fix the failing behavior
  at its root (rewrite the causing section, add a missing rule) rather than reword a
  line. Run the eval. Train up + test flat → suspect overfitting, revert. Regression
  → revert. Train and test both up → keep (Figure 6).
- Stall for two or three rounds (or early, if no single fix could exceed noise):
  read each remaining train failure and sort by cause; can surface ambiguous cases,
  harness errors, run-to-run variance. Only legitimate failures continue into
  further rounds.
- Finish: leave code at the version best on the test set for the goal; report test
  result vs baseline with confidence intervals (Figure 7); if gain is within noise,
  say so and recommend against merging.

## Examples

### Hillclimbing for cost reduction

Internal customer-support benchmark, goal: reduce cost and improve performance. 44
tickets: 30 search, 14 held out. Start: Opus 4.8, default (high) effort, 74.4%
decision accuracy on search tickets, 4.6 cents/ticket.
1. Prompt audit removed mandatory tool-call rituals, a scratchpad step, and
   contradictory rules.
2. Tried Opus 5.5 at low effort: 87.8%, 1.9 cents/ticket (< half). Part of the
   saving is pricing: Opus 5.5 input/output tokens 20% cheaper than Opus 4.8, cache
   reads 60% cheaper.
3. Stepped down a tier: Sonnet 5 at low effort ≈ 88.9% at ~1 cent/ticket (Figure 8).
   (The post says "Sonnet 5", not Sonnet 5.5.)
4. Prompt improvements (routing rules, refund-cap cross-reference): Sonnet 5 at
   98.9%, about the same cost.
Held-out 14 tickets: final 90.5% vs original 78.6%, at about one fifth of the cost.

### Hillclimbing for performance improvement

Target: the `claude-api` skill itself, evaluated on a set derived from Anthropic's
documentation (can the skill correctly implement API-using code). Start 66% (chart:
66.1%). Hillclimber given access to docs and SDKs to find and self-correct errors.
- Found missing coverage of eight features; adding sections → 74%.
- Fixed errors in C# and Java type tables → 77%.
- Stalled two rounds; reflection step (no edit, sort every remaining failure by
  root cause; a normal round makes one edit for the most common failure):
  - Content was present but Claude wrote older API shapes from trained priors. Fix:
    a table near the top of the skill mapping remembered forms to current ones —
    e.g. extended thinking with a fixed token budget (now rejected by the API on
    recent Opus models) → adaptive thinking; older web search / web fetch tool
    versions → current. Also moved C#/Java warnings against fixed-budget thinking
    above their adaptive-thinking examples → 80%.
  - Tasks that never improved despite fixing obvious content gaps signal flawed
    examples or graders: one task asked to catch one error type while its grader
    required a chain of at least three (task reworded); another grader's
    instructions contradicted the docs, and testing the real API showed the docs
    right. With further skill edits → ~88% (chart: 87.9%; "three phases of work").

## Getting started

`claude update` (the skill ships inside Claude Code), then `/claude-api build-eval`
(steer by providing examples such as traces; Claude designs examples and grader and
gets user approval of both) and `/claude-api hillclimb` (given an eval and a goal;
checks for overfitting and for eval bugs — a grader marking a correct-looking answer
wrong, harness errors — before round 1 and whenever the score stalls).
Acknowledgements: Misha Khalman (skill development) and reviewers.
