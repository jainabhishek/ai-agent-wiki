# How the Claude Code team does code review — Anthropic (claude.dev blog) (raw capture)

> Source: https://claude.dev/blog/solving-code-review-at-anthropic/
> Publisher: Anthropic (claude.dev blog) · Date: 2026-10-15
> Captured: 2026-11-24 via curl (HTML stripped to text), condensed paraphrase.
> Byline: Addy Osmani, Morgan Westlee Lunt, and Qing Wang; category "Engineering"; 14 min read.
> The URL slug says "solving-code-review-at-anthropic", but the page `<title>`, headline, and
> JSON-LD `headline` all say "How the Claude Code team does code review". JSON-LD
> `datePublished` is 2026-10-15. Figure values (Fig A–D) were read from the SVG text and
> aria-labels embedded in the page. Reviewers thanked: Emma Webb, Michael Segner, Amie Rotherham.
> The post names no model. The related-posts navigation is omitted.

Subtitle (paraphrased): once coverage and review depth were high, the team optimized for the
least human review time that does not raise reverts or incidents.

## Introduction

- Claude writes about 90 percent of Claude Code's own code.
- June to September: merged PRs to Claude Code's codebase more than doubled, while the share
  reverted fell by more than 40 percent.
- Review was not removed. Most reading moved to machines, optimized for human time, with heavy
  investment in fast, easy undo.

## Rethinking the purpose of code review

- Anthropic's monorepo: roughly 2,500 changes landed daily in May; by September, over
  30,000 a day. Claude Code has its own repo, also under pressure. Line-by-line manual
  review is close to impossible at this pace.
- Review serves two purposes: catching problems pre-release, and spreading knowledge of the
  codebase across the team. The post focuses on the first, returns to the second later.
- "Did a human read the code?" is called an imprecise proxy for: what could go wrong, and which
  check (automated or human) should catch it.
- Review moved from a gate at the end to a continuous process, like spellcheck while writing.
  By the time a person is asked, Claude has usually done at least one review-and-fix pass.

## The scarce resource: human time and attention

- Human time covers both reviewing and fixing what bad code breaks; cutting the first is no gain
  if it reappears in the second.
- Goal: across the Claude Code repos (CLI, desktop and web apps, mobile apps), most PRs should
  land with no more than one person involved (the author may be that person) and no increase
  in reverts or incidents.
- Human-time metrics: per-PR human approvals (median and p95), human comment counts, and how
  long PRs sit waiting for someone. The guardrail metrics are reverts and incidents.

## The life of a change

- **Fig A** (flow, from SVG text): Before the PR — the work is verified (Claude runs tests,
  build, linter; a second agent reviews the diff in fresh context). On every PR — required CI
  (lint, types, cross-platform tests, build and packaging; red blocks merge); Claude code review
  (parallel bug hunters, verifiers vote, survivors ranked by severity); security review (separate
  pass; open findings from either review block merge); risk-based approval (a classifier sets
  the tier: no person, one, or two; some paths always need a person). Merging — merge queue
  (checks rerun on latest main with the change applied). After the merge — behind a flag, used
  internally first; gradual release (latest channel first, stable trails); watch, fix forward,
  or roll back. Caption: most of the path is automated; human attention goes where the risk is.

## Layer by layer

- **Fig B**: six layers (verification, required CI, AI review, security review, human approval,
  merge queue plus flags) each with holes in different places; fast rollback sits beneath them.

### 1. The work is verified before anyone else looks
- The bulk of review now precedes the PR. Claude gets a runnable check (tests, a build, a
  design screenshot to match) and must present the output instead of just declaring success.
  A subagent then reviews the diff with fresh context. Both habits are from the best-practices
  guide.
- Before a PR, many engineers run internal skills: one hunts bugs, one simplifies the diff, one
  checks behavior end to end. UI changes are checked against design guidelines.
- Boris Cherny (creator of Claude Code) ranks self-verification as likely the single biggest
  lever on output quality, estimating a 2–3x better result. The form varies by field: one shell
  command, a suite of tests, or a run in a browser or a phone simulator.
