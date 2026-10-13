---
title: "Anthropic: Mitigating the risk of prompt injections in browser use"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (Research)
date: 2025-11-24
source_url: https://www.anthropic.com/research/prompt-injection-defenses
source_path: raw/anthropic-prompt-injection-defenses-browser.md
tags: [prompt-injection, security, browser-agents, guardrails, red-teaming, anthropic]
---

# Anthropic: Mitigating the risk of prompt injections in browser use

> Anthropic research post (Nov 24, 2025, with the Claude Opus 4.5 launch). It
> describes a three-layer defense against prompt injection for the Claude for
> Chrome browser agent, and reports attack success rates against an adaptive
> attacker.

## Summary

Anthropic frames prompt injection as one of the most significant security
challenges for browser agents. Browsing amplifies the general risk in two ways.
The attack surface is vast: every page, document, ad, and script. The action
space is wide: navigation, forms, clicks, and downloads. The worked example is a
hidden white-text instruction in an email. It tells the agent to forward
"confidential" mail to an outsider while the agent drafts replies.

**Model and date scope.** The measurements are from Nov 2025 on Claude Opus 4.5,
Sonnet 4.5, Haiku 4.5, and Sonnet 4. These are now legacy models. Read the
numbers as a historical datapoint. The defense architecture is the durable part.

**Defense architecture (three layers):**
1. **Model training.** Reinforcement learning on injections embedded in simulated
   web content. The model is rewarded for identifying and refusing them, even
   when they look authoritative or urgent.
2. **Classifiers on all untrusted input.** Every piece of untrusted content that
   enters the context is scanned for injections: hidden text, manipulated
   images, and deceptive UI. A separate post-detection *intervention* then steers
   the model's behavior.
3. **Human red teaming.** An internal team probes continuously, plus external
   Arena-style challenges. Anthropic says human researchers consistently beat
   automated systems at finding creative attacks.

See [[guardrails]].

## Key points

- **Evaluation method.** An internal adaptive "Best-of-N" attacker combines
  known-effective techniques. It gets 100 attempts per environment. Attack
  success rate (ASR) is measured over the attacks each model encountered. See
  [[agent-evals]].
- **Safeguards outweigh model generation in this chart.** For every model, the
  improved safeguards cut ASR by a large factor. Sonnet 4 drops from 13.8%
  (model only) to 2.0%. The newest model alone (Opus 4.5, 8.0%) stays far above
  any model with the improved safeguards (1.4%–2.4%).
- **Residual risk is explicit.** Anthropic says even about 1% ASR is
  "meaningful risk" and that no browser agent is immune. It shares the numbers
  to show progress, not to claim the problem is solved.
- These results moved Claude for Chrome from research preview to beta for all
  Max-plan users.

## Notable claims & data

ASR, lower is better (N = attacks encountered):

| Model | Model only | + old safeguards | + improved safeguards |
|---|---|---|---|
| Sonnet 4 | 13.8% (2734) | 10.7% (2459) | 2.0% (2870) |
| Sonnet 4.5 | 13.8% (2878) | 10.8% (2634) | 1.9% (2373) |
| Haiku 4.5 | 12.0% (3157) | 11.1% (2948) | 2.4% (2248) |
| Opus 4.5 | 8.0% (3073) | 7.6% (3003) | 1.4% (2782) |

- The prose cites "a 1% attack success rate". The chart's best figure is 1.4%
  (Opus 4.5 with improved safeguards). Both are recorded here.

## Entities

[[anthropic]], [[claude]]

## Concepts

[[guardrails]], [[agent-evals]], [[tool-design]]

## Connections

Fits the layered-defense view in [[guardrails]] next to the classifier designs in
[[anthropic-eng-claude-code-auto-mode]] and the containment approach in
[[anthropic-eng-how-we-contain-claude]]. OpenAI's parallel work on browser-agent
injection appears in [[openai-hardening-atlas-prompt-injection]],
[[openai-designing-agents-resist-prompt-injection]], and
[[openai-understanding-prompt-injections]].
