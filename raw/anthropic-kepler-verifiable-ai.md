# How Kepler built verifiable AI for financial services with Claude — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/how-kepler-built-verifiable-ai-for-financial-services-with-claude
> Publisher: Anthropic (claude.com articles) · Date: 2026-04-30
> Captured: 2026-10-12 via curl (condensed).

Category: Best practices. Product: Claude Platform. No author byline. Part of the
"How startups build with Claude" series. Case study; all figures are
self-reported by Kepler.

## Intro and quick pitch

- Kepler: founded 2025 by Vinoo Ganesh (CEO) and John McRaven (CTO), both
  ex-Palantir. Stack: AWS, Rust, Python, containers for orchestration.
- Indexed 26M+ SEC filings, 50M+ public documents, 1M+ private documents, and
  14,000+ companies across 27 global markets in under three months.
- Problem: financial figures must be auditable against source documents.
  Traditional tools pull data but need analysts to verify; AI can interpret a
  freeform question but computes the numbers in the same step, so numbers are
  model-generated and can be wrong.
- Founders interviewed 147 financial firms (PE, hedge funds, investment banks);
  nearly all wanted AI for research but did not trust its output.
- Answer: deterministic infrastructure as a trust and verification layer, with
  Claude as the reasoning and interpretation layer. Product: Kepler Finance,
  plain-English questions with verifiable answers.

## Handling long, multi-step tasks and flagging ambiguity

- Example task: inventory days outstanding over eight quarters requires the right
  formula, correct fiscal periods, and awareness of restatements.
- Kepler benchmarked frontier models. On simple queries they were comparable. On
  long plans with interdependencies, all but Claude took shortcuts or lost
  constraints by step four or five (Kepler's claim, on its workloads).
- On ambiguous terms with two meanings, other models picked one and continued;
  Claude stopped and asked the analyst. Ganesh: one wrong early assumption breaks
  everything downstream.

## Engineering the context around Claude

- Claude did better with precisely defined tasks plus structured domain
  knowledge, definitions, and hard boundaries on what to resolve vs escalate.
  McRaven: the model is one pipeline stage, not the whole system; the team calls
  this "content engineering" (optimizing the system around a call) vs prompt
  engineering (optimizing the call).
- Deterministic execution environments that Claude invokes for any operation
  that must be provably correct (computing a ratio, resolving a fiscal period).
- Proprietary ontology mapping financial concepts to definitions and formulas,
  customizable per use.
- Security and access control enforced at every step (which sources each user
  may pull from).
- Reusable, customizable skills for common workflows: enterprise value across
  complex capital structures (preferreds, convertibles, minority interests);
  segment revenue waterfall reconciliation across reporting-period changes.
  Skills coordinate deterministic and nondeterministic stages and are idempotent
  (same input, same output).
- Multi-stage pipeline with model-per-stage: Opus 4.7 for intent decomposition,
  ambiguity resolution, and structured execution plans; Sonnet 4.6 for
  constrained, higher-throughput stages.
- Own specialized recall models (some Claude-based, some proprietary): 94%
  accuracy mapping financial-statement labels to standardized taxonomy codes vs
  38–46% for other models.
- Every prompt change, model upgrade, and context change is tested against
  thousands of cases before production. Automated eval pipelines compare output
  against known-correct answers at every stage, checking both the structured plan
  and the computed result. Failures are traced to reasoning, context, or
  downstream execution. New Anthropic models are benchmarked within hours, per
  stage (improves / regresses / needs prompt changes).

## Scaling with Claude

- Claude interprets questions against the corpus and reconciles terminology
  across companies and periods. The retrieval layer pulls figures from verified
  SEC filings, computes, and fills the desk's Excel template; one click traces
  each number to its line item highlighted in the source.
- The reasoning/infrastructure split lets a small team work at scale; modular
  architecture means one stage can improve without touching others (weeks vs
  months, self-reported).
- Compliance from the start: full audit logging, siloed customer environments,
  end-to-end provenance, SOC 2 Type II; ISO 27001 underway.
- Platform is domain-agnostic; finance chosen first as the hardest case. Pattern
  stated: Claude reasons about the question, infrastructure guarantees the answer.

## Best practices from the Kepler team

- **Give Claude the right job.** Retrieval belongs to a query engine, computation
  to a formula engine; Claude interprets, decomposes, reasons.
- **Match models to stages.** Opus for complex reasoning, Sonnet for constrained
  high-throughput work; one model everywhere wastes quality or cost.
- **Invest in evaluation before prompts.** Automated tests against known-correct
  answers per stage and end to end; silent regressions lose clients.
- **Build for provenance from day one.** Provenance must shape the whole system.
