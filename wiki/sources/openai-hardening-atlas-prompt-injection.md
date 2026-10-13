---
title: "OpenAI (Security): Continuously Hardening ChatGPT Atlas Against Prompt Injection"
type: source
created: 2026-10-12
updated: 2026-10-12
author: OpenAI
date: 2025-12-22
source_url: https://openai.com/index/hardening-atlas-against-prompt-injection/
source_path: raw/openai-hardening-atlas-prompt-injection.md
tags: [security, prompt-injection, red-teaming, reinforcement-learning, browser-agents, adversarial-training, primary-source]
---

# OpenAI (Security): Continuously Hardening ChatGPT Atlas Against Prompt Injection

> OpenAI trains an RL attacker that tests injections against a simulated victim
> agent, then uses the attacks it finds to adversarially train the Atlas
> browser agent and fix the wider defense stack.

## Summary

Agent mode in ChatGPT Atlas acts inside the user's browser, so the injection
surface is every email, invite, document, and page it reads, and the impact is
anything the user could do. OpenAI built an LLM attacker trained end to end
with reinforcement learning. While reasoning, the attacker sends candidate
injections to a simulator that runs the victim agent and returns its full
reasoning and action trace; it iterates before committing. Access to the
defender's private reasoning gives OpenAI an advantage over outside attackers.
Found attacks feed a "rapid response loop": adversarial training of new agent
checkpoints, plus fixes to monitoring, in-context safety instructions, and
system safeguards. OpenAI says prompt injection is unlikely ever to be fully
solved. The post names no model; the checkpoint is "the Atlas browser agent" as
of December 2025. See [[guardrails]], [[agent-evals]].

## Key points

- **Why RL for red teaming:** real harmful goals are long-horizon with sparse,
  delayed reward; an RL attacker built on a frontier model improves as base
  models improve; and it scales compute the way adaptive human attackers
  iterate.
- **Long-horizon findings:** the attacker drove agents through harmful
  workflows of tens to hundreds of steps, beyond prior work's single strings or
  single tool calls, and found strategies absent from human red teaming and
  external reports.
- **Demo:** an injected email makes the agent send a resignation letter to the
  user's CEO while drafting an out-of-office reply; after the update, agent mode
  detects the injection.
- **Loop outputs:** (1) new adversarially trained checkpoint, rolled out to all
  Atlas users; (2) non-model fixes (monitoring, safety instructions in context,
  system safeguards); (3) replay of tactics seen in the wild.
- **User advice:** use logged-out mode or limit sign-ins; review confirmation
  requests; give specific, scoped instructions instead of broad ones.

## Entities

[[openai]]

## Concepts

[[guardrails]], [[agent-evals]], [[agent-instructions]]

## Notable claims & data

- No success rates or before/after numbers are published.
- "Deterministic security guarantees" are called challenging for prompt
  injection, so the strategy is continuous pressure-testing.

## Connections

- **Agrees with** [[anthropic-eng-how-we-contain-claude]]: model defenses are
  never complete. Anthropic reports Gray Swan adaptive attacks reaching about
  5–6% after 100 attempts on Claude Opus 4.7; OpenAI's adaptive RL attacker is
  the same idea run internally.
- **Different emphasis from** [[anthropic-eng-how-we-contain-claude]]: this post
  centers model-layer hardening (training) and gives the environment layer one
  line; Anthropic puts most effort into containment. Not a contradiction: OpenAI
  still lists system-level safeguards as part of the loop.
- The user advice to scope instructions narrowly matches the "Explicit
  instructions" advice in [[openai-understanding-prompt-injections]].
- Automated attack generation as an eval method: compare the synthetic
  exfiltration dataset in [[anthropic-eng-claude-code-auto-mode]] and the
  third-party red-teaming in [[anthropic-auto-mode-default]].
- Wider framework: [[openai-designing-agents-resist-prompt-injection]].
