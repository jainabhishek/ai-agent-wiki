---
title: "Anthropic: How Anthropic secures its AI-native software development lifecycle"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Jason Clinton (Deputy CISO, Anthropic)
date: 2026-07-21
source_url: https://claude.com/resources/articles/how-anthropic-secures-its-ai-native-software-development-lifecycle
source_path: raw/anthropic-securing-ai-native-sdlc.md
tags: [security, sdlc, code-review, multi-agent, egress-control, agent-identity, governance, claude-code]
---

# Anthropic: How Anthropic secures its AI-native software development lifecycle

> Stage-by-stage security controls (plan, code, CI, CD, monitor, governance) for an engineering organization where Claude writes most merged code, each stage with an "enduring principle".

## Summary

Jason Clinton (Deputy CISO, Anthropic) published this on claude.com on 2026-07-21. It applies [[anthropic-zero-trust-for-ai-agents]] to Anthropic's own SDLC. The figures are self-reported. Claude authors about 80% of merged code, and more than half of all code is merged by the internal version of Claude Tag. Engineers ship 8x as much code per quarter as in 2021–2025. The post defends against three named threats: a compromised or prompt-injected agent introducing a malicious change; supply-chain poisoning that the agent takes in as trusted input; and ordinary vulnerability classes arriving at higher volume.

## Key points

- **Plan: bring security agents to organizational context.** A Claude Opus project security review (PSR) checks design docs against MITRE ATT&CK and an internal knowledge index. Teams may self-approve projects that Claude rates low-risk. (see [[context-engineering]])
- **Code: close the loop into instructions.** Each discovered bug class goes back into CLAUDE.md or org-wide skills. Authors run `/security-review` before a PR, and a security-guidance plugin reviews the code while Claude writes it. Some customers gate `/security-review` with a PreToolUse hook; Anthropic puts its hard gate in CI instead. (see [[agent-steering]], [[agent-skills]])
- **Remote VMs to contain agents.** Developers code on remote VMs with egress-allowlisted agent traffic, so an injected instruction can reach only monitored services. (see [[guardrails]])
- **CI: many narrow reviewers instead of one mega-prompt.** Several agents, each scoped to one concern and using RAG over past incidents, review every PR. The stated reasons: they do not share blind spots, one can catch another's compromise or mistake, and effort is not spread thin. Agents must write a proof that each finding is valid. (see [[agent-orchestration]], [[workflow-patterns]])
- **Humans placed by risk tier.** Some codebases keep strict human approval. For code that Claude reviews and merges, every approval is logged with its reasoning, and humans review a risk-weighted sample. Invariant tests (for example, "user A never reads user B's data") trigger manual review.
- **CD: dynamic testing matches deployment cadence.** Anthropic is adding continuous AI-driven DAST in staging. It targets wrong assumptions between services.
- **Monitor: single-purpose identities.** The alert agent has three permissions (write new docs, post in channels, read production logs) and cannot deploy. Its access to other agents is part of its boundary. Agents coordinate over the same channels that humans use. (see [[anthropic-ciso-guide-agentic-ai]])
- **Governance: monitor loops, not bugs.** New AI reviewers start in shadow mode and are red-teamed. Humans sample automated approvals. Every agent action, approval, and agent-to-agent message goes to the SIEM, and agents are treated as a new kind of insider threat. (see [[agent-evals]])

## Notable claims & data

- The share of PRs with substantive review comments rose from 16% to 54% after agents were required to prove their findings. About a third of the bugs behind past claude.ai incidents would have been caught by the current automation.
- Cited from other companies: Intercom auto-approves 19% of PRs (deployments doubled, and downtime from breaking changes fell 35%). CircleCI's Chunk doubled the rate at which agent tasks become completed PRs.
- Claude-driven migrations now cover tens of thousands of lines in days. Scanning costs grow with code throughput; Anthropic expects unit cost to fall.

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[guardrails]], [[agent-orchestration]], [[workflow-patterns]], [[agent-steering]], [[agent-skills]], [[agent-evals]], [[context-engineering]]

## Connections

Risk framework: [[anthropic-ciso-guide-agentic-ai]]. Control catalog: [[anthropic-zero-trust-for-ai-agents]]. Verification method: [[anthropic-llms-secure-source-code]]. Engineering-side view of the same SDLC: [[anthropic-ai-native-sdlc-playbook]], [[anthropic-ai-ci-cd-on-call]], [[anthropic-running-ai-native-engineering-org]]. Hooks as gates: [[anthropic-configure-hooks]].
