---
title: "Anthropic: How to Prepare for AI-Driven Code Modernization Projects"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Jonah Ezekiel, Lexie Tonelli (Anthropic forward deployed engineers)
date: 2026-09-23
source_url: https://claude.com/resources/articles/how-to-prepare-for-ai-driven-code-modernization-projects
source_path: raw/anthropic-ai-code-modernization.md
tags: [code-modernization, legacy-code, verification, governance, claude-code, enterprise]
---

# Anthropic: How to Prepare for AI-Driven Code Modernization Projects

> A six-step method from Anthropic's forward deployed engineers for running
> agent-driven modernizations of critical, regulated systems, built around a
> machine-checkable "certificate" and a pre-agreed "promotion policy".

## Summary

Part of Anthropic's "Notes from the Field" series (2026-09-23). The argument:
agents shrink multi-year modernizations to months or weeks, so the bottleneck
moves from producing changes to mobilizing the organization (change management,
review, approval) around them. Six steps: (1) **define the target** — pick
*uplift* (same-stack version bump), *transform* (cross-stack rewrite, behavior
fixed), or *reimagine* (new architecture, new behavior, needs a written
behavioral spec); (2) **create the certificate** — the set of conditions, each
checkable without a human, that every change must meet; (3) **set the promotion
policy** — a tiered human-review path agreed in advance; (4) **put prerequisites
in place** — environment, CI/CD, review capacity, security approvals; (5) **build
and refine the agentic workflow** — a custom [[claude-code]] workflow fanned out
to parallel subagent workstreams, starting from the code modernization plugin;
(6) **run** — prove end to end on a small partition, then scale.

## Key points

- **Settle the modernization type first**; otherwise the disagreement returns as
  arguments over whether each change is "correct".
- **Risk reduction, not cost, usually justifies the project** (authors'
  experience): weigh the risk of *not* modernizing.
- **Certificate = machine-checkable verification**: original and new tests,
  coverage threshold, benchmarks, adversarial Claude reviews each in a fresh
  context window, computer-use UI checks, differential output checks, round-trip
  of state and wire formats, staging soak, static/security scans, clean build.
  Transform relies on traffic replay and differential testing because old tests
  rarely run on the new stack; reimagine is hardest because the spec is less
  objective. Use Claude to build missing evidence (replay harness, prod-parallel).
- **Promotion policy**: tier by blast radius and agent confidence; fix recurring
  flags at the source (workflow or certificate), not per change; design the
  review output format with reviewers; front-load SME time on samples. The
  mandate should come from leadership so responsibility is shared.
- **Fix the workflow, not each change** when issues surface during refinement.
- **Least privilege**: write access only to modernization branches, no
  production credentials, secrets/PII masked, every PR linked to the agent
  transcript and certificate evidence.
- **In-place uplift**: partition from the leaves inward, freeze and modernize one
  partition at a time, gate CI/CD so commits cannot undo a finished partition.
- **Cost**: measure tokens in the pilot to get a cost floor; in regulated
  settings verification usually costs more than writing; put expensive checks
  behind cheaper gates; use a cheaper model (Sonnet) for certificate-checked
  mechanical work and stronger models for hard transformations and adversarial
  review; watch retry rates when escalating models.

## Entities

[[anthropic]], [[claude-code]], [[claude]]

## Concepts

[[agent-evals]], [[guardrails]], [[workflow-patterns]], [[agent-orchestration]],
[[multi-agent-economics]], [[boundary-contracts]]

## Notable claims & data

- Modernizations that were multi-year can finish in months or weeks (stated, not
  quantified per project).
- The code modernization plugin offers `assess`, `map`, and `extract-rules`
  commands that mine business rules with source citations.

## Connections

Builds on the stage model in [[anthropic-ai-native-sdlc-playbook]]; related to
[[anthropic-onboarding-claude-code-legacy-codebase]] and
[[anthropic-claude-code-large-codebases]]. The certificate idea parallels the
verifier-first harnesses in [[anthropic-eng-building-c-compiler]] and
[[anthropic-datadog-universal-machine-tool]]; the cheap-vs-strong model split
echoes [[multi-agent-economics]].
