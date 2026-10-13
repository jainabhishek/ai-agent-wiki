# How to prepare for AI-driven code modernization projects — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/how-to-prepare-for-ai-driven-code-modernization-projects
> Publisher: Anthropic (claude.com articles) · Date: 2026-09-23
> Captured: 2026-10-12 via curl (HTML downloaded, text extracted locally; condensed).

Authors: Jonah Ezekiel, Lexie Tonelli. Category: Best practices, Perspectives.
Product: Claude Code. Reading time 19 min. Part of the "Notes from the Field"
series, in which Anthropic forward deployed engineers (FDEs) share practices from
customer deployments. Scope: critical systems and regulated enterprises.

## Introduction

- Modernizations once scoped as multi-year efforts can now finish in months or
  weeks, but the organizational work around them is unchanged.
- Change management, review, and approval (e.g. for a critical banking system)
  assume a human wrote and a human reviews each diff. Once agents accelerate
  writing, the bottleneck shifts from producing changes to mobilizing the
  organization around them.
- Six steps:
  1. Define the target (stack and behavior of the modernized code).
  2. Create the certificate (conditions a change must meet to count as correct).
  3. Set the promotion policy (path for certified changes into production at the
     rate they are produced).
  4. Put prerequisites in place (environment, CI/CD, review capacity, approvals).
  5. Build and refine the agentic workflow (a custom Claude Code dynamic workflow
     that splits the work across many parallel subagent workstreams).
  6. Run the modernization (prove end to end on a small partition, then scale).

## Step 1: Define the target

### Determine the modernization type

| Type | What it is | Choose when | The target is |
|---|---|---|---|
| Uplift | Same-stack version bump (e.g. C++11 → C++20) | Stack is fine but version is behind: EOL runtimes, unpatched security issues, dependencies that can no longer upgrade | A runtime version and package set |
| Transform | Cross-stack rewrite, behavior fixed (e.g. COBOL → Java) | Stack is the problem; behavior is trusted | Uplift target plus language, frameworks, architectural conventions |
| Reimagine | Greenfield rebuild on new architecture with modified behavior | Behavior must change alongside code | Transform target plus a written behavioral spec |

- Typical split: people closest to production want a transform (contain risk);
  long-time engineers want tech-debt paydown and business stakeholders want new
  requirements (reimagine). Unresolved, the disagreement resurfaces later as
  arguments over whether a change is "correct". Settle it up front.

### Map the codebase and create the behavioral spec
- Inventory what the old code actually does; this decides change/drop and so
  transform vs reimagine, and surfaces unknown business logic and edge cases.
- Claude maps dependencies and documents forgotten workflows. The code
  modernization plugin's `assess`, `map`, and `extract-rules` commands mine
  business rules with source citations for engineers to review.
- Claude's discovery alone may miss behavior; add interviews with business users
  and developers and internal docs.
- Reimagine needs a detailed behavioral spec agreed with user groups.
- (Figure: interactive dependency map from the plugin.)

### Establish the project's justification and goals
- Cost reduction has rarely been the driving goal in the authors' experience.
  Risk reduction is often the most important benefit; weigh the risk of not
  modernizing (unpatched vulnerabilities, unsupported runtime, shrinking pool of
  engineers who know the system).
- Budgets remain hard to estimate, which causes inertia; Anthropic and others
  have published costs of large modernizations as rough baselines.
- Main challenge: consensus and commitment from owning and dependent teams.
  Leadership-level business case and goals anchor later tradeoffs; the risk of
  not modernizing is the counterweight when stakeholders disagree on risk.

## Step 2: Define the certificate

- The certificate = conditions/tests every change must meet; choose those giving
  the strongest cumulative evidence of correctness against the target.
- Each condition must be checkable without a human, so the workflow can iterate
  until the certificate is met or flag the change for human review.
- Typical conditions:
  - original test suite passes;
  - Claude-authored tests from the modernization pass;
  - coverage meets an agreed threshold;
  - performance benchmarks within an agreed bound;
  - independent adversarial reviews by Claude, each in a fresh context window,
    find no blocking issues;
  - for UIs, Claude-driven computer use finds no regressions;
  - current and target versions give the same output for the same input (live,
    recorded, or Claude-generated input);
  - persisted state and wire formats round-trip between versions;
  - staging run for an agreed period with no regressions in error rate, latency,
    or alerts;
  - static analysis and security scans show no new findings;
  - for compiled targets, clean build and type checks pass.
- Write the certificate with the people who will review and promote changes
  (developers, user groups, business leads) while the workflow is being designed.
  Test: would they merge on the certificate's evidence alone? If so, the
  promotion policy can be lighter.
- By type:
  - Uplift: parity against the original; the original test suite can be the core.
  - Transform: parity against the original, but old tests rarely run on the new
    stack; production traffic replay, differential testing, and a prod-parallel
    deployment do most of the work.
  - Reimagine: anchored in the behavioral spec; hardest case, more model
    judgment, more variable outcomes. Leans on spec-derived tests, adversarial
    reviews against the spec, and differential checks where behavior is kept.
    Expect to revise the certificate as the spec is clarified.