- Repeated reviewer flags get fixed upstream: the skill, a
  lint rule, or instruction files:
  - `CLAUDE.md`: what the project is (stack, conventions, goals, non-goals). Every review loads
    it, so keep it short and point to other docs. The reviewer also points out code violating
    those conventions and edits that leave a line of the file outdated.
  - `REVIEW.md`: owners use it to tell the reviewer what to care about in their code. The team
    checks separately whether the reviewer follows it. Good ones are short; state what failure
    looks like in that repo (docs: "it lies"; config: "it misroutes"); cap nits; list paths to
    skip; require a file and line as evidence rather than a guess from a name; ask for a summary
    that opens with a count and says plainly when nothing needs fixing.

### 2. AI review on every pull request
- Claude reviews each PR ahead of any human. It weighs the diff against the full repo and what
  the PR says it intends: is the problem solved, does it fit, does anything else break? For a
  bug fix it hunts for the underlying cause.
- Externally the product is Code Review for Claude Code, generally available on Team and Enterprise
  plans; `/code-review` runs a lighter version locally.
- With the research-preview launch, internal PRs receiving substantive comments rose 16% → 54%.
  Large PRs (over 1,000 lines) usually draw findings; small ones usually do not.
- Per-repo depth setting chosen by admins: Quick, Standard, or Deep. Choose Deep when a single
  escaped bug would outweigh the added review time.
- Findings are verified by other agents before humans see them: several agents hunt in
  parallel, a separate group votes on each finding, and only findings with enough agreement are
  posted. Style-, diagnostics-, or cleanup-only findings are dropped; these filters were A/B
  tested on internal PRs. Output: inline comments sorted by severity, tagged Important, Nit, or
  Pre-existing.
- Every finding must be answered: fix it or resolve the thread with a reason. An agent often
  picks up the fix overnight.

### 3. Security review that can block
- Separate automated security review. A PR cannot merge while any bug-review or security-review
  finding is open; close a false positive with a short reason. A later fixing commit clears the
  finding automatically.
- Public equivalents: the open-source security review GitHub Action and `/security-review`.

### 4. Automated checks that block
- Lint, type checks, tests on every platform, build. A typical CLI PR may run dozens of checks
  before anyone looks. (Links to the post on scaling CI.)
- PR template fields: how it was tested, how to roll it back. Claude may draft the answers;
  the requester of the change is the one who signs off.

### 5. Human approval, scaled by risk
Risk table (paraphrased):

| Risk | Examples | Human approvals |
|---|---|---|
| Low | Documentation and copy edits, internal-only features, flagged additions | Zero, after automated and security review pass |
| Medium | Everyday product work; touchy areas (caching, auto-updater, system prompts) | One |
| High | The riskiest code and a few paths that always need two people | Two |

- The tier depends on what changed, not on who wrote it. A classifier assigns it from the change. A
  second classifier asks whether this change needs another person even if its tier says no.
  Owner-listed sensitive paths and any CI workflow file always need a person.
- Only authors on the repo's trusted list (mostly the owning team) get the lighter paths;
  everyone else needs a second approver. An agent's approval never counts as a person's.
- Whoever prompted an agent-written PR counts as one of the required reviewers.
- An approval covers one commit. New commits the system cannot vouch for (an agent's push, a
  hand-resolved merge) require re-approval.

### 6. Merge queue, flags and a gradual release
- The merge queue reruns every check against main with the change applied, so two separately
  passing PRs cannot combine into a broken main. New behavior ships behind a flag to employees
  first; public releases go to the latest channel, then stable.

### 7. Fast detection, fast rollback
- Flags can be switched off with no deploy. Weekly on-call rotation. Each incident review names the layer
  that ought to have stopped it.
- Spotting a bad merge still relies on the author, the on-call engineer, and dashboards of
  reverts and incidents.
  There are no circuit breakers yet that tighten approval when those numbers move; engineers
  want them before more code moves to zero-human merges.
- A colleague's point, paraphrased: slowing down lowers errors mostly by doing less; the team
  prefers getting faster at noticing and fixing.

## How we make the reviewer better

- Incidents are the eval. Past PRs that caused incidents, with fix-forwards and reverts, were
  collected; engineers who know the code confirmed each bug and its location. The reviewer runs
  against the set daily.
- **Fig C** (loop): incident or revert → expert-checked case → added to the set; a change to the
  reviewer (prompts, tools, or model) → daily eval run against every case → keep if the score
  rose, drop if not.
- Noise: every comment is sorted by the PR author's response (fixed it; said it was wrong; said
  behavior was intentional; decided it did not matter). The reviewer also runs on known-clean
  PRs, counting reports that would have led to a harmful change. Written priority: catch real
  bugs first, cut review rounds second.
