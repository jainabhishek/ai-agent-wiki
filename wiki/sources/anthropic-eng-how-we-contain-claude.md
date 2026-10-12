---
title: "Anthropic (Eng): How We Contain Claude Across Products"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Max McGuinness, Mikaela Grace, Jiri De Jonghe, Jake Eaton, Abel Ribbink (Anthropic Engineering)
date: 2026-05-25
source_url: https://www.anthropic.com/engineering/how-we-contain-claude
source_path: raw/anthropic-eng-how-we-contain-claude.md
tags: [security, containment, sandboxing, prompt-injection, guardrails, claude-code, primary-source]
---

# Anthropic (Eng): How We Contain Claude Across Products

> Anthropic's account of how it isolates Claude in claude.ai, Claude Code, and
> Claude Cowork, including five incidents it missed. Thesis: contain at the
> environment layer first, then steer at the model layer.

## Summary

Agent risk is likelihood of failure times damage. Training and safeguards lower
the likelihood; more capability and access raise the damage, so engineering
must cap the blast radius. The post separates **supervision** (per-action human
approval; users approved about 93% of Claude Code prompts, so approval fatigue
set in) from **containment** (sandboxes, VMs, egress controls), where most of
the effort went. It names three risk sources (user misuse, model misbehavior,
external attackers) and three defense components (environment, model, external
content). It then describes three isolation patterns matched to how much the
user can oversee: an ephemeral gVisor container (claude.ai), an OS-level
human-in-the-loop sandbox (Claude Code), and a sealed local VM (Claude Cowork).
See [[guardrails]] and [[agent-harness]].

## Key points

- **Environment vs. model layer.** Environment controls set what the agent
  *can* do; prompts, classifiers, probes, and training set what it *tends* to
  do. Model defenses cannot be 100% effective, so they cannot stand alone. Where
  environment controls are absent, the model layer compensates (auto mode).
- **Pattern 1, ephemeral container:** gVisor + seccomp held; the custom proxy
  around them caused the most consequential incident.
- **Pattern 2, HITL sandbox:** Seatbelt (macOS) / bubblewrap (Linux) allow
  reads and in-workspace writes and deny network by default; this cut
  permission prompts by 84%. The runtime is open source.
- **Pattern 3, sealed VM:** platform hypervisor (Apple Virtualization / HCS);
  only workspace and `.claude` mounted; credentials in host keychain. Later the
  agent loop and local MCP servers moved to the host; code execution stayed in
  the VM. Mount modes: read-only, read-write, read-write-no-delete.
- **Missed risks:** (1) project config (`.claude/settings.json` hooks) ran
  before the trust dialog; (2) a phished user prompt exfiltrated
  `~/.aws/credentials` in 24 of 25 tries, invisible to intent-anchored
  classifiers; (3) exfiltration via an allowlisted domain (`api.anthropic.com`
  Files API with an attacker key); (4) VM isolation also blinded host EDR.
- **"An allowlist is a capability grant, not just a destination filter."** The
  fix is an in-VM proxy that accepts only the VM's session token.
- **Trusting what the agent reads:** remote tools can change after approval;
  tool output from trusted tools is still an attack surface and needs live
  inspection, which a small fast classifier can do.

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[guardrails]], [[agent-harness]], [[tool-design]], [[agent-orchestration]],
[[agent-design-principles]]

## Notable claims & data

- Gray Swan Agent Red Teaming: Claude Opus 4.7 about 0.1% attack success on one
  attempt, about 5–6% after 100 adaptive attempts.
- Auto mode catches about 83% of overeager actions; footnote: blocks about 0.4%
  of benign commands, misses about 17% — consistent with
  [[anthropic-eng-claude-code-auto-mode]].
- Experienced users auto-approve about 2x as often as new users but interrupt
  more mid-execution.
- Claude Mythos Preview was judged too risky to ship in April 2026.
- Every deployment: standard primitives (hypervisors, syscall filters, container
  runtimes) held; custom glue failed.
- Open problems: persistent memory poisoning via cross-session state (memory,
  CLAUDE.md, scheduled-agent state); subagent output trusted more than raw tool
  output as a new injection path; agent identity (own principal vs. inherited
  user permissions).

## Connections

- Gives the environment-layer half of the defense that
  [[anthropic-eng-claude-code-auto-mode]] supplies at the model layer; the two
  posts share the 93% approval and 17% miss figures.
- Extends the credential-isolation idea in
  [[anthropic-eng-scaling-managed-agents]] and
  [[anthropic-evolution-of-agentic-surfaces]] (credentials never enter the
  sandbox) to local products.
- Adds a deterministic-containment layer to the layered-guardrail model in
  [[openai-practical-guide-to-building-agents]]; complements hook-based denial
  in [[anthropic-steering-claude-code]].
- "Multi-agent trust escalation" is a security caveat for the subagent patterns
  in [[anthropic-eng-multi-agent-research-system]].
