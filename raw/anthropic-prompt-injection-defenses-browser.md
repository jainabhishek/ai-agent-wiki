# Mitigating the risk of prompt injections in browser use — Anthropic (raw capture)

> Source: https://www.anthropic.com/research/prompt-injection-defenses
> Publisher: Anthropic (Research) · Date: 2025-11-24 (page byline "Nov 24, 2025")
> Captured: 2026-10-12 via curl + HTML-to-text; chart values read from the embedded chart image (condensed).
> HTML title: "Mitigating prompt injections in browser use". Published alongside the Claude Opus 4.5 launch.

Note: paraphrased.

## (Intro)

- Anthropic says Claude Opus 4.5 sets a new standard in robustness to prompt injection (adversarial instructions hidden in content the model processes), improving both the model's core performance and the surrounding safeguards.
- Prompt injection is "far from a solved problem", especially as models take more real-world actions. Goal: agents that handle high-value tasks without significant injection risk.

## What is prompt injection?

- Useful agents must act for the user — browse, complete tasks, use the user's context and data — so every webpage visited is a potential attack vector.
- Content met while browsing cannot be fully trusted; an attacker can embed malicious instructions among legitimate results, documents, and apps to hijack the agent.
- Anthropic calls these one of the most significant security challenges for browser agents.
- These improvements informed moving the Claude for Chrome extension from research preview to beta, available to all Max-plan users.

## Why browser use creates unique prompt injection risks

- Example: user asks Claude to read recent emails and draft replies to meeting requests. A fake vendor email hides white-text instructions to forward emails containing "confidential" to an external address before drafting. Success = silent exfiltration.
- All agents processing untrusted content are exposed; browser use amplifies risk two ways:
  1. **Vast attack surface:** every page, embedded document, ad, and dynamically loaded script.
  2. **Wide action space:** navigating URLs, filling forms, clicking buttons, downloading files.

## Claude's progress on browser use robustness

- Comparison: the browser-extension configuration launching now vs. the original research-preview configuration, evaluated against an internal **adaptive "Best-of-N" attacker** that tries and combines many known-effective injection techniques.
- Method (chart caption): attack success rate (ASR), lower is better; the adaptive attacker gets **100 attempts per environment**; ASR is a percentage of attacks encountered by each model.
- Chart "Claude for Chrome Prompt Injection Robustness" (values read from image; N = attacks encountered):

| Model | Model only | Model + old safeguards | Model + improved safeguards |
|---|---|---|---|
| Sonnet 4 | 13.8% (N=2734) | 10.7% (N=2459) | 2.0% (N=2870) |
| Sonnet 4.5 | 13.8% (N=2878) | 10.8% (N=2634) | 1.9% (N=2373) |
| Haiku 4.5 | 12.0% (N=3157) | 11.1% (N=2948) | 2.4% (N=2248) |
| Opus 4.5 | 8.0% (N=3073) | 7.6% (N=3003) | 1.4% (N=2782) |

- Text: Opus 4.5 shows stronger browser-use injection robustness than previous models; new safeguards since the preview substantially improve safety across **all** Claude models.
- Text cites "a 1% attack success rate" as a significant improvement that still represents meaningful risk (the chart's best figure is 1.4%, Opus 4.5 with improved safeguards). No browser agent is immune; findings shared to show progress, not to claim the problem solved.

### Areas of work

1. **Training Claude to resist prompt injection:** reinforcement learning with injections embedded in simulated web content; Claude is rewarded for identifying and refusing malicious instructions, including ones made to look authoritative or urgent.
2. **Improving classifiers:** all untrusted content entering the context window is scanned; classifiers flag injections in many forms — hidden text, manipulated images, deceptive UI elements — and adjust Claude's behavior on detection. Both the classifiers paired with Claude for Chrome and the post-detection intervention that guides model behavior were improved since the preview.
3. **Scaled expert human red teaming:** human security researchers consistently beat automated systems at finding creative attack vectors; an internal red team continuously probes the browser agent; Anthropic also takes part in external Arena-style challenges that benchmark robustness across the industry.

## The path forward

- The web is adversarial; safe browser agents need ongoing vigilance. Prompt injection remains active research; Anthropic commits to keep investing as attacks evolve and to publish progress transparently so customers can make informed deployment decisions.
- Recruiting note: invites applicants to work on injection robustness.
