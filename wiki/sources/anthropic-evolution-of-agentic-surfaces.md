---
title: "Anthropic: The Evolution of Agentic Surfaces (Claude Managed Agents)"
type: source
created: 2026-06-21
updated: 2026-06-21
author: Anthropic (Claude blog)
date: 2026-06-10
source_url: https://claude.com/blog/building-with-claude-managed-agents
source_path: raw/anthropic-evolution-of-agentic-surfaces.md
tags: [agents, harness, architecture, claude-managed-agents, sessions]
---

# Anthropic: The Evolution of Agentic Surfaces

> Traces agent infrastructure from hand-rolled loops (2023) to a tuned SDK (2025)
> to managed agents (2026), and extracts the architectural pattern that makes
> agents durable in production: **separate the brain from the hands.**

## Summary

Introduces [[claude-managed-agents]] and the **brain–hands separation**: the
harness that calls Claude runs separately from the sandbox where code executes,
connected by a **session** — an append-only log of every model call, tool call,
and result. See [[agent-harness]] and [[agent-orchestration]].

## Key points

- **Evolution**: 2023 "tokens in, tokens out" (DIY loops) → 2025
  [[claude-agent-sdk]] (tuned harness) → 2026 [[claude-managed-agents]]
  (reasoning decoupled from execution).
- **Brain–hands separation** yields lower latency (reasoning starts while the
  sandbox spins up: ~60% p50 / ~90% p95), security isolation (credentials in
  vaults, not sandboxes), and durable, resumable, observable sessions.
- **Harness–model co-evolution**: the "context anxiety" of Sonnet 4.5 (rushing
  near context limits) prompted harness context resets; Opus 4.5 removed the
  behavior, making those resets pure overhead. Lesson: delegate harness tuning to
  the platform. See [[agent-harness]].
- **Three production resources**: Agents (model/prompt/tools/guardrails),
  Environments (sandbox/networking/packages), Sessions (isolated, persistent,
  auditable).

## Concepts

[[agent-harness]], [[agent-orchestration]], [[context-engineering]],
[[guardrails]], [[agent-core-components]]

## Entities

[[anthropic]], [[claude-managed-agents]], [[claude-agent-sdk]]

## Notable claims & data

- Session = append-only event log connecting harness and sandbox; enables
  pause/resume and full audit — a concrete realization of the [[agent-orchestration]]
  "run loop / exit conditions" idea.
- Credentials via **Vaults** (envelope encryption, signed request tokens) — a
  production extension of [[guardrails]] tool-safeguard thinking.

## Connections

The infrastructure counterpart to the principles in
[[harnessing-claudes-intelligence]]; its "Agents = model/prompt/tools/guardrails"
matches OpenAI's [[agent-core-components]].