- Noise costs more with an agent author: a person waves off a nit; an agent fixes it, adding a
  commit and another review round.
- Review must converge. One CLI PR went through more than fifty review-and-fix rounds overnight
  before its author stopped it. `git blame` on repeat flags: about 59% was code present since
  the reviewer's first pass — it found a few more old bugs each round, rarely new ones. The team
  had made it worse by running several rounds by default.
- The team tracks rounds-to-pass alongside recall. Changes to re-review:
  - Round cap: at three rounds, the reviewer tells the author to rethink the approach.
  - Later passes look only at the new diff.
  - Name the bug class, so every occurrence gets fixed rather than a single line.
  - Never re-post a finding.
- Separately, review agents sweep the existing codebase every night.
- **Fig D** (internal PRs, before → after the convergence work): pass after one review-and-fix
  round 65% → 78%; PRs needing five or more rounds 8.9% → 1.5%; mean reviews to pass
  2.08 → 1.32.

## Where humans stay in the loop

- Pulling a senior engineer from deep work for a routine mistake costs far more than automated
  review. People remain responsible for:
  - Deciding whether to build it (direction, taste, scope). Even a team that considered its review
    bottleneck fixed kept a person reviewing contributions from other teams.
  - Reviewing risky code (billing, the auto-updater, CI workflows).
  - Reviewing architecture that sets a pattern others copy.
  - Reading the evidence (test output, the command and its result, a screenshot, findings). If
    you cannot say what the checks would miss, ask for a real review.
  - Owning the outcome: every shipped change has an accountable person.

## Sharing context across the team

- No formal process. Nobody holds a complete mental model of Claude Code, and the team thinks
  nobody needs to. To learn a slice, ask Claude for an explainer of exactly that slice (minutes;
  current code). Some have Claude build a small visual artifact tailored to how they learn.
- An explainer for the module you will change teaches more than reading trivial diffs. Working
  in open Slack channels also spreads context.

## "You land it, you own it"

- Team norm: if your small or medium change breaks, you usually fix it. Safeguards: small
  changes; everything reversible (flags, reverts, and staged rollout fix most errors within
  minutes); the bar scales with blast radius; regressions surface fast via telemetry and internal use;
  not blame (incident reviews look at the system).
- Ownership is shared through open channels; feedback comes from non-owners too.

## When we change direction

- Agents make starting cheap, so some work should not land. Typically a channel member questions
  the motive, recalls a prior decision, or proposes something simpler, and the PR is closed or
  reworked. Push back early in the discussion rather than blocking a completed PR.

## How you can adopt this process

### Before the pull request
- A brief `CLAUDE.md` naming the checks the agent can run; hooks for formatting and linting.
- Local `/code-review` and `/security-review`, or a subagent reviewing with fresh context.
- Create `REVIEW.md` and migrate recurring review remarks there.

### On every pull request
- Make CI mandatory; give the PR template "Testing", "Risk", and "How to revert" sections.
- Pilot an AI reviewer, either Code Review for Claude Code or the Claude Code GitHub Action, in a
  single repo, refine `REVIEW.md` over several weeks, and expand afterwards.
- Turn on automated security review; block merge until all review threads are resolved.
- Scale review depth with risk (Quick, Standard, or Deep).
- Limit the number of rounds; beyond the first few, check only what is new.

### Approval
- Written risk tiers set from the change, not the author; start strict, loosen with evidence.
- Lighter approval paths only for trusted authors.
- Use CODEOWNERS plus branch protection to force a human on auth, billing, installers, and CI
  and release workflows.
- A bot's approval never replaces a required human's; dismiss approvals on new commits.

### Merge and after
- Merge queue, feature flags, internal use first, staged releases, one-step rollback.
- Build an eval set from incidents and reverts; re-score the reviewer after any change to its
  model, tools, or prompts.
- Track human time; reverts and incidents act as the guardrail.

## Where this is going

- At launch, Code Review was positioned as leaving PR approval to humans; it posts findings,
  never approvals. Internally the team goes further: owners pick which low-risk changes may land
  on automation alone, and that boundary keeps shifting.
- After a review miss, ask what context the model was missing and encode the fix in
  `CLAUDE.md`, a skill, or an added check. Goal: less human time per change, no more reverts than before.
- Invites readers to share which checks they automated and which still need a person.
