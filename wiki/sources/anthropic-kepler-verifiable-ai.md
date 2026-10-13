---
title: "Anthropic: How Kepler built verifiable AI for financial services"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com articles)
date: 2026-04-30
source_url: https://claude.com/resources/articles/how-kepler-built-verifiable-ai-for-financial-services-with-claude
source_path: raw/anthropic-kepler-verifiable-ai.md
tags: [case-study, financial-services, deterministic-tools, provenance, evals, model-routing]
---

# Anthropic: How Kepler built verifiable AI for financial services

> Case study: a finance research platform where Claude interprets and plans,
> and deterministic infrastructure retrieves and computes every number, so each
> figure traces to a filing line item.

## Summary

Published by Anthropic on claude.com (2026-04-30, "How startups build with
Claude" series); all results are self-reported by Kepler. Kepler separates
interpretation from computation: Claude decomposes the analyst's question and
resolves ambiguity, while deterministic engines do retrieval and arithmetic and
attach provenance. The pipeline uses **Opus 4.7** for planning stages and
**Sonnet 4.6** for constrained high-throughput stages (models as of April 2026).
Kepler says other frontier models dropped constraints by step four or five on
long plans, while Claude held the plan and asked the analyst when a term was
ambiguous; this is a vendor-published customer claim on Kepler's own workloads.

## Key points

- **Split the jobs.** Model interprets and plans; query engine retrieves;
  formula engine computes. Numbers are never model-generated.
- **Context around the model.** Precise task definitions, a domain ontology,
  and explicit rules on what to resolve vs escalate to the analyst.
- **Idempotent skills** wrap recurring workflows and coordinate deterministic
  and nondeterministic stages.
- **Model per stage.** Frontier model for decomposition and plans; cheaper model
  for constrained stages.
- **Per-stage evals.** Thousands of cases against known-correct answers, testing
  the plan and the result separately; failures traced to reasoning, context, or
  execution. New models benchmarked within hours, stage by stage.
- **Provenance and access control by design:** per-user source permissions at
  every step, audit logging, click-through to the source line item.

## Notable claims & data

- Corpus: 26M+ SEC filings, 50M+ public and 1M+ private documents, 14,000+
  companies, 27 markets, indexed in under three months.
- Custom recall models: 94% on label-to-taxonomy mapping vs 38–46% for other
  models (Kepler's comparison, models unnamed).
- 147 firms interviewed before founding; trust in output was the common blocker.

## Connections

[[anthropic]], [[claude]]. Concepts: [[tool-design]], [[agent-evals]],
[[context-engineering]], [[agent-skills]], [[multi-agent-economics]],
[[boundary-contracts]]. Compare the stage-matched model routing in
[[anthropic-advisor-strategy]] and [[anthropic-choosing-claude-model]]; the
finance-domain evaluation in [[anthropic-balyasny-evaluates-fable-5]].
