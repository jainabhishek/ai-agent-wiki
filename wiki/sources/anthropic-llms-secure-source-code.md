---
title: "Anthropic: Using LLMs to secure source code"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Eugene Yan and Henna Dattani (Anthropic), with contributors
date: 2026-05-27
source_url: https://claude.com/resources/articles/using-llms-to-secure-source-code
source_path: raw/anthropic-llms-secure-source-code.md
tags: [security, vulnerability-discovery, verification, triage, sandboxing, multi-agent, threat-model, prompting]
---

# Anthropic: Using LLMs to secure source code

> A six-step find-and-fix loop for model-driven vulnerability work: threat model, sandbox, discovery, verification, triage, and patching. Its main design lesson: keep discovery (recall) and verification (precision) in separate, independent agents.

## Summary

Anthropic published this best-practice guide on claude.com on 2026-05-27. The authors are Eugene Yan and Henna Dattani, with contributors. The guide is written for "Claude Opus" (no version given) and draws on Anthropic's own scanning and on partner security teams. Readers should judge the prompting advice against current models. The main claim: discovery is now easy to parallelize, and the bottleneck has moved to verification, triage, and patching. As of 2026-05-22, Anthropic had disclosed 1,596 open-source vulnerabilities, and to its knowledge 97 were patched. A companion repo, `defending-code-reference-harness`, has one skill per step (`threat-model`, `vuln-scan`, `triage`, `patch`) and an autonomous demo harness.

## Key points

- **Loop structure.** You build the threat model and the sandbox once per codebase. Discovery, verification, triage, and patching then repeat. Model stochasticity gives a long tail of findings, so run the loop several times first, then on a schedule or after code changes.
- **The threat model drives precision.** Most false positives come from wrong trust-boundary assumptions, not misread code. First bootstrap the threat model from docs, git history, and past CVEs. Then have the model interview a system owner with Shostack's four questions. Keep a `THREAT_MODEL.md` in the repo. Discovery uses it as scope and triage uses it as a filter. (see [[context-engineering]])
- **The sandbox protects your systems and proves exploits.** Agents broke soft constraints, for example by fetching from GitHub when told they had no network. So enforce limits in configuration: give network access only during setup, then snapshot, and allow egress only to the model API through a proxy. Never expose credentials. Pin images, SHAs, and dependencies to match production. (see [[guardrails]])
- **Shorter prompts for discovery.** Prescriptive checklists reduced novel findings. Give the goal and context, leave the method to the model, define ordered output fields, and include an escape hatch for weak findings. Let the model ask for or build its own tools. (see [[agent-instructions]], [[tool-design]])
- **Partition, then fan out.** A first pass partitions the search space, parallel agents search each partition, and a final system-level pass uses their findings. Adding more agents without partitions gave mostly duplicates. (see [[agent-orchestration]])
- **An independent, adversarial verifier.** When discovery agents also verified, they self-censored true positives. Run the verifier in a fresh container with no shared filesystem or conversation history. Give it only the finding (or PoC) and the codebase, and prompt it to assume the finding is a false positive. Optional: several verifiers voting, plus a judge. (see [[workflow-patterns]])
- **Triage rubric.** Deduplicate by root cause: first a deterministic pass (same file, same category, within 10 lines), then model rules. To score severity, the model first answers six questions: reachability, attacker control, preconditions, authentication, read vs write, and blast radius. This stops it from anchoring on the bug class.
- **A validation ladder for patches.** Write a failing test first. Then check, in order: build, the original PoC stops working, no regressions, and a fresh agent re-attacks the patch. Ask for the minimal root-cause change. A human owns each patch. (see [[agent-evals]])

## Notable claims & data

Partner-reported: findings were exploitable about 90% of the time on systems with well-documented threat models. A project without a fitting threat model had a 40% false-positive rate. Tools to probe the running application brought true positives near 100%. An adversarial verifier roughly halved non-exploitable findings, and requiring a PoC as well brought false positives near zero. Severity thresholds: zero preconditions plus unauthenticated remote access is critical or high; one or two preconditions, or an authenticated path, is medium; three or more, or local-only, is low.

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[agent-orchestration]], [[workflow-patterns]], [[guardrails]], [[agent-instructions]], [[tool-design]], [[agent-evals]], [[context-engineering]]

## Connections

Applied at scale: [[anthropic-comcast-booz-allen-exploit-chains]] (validation as the bottleneck). Same separation of verifier from builder: [[anthropic-harness-for-every-task]], [[anthropic-eng-harness-design-long-running-apps]]. The SDLC version of agentic review: [[anthropic-securing-ai-native-sdlc]].
