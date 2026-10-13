---
title: "Anthropic: How Balyasny Asset Management evaluates and governs Claude Fable 5"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Anthropic (claude.com articles); interviewee Charlie Flanagan (Balyasny)
date: 2026-09-17
source_url: https://claude.com/resources/articles/working-at-the-frontier-how-balyasny-asset-management-evaluates-and-governs-claude-fable-5
source_path: raw/anthropic-balyasny-evaluates-fable-5.md
tags: [case-study, agent-evals, model-selection, governance, least-privilege, financial-services]
---

# Anthropic: How Balyasny Asset Management evaluates and governs Claude Fable 5

> Interview case study: a hedge fund's eval suite of real tasks, its
> controls-around-the-model governance, and its in-house agent platform.

## Summary

Anthropic published this interview on claude.com on 2026-09-17. Results are
self-reported by Balyasny Asset Management (BAM) via Anthropic and are not
independently verified. The model findings apply to Claude Fable 5 as of
September 2026. BAM uses Anthropic models but builds its own execution harness,
data access, and review controls. Its agent platform, BAMAgent, runs thousands
of agents.

## Key points

- **Evals on real tasks with verifiable outcomes.** BAM tests thousands of
  financial tasks across equities, macro, and commodities, not general
  benchmarks. It tests each model alone and inside its own agent environment
  with production tools and files. See [[agent-evals]].
- **Failure modes graded on their own:** numerical errors, missed coverage,
  unsupported conclusions, retrieval problems.
- **Claimed result:** Fable 5 scored 89.4% vs 86.1% for the prior production
  model on the relevant subset.
- **Suspect a step change before accepting it.** When Fable solved economics
  problems no model had solved, BAM reran the eval and checked task and scoring
  logic independently. It also reviewed the result with Anthropic.
- **Controls around the model, not the model as the control.** Approved data
  boundaries, least privilege, tool-level permissions, logging, human review of
  material outputs, escalation paths. A stronger model gets no wider authority
  and cannot grant itself access. See [[guardrails]], [[agent-identity-and-access]].
- **Strongest model where errors propagate.** Fable runs planning and analysis
  stages, because mistakes there flow into every downstream deliverable. See
  [[multi-agent-economics]].
- **Model vs harness split:** the model reasons; BAM's harness supplies
  workflow, data and tool access, permissions, monitoring, and review. See
  [[agent-harness]].
- **Claimed workloads:** merger-arbitrage package from 3–5 days to under one
  day (~30-minute agent run); central-bank analysis from ~2 days to ~30 minutes;
  an agent that searched 90,000 tables; teams running 300+ agents.

## Connections

Sibling "Working at the frontier" interviews: [[anthropic-cursor-evaluates-models]],
[[anthropic-jetbrains-evaluates-fable-5]]. Model guidance:
[[anthropic-prompting-claude-fable-5]]. Entities: [[anthropic]], [[claude]],
[[claude-code]].
