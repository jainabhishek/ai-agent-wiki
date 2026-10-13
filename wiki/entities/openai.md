---
title: OpenAI
type: entity
subtype: org
created: 2026-06-21
updated: 2026-10-13
tags: [openai, agents]
---

# OpenAI

> AI research and deployment company; maker of the GPT models and the
> [[openai-agents-sdk]], and publisher of "A Practical Guide to Building Agents."

## Overview

In this wiki, OpenAI is the source of [[openai-practical-guide-to-building-agents]],
which defines agents as systems that independently accomplish tasks, and lays out
three design foundations (model, tools, instructions), orchestration patterns,
and a layered guardrails model.

## Key facts

- Defines an agent's three core components as **Model, Tools, Instructions**.
  (see [[agent-core-components]])
- Recommends **maximizing a single agent first**, moving to multi-agent only when
  needed. (see [[agent-orchestration]])
- Treats **guardrails** as a first-class, layered defense, with optimistic
  execution in the SDK. (see [[guardrails]])
- Offers three agent runtimes: the [[openai-agents-api]] (OpenAI runs the loop),
  the [[openai-agents-sdk]] (your app runs it), and the Responses API (you build
  it). (see [[openai-agents-api-guide]])
- Shut down the Assistants API on 2026-08-26 and pointed users to the Responses
  and Conversations APIs. (see [[openai-agents-api-guide]])
- Current model lineup as of 2026-10-12: GPT-6 Astra, GPT-6.1 Sol, and GPT-6
  Luna. Prompting guidance for the family is in the GPT-6 Astra guide. (see
  [[openai-prompting-gpt-6-astra]])
- Open-sources the [[openai-codex]] harness and positions it as an embeddable
  agent runtime. (see [[openai-codex-as-a-platform]])
- Most 2026 guidance on skills, `AGENTS.md`, and long-running agents is written
  against Codex. (see [[openai-shell-skills-compaction]],
  [[openai-testing-agent-skills-with-evals]],
  [[openai-skills-for-oss-maintenance]])
- Ships Secure MCP Tunnel so its products can reach private MCP servers. (see
  [[openai-private-mcp-servers]], [[model-context-protocol]])
- Explains the Responses API as an agentic loop that keeps encrypted reasoning
  state across turns, returns typed output items, and runs hosted tools
  server-side. (see [[openai-why-we-built-responses-api]]) Later Responses
  additions include a hosted computer environment and a WebSocket mode. (see
  [[openai-responses-api-computer-environment]],
  [[openai-websockets-agentic-workflows]])

### Guidance sources on openai.com

- **Engineering posts** (titled "OpenAI (Eng)" in the wiki) describe internal
  builds: the Codex agent loop, the App Server, harness engineering, Symphony,
  the Windows sandbox, the data agent, Sora Android, Tax AI, the Responses
  computer environment, and WebSocket mode. (see
  [[openai-unrolling-codex-agent-loop]], [[openai-codex-app-server-harness]],
  [[openai-harness-engineering]], [[openai-symphony-codex-orchestration]],
  [[openai-codex-windows-sandbox]], [[openai-in-house-data-agent]],
  [[openai-sora-android-with-codex]],
  [[openai-self-improving-tax-agents-codex]],
  [[openai-responses-api-computer-environment]],
  [[openai-websockets-agentic-workflows]])
- **Security posts** ("OpenAI (Security)") cover prompt injection and Codex
  deployment. (see [[openai-understanding-prompt-injections]],
  [[openai-hardening-atlas-prompt-injection]], [[openai-agent-link-safety]],
  [[openai-designing-agents-resist-prompt-injection]],
  [[openai-running-codex-safely]])
- **Model guide.** "A practical guide to building with GPT-6" (2026-10-02) is a
  buyer-oriented companion to the API docs page. It covers GPT-6 Astra,
  GPT-6.1 Sol, and GPT-6 Luna by display name only. It lists prices per million
  tokens (input / output / cached): Astra $10 / $50 / $1, 6.1 Sol $2 / $10 /
  $0.10, Luna $0.10 / $0.50 / $0.01. It recommends measuring cost per
  successful task before deployment. (see
  [[openai-practical-guide-building-with-gpt-6]],
  [[openai-prompting-gpt-6-astra]])
- **Agent security white paper.** "Agent security in the enterprise" (Aug 2026,
  listed Sep 2026) is OpenAI's CISO guide: task-scoped authority, reach and
  blast radius, agent identity with task tokens, capability governance, and
  incident response. It sits behind a lead form; the human supplied the PDF.
  (see [[openai-agent-security-enterprise]])

### Prompt-injection posture

