---
title: "OpenAI (Eng): Inside the Codex Sandbox"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Michael Bolin (OpenAI)
date: 2026-11-18
source_url: https://openai.com/index/inside-the-codex-sandbox/
source_path: raw/openai-inside-the-codex-sandbox.md
tags: [security, sandboxing, containment, codex, permissions, network-isolation, harness, mcp, primary-source]
---

# OpenAI (Eng): Inside the Codex Sandbox

> OpenAI's description of how Codex runs shell commands on the user's own
> machine under OS-enforced filesystem and network limits. It covers permission
> profiles, layered and managed configuration, the domain-filtering network
> proxy, and the macOS, Linux, and Windows implementations.

## Summary

OpenAI frames agent safety as defense in depth. Training and alignment shape
how the model uses its access. The harness sandbox limits what that access is.
Codex does not move work into a VM or a container. It constrains commands in
the user's existing environment with each operating system's own sandbox, so
native toolchains (for example the iOS build tools and simulator on a Mac) keep
working. One harness API, `spawn_command_under_sandbox`, takes a command, a
**permission profile**, and an optional network proxy on all three platforms.
Every child process inherits the limits. Users define named profiles in
`config.toml`. Enterprises constrain the allowed profiles with managed
requirements. The `codex sandbox` command exposes the same mechanism to other
tools, for example to lock down a stdio MCP server. See [[guardrails]] and
[[agent-harness]].

## Key points

- **Conservative default, `:workspace`.** Writes are allowed inside the
  workspace. `.git`, `.codex`, `.agents`, and `.aws` stay read-only. Reads are
  broad, because build tools need files outside the repo. Network is off. The
  post names the trade-off: secrets elsewhere on the disk stay readable.
- **Residual risk is named.** An agent could plant code in an ignored
  `node_modules` package that the editor later runs outside the sandbox. The
  sandbox does not remove the need for model alignment.
- **The model asks; the harness decides.** `exec_command` carries a
  `sandbox_permissions` field: `use_default`, `with_additional_permissions`, or
  `require_escalated` (with a `justification`). The harness grants or refuses,
  by asking the user or by routing to auto-review. See [[agent-steering]].
- **Profiles are tables so that config layers merge.** Tables merge
  recursively, and arrays replace wholesale. A team can override one path or
  one domain and inherit the rest. Admins set `allowed_permission_profiles` in
  `requirements.toml`. Cloud policy outranks the system file. See
  [[agent-identity-and-access]].
- **Network has three modes:** off, full, or through a proxy.
  `codex-network-proxy` filters by domain rules, and deny beats allow. It can
  pause an unmatched request for approval. It resolves DNS only after it
  approves the host, because a DNS lookup can leak data in the hostname.
- **Codex does not sandbox stdio MCP servers by default**, because it cannot
  infer what a server needs. The post shows how to wrap one in
  `codex sandbox --permission-profile ...` with no network. See
  [[model-context-protocol]].
- **Per-OS enforcement:**
  - macOS uses Seatbelt (`sandbox-exec`, SBPL with `(deny default)`), even
    though Apple marks it deprecated.
  - Linux uses bubblewrap plus seccomp-bpf, with `no_new_privs`. A host bridge
    relays loopback connections out of the isolated network namespace to the
    proxy.
  - Windows is moving to Microsoft's MXC library. The reason is that the
    earlier sandbox needed admin setup, slow ACL work, and persistent host
    state.
- **Deny globs are expanded to concrete paths at launch** on Linux and
  Windows. A file that matches the glob after launch is not covered.

## Entities

[[openai]], [[openai-codex]].

## Concepts

[[guardrails]], [[agent-harness]], [[agent-identity-and-access]],
[[model-context-protocol]], [[prompt-injection]], [[agent-steering]].

## Notable claims & data

- The default `exec_command` timeout is 10,000 ms.
- `:danger-full-access` is the built-in profile with full direct network access.
- The Windows section reports that the sandbox described in
  [[openai-codex-windows-sandbox]] (May 2026) is being replaced by an MXC-based
  sandbox. The earlier page stays accurate for its date. Current Windows
  behavior follows this post.
- Codex vendors its own `bwrap` but prefers a compatible system copy, because
  some Linux distributions allow user namespaces only for the system `bwrap`.

## Connections

- Same design choice as Anthropic's Claude Code sandbox: OS-level Seatbelt and
  bubblewrap, not containers, with network through a proxy
  ([[anthropic-eng-claude-code-sandboxing]]). Anthropic's containment post
  warns that "an allowlist is a capability grant"
  ([[anthropic-eng-how-we-contain-claude]]). The Codex post's DNS-exfiltration
  caveat for broad wildcards makes the same point.
- Extends [[openai-unrolling-codex-agent-loop]] (where the harness runs tool
  calls) and [[openai-running-codex-safely]] (approval modes, auto-review).
- The enterprise view is in [[openai-agent-security-enterprise]] and
  [[openai-securing-persistent-agents-openclaw]].
