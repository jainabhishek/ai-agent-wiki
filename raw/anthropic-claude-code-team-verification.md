# How the Claude Code team thinks about verification — Anthropic (claude.dev blog) (raw capture)

> Source: https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/
> Publisher: Anthropic (claude.dev blog) · Date: 2026-11-16
> Captured: 2026-11-24 via curl (HTML stripped to text), condensed paraphrase.
> Byline: Addy Osmani; category "Engineering"; 10 min read. Byline and JSON-LD
> `datePublished` both give 2026-11-16. Fig A content was read from the image's alt text.
> The post names no model. The related-posts navigation is omitted.

Subtitle (paraphrased): how end-to-end, property, and differential tests let coding agents
check their work with evidence, and how the Claude Code team keeps its verifiers honest.

## Introduction

- On the Claude Code team, Claude writes and reviews about 90% of the code. At that scale,
  how agents verify their work with evidence matters most.
- Verification loops are what let you delegate more. Without them you can run only one or two
  Claudes at a time because you check everything yourself; with them, dozens or hundreds in
  parallel.
- Internal testing on structured file generation: adding an independent rubric-based grader
  lifted task success as much as 10 points versus a plain prompting loop; the hardest problems
  gained most. (The figure links to the Claude Managed
  Agents launch post.)
- Tests, benchmarks, specs, and real end-to-end runs used to be expensive; an agent now
  generates them cheaply, and once written they run as software without many extra tokens.
- Close the loop: if an agent keeps failing a test (example: a test that checks logs for user
  data), add a hook or a more explicit `CLAUDE.md` rule. This "(mostly)" stops repeats.

## Not all tests are created equal: 3 tests worth investing in

Failure modes for any test type:
- Flaky tests teach the agent to rerun instead of fixing the code.
- Slow tests make the agent run fewer tests across batches, which makes issues harder to
  pinpoint. Run heavier tests before the change is committed.

### E2E tests
- If you pick one type, pick end-to-end. E2E tests describe real user flows (add to cart,
  check out, reach the confirmation page).
- They are hard to fool: the whole feature works or it does not. They have clear done criteria
  and say concretely what broke.
- **Fig A** (alt text): a unit test failure shows only "Timeout after 30s" ("shooting blind");
  an E2E failure shows a step trace (Register, Add item to cart, Checkout failed, confirmation
  page not reached), a screenshot with "Payment form failed to load", and a description of the
  failed step.
- Unit tests are faster and less flaky, but an agent can pass them and still break the feature,
  because neither the agent nor the test understands the full task.
- Give the agent "hands and eyes" on the running system: a skill that boots, drives, and
  inspects the app with tools like CDP, simulators, or API harnesses.
- A feature map (features from the user's view, with paths, keyboard shortcuts, selectors, and
  expected results) can serve as a guide and grading rubric.

### Property tests: constraints that can't break
- Many tests encode what you guessed might go wrong. Property tests probe the edge cases people
  miss, which is where agents often fail.
- Write a statement that should never fail, then let a library generate thousands of inputs
  that try to break it: fast-check (JS/TS), Hypothesis (Python), proptest (Rust).
- Common properties: round-trip encoding (encode then decode gives X; also parsing and
  serialization); invariants ("account balance can never become negative"); idempotency (a
  migration, normalization, or retry done twice equals once); equivalence (optimized code
  matches naive correct code).
- Generated edge cases do not share the bias of the agent that wrote the code. Useful for
  rewrites where the spec has drifted from production behavior.

### Differential tests: the old system is the oracle
- For large migrations where behavior should not change: run old and new systems on the same
  inputs; any difference is a bug or a breaking change.
- Use random inputs or sampled production traffic. Normalize irrelevant factors such as
  whitespace. Keep a list of approved differences.

## How the Claude Code team thinks about verification

Links back to the earlier code review post; this one goes deeper on verification.

### Verification means running the change
- The team ranks an end-to-end run of the app above tests. Analogy: nobody ships an iOS change
  untried in a simulator.
- Claude can exercise the app like a person or QA engineer: web via the Claude Chrome
  extension, mobile via an iOS or Android MCP, desktop via computer use, backend via a local run.