- OpenAI frames prompt injection as social engineering by a third party and
  says it is unlikely ever to be fully solved. (see
  [[openai-understanding-prompt-injections]],
  [[openai-hardening-atlas-prompt-injection]], [[prompt-injection]])
- Its 2026 design rule is to limit what a fooled agent can do: analyze sources
  and sinks, and defend the sinks. "Safe Url" auto-fetches only URLs that an
  independent public web index has already seen. (see
  [[openai-designing-agents-resist-prompt-injection]],
  [[openai-agent-link-safety]])
- For ChatGPT Atlas, an RL-trained attacker tests a simulated victim agent;
  found attacks feed adversarial training and non-model fixes. (see
  [[openai-hardening-atlas-prompt-injection]])
- Codex at OpenAI runs in a sandbox with a managed network proxy, keyring
  credentials, and an Auto-review subagent. (see
  [[openai-running-codex-safely]], [[openai-codex]])

## Relationships

- Industry counterpart to [[anthropic]]; agent guidance largely agrees — see
  [[agent-building-best-practices-anthropic-vs-openai]].
- Ships the [[openai-agents-sdk]] referenced throughout its guide.
- Builds [[openai-codex]] and the [[openai-agents-api]].

## Appears in

- [[openai-agent-security-enterprise]]
- [[openai-practical-guide-to-building-agents]]
- [[openai-prompt-guidance-gpt-5-6]] (legacy)
- [[openai-prompting-gpt-6-astra]]
- [[openai-rethinking-skills-prompts-gpt-6-astra]]
- [[openai-agents-api-guide]]
- [[openai-codex-as-a-platform]]
- [[openai-automating-repetitive-work-codex]]
- [[openai-one-year-of-responses]]
- [[openai-shell-skills-compaction]]
- [[openai-testing-agent-skills-with-evals]]
- [[openai-skills-for-oss-maintenance]]
- [[openai-private-mcp-servers]]
- [[openai-practical-guide-building-with-gpt-6]]
- [[openai-why-we-built-responses-api]]
- Engineering posts: [[openai-unrolling-codex-agent-loop]],
  [[openai-codex-app-server-harness]], [[openai-harness-engineering]],
  [[openai-in-house-data-agent]], [[openai-responses-api-computer-environment]],
  [[openai-websockets-agentic-workflows]],
  [[openai-symphony-codex-orchestration]], [[openai-codex-windows-sandbox]],
  [[openai-self-improving-tax-agents-codex]], [[openai-sora-android-with-codex]]
- Security posts: [[openai-understanding-prompt-injections]],
  [[openai-hardening-atlas-prompt-injection]], [[openai-agent-link-safety]],
  [[openai-designing-agents-resist-prompt-injection]],
  [[openai-running-codex-safely]]
- Developers blog and Codex guides: [[openai-run-long-horizon-tasks-codex]],
  [[openai-codex-code-review-rules]], [[openai-skyscanner-codex-jetbrains-mcp]],
  [[openai-codex-maxxing-long-running-work]], [[openai-how-openai-uses-codex]]
- Anthropic pages that compare OpenAI products:
  [[anthropic-auto-mode-default]], [[anthropic-opus-5-5-long-coding-sessions]]

## Contradictions / open questions

- [[openai-prompt-guidance-gpt-5-6]] (Aug 2026) records OpenAI describing Sol,
  Terra, and Luna as durable capability tiers. The GPT-6 lineup (Sep 2026) has
  no Terra and adds Astra. (see [[openai-prompting-gpt-6-astra]])
- GPT-6 Sol was released on 2026-09-22 but is absent from the current model
  picker; the Astra guide mentions it only as a model to migrate from. (see
  [[openai-prompting-gpt-6-astra]])
- **Chat Completions and agentic features.** In 2025-09 OpenAI said Chat
  Completions "isn't going away" ([[openai-why-we-built-responses-api]]). The
  GPT-6 Astra docs page (2026-09) says tool calling requires the Responses API;
  GPT-6 Sol and Luna allow Chat Completions function calling only with
  `reasoning_effort: "none"` ([[openai-prompting-gpt-6-astra]]). Both can hold: the endpoint
  remains, but newer models gate agentic features to Responses.
- **Injection classifiers.** The 2025 practical guide lists safety classifiers
  that detect jailbreaks and injections
  ([[openai-practical-guide-to-building-agents]]). In 2025-11 OpenAI described
  AI monitors that "identify and block" injections
  ([[openai-understanding-prompt-injections]]). In 2026-03 OpenAI said "AI
  firewalling" usually misses socially engineered attacks
  ([[openai-designing-agents-resist-prompt-injection]]). OpenAI does not
  reconcile these. One possible reading is that monitors watch behavior, not
  only inputs.
