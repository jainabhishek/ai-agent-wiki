---
title: "Anthropic: Zero Trust for AI Agents (eBook)"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com articles)
date: 2026-05-27
source_url: https://claude.com/resources/articles/zero-trust-for-ai-agents
source_path: raw/anthropic-zero-trust-for-ai-agents.md
tags: [security, zero-trust, least-agency, agent-identity, prompt-injection, memory-poisoning, supply-chain, observability, tool-security]
---

# Anthropic: Zero Trust for AI Agents (eBook)

> A 36-page Anthropic framework that applies Zero Trust to agent deployments: an agent threat taxonomy, three control tiers across ten capability areas, an eight-phase implementation workflow, and model-first security operations.

## Summary

Anthropic published this eBook through a claude.com landing page bylined 2026-05-27. The PDF itself is dated 2026-05-18 (from its metadata and filename). This page uses the byline date. No author is named. The eBook calls itself Anthropic's current thinking, not legal or compliance assurance. The premise: frontier models compress the time from vulnerability to exploit from months to hours. Agents are therefore exposed twice: their infrastructure faces faster attacks, and their own autonomy can misuse legitimate permissions. Zero Trust ("never trust, always verify; assume breach; least privilege") is the proposed foundation. The eBook introduces two terms: **least agency** (an OWASP term) and the **"impossible, not tedious"** design test. Claude Code features appear as "pro-tips"; the raw capture lists the exact setting names.

## Key points

- **"Impossible, not tedious" test.** Friction-based controls fail against agentic attackers, who have unlimited patience and near-zero cost per attempt. Examples of friction: rate limits, extra pivot hops, non-standard ports, SMS MFA. Prefer controls that remove a capability: hardware-bound credentials, expiring tokens, cryptographic identity, and network paths that do not exist. (see [[guardrails]])
- **Least agency.** Least privilege extends to what each agent tool can do, how often, and where. Examples: a read-only database tool, and an email summarizer with no send or delete rights. (see [[tool-design]])
- **Threat taxonomy.** Direct and indirect prompt injection. Tool poisoning and rug pulls through MCP metadata. Tool chaining, which uses only legitimate tools and is therefore invisible to host monitoring. Loop amplification. Unscoped privilege inheritance and the confused deputy between agents. Memory-based privilege retention. Model, tool, and dependency supply-chain attacks. RAG and shared-context poisoning, plus slow memory drift. (see [[model-context-protocol]], [[context-engineering]])
- **Tiers.** Foundation, Enterprise (the target for most organizations), and Advanced (regulated or national-security work). The tiers apply across identity, service authentication, permissions, privilege scoping, resource boundaries, logging, traceability, baselines, anomaly detection, response, input and output controls, configuration integrity, recovery, and governance. The eBook says AI offense has "raised" the Foundation floor. Foundation now requires short-lived IdP tokens, cryptographically rooted identity, identity-based isolation, and automated first-pass triage. Static API keys are not acceptable even at Foundation.
- **Identity over network.** Isolation should be enforced by the receiving service. Each service accepts only named, cryptographically identified callers, and network segmentation is only a backstop. When work is split across agents, each agent needs its own ID and its own credentials; shared credentials defeat the split. (see [[agent-orchestration]])
- **Inter-agent trust.** Before an agent accepts a delegated task, it verifies the delegating agent's identity and authorization. Each step is authorized again, and all inter-agent messages are logged.
- **Memory safeguards.** Isolate memory per session and per user. Validate memory integrity at every retrieval, not only at storage: hash each element, tag its source, and store the hashes apart from the content. Give unverified memory a TTL, and keep versioned stores for rollback. (see [[context-engineering]])
- **Operations.** Automate the bookkeeping, not the decisions: humans keep the containment, disclosure, and customer-communication calls. Put a model at the front of the alert queue. Start with one noisy rule and read-only access, and measure agreement with a human reviewer for two weeks before you expand. Measure dwell time and coverage first. (see [[agent-evals]])

## Notable claims & data

- Cited figures: Microsoft's Spotlighting reduced indirect-injection success from over 50% to under 2%. Anthropic's constitutional classifiers blocked 95% of jailbreak attempts in testing. 250 poisoned documents can backdoor LLMs of 600M to 13B parameters, and the backdoor persists through SFT and RLHF. About 100 malicious models were found on public platforms. The US requires federal agencies to adopt Zero Trust by 2027.
- Detection target: an anomaly reaches human awareness within one hour for critical systems.
- **Internal inconsistency:** the landing page lists the tiers as "Foundation, Advanced, and Optimized". The PDF uses Foundation, Enterprise, and Advanced throughout. This page follows the PDF.
- Rate limits are called "friction, not barriers". [[guardrails]] treats spend caps as guardrails. These claims are compatible: caps limit cost, but they do not stop a determined attacker.

## Entities

[[anthropic]], [[claude-code]]

## Concepts

[[guardrails]], [[tool-design]], [[model-context-protocol]], [[context-engineering]], [[agent-orchestration]], [[agent-evals]]

## Connections

Operational companions: [[anthropic-ciso-guide-agentic-ai]] (four-question assessment), [[anthropic-securing-ai-native-sdlc]] (applied to the SDLC). Related identity and injection work: [[anthropic-agent-identity-access-model]], [[anthropic-prompt-injection-defenses-browser]], [[anthropic-eng-how-we-contain-claude]], [[anthropic-eng-claude-code-sandboxing]]. OpenAI counterparts: [[openai-agent-security-enterprise]], [[openai-understanding-prompt-injections]], [[openai-designing-agents-resist-prompt-injection]].
