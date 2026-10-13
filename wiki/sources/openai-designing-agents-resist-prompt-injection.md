---
title: "OpenAI (Security): Designing AI Agents to Resist Prompt Injection"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Thomas Shadwell, Adrian Spânu (OpenAI)
date: 2026-03-11
source_url: https://openai.com/index/designing-agents-to-resist-prompt-injection/
source_path: raw/openai-designing-agents-resist-prompt-injection.md
tags: [security, prompt-injection, social-engineering, guardrails, exfiltration, chatgpt, primary-source]
---

# OpenAI (Security): Designing AI Agents to Resist Prompt Injection

> OpenAI argues that effective prompt injections now look like social
> engineering, so input filtering cannot be the main defense; systems must cap
> the damage of a successful manipulation, using source-sink analysis.

## Summary

OpenAI's security team says real-world injections have moved from plain
override strings to social engineering as models became harder to fool. An
example 2025 attack email, posing as HR follow-up, got ChatGPT deep research to
leak an employee's name and address 50% of the time in testing. The post
argues that "AI firewalling" (an input classifier between agent and world)
usually misses such attacks, because detecting them is like detecting a lie
without context. Its alternative: treat the agent like a human customer-service
worker in a three-actor system, give it rules, expect it to be fooled
sometimes, and limit what a fooled agent can do. See [[guardrails]].

## Key points

- **Source-sink analysis.** An attack needs a source (untrusted content that
  influences the agent) and a sink (a capability that is dangerous in the wrong
  context: sending data out, following a link, calling a tool). Defend the
  sinks.
- **User expectation to preserve:** dangerous actions and transmissions of
  sensitive data never happen silently.
- **Safety training stops most attempts** to move secrets out of a conversation.
- **Safe Url** catches the rest at the sink: it detects when conversation data
  would go to a third party, then asks the user to confirm (showing the data) or
  blocks and tells the agent to try another way. Applied to Atlas navigations
  and bookmarks and Deep Research searches; Canvas and Apps run in a sandbox
  that flags unexpected communication.
- **Design heuristic:** give the agent the controls a human agent would have in
  the same role (caps, flags, approvals).
- OpenAI expects a maximally capable model to resist social engineering better
  than a human, but says relying on that is not always feasible or
  cost-effective.

## Entities

[[openai]]

## Concepts

[[guardrails]], [[agent-design-principles]], [[tool-design]]

## Notable claims & data

- 50% success for the reported 2025 injection against deep research (one user
  prompt; OpenAI test). No model named.
- Claim that intermediary injection classifiers usually miss fully developed
  attacks. This is in tension with the classifier taxonomy on [[guardrails]]
  (from [[openai-practical-guide-to-building-agents]]) and with OpenAI's own
  earlier description of AI-powered injection monitors
  ([[openai-understanding-prompt-injections]]). See Connections.

## Connections

- **Agrees with** [[anthropic-eng-how-we-contain-claude]]: model-layer defenses
  cannot be 100% effective, so the environment must cap the blast radius. OpenAI
  says "constrain the impact"; Anthropic says "contain first". Both frame risk
  as likelihood times damage, in different words.
- **Partly agrees with** [[anthropic-eng-claude-code-auto-mode]]: Anthropic's
  classifier also avoids judging injected content. It reads user messages and
  tool calls only, and judges the action (the sink). Anthropic does keep an
  input-side injection probe, but it only adds a warning. Anthropic's
  containment post adds that a phished user prompt exfiltrated credentials in
  24 of 25 tries and was invisible to intent-anchored classifiers; a sink check
  like Safe Url does not rely on intent.
- **Tension with** the "safety classifier detects prompt injections" row in
  [[guardrails]] (source: [[openai-practical-guide-to-building-agents]]). This
  post narrows it: input classifiers alone miss socially engineered attacks.
- Details of Safe Url: [[openai-agent-link-safety]]. Model-side hardening:
  [[openai-hardening-atlas-prompt-injection]]. Framework post:
  [[openai-understanding-prompt-injections]].
- Compare Anthropic's browser-agent view in
  [[anthropic-prompt-injection-defenses-browser]].
