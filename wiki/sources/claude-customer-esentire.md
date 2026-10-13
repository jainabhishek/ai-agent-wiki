---
title: "Anthropic customer story: eSentire (autonomous threat investigations)"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com customer stories)
date: "accessed 2026-10-12"
source_url: https://claude.com/customers/esentire
source_path: raw/claude-customer-esentire.md
tags: [case-study, cybersecurity, multi-agent, production-evals, human-in-the-loop, claude-agent-sdk]
---

# Anthropic customer story: eSentire (autonomous threat investigations)

> Vendor-published case study of eSentire's Atlas platform, which runs multi-agent security investigations on the Agent SDK and grades them against senior analysts in production.

## Summary

Anthropic publishes this story on claude.com; the page has no date (accessed 2026-10-12). All results are self-reported by eSentire, a managed detection and response (MDR) provider, through Anthropic. The page says Atlas runs Claude Opus 4.6 on Amazon Bedrock through the [[claude-agent-sdk]], so the performance figures describe that model. eSentire argues that saturated security benchmarks test known problems with verifiable answers, while production gives the agent a detection event and telemetry but no answer. It therefore measures quality by continuous production evaluation against human experts.

## Key points

- **Production evaluation against experts.** Senior SOC experts independently review a sample of agent-investigated cases; alignment is scored on compromise yes/no, severity, and recommended response. Over 500+ adjudicated outcomes, alignment on final verdict is above 90%; under the same method the agent beats junior analysts. (see [[agent-evals]])
- **Benchmarks vs. open-ended production.** Saturated benchmarks with defined answers did not predict the open-ended task; the team evaluated models on real-world scenarios. (see [[agent-evals]])
- **Multi-agent mirror of an analyst workflow.** Several sub-agents collaborate per case; investigations average 44 tool calls across threat intel, SIEM, endpoint, identity, and network data. (see [[agent-orchestration]])
- **Humans own consequential decisions.** Senior analysts review and act on every critical finding; humans keep containment and remediation decisions. (see [[guardrails]])
- **Breadth of workflows.** 3,600+ distinct investigation workflows across EDR, SIEM, and identity platforms.

## Notable claims & data

Self-reported, 12 months: 120,000+ investigations; 5M+ tool calls (≈468,000 expert-hours, ≈5 analyst-minutes per call); 6-minute average investigation; 41% more confirmed attacks per customer with 11% fewer alerts; 99.96% ransomware containment before encryption (industry: 44%); lateral movement in <0.5% of incidents across ~2M endpoints. Escalated-incident mix (~10,000 across 1,400+ customers): 31% blocked pre-execution, 18% failed attempts, 36% identity compromises, 14% device compromises.

## Entities

[[anthropic]], [[claude]], [[claude-agent-sdk]]

## Concepts

[[agent-evals]], [[agent-orchestration]], [[guardrails]]

## Connections

Other security-agent stories: [[anthropic-cybersecurity-triage-agents]], [[anthropic-outtake-cyber-investigator]], [[anthropic-comcast-booz-allen-exploit-chains]]. Evaluation method: [[anthropic-eng-demystifying-evals]].
