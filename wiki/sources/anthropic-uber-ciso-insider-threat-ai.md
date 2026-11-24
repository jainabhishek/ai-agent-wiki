---
title: "Anthropic: Uber's CISO on building an insider threat program for AI"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Anthropic (claude.com articles); interview with Philip Martin (CISO, Uber)
date: 2026-10-13
source_url: https://claude.com/resources/articles/uber-s-ciso-on-building-an-insider-threat-program-for-ai
source_path: raw/anthropic-uber-ciso-insider-threat-ai.md
tags: [security, monitoring, insider-threat, observability, enterprise-frontier-safeguards, threat-modeling, case-study]
---

# Anthropic: Uber's CISO on building an insider threat program for AI

> An Anthropic interview with Uber's CISO. He argues that AI agents need an insider threat program like the one for employees, built from real-time telemetry and vendor classifier signals.

## Summary

Anthropic published this interview on claude.com on 2026-10-13. The interviewee is Philip Martin, Chief Information Security Officer at Uber. Uber handles more than 40 million trips and delivery orders a day. Martin's team used Claude for threat modeling before Claude Code existed. At first the team assembled the context by hand. Now Claude gathers context itself from code, design documents, and ticket history. Martin's thesis: companies already monitor employees, because people sometimes act outside their role. Frontier models carry the same risk, so they need an equivalent insider threat program. All claims are Martin's own and are not independently verified.

## Key points

- **Insider threat framing.** Companies accept data retention and monitoring for employees, even when it is unwelcome. Models may also be directed to act outside their expected limits. An insider threat program for models is therefore essential to safe rollout. (see [[guardrails]], [[agent-identity-and-access]])
- **Uber's AI security architecture has three parts.** (1) **AI Detection and Response (ADR)**, which Uber recently open-sourced. ADR collects real-time telemetry from Uber's agent harnesses and acts on it in real time. (2) Signals from Anthropic's classifier, delivered through Enterprise Frontier Safeguards. Martin expects these to become an ADR data source. (3) An **LLM gateway**, which forms a perimeter and controls how AI is used inside Uber. (see [[agent-harness]])
- **Two signal sources, one detection environment.** Uber merges its own telemetry with the vendor's classifier output, as in a traditional security operations setup. The goal is to reach a decision fast and with high certainty.
- **Customer control of safeguards.** Under Enterprise Frontier Safeguards, the safeguards run, but Anthropic cannot access Uber's data without permission. Uber controls the data and decides what action to take after a safeguard triggers.
- **Priority 1: real-time intervention.** Detect problems as close as possible to the moment a person types a prompt. Warn the person before the model calls an unwanted tool or connects to an unwanted destination. (see [[prompt-injection]])
- **Priority 2: find emerging behaviors.** Watch trends in model behavior, often with LLM help. Build safeguards for new behaviors back into the real-time platform. Constraints produce new behaviors, so this loop repeats.
- **Accidental misuse.** Martin says he focuses on accidental misuse, not only on attackers.
- **Agent teams for threat modeling.** Martin expects one agent per service. Each agent would know its service well and would exchange threat models with the agents of the services it talks to. This is a prediction, not a deployed system. (see [[agent-orchestration]], [[human-agent-teams]])

## Notable claims & data

- Uber's scale: more than 40 million trips and delivery orders a day.
- Uber names ADR as open source but gives no license or repository details in this post.
- Context: Enterprise Frontier Safeguards combines zero-data-retention privacy with misuse detection, and customers can hold the data in storage they control. [[anthropic-securing-coding-agents-enterprise]] describes it.

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[guardrails]], [[agent-identity-and-access]], [[prompt-injection]], [[agent-harness]], [[human-agent-teams]]

## Connections

Anthropic's SDLC post also treats agents as a new kind of insider whose actions go to the SIEM: [[anthropic-securing-ai-native-sdlc]], [[anthropic-ciso-guide-agentic-ai]]. Trace export that could feed such a program: [[anthropic-agent-observability-claude-platform]]. OpenAI counterparts on agent telemetry and monitoring: [[openai-running-codex-safely]], [[openai-securing-persistent-agents-openclaw]], [[openai-agent-security-enterprise]].
