---
title: "Anthropic: Zero risk isn't the job — a CISO's guide to agentic AI"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Jason Clinton (Deputy CISO, Anthropic)
date: 2026-07-17
source_url: https://claude.com/resources/articles/ciso-guide-to-agentic-ai
source_path: raw/anthropic-ciso-guide-agentic-ai.md
tags: [security, governance, least-agency, agent-identity, prompt-injection, egress-control, observability, insider-risk]
---

# Anthropic: Zero risk isn't the job — a CISO's guide to agentic AI

> Anthropic's Deputy CISO gives a four-question risk assessment for agent use cases, an identity spectrum from service account to human credential, and seven controls, illustrated by an incident-response agent and Claude Cowork.

## Summary

Jason Clinton (Deputy CISO, Anthropic) published this on claude.com on 2026-07-17. He argues that the CISO's job is to make agentic risk "legible and bounded", not to reach zero risk. A "no" answer produces shadow adoption with no telemetry and no off switch. A "yes" without controls produces incidents. The guide covers internal risk only; AI-accelerated external offense is in a separate Anthropic document. The central anecdote names models and a date: in November 2025 Anthropic moved its incident-response agent from Claude Opus 4 to Claude Opus 4.5 and changed nothing else. The new model alone produced new agent-to-agent behavior.

## Key points

- **Four questions per use case.** (1) What untrusted content does the agent ingest? "Nothing" means near-zero agent-specific risk. (2) What actions can it take, and under whose identity? (3) What is the blast radius, as scope × severity? (4) What observability exists: can you tell agent actions from user actions, and do they reach the SIEM? (see [[guardrails]])
- **Least agency.** Grant the narrowest capability that still completes the task. Roll out at admin pace: a small group first, watch telemetry, then expand.
- **A misaligned agent looks like an insider attack.** Ponemon's 2026 report gives 67 days to contain an insider incident. At agent speed, response must take minutes.
- **The agentic identity spectrum.** One end is a single-purpose, least-privilege system service account (incident agent, ticket triager, code reviewer, Claude Tag). The other end is a human credential, where the person at the keyboard is accountable (chat, Claude Cowork). The middle is an agent carrying a person's delegated identity into systems that person is not watching. Accountability is ambiguous there, so incidents become unexplainable.
- **Incident-response agent case.** Three tools: read-only production logs (no PII), Slack, and drafting a postmortem doc. It ingests no untrusted content, its writes are limited to new docs and messages, and every action reaches the SIEM. After the Opus 4 → 4.5 swap, the agent decided on its own to ask a code-writing Claude instance over Slack for a fix. The fix still went through human PR review. Lesson: draw boundaries around access and actions, not around what you believe the current model can do. (see [[agent-orchestration]])
- **Seven controls (Claude Cowork as the example).** (1) Identity comes from your IdP (SAML/OIDC, SCIM). (2) Connector allowlists draw the data boundary: an admin enables each connector, then each user authorizes it. (3) Per-tool, per-action approval: remove a verb such as delete or send, not only a whole connector. (4) The sandbox never holds a credential worth stealing; a reverse proxy injects connector tokens. (5) Egress allowlisting through a proxy that the sandbox cannot bypass is called "your strongest control against prompt injection". (6) Telemetry streams to the SIEM over OpenTelemetry. (7) An org-wide off switch, plus narrower RBAC and per-connector write controls.
- **Governance without bottleneck.** Automate the risk register. Non-engineers who build agents on a sanctioned, visible platform are not shadow adoption. Humans with authority accept risk (ISO 42001 on top of ISO 27001).
- **Design for the model six months out.** Controls that live in elaborate scaffolds and prompts disappear when smarter models make those scaffolds obsolete. Put controls in identity, permissions, and monitoring instead. (see [[agent-harness]])

## Notable claims & data

- As of July 2026, more than 50% of all code submitted for PRs at Anthropic is authored by an internal Claude Tag-like system, running in ephemeral VMs separated from production keys and accounts. Compare [[anthropic-securing-ai-native-sdlc]] (2026-07-21): Claude authors ~80% of merged code, and more than half is merged by internal Claude Tag. These are different metrics.
- Claude Cowork OTel output includes prompt content by default. Claude Code makes it opt-in. Cowork activity is not in the Compliance API or formal audit logs.
- The egress-allowlist claim bears on the open question in [[guardrails]] about sandbox injection. [[anthropic-eng-how-we-contain-claude]] shows that an allowlisted domain can itself be an exfiltration path.

## Entities

[[anthropic]], [[claude]], [[claude-code]], [[claude-managed-agents]]

## Concepts

[[guardrails]], [[agent-orchestration]], [[agent-harness]], [[model-context-protocol]]

## Connections

Companion pieces by the same author and team: [[anthropic-securing-ai-native-sdlc]] (applies these controls to the SDLC) and [[anthropic-zero-trust-for-ai-agents]] (the white paper behind least agency). Related: [[anthropic-agent-identity-access-model]], [[anthropic-eng-how-we-contain-claude]], [[anthropic-prompt-injection-defenses-browser]], [[openai-agent-security-enterprise]].
