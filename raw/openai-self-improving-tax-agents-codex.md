# Building self-improving tax agents with Codex — OpenAI (raw capture)

> Source: https://openai.com/index/building-self-improving-tax-agents-with-codex/
> Publisher: OpenAI (Engineering) · Date: 2026-05-27
> Authors: Aravind Srinivasan, Samay Shamdasani (Thrive Holdings); Arthur
> Fernandes Araujo, John de Wasseige (OpenAI).
> Captured: 2026-10-12 via built-in browser (condensed). Case study; all figures
> are self-reported by the authors.

## Introduction

- Production failures are hard to predict; teams usually fix them by hand after
  launch, slowly. The post claims that with eval infrastructure, direct access to
  practitioners and real environments, and Codex, agents can self-improve.
- Over six months, OpenAI forward-deployed engineers and researchers and Thrive
  Holdings engineers built "Tax AI" with and for Crete, a network of 30+
  accounting firms, to prepare 1040 and 1041 returns.
- Crete prepares tens of thousands of returns per season from millions of
  documents; data entry for medium-to-large returns can take eight hours each.
- Tax AI processed 7,000 returns in the pilot season.

## Measurable self-improvement

- Practitioners upload source files and client notes; Tax AI produces a
  tax-engine submission for review. Reported: about a third of preparation time
  saved, drafts up to 97% accurate, throughput up about 50%.
- Accuracy metric: share of returns reaching 75%, 90%, or 100% correct field
  completion. At launch about a quarter reached 75%; within six weeks 86% did;
  the 90% and 100% levels grew faster.
- Scope grew from W-2s and 1099s to K-1s, schedules, and edge cases.
- Three pillars: practitioner feedback; production traces (full history from
  inputs to final output); a Codex-driven iteration loop on tailored evals.

## The problem

- Harder work (K-1s, rental real-estate schedules, values reconciled across
  files) showed that the real challenge was making production failures visible,
  understandable, and actionable.
- Early corrections were manual and lacked context: a changed value could be an
  extraction miss, a mapping problem, unsupported product behavior, or expected
  workflow noise. Engineers had to sort this out; there was no signal for
  "the right hill to climb".

## Our approach: a three-part loop

1. **Stay close to practitioners** — they decide which errors matter.
2. **Build the product so production creates evidence** — capture the path from
   source material to extracted fields with provenance, to submission, to
   expert correction.
3. **Create a Codex-driven improvement loop** — structured issues become
   findings, tailored evals, and scoped engineering tasks; Codex investigates,
   proposes changes, and validates against targeted and regression evals.

## Rental property example

Rental income goes on Schedule E. The system reads messy sources (handwritten
notes, emails, spreadsheets), extracts fields it can confidently map, and keeps
evidence (citations to source) so a practitioner can approve or correct.

### 1. A practitioner correction reveals a failure

A predicted-vs-filed difference may be an extraction miss, practitioner
preference, a prior-year carry-forward, or a change elsewhere in the workflow.
Practitioners helped classify these. Review became a continuous learning step:
the workflow records what Tax AI proposed, what the practitioner changed, and
what was filed.

### 2. Product traces turn corrections into evals

Path: documents organized, split, classified → fields extracted with citations
→ mapped into the tax engine → possibly corrected. Three steps turn corrections
into eval targets:
- **Capture the difference:** compare output with the filed return into
  field-level review rows (expected, predicted, whether actionable).
- **Group related failures:** separate recurring failures from noise (e.g.
  missed fair-rental-days fields, mishandled "other expenses", confusing
  multiple properties in one package).
- **Turn repeated patterns into eval targets** once reviewed and measured.

### 3. The finding becomes a hill to climb for Codex

Example: Tax AI misses "fair rental days" that practitioners fill in. With a
targeted eval set (representative source packages, expected outputs), Codex
inspects the trace, eval, repo, and skills together:
- **Investigate the pipeline:** unsupported field, missed extraction pattern,
  source-selection problem, mapper gap, or grader issue.
- **Implement targeted fixes:** extend the extraction schema, improve source
  selection, update the mapper, or refine the grader if noise counts as failure.
- **Validate and propose:** rerun the targeted eval, run regression suites,
  open a candidate PR for engineer review.
- **Close the loop:** ambiguous or not-safely-automatable evidence routes back
  to the product team rather than being forced through.

## How to use Codex to build this loop

- Inputs to Codex: reviewed findings, source traces, expected tax-engine output,
  relevant code examples, eval commands. Builds on OpenAI's harness-engineering
  and Symphony posts (legible tasks, scoped context and tools, validation and
  human review in the environment).
- Evidence becomes a Codex task only after repeated differences are reviewed and
  grouped into an actionable finding with a clear success condition.
- Automation is applied to a bounded layer (extraction and mapping). Engineers
  own architecture, product decisions, and shipping; practitioners steer through
  their normal work.
- Representative task environment `/candidates/FIND-RENTAL-0042/`:
  - `repo/` on branch `codex/fix-rental-0042` (writable worktree) with
    `AGENTS.md`; `tasks/FIND-RENTAL-0042/` (`task.yaml`, `EXEC_PLAN.md`,
    `RESULTS.md`); the product surface `app/tax-ai/rental-income/` (`agent.ts`,
    `schema.ts`, `provenance.ts`, `mapper.ts`); `evals/` (dataset
    `fair-rental-days.yaml`, suites `fair-rental-days.yaml` and
    `rental-income-regression.yaml`, grader `rental-income.yaml`); `skills/`
    (`eval-runner/`, `tax-field-docs/`); `docs/` (`architecture/`,
    `task-environments/`).
  - `scoped-tools/` (read-only production context): `production-trace`,
    `source-artifacts`, `tax-engine-docs`.
- The split lets Codex investigate without mutating the underlying evidence.

## Expanding to new domains

- Rental properties took about six weeks and substantial engineering oversight to
  reach 90% precision and recall; the reusable abstractions, review artifacts,
  eval conventions, and patterns then made Schedule C and Schedule A easier.
- Thrive Holdings, as owner-operator of businesses like Crete, works directly
  with practitioners and production data.
- One senior accountant went from 180 hours of tax prep last year to 15 hours.
- The same three-part design is being applied to bookkeeping, audit, and IT
  help-desk automation.
