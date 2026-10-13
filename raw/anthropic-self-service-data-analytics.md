# How Anthropic enables self-service data analytics with Claude — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/how-anthropic-enables-self-service-data-analytics-with-claude
> Publisher: Anthropic (claude.com articles) · Date: 2026-06-03
> Captured: 2026-10-12 via curl (condensed). Appendix templates described by structure, not reproduced.

Authors: Josh Cherry, Clement Peng, Johanne Jiao, Justin Leder, Chen Chang
(Anthropic Data Science and Data Engineering team). Category: Best practices.
Product: Claude Code. Listed reading time 5 min. Internal, self-reported results.

## Introduction
- Traditional self-service routes fail: wide denormalized tables create
  overlapping views with inconsistent definitions; ringfenced environments miss
  the long tail and cause dashboard bloat.
- Pointing Claude at a warehouse unguided gives a false sense of precision and
  cuts users off from curated datasets and expertise.
- At Anthropic, 95% of business analytics queries are automated via Claude, at
  ~95% aggregate accuracy; data scientists move to causal modeling,
  forecasting, ML.
- Post covers: accuracy as a context and verification problem; three failure
  modes; the stack; measurement; a skill template (appendix).

## Data is not software
- Coding is open-ended and has docs and tests as guardrails; analytics often has
  one correct answer from one correct source with no deterministic proof.
- Core problem: map a user's question to specific, current entities in the data
  model and know how to use them; then SQL is trivial.
- Three failure modes behind most wrong answers:
  - Concept–entity ambiguity: hundreds of viable fields (of possibly millions);
    example "active users" (which actions, fraud included, lookback window).
  - Data staleness: sources, definitions, schemas change; knowledge goes stale.
  - Retrieval failure: the right info exists and is annotated but the agent does
    not find it.

## Our agentic self-service analytics stack
Layer-to-failure mapping: data foundations and sources of truth → ambiguity;
maintenance and validation → staleness; skills → retrieval. (Ad-hoc Slack
questions are handled by a data agent on Claude Tag, covered separately.)

### Data foundations
- Standard practice still applies (dimensional modeling, shift-left testing,
  freshness and completeness checks). New: the consumer is an agent acting for
  non-experts who cannot validate correctness.
- Canonical datasets: fewer, heavily governed logical models; a small set of
  owned, consumption-ready, discoverable single-source-of-truth datasets;
  aggressively deprecate near-duplicates; physical rollups derive mechanically.
- Enforce standards via tooling (agent routed to canonical models first), CI
  (bypassing changes fail review), and mandate. Without enforcement governance
  decays.
- Colocate artifacts: modeling, semantic layer, reference docs, canonical
  dashboard definitions in one repo; CI protects cross-layer integrity, fixes
  ship in the same PR.
- Metadata as a first-class product: descriptions, metric definitions, grain,
  valid ranges, lineage, ownership, tiering.

### Sources of truth
In descending order of trust:
- Semantic layer: compiled metric and dimension definitions; one function call,
  one number matching every other surface. Agents are required by skill
  instruction to use it first. Failed experiment: LLM-generated metric
  definitions from raw tables and query logs encoded the same ambiguities and
  were net-negative on evals versus a smaller human-curated layer.
  Recommendation: Claude drafts docs, a human owns definitions.
- Lineage and transformation graph: lineage plus table ranking by reference
  count to find upstream, deprecated, and same-grain models; backbone of
  freshness and provenance signals.
- Query corpus: raw retrieval over thousands of prior queries moved accuracy by
  under one point. What works: distill into structured per-domain reference docs
  and reusable analysis patterns in skills.
- Business context: company knowledge graph (indexed docs, roadmaps, decision
  logs, org structure) to resolve ambient references and ask better clarifying
  questions. Called the most-skipped and longest-underrated layer.
- Common failure across all four: poor or stale documentation. Claude drafts
  descriptions and flags undocumented models in CI; humans curate and own.

### Skills
- Skills = procedural knowledge (which sources, in what order, how to handle
  ambiguity, what a finished analysis looks like).
- Without skills, accuracy on their evals did not exceed 21%; with skills,
  consistently above 95% in aggregate and around 99% in some domains.
- Pairwise skills: a thin knowledge skill routes (semantic layer first, else
  ~30 per-domain reference files on tables, columns, joins, gotchas) — their
  answer to retrieval failure. A runbook skill encodes a senior analyst's
  process: clarify, find sources, query, loop through adversarial review
  sub-agents; bundles about a dozen analysis patterns (retention curves, rate
  decomposition, funnel analysis).
- Reference docs written for LLM retrieval: table grain, scope, exclusions;
  gotcha mechanics (example: exclude free-email domains but keep custom ones);
  explicit IF/DO NOT routing triggers; no prescriptive recipes that go stale.
  Skeleton sections: Quick Reference (business context, entity grain, standard
  hygiene filter), Dimensions, Key Tables (grain, scope, usage per table),
  Gotchas, Best Practices / Common Query Patterns, Cross-References.
