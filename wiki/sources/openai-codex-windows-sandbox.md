---
title: "OpenAI (Eng): Building a Safe, Effective Sandbox to Enable Codex on Windows"
type: source
created: 2026-10-12
updated: 2026-10-12
author: David Wiesen (OpenAI)
date: 2026-05-13
source_url: https://openai.com/index/building-codex-windows-sandbox/
source_path: raw/openai-codex-windows-sandbox.md
tags: [security, sandboxing, containment, windows, codex, permissions, network-isolation]
---

# OpenAI (Eng): Building a Safe, Effective Sandbox to Enable Codex on Windows

> OpenAI Engineering and Security post (2026-05-13) on how Codex got an
> OS-enforced sandbox on Windows, which has no Seatbelt or bubblewrap
> equivalent. The result uses dedicated local users, write-restricted tokens,
> and firewall rules.

## Summary

Codex's default local policy is to read almost anywhere, write only in the
workspace, and have no network unless the user asks. Without a sandbox, Windows
users had to choose between approving nearly every command and Full Access mode.
OpenAI rejected three built-in Windows options. AppContainer is too narrow for
open-ended developer tooling. Windows Sandbox is a separate VM, not the user's
real checkout, and is missing on Home editions. Mandatory Integrity Control
relabeling would weaken the trust model of the checkout for the whole host.

The first "unelevated" prototype limited writes well. A synthetic `sandbox-write`
SID received ACLs on the cwd and the `writable_roots`. `.git`, `.codex`, and
`.agents` were denied for writes. Commands ran under a write-restricted token.
But network limits were only environment-variable poisoning (dead-end proxies,
a failing `GIT_SSH_COMMAND`, stub `ssh`), which any program can bypass.
Firewall rules cannot target a restricted token's extra SIDs. So the current
"elevated" design runs commands as a separate principal: local users
`CodexSandboxOffline` (firewall blocks all outbound) and `CodexSandboxOnline`.
An admin setup binary creates these users and stores their credentials with
DPAPI. A command-runner binary, already running as the sandbox user, mints the
restricted token and spawns the child.

## Key points

- **Write policy:** the workspace and configured `writable_roots` are writable.
  Metadata directories inside them (`.git`, `.codex`, `.agents`) stay read-only.
- **Advisory network controls are not controls.** Proxy environment variables
  and `PATH` stubs catch well-behaved tools but not code that opens sockets
  directly. OpenAI judged network suppression important enough to accept an
  elevation step at setup.
- **Enforcement keys on identity.** Windows Firewall matches principals, not
  restricted-SID lists or a single process tree. The sandbox therefore needs its
  own user account.
- **Separate binaries by privilege.** `codex.exe` stays unelevated.
  `codex-windows-sandbox-setup.exe` crosses UAC only for setup.
  `codex-command-runner.exe` spawns children on the sandbox-user side, because
  `CreateProcessAsUserW` failed from the real-user side.
- **Read parity is extra work.** A separate user cannot read the real user's
  profile by default. Read ACLs for common paths are granted asynchronously, on
  a best-effort basis.
- **Lesson:** no single Windows primitive maps to "safe autonomous coding
  agent". Agent security must balance compatibility with real developer
  workflows against real enforcement.

## Entities

[[openai]], [[openai-codex]]

## Concepts

[[guardrails]], [[agent-harness]], [[tool-design]]

## Notable claims & data

- The network policy is binary per principal (offline or online). The post
  describes no per-domain allowlist for the Windows sandbox.
- Tradeoffs the post names for any ACL-based design: setup time grows with the
  workspace topology, ACLs leave a real footprint on the host, and the
  semantics are expensive to change compared with regenerating a macOS `.sbpl`
  profile.

## Connections

- **Agrees with [[anthropic-eng-claude-code-sandboxing]]** that both
  boundaries (filesystem and network) are needed. Both sandboxes write to the
  workspace by default and enforce limits on the whole subprocess tree.
- **Differs in network design.** Anthropic routes all egress through a proxy
  outside the sandbox, with a per-domain allowlist and user confirmation.
  Codex on Windows uses a firewall-blocked offline user versus an online user,
  with no per-domain policy described. This is a design difference, not a
  contradiction.
- Supports the [[guardrails]] point from [[anthropic-eng-how-we-contain-claude]]
  that the environment layer must bound capability. OpenAI's discarded
  environment-variable proxy poisoning shows how soft controls fail. OpenAI
  still had to build custom glue (two binaries and dedicated users), because
  Windows lacks a standard primitive for this.
- The sandbox and approval policies that the harness exposes are listed in
  [[openai-codex-as-a-platform]]. For safe-operation guidance, see
  [[openai-running-codex-safely]].
