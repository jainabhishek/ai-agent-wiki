# Index

The content catalog for this wiki. The LLM updates this on every ingest. Each
page is listed with a wikilink and a one-line summary. When answering a query,
read this first to find relevant pages, then drill in.

## Overview

- [[overview]] — building effective LLM agents; current thesis + map of the wiki

## Sources

- [[anthropic-building-effective-agents]] — Anthropic's field guide: workflows vs.
  agents, five patterns, ACI, start-simple (Dec 2024)
- [[openai-practical-guide-to-building-agents]] — OpenAI's 34-page guide:
  components, orchestration, guardrails (2025)

## Entities

- [[anthropic]] — AI lab; *Building Effective Agents*
- [[openai]] — AI lab; *A Practical Guide to Building Agents*
- [[openai-agents-sdk]] — OpenAI's code-first agent library (run loop, handoffs, guardrails)

## Concepts

- [[agents-vs-workflows]] — when to use a dynamic agent vs. a predefined workflow
- [[agent-design-principles]] — start simple, measure with evals, add complexity only when justified
- [[agent-core-components]] — Model, Tools, Instructions
- [[tool-design]] — ACI craft + tool types; clarity beats count
- [[workflow-patterns]] — Anthropic's five: chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer
- [[agent-orchestration]] — run loop; single-agent first; manager vs. decentralized
- [[agent-instructions]] — unambiguous, action-oriented instructions from real SOPs
- [[guardrails]] — layered safety: classifiers, PII, moderation, tool safeguards, human-in-the-loop

## Synthesis

- [[agent-building-best-practices-anthropic-vs-openai]] — where the two guides
  agree/differ + a distilled best-practices checklist