- Codify start-up in a skill named `verify`, under `.claude/skills/` in the repo, as close to
  the relevant code as possible; add as many as needed. Claude knows to use the verify skill
  before committing.
- Make the verify skill fast and reliable; ask Claude to iterate on and stress-test it. It is
  your smoke-test harness. The team tests nearly all changes at Anthropic this way.

### Failing tests require human attention
- Reading every change is impossible, so failures are what route work to people. Claude
  executes the checks and attempts repairs; a check still red after three rounds makes Claude halt and hand off
  to a person.

### Code owners write their own checks
- Owners write the checks for their code and refine them until they flag what the owner would.
  A check that pulls in a reviewer should say why.

### Reliability checks trigger on the diff
- A reliability checklist of 39 items. Every item pairs a diff-detectable trigger and a check with
  the incidents or PRs that motivated it. Example item: "--resume loads old transcripts" — when session
  storage or message types change, ask whether a new field loads safely from older transcripts.
- Claude reads the diff and checks only items whose trigger matches, usually 3 to 10, so nobody
  memorizes past outages.

### One reviewer, multiple rounds
- The team does not stack reviewers. A second, more expensive reviewer on top of the primary is
  often worse than tuning the primary. A `REVIEW.md` says what the reviewer should look at for
  this code.
- Rounds build on each other: each pass gets context from earlier rounds and past failures
  instead of re-checking from scratch. Cheaper, and finds more.

### Changes can't modify their own checks
- A check that the change under review can edit is not a real check. Code Review takes
  `REVIEW.md` from the base or default branch and ignores any copy in the PR. The gating rules
  sit on a branch that the change has no write path to.
- Reviews are reserved for commits: a pass on an out-of-date commit means nothing if someone
  pushes during review.
- Cheap checks first: Claude runs tests, build, and linter before opening a PR. Enforce it via a
  hook that fires the tests once Claude is done, or set `/goal` to a green test suite.

### Start a new gate in observe mode
- Each commit is stamped with how it was verified; the stamp can be "none", so unverified
  commits are queryable.
- A commit gate may refuse a commit when the session lacked `/code-review` or `/verify` (the
  post does not say whether one suffices).
  Modes: off, observe, enforce.
- Observe logs what would have been blocked, to review false positives.
- Enforce blocks. A commit message can explain why it was not verified. After two blocks in a
  session the next commit is allowed through, so Claude does not get stuck.

### Test your checks on what actually matters
- The team reviews the reviewers: it tracks merged changes later reverted, changes a maintainer
  rejected before merge, and a size-matched subset of changes that stayed clean.
- Formal eval (the post attributes it to the earlier code review post, but the capture of that
  post at raw/anthropic-solving-code-review.md does not contain these details): past incidents and reverts; the repo is recreated at
  review time; a one-sentence answer key names the bug; only findings that describe that bug
  score. Merged, stable changes are a control against over-flagging. The tuning set is separate
  from the fixed test set.
- Recall is measured separately for raw findings, post-verification, and final review, to see
  whether the system loses bugs it already found. A single end-to-end score hides this.
- Second dimension besides validity: importance (must-fix, should-fix, nit). Code Review tags
  findings Important, Nit, or Pre-existing; Pre-existing means the author is not held
  responsible.
- Recall is tuned up to the point where the next gain would be overfitting to the eval.

### Turn misses into rules
- Method 1: mine human review comments and PR reverts for patterns. A candidate needs two or more
  PRs showing it and must be detectable from a diff alone. Three agents try to disprove it; a human
  approves it in a PR.
- Method 2: replay three bug finders against a PR tied to a known incident. If at least two find
  it, the bug is detectable. A miss on a small diff is a gap worth a rule in `REVIEW.md`.
- Flaky tests: skipping, inserted sleeps, and retry-until-green are all off limits for Claude.
  When no root cause turns up, the test is removed and the reason recorded.
- Rules need cleanup: test suites, verification steps, and `.md` files only grow, so they are
  tidied on a routine.

## Good tests, good results

Treat the verification layer as a system: keep it out of reach of the changes it judges, grade
it against the bugs that mattered, record lessons from misses, and prune them. The human job
shifts from reading every diff to defining "done" and reviewing the evidence, which lets you run
many Claudes at once.
