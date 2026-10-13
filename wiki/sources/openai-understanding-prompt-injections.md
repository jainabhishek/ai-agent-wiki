---
title: "OpenAI (Security): Understanding Prompt Injections"
type: source
created: 2026-10-12
updated: 2026-10-12
author: OpenAI
date: 2025-11-07
source_url: https://openai.com/index/prompt-injections/
source_path: raw/openai-understanding-prompt-injections.md
tags: [security, prompt-injection, guardrails, human-in-the-loop, red-teaming, chatgpt, primary-source]
---

# OpenAI (Security): Understanding Prompt Injections

> OpenAI's user-facing explainer: what prompt injection is, the seven layers
> OpenAI uses against it, and four steps users can take.

## Summary

OpenAI defines prompt injection as social engineering aimed at conversational
AI: a third party, neither user nor AI, plants instructions in content the AI
reads. Risk grows with data access, initiative, and task length. OpenAI lists a
multi-layer defense: safety training (including Instruction Hierarchy research
on trusted vs. untrusted instructions), AI-powered monitors that can be updated
faster than training, per-product security protections (link approval,
sandboxing for Canvas and Codex), user controls (logged-out mode,
confirmations, Watch Mode), red-teaming, a bug bounty, and informed consent
when connecting apps. In November 2025 OpenAI said it had not yet seen
significant attacker adoption. See [[guardrails]].

## Key points

- **Two worked threats:** an injected apartment listing biases a
  recommendation; an injected email makes an agent told to "respond to my
  overnight emails" find and share bank statements.
- **Monitors complement training** because they can be updated rapidly for new
  attacks, and they can catch attackers testing injections on OpenAI's own
  platform.
- **Sandboxing** for code-running tools (Canvas, Codex) limits harm from a
  successful injection.
- **User controls:** logged-out mode in Atlas; confirmation before sensitive
  steps such as purchases; **Watch Mode** on sensitive sites, where the agent
  pauses if the user leaves the tab.
- **Organization controls:** admins choose which features workspaces enable.
- **User steps:** give the agent only needed data and credentials; review
  confirmations; watch the agent on sensitive sites; prefer specific
  instructions over "take whatever action is needed".

## Entities

[[openai]], [[openai-codex]]

## Concepts

[[guardrails]], [[agent-instructions]], [[agent-design-principles]]

## Notable claims & data

- "Thousands of hours" of red-teaming focused on prompt injection.
- Bug bounty pays for realistic paths to unintended user-data exposure.

## Connections

- **Agrees with** [[guardrails]] (layered defense,
  [[openai-practical-guide-to-building-agents]]): classifiers, tool gating, and
  human confirmation together.
- **Tension with** [[openai-designing-agents-resist-prompt-injection]]
  (2026-03-11): that later post says input classifiers ("AI firewalling")
  usually miss socially engineered attacks. This post endorses AI monitors that
  "identify and block" injections. Possible reconciliation, not stated by
  OpenAI: monitors may watch behavior, not only inputs.
- **Tension with** Anthropic's approval-fatigue data: this post leans on users
  reviewing confirmations and watching the agent; Anthropic reports users
  approved about 93% of prompts and human catch rates fell to about 5% after
  50+ prompts ([[anthropic-eng-how-we-contain-claude]],
  [[anthropic-auto-mode-default]]).
- Follow-ups: [[openai-hardening-atlas-prompt-injection]],
  [[openai-agent-link-safety]].