- Skill maintenance: offline accuracy drifted from ~95% at launch to ~65% within
  a month before maintenance was treated as engineering. Fix: skill markdown in
  the same repo as transformation models; a code-review hook flags
  reporting-model changes without a skill-file change; ~90% of data-model PRs
  now include a skill change. Scaffolding pruned as models improve.
- Same answer on every surface (Slack, IDE, dashboard tool, standalone agent):
  one canonical source; on merge, skills sync to a plugin marketplace (IDE), to
  cloud-storage blobs (hosted apps), and are served as MCP resources. No
  hardcoded repo paths or surface-specific namespaces.

### Validation

#### Offline evaluations
- Many teams have no accuracy process. Offline evals = question/answer pairs,
  like offline ML testing.
- Two kinds: dashboard-based (Claude-generated, human-validated, common
  questions) and long-tail (Claude generates plausible questions from roadmaps
  and table docs). Every stakeholder correction in a thread is a candidate eval.
- Practices: pin ground truth (snapshot date, stable fact table, or grade the
  query not the number), wire into CI so dependency PRs re-run affected evals;
  store results as telemetry in a warehouse table (skill version, git SHA, model
  ID, per-assertion pass/fail, token count, wall-clock); gate launches per
  domain (initially ~90% threshold); diminishing returns past a few dozen evals
  per topic, ceiling dropping each model generation; offline accuracy should be
  ~100% with every correct answer hitting the semantic layer.

#### Ablation techniques
- Hold the offline eval set fixed and vary one component; each run takes about
  an hour.
- Design for null results: direct grep access to thousands of dashboard,
  transformation, and notebook SQL files (verified read in transcripts) moved
  accuracy under one point; for wrong answers the answer was in the corpus ~80%
  of the time; "answer present" did not predict a flip. Bottleneck was
  structure, not access; redirected months of roadmap.
- Ablate at PR granularity with the before/after delta in the PR description.
- Keep a list of what did not work: doc refinement past three consecutive
  net-negative iterations (docs got longer, not better); a cheaper adversarial
  reviewer model lost most accuracy wins for no real speedup.

#### Online validation
- Adversarial review skill: +6% accuracy on the eval set, at +32% tokens and
  +72% latency.
- Provenance footer: source tier (semantic layer › curated reference › raw
  table), data freshness, model owner.
- Data quality checks on referenced fields (up to date, complete, no anomalies).
- Passive monitoring: share of queries resolved via the semantic layer; share of
  responses with correction language; weekly dashboard with offline pass rate.
- Active correction harvesting: a scheduled agent scans stakeholder channels
  every few hours for corrections, drafts a one-line reference-doc fix, opens a
  PR tagged to the domain owner; corrections also feed offline evals.
- Silent failures (plausible wrong answers) are not fully caught; mitigations:
  provenance footer, human sign-off on leadership-bound work, a daily per-domain
  top-KPI eval against the blessed dashboard.

## Getting started with self-service analytics
- Minimal start: a handful of canonical datasets, a few dozen offline evals, a
  thin knowledge skill.
- Questions to align on: correctness now vs later (models improve; infra for
  current shortfalls may become moot); expected business complexity; audience
  technicality; willingness to pay for accuracy (adversarial validation costs
  tokens and latency); access-control posture (one agent vs many scoped ones).

## Appendix: Skill File Skeleton (structure only)
- Frontmatter: `name`, `version`, and a `description` written as IF/THEN with a
  DO NOT clause for adjacent tasks.
- Role: act as a data analyst; out-of-scope decisions are surfaced as data and
  deferred to the owning team.
- Query execution priority: managed connection, then CLI fallback, else ask the
  user to authenticate and stop.
- Semantic layer is the mandatory first step (load, discover with segments
  always checked, compile and run, fallback to raw SQL via `references/*.md`
  only if not covered), with a pre-rebutted list of excuses for skipping it, and
  rules for date windows, timezone, and freshness lag (anchor on MAX(date)).
- Part 1 (must know): quick-start workflow (red flags, escalate out-of-scope,
  clarify, check dashboards, pick source, execute, deliver), entity
  disambiguation, terminology, data integrity rules (never invent data; safe
  division; separate observations from interpretations).
- Part 2 (how to): execution details; PII rule (return SQL, not results, for
  restricted data); analysis practices including mandatory adversarial SQL
  review sub-agent before the final answer (no self-certification) and a
  provenance footer (source, confidence, reviewed, freshness, owner).
- Part 3 (references): per-domain navigation to reference files and dashboard
  catalogs (a few dozen domains); troubleshooting; field-naming gotchas.