- Legacy systems often have thin coverage, flaky tests, little telemetry. Use
  Claude to build the missing evidence: a prod-parallel setup, a replay harness,
  more tests.

## Step 3: Set the promotion policy

- Agents outpace diff-by-diff human review. The promotion policy is a tiered
  review path, written and agreed in advance, setting human review depth per
  change. Fit it into existing change management.
- Rules that hold everywhere:
  - Tier changes by blast radius and agent confidence (use the org's own risk
    classification if it has one); keep full human review for critical paths.
  - Fix recurring flags at the source: group flagged changes over time and fix
    the cause in the workflow or certificate instead of reviewing each.
  - Design the output format with the reviewers; have them review early samples
    in Step 5.
  - Allocate SME time to the highest-risk tiers and the flagged agent decisions
    within them, without large diffs.
- SME hours are front-loaded — the reverse of the traditional pattern where
  review happens at the end. Their sign-off on samples justifies lighter review
  where confidence is high.
- Speed vs review depth: a hard deadline (runtime losing support) needs lighter
  review and explicit acceptance of more risk per change; a longer timeline
  affords deeper review and slower cutover. Lock this in before work starts.
- Regulated environments: approvers hesitate because they carry the risk of a bad
  change while leadership carries the larger risk of an aging system. The
  directive should come from the top and be agreed in advance, so responsibility
  for a production bug is shared.
- All of this depends on a certificate detailed enough to be real evidence and
  reviewers who understand how Claude arrived at a change.

## Step 4: Put the prerequisites in place

Much of this runs through other teams (platform, QA/release engineering,
security/compliance) with their own backlogs — start conversations early, during
Steps 1–3.

### Environment
- Dedicated remote host for the workflow, with codebase and sources reachable.
- Test capacity as the certificate requires.
- Anything that strengthens the certificate: production telemetry, prod-parallel
  setup, production data for replay.

### Codebase and CI/CD
- Dependency map grounded in build/compile logs, import analysis, or runtime
  traces (the plugin's `map` command is a start; large/old codebases need more).
- Planned treatment of dependencies/packages as part of the target.
- A compatibility check ready to add to CI/CD if needed.
- Agreed code-freeze policy when modernizing in place.
- Communication plan for active developers (freezes, new compatibility rules).

### Teams and review
- Agreement from dependent teams on their role (certificate sign-off, review
  under the promotion policy) with reviewer time reserved.

### Security and compliance
- Approved model access path for Claude Code on source code.
- Least privilege: write only to modernization branches, no production
  credentials.
- Secrets and PII scrubbed or masked from the modernization branch.
- Every change traceable; each PR linked to an agent transcript and certificate
  evidence.
- License and vulnerability checks on new dependencies.

## Step 5: Build and refine the agentic workflow

- Use Claude Code to build a custom dynamic workflow. Start from the code
  modernization plugin; put everything on the file system or behind MCP: target,
  certificate, promotion policy, codebase, docs, data sources, certificate
  tooling (the article itself can be given as context). This is the project's
  central knowledge base.
- SMEs review Claude's work, including codebase-specific skills and extracted
  rules, before anything downstream relies on it.
- Refine on small parts of the codebase; SMEs review changes, agent process, and
  certificate evidence. When issues surface, change the workflow, not each
  individual change. Goal: confidence that at scale changes almost always meet
  the certificate and reviewers are comfortable merging under the policy.

## Step 6: Run the modernization

- Complete end to end on a small part (including review and landing via the
  promotion policy); fix what breaks while cheap; repeat; then scale.
- Transform and reimagine build alongside the old system and cut over. Uplift
  can also modernize in place while development continues (when the system cannot
  go down or changes too fast for a separate copy): partition the codebase from
  the leaves inward, freeze and modernize one partition at a time, and gate CI/CD
  so new commits cannot undo a modernized partition.

## A note on cost

- Token cost drivers: how much code is read vs changed; how involved the
  certificate is (in regulated settings verification, not writing, is usually
  the larger share); how much new test writing and repair is needed; how much
  reconciliation comes from other teams merging during the run.
- Measure token usage in the pilot and extrapolate; treat what the pilot could
  not see (e.g. reconciliation on a live codebase) as unknown — the result is a
  cost floor.
- Optimize: find the most token-hungry workflow parts; put compute-heavy
  verification behind cheaper gates that run first.
- Use cost/capability-balanced models such as Sonnet for mechanical, high-volume
  work the certificate fully checks; keep stronger models for hard
  transformations and adversarial reviews.
- Escalating to a pricier model after a cheap one fails is possible, but analyze
  retry rates in the pilot: several cheap attempts can cost more than one
  expensive one. Claude can do this analysis given workflow and pilot data.

## Beyond the modernization

Other outputs besides the code: the workflow, a written certificate, a promotion
policy already accepted by change management, and an evidence trail per change.
Codify the playbook as a reusable asset for the next upgrade.

## Additional resources
Links: public codemod plugin for Claude Code; the AI-Native SDLC playbook; a code
modernization playbook; "COBOL Modernization with AI: Breaking the Cost Barrier".
