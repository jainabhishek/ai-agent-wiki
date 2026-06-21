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
- [[anthropic-steering-claude-code]] — seven mechanisms to steer an agent: CLAUDE.md, rules, skills, subagents, hooks, styles (Jun 2026)
- [[anthropic-lessons-building-claude-code-skills]] — skills best practices: gotchas, progressive disclosure, model-facing descriptions (Jun 2026)
- [[harnessing-claudes-intelligence]] — three patterns: use what Claude knows, stop doing, set boundaries (Apr 2026)
- [[anthropic-evolution-of-agentic-surfaces]] — brain–hands separation, sessions, harness–model co-evolution (Jun 2026)

## Entities

- [[anthropic]] — AI lab; *Building Effective Agents* + operational blog posts
- [[openai]] — AI lab; *A Practical Guide to Building Agents*
- [[openai-agents-sdk]] — OpenAI's code-first agent library (run loop, handoffs, guardrails)
- [[claude]] — Anthropic's LLM family (the agent's reasoning engine)
- [[claude-code]] — Anthropic's agentic coding tool (steering + skills example)
- [[claude-agent-sdk]] — Anthropic's tuned agent harness (2025)
- [[claude-managed-agents]] — Anthropic's managed agent platform (2026)

## Concepts

- [[agents-vs-workflows]] — when to use a dynamic agent vs. a predefined workflow
- [[agent-design-principles]] — start simple, eval, prune scaffolding, design for cache hits
- [[agent-core-components]] — Model, Tools, Instructions
- [[tool-design]] — ACI craft + tool types; clarity beats count; use general-purpose tools
- [[workflow-patterns]] — Anthropic's five: chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer
- [[agent-orchestration]] — run loop; single-agent first; manager vs. decentralized; subagents
- [[agent-instructions]] — unambiguous, action-oriented instructions from real SOPs
- [[guardrails]] — layered safety: classifiers, PII, moderation, tool safeguards, hooks, human-in-the-loop
- [[agent-skills]] — on-demand procedural know-how; gotchas, progressive disclosure
- [[agent-steering]] — choosing the right instruction mechanism (CLAUDE.md/rules/skills/hooks/...)
- [[context-engineering]] — load on demand, let the agent manage/persist context, design for cache hits
- [[agent-harness]] — brain–hands separation, sessions, harness–model co-evolution

## Synthesis

- [[agent-building-best-practices-anthropic-vs-openai]] — where the two guides
  agree/differ + a distilled best-practices checklist
