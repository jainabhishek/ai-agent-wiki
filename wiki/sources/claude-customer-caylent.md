---
title: "Anthropic customer story: Caylent (Claude Agent SDK migrations)"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com customer stories)
date: "accessed 2026-10-12"
source_url: https://claude.com/customers/caylent
source_path: raw/claude-customer-caylent.md
tags: [case-study, claude-agent-sdk, multi-agent, database-migration, model-routing, aws-bedrock]
---

# Anthropic customer story: Caylent (Claude Agent SDK migrations)

> Vendor-published case study of Caylent Accelerate, a staged multi-agent pipeline on the [[claude-agent-sdk]] that translates database stored procedures inside customer AWS accounts.

## Summary

Anthropic publishes this story on claude.com; the page has no date (accessed 2026-10-12). All results are self-reported by Caylent, an AWS consultancy, through Anthropic, and are not independently verified. The page names model families (Haiku, Sonnet) but no model versions. Caylent first built Accelerate on a homegrown harness, found it brittle, and rebuilt it on the [[claude-agent-sdk]], with agent behavior defined in markdown prompts rather than application code. Each workflow is a pipeline of specialized agents, each scoped to the tools it needs, with an orchestrator that routes work and picks a model per task. Deterministic scripts do precision work; engineers validate edge cases and final output.

## Key points

- **Staged, tool-scoped agents.** Inventory parser → dialect translator → guardrail validator → summary generator. Each agent gets only the tools its stage needs. (see [[agent-orchestration]], [[tool-design]])
- **Model routing by task.** Haiku for high-volume parsing; Sonnet for synthesis and executive output. (see [[multi-agent-economics]])
- **Validate before commit.** A guardrail agent checks each translation before it commits. (see [[guardrails]])
- **Deterministic code for precision, model for judgment.** The team splits work so scripts handle exact tasks and Claude handles reasoning and language. (see [[agents-vs-workflows]])
- **Inventory before translation.** In the Arborgold migration, 1,850 of 2,500 stored procedures were dead code; retiring them first cut the work from about 2,600 to about 220 hours.
- **Deployment constraint drove model choice.** Running inside customer AWS accounts via Amazon Bedrock excluded models not on Bedrock; CloudTrail logs every AI-assisted action.

## Notable claims & data

All self-reported: 90% fewer engineering hours (Arborgold); 82% cut, $202,000 saved on 257 Oracle objects (1,486 → 268 hours); 58–82% faster migrations across four more engagements; $600,000 annual licensing removed; 70% of cloud-ops remediation expedited and MTTR down 40%; 85%+ daily Claude use across 900+ staff. DevBench, an internal backlog harness, reportedly compresses hundreds of hours into 10–20.

## Entities

[[anthropic]], [[claude]], [[claude-agent-sdk]], [[claude-code]]

## Concepts

[[agent-orchestration]], [[agent-harness]], [[multi-agent-economics]], [[guardrails]], [[agents-vs-workflows]], [[tool-design]]

## Connections

Same "rebuild a brittle homegrown harness on the Agent SDK" move as [[claude-customer-greptile]]. Legacy-modernization context: [[anthropic-ai-code-modernization]], [[claude-customer-lg-cns]]. Pipeline-of-specialists pattern: [[anthropic-building-multi-agent-systems]], [[workflow-patterns]].
