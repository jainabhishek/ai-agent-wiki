---
title: "Anthropic: Agent observability on the Claude Platform"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Anthropic (claude.com articles); no byline
date: 2026-10-14
source_url: https://claude.com/resources/articles/agent-observability-on-the-claude-platform
source_path: raw/anthropic-agent-observability-claude-platform.md
tags: [observability, opentelemetry, tracing, claude-managed-agents, evals, production-monitoring]
---

# Anthropic: Agent observability on the Claude Platform

> A short launch post. Claude Managed Agents, the Messages API, and the Anthropic SDKs now export OpenTelemetry traces (public beta) to any OTel tool.

## Summary

Anthropic announced the feature on claude.com on 2026-10-14, with no named author. Claude Managed Agents, the Messages API, and the Anthropic SDKs can now send OpenTelemetry (OTel) traces to any OTel-compatible tool. Claude Code and Cowork could already export traces. Platform-built agents can now appear in the same tool. The post frames tracing as the first step toward trust: trace the agent, review the traces, then widen its access as it proves reliable. The feature is in public beta. For Managed Agents and the Messages API, you set a destination in the Claude Console. The Anthropic SDKs export traces automatically.

## Key points

- **What a trace holds.** Each agent turn, model call, and tool use arrives as a standard OTel trace with latency, token counts, and IDs. MCP server calls are traced too. (see [[claude-managed-agents]])
- **Standard schema.** Traces follow the OpenTelemetry GenAI semantic conventions. Claude data and data from other providers therefore work in the same tools and dashboards. Any tool with a standard OTLP endpoint works.
- **Three named uses.** (1) Debug beside the rest of the stack, in Grafana Cloud, Honeycomb, Sentry, or Splunk. (2) Turn production traces into evals and measure whether a change helped, in Arize AI, Braintrust, Datadog, Langfuse, LangSmith, New Relic, or PostHog. (see [[agent-evals]]) (3) Track token usage per team and flag unusual activity, in Databricks Unity Gateway.
- **Traces as access evidence.** The post ties observability to autonomy: you widen an agent's access after its traces show it is reliable. (see [[guardrails]], [[human-agent-teams]])

## Notable claims & data

- Ramp (David Traina, self-reported): "Reflect", an agentic system, scores Langfuse traces, finds recurring failures, and proposes fixes. On some agents Ramp cut token usage by 10–20% and made sessions 30% faster.
- An unnamed company (Ankush Sharma, Head of Infrastructure) puts each model call in the same trace as the accounting workflow it ran inside. The trace includes prompt version, tool calls, latency, and token spend. The company uses this to answer auditors from one timeline.
- Foxglove and Sterling Labs report analysis in PostHog and Langfuse without custom instrumentation. They give no numbers.

## Entities

[[anthropic]], [[claude-managed-agents]], [[claude-code]]

## Concepts

[[agent-evals]], [[guardrails]], [[human-agent-teams]]

## Connections

The OpenAI counterpart for coding agents exports OTel logs to a triage agent: [[openai-running-codex-safely]]. Anthropic's security guidance asks for session telemetry and OpenTelemetry export: [[anthropic-securing-coding-agents-enterprise]], [[anthropic-securing-ai-native-sdlc]]. Managed Agents architecture: [[anthropic-eng-scaling-managed-agents]]. For monitoring as an insider-threat control, see [[anthropic-uber-ciso-insider-threat-ai]].
