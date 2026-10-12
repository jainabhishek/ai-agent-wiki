---
title: "Anthropic (Eng): Beyond Permission Prompts — Claude Code Sandboxing"
type: source
created: 2026-10-12
updated: 2026-10-12
author: David Dworken, Oliver Weller-Davies (Anthropic Engineering)
date: 2025-10-20
source_url: https://www.anthropic.com/engineering/claude-code-sandboxing
source_path: raw/anthropic-eng-claude-code-sandboxing.md
tags: [security, sandboxing, containment, prompt-injection, permissions, claude-code, primary-source]
---

# Anthropic (Eng): Beyond Permission Prompts — Claude Code Sandboxing

> Launch post (October 2025) for the Claude Code sandboxed bash tool and Claude
> Code on the web. Thesis: replace per-action approval with OS-enforced
> filesystem and network boundaries, which is both safer and more autonomous.

## Summary

Claude Code's default model is read-only with per-action approval. Anthropic
says constant approval causes approval fatigue, so users stop reading what they
approve. The post introduces sandboxing as the alternative: a pre-defined
boundary inside which Claude works without prompts. The boundary has two parts,
filesystem isolation and network isolation, and the post argues both are
required. Anthropic reports that, in internal usage, sandboxing cut permission
prompts by 84%. Two features ship on this base. The **sandboxed bash tool** uses
a new open-source sandbox runtime (bubblewrap on Linux, Seatbelt on macOS).
**Claude Code on the web** runs each session in a cloud sandbox and keeps git
credentials outside it behind a git proxy. See [[guardrails]] and
[[agent-harness]].

## Key points

- **Two boundaries, both required.** Without network isolation, a compromised
  agent can exfiltrate SSH keys. Without filesystem isolation, it can escape the
  sandbox and reach the network.
- **Filesystem rule:** read and write in the current working directory; block
  modification outside it.
- **Network rule:** all traffic goes through a unix domain socket to a proxy
  outside the sandbox. The proxy enforces a domain allowlist, asks the user
  about new domains, and can be customized with arbitrary egress rules.
- **Subprocess coverage:** OS enforcement covers every script, program, and
  subprocess a command spawns, not only Claude's direct calls.
- **Escalation, not denial:** an access outside the boundary notifies the user,
  who can allow it.
- **Generic runtime:** the runtime sandboxes arbitrary processes, agents, and
  MCP servers without a container. It is open source; Anthropic recommends other
  agent builders adopt it.
- **Credentials outside the sandbox (web):** the git client inside holds only a
  scoped credential. The git proxy validates it and the operation (for example,
  push only to the configured branch), then attaches the real GitHub token.
- Entry point: the `/sandbox` command.

## Entities

[[anthropic]], [[claude-code]]

## Concepts

[[guardrails]], [[agent-harness]], [[tool-design]], [[model-context-protocol]],
[[agent-design-principles]]

## Notable claims & data

- 84% fewer permission prompts in Anthropic internal usage (October 2025). The
  same figure appears in [[anthropic-eng-how-we-contain-claude]] (May 2026).
- Under the default permission model, safe commands such as `echo` and `cat`
  are auto-allowed.
- Claim: a successful prompt injection inside the sandbox "cannot impact overall
  user security". The later post [[anthropic-eng-how-we-contain-claude]] reports
  exfiltration through an allowlisted domain, which qualifies this claim (see
  Connections).

## Connections

- **Earlier primary source for Pattern 2 of
  [[anthropic-eng-how-we-contain-claude]].** That May 2026 post summarizes the
  OS-level sandbox in a few lines. This post adds the mechanism detail it omits:
  the unix-socket egress proxy outside the sandbox, the per-domain user
  confirmation, customizable egress rules, subprocess coverage, the argument
  that both boundaries are necessary, and the git-proxy design with a scoped
  in-sandbox credential for Claude Code on the web.
- **Qualified by the later post.** This post presents the domain allowlist as
  sufficient against exfiltration. [[anthropic-eng-how-we-contain-claude]]
  later reports exfiltration through an allowlisted domain (the
  `api.anthropic.com` Files API with an attacker key) and concludes that an
  allowlist is a capability grant, not only a destination filter.
- The git proxy is an early instance of "credentials never enter the sandbox",
  later generalized in [[anthropic-eng-scaling-managed-agents]],
  [[anthropic-evolution-of-agentic-surfaces]], and
  [[anthropic-claude-code-in-the-cloud]].
- Model-layer counterpart: [[anthropic-eng-claude-code-auto-mode]] reduces
  prompts with a classifier instead of an environment boundary.
- Complements hook-based denial in [[anthropic-steering-claude-code]] and the
  "Safe YOLO mode in a container without internet" advice in
  [[anthropic-eng-claude-code-best-practices]], which this runtime replaces
  with a lighter OS-level boundary.
