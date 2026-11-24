---
title: "OpenAI (Developer blog): Securing Persistent Agents like OpenClaw at OpenAI"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Kevin S Lin (OpenAI)
date: 2026-11-12
source_url: https://developers.openai.com/blog/securing-persistent-agents-like-openclaw-at-openai
source_path: raw/openai-securing-persistent-agents-openclaw.md
tags: [security, persistent-agents, openclaw, codex, sandboxing, network-policy, agent-identity, auto-review, observability, guardrails, primary-source]
---

# OpenAI (Developer blog): Securing Persistent Agents like OpenClaw at OpenAI

> How OpenAI secures its internal fleet of persistent OpenClaw agents: a
> trusted gateway split from an untrusted agent harness, the Codex sandbox with a
> locked-down config, auto-review on every action, a separate identity per
> agent, and full logging.

## Summary

A **persistent agent** runs 24/7 with a broad scope and acts without user input,
unlike a Codex session with a fixed goal and human steering. The post argues that
such agents break two assumptions of traditional software security: that
configuration and code are deterministic, and that threats come from outside. A
persistent agent can rewrite its own config and write arbitrary code, so the
threat can come "from the inside" as misaligned actions. OpenAI reports
"hundreds of OpenClaw agents" internally, and later "over 500 agents" running
proactively. The post lists five controls. It is an internal deployment account
with config excerpts; it reports no incident or error rates, and it names no
model. See [[guardrails]] and [[agent-identity-and-access]].

## Key points

- **Trusted versus untrusted execution.** Networking, identity, and sandboxing
  are trusted deterministic code. The agent, its environment, and the code it
  writes are untrusted. OpenAI added **remote harness execution** to the open
  source OpenClaw project so the OpenClaw Gateway (which configures the agent)
  runs in a separate container, and at OpenAI a separate cluster, from the
  agent harness. Compare the brain–hands split in [[agent-harness]].
- **Four sandbox controls**, using the built-in [[openai-codex]] sandbox:
  network (org-managed allowlist plus explicit denials), workspace (writes only
  in agent working directories), process (Codex Linux sandbox isolation), and
  secrets (a credential broker, so the agent never sees secrets).
- **Admin-enforced `requirements.toml`.** Removes `danger-full-access`; allows
  only cached web search; requires the managed network proxy;
  `managed_allowed_domains_only = true` stops user config from widening the
  allowlist. The deny list includes `pastebin.com`, `webhook.site`, and the
  cloud metadata endpoints `metadata.google.internal` and `169.254.169.254`.
- **`config.toml` permission profile `openclaw`.** Filesystem: minimal runtime
  read, workspace write, managed assets read-only, `.ssh` denied. Network:
  through the proxy only, with `allow_local_binding = false`, SOCKS5 off, no
  upstream proxy, no non-loopback proxy listeners, no blanket Unix sockets.
  Shell environment: GitHub token variables stripped (the post notes this does
  not hide credentials in readable files). Apps: off by default, with
  destructive and open-world operations off.
- **Model-based safeguards.** The post calls the controls above static and
  says that, as models get smarter, defenses must also "scale with compute": **Auto-review**,
  where a second agent monitors and approves the primary agent's actions. The
  stated reason is review fatigue in humans. OpenAI enforces auto-review on
  **all** agent actions in this deployment.
- **Agent identity separate from user identity.** Needed to audit actions, grant
  resources, and tell agent-initiated from user-initiated actions. The post
  cites IETF drafts WAG (agent's own access) and XAA (OAuth delegation on a
  user's behalf). It says agent identity "is different from service accounts"
  and the two should be combined: the agent acts under its own identity and
  reaches third-party services through linked service accounts. Each OpenClaw
  agent has a unique identity tied to a ChatGPT Service Account, with its own
  inference credential; OpenAI can audit it and turn off its inference.
- **Observe everything.** Every control-plane configuration change and every
  agent turn is logged; access to those logs is limited to a few security staff
  because turns can hold sensitive data.
- **OpenClaw Enterprise (OCE).** Announced at OpenAI dev day: an open source,
  vendor-neutral agent control plane whose "standard codex preset" ships many of
  these safeguards. Pilot phase; 1.0 planned by end of year.

## Entities

[[openai]], [[openai-codex]]. OpenClaw, OpenClaw Gateway, and OpenClaw
Enterprise have no wiki page.

## Concepts

[[guardrails]], [[agent-identity-and-access]], [[agent-harness]]

## Notable claims & data

- Agent counts are self-reported and worded two ways: "hundreds of OpenClaw
  agents" and "over 500 agents" running proactively in the background.
- **Auto-review scope differs from the earlier Codex post.** Here auto-review is
  enforced on all agent actions. In [[openai-running-codex-safely]], the
  auto-approval subagent handles "requests that cross the sandbox boundary".
  The two deployments differ (persistent agents versus developer Codex); this is
  a different policy, not a contradiction.
- **`allow_local_binding` differs.** This post sets it to `false` (in
  `config.toml`, table `[permissions.openclaw.network]`) to keep the
  proxy's local/private-address guard on. [[openai-running-codex-safely]] sets
  `allow_local_binding = true` (localhost allowed) in `requirements.toml`, table
  `[experimental_network]`, for developer machines.
- **Cloud metadata endpoints are denied explicitly** here; the earlier post's
  deny list shows only `pastebin.com`.
- **Service accounts.** This post says agent identity "is different from service
  accounts" and should be used together with them. [[agent-identity-and-access]]
  currently describes a "warehouse service account" or "single-purpose service
  account" as one form of the agent acting as its own principal. A wording
  difference worth recording on that page.
- The example allowlist (`github.com`, `api.github.com`, `codeload.github.com`)
  is not discussed as an exfiltration path. Anthropic reports that an
  allowlisted domain can itself carry data out
  ([[anthropic-eng-how-we-contain-claude]]). Wiki inference: an agent that can
  push to GitHub may have such a path. Open question, not a contradiction.

## Connections

- **Extends** [[openai-running-codex-safely]] from developer Codex to unattended
  persistent agents, with the same `requirements.toml` / `config.toml` split and
  a stricter network profile. Sandbox internals (permission profiles, network
  proxy) are on [[openai-inside-the-codex-sandbox]];
  [[openai-codex-windows-sandbox]] covers the Windows sandbox.
- **Applies** [[openai-agent-security-enterprise]]: agents as identifiable
  non-human actors, credentials outside the agent's context, actions observed.
- **Parallels** Anthropic's credential handling outside the sandbox
  ([[anthropic-eng-scaling-managed-agents]]) and its argument that per-action
  approval fails through fatigue ([[anthropic-eng-how-we-contain-claude]],
  [[anthropic-eng-claude-code-auto-mode]], [[anthropic-auto-mode-default]]).
- Agent as its own principal: compare [[anthropic-agent-identity-access-model]]
  (Claude Tag) and [[anthropic-zero-trust-for-ai-agents]] (one identity per
  agent).
- Log everything, treat the agent as an insider: compare
  [[anthropic-securing-ai-native-sdlc]].
