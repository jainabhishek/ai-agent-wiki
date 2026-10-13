---
title: "Claude customer story: LG CNS modernizes 20-year-old enterprise systems"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com customer stories); spokesperson Hyosup Bae, LG CNS
date: "accessed 2026-10-12"
source_url: https://claude.com/customers/lg-cns
source_path: raw/claude-customer-lg-cns.md
tags: [case-study, claude-code, legacy-modernization, code-migration, agent-harness, context-engineering, amazon-bedrock]
---

# Claude customer story: LG CNS modernizes 20-year-old enterprise systems

> Vendor-published case study of an IT services firm that built a "software
> factory" around Claude Code to migrate legacy enterprise systems.

## Summary

Anthropic published this customer story on claude.com. The page shows no
publication date; the wiki records it as accessed 2026-10-12. All results are
self-reported by LG CNS through Anthropic and are not independently verified.
The core work uses Claude Opus 4.6, accessed through Amazon Bedrock.

LG CNS (the IT services arm of LG Group) built a harness around [[claude-code]]
for its 200-engineer Build Center. The harness decomposes migration work into
small YAML-defined tasks and chains context between stages through files. On one
construction-company project management system, LG CNS reports 2,888 of 2,913
APIs converted (99.1%) and 1,340 screens moved to React. The project ran
November 2025 to June 2026 at about 50% of the cost of a conventional rebuild.

## Key points

- **Model choice by task completion, not public benchmarks.** LG CNS tested
  planning, to-do sequencing, tool calls, and recovery after errors.
- **Plan first, then decompose.** A 5–7 person pod gives Claude the objective
  and intent, asks for an approach, then splits work into small YAML tasks.
- **File-mediated context chaining.** Each stage writes files that the next
  stage reads. This began as a workaround for context degradation before
  1M-token windows. LG CNS still prefers it: context taxonomy and output
  consistency matter more than raw context length at this scale.
- **Thin, multi-layered harness.** "Trust the model": a thick harness that
  guards every failure constrains the model and costs tokens. Lightweight
  layers handle validation, context scoping, and quality checks.
- **Senior engineers set direction.** They define task boundaries, sequence,
  and chaining strategy.
- **Planned next steps:** deterministic validation, golden-dataset quality
  measurement, a self-improving harness.

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[agent-harness]], [[context-engineering]], [[workflow-patterns]],
[[agent-orchestration]], [[agent-evals]]

## Notable claims & data

- 99.1% API conversion (2,888/2,913); 1,340 screens; 7 months; about 50% cost;
  go-live June 2026 (all self-reported).
- The story asserts the file-handoff patterns "anticipated" later native
  features; this is the vendor's framing.

## Connections

Same migration domain as [[claude-customer-caylent]] and
[[anthropic-ai-code-modernization]]. The thin-harness stance matches the
co-evolution rule in [[agent-harness]] and [[harnessing-claudes-intelligence]].
File-based state between stages parallels
[[anthropic-eng-effective-harnesses-long-running-agents]].
