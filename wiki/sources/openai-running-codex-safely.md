---
title: "OpenAI (Security): Running Codex Safely at OpenAI"
type: source
created: 2026-10-12
updated: 2026-10-12
author: OpenAI
date: 2026-05-08
source_url: https://openai.com/index/running-codex-safely/
source_path: raw/openai-running-codex-safely.md
tags: [security, codex, sandboxing, permissions, network-policy, telemetry, guardrails, primary-source]
---

# OpenAI (Security): Running Codex Safely at OpenAI

> How OpenAI's own security team deploys [[openai-codex]] internally: a
> sandbox plus approval policy, an auto-review subagent, a managed network
> proxy, keyring credentials, command rules, admin-enforced configs, and
> OpenTelemetry logs read by a security triage agent.

## Summary

OpenAI's stated deployment principle for Codex: be productive inside a bounded
environment, keep low-risk actions frictionless, and stop higher-risk actions
for review. The post lists six controls, each with a config excerpt: sandbox
and approvals, network access, identity and credentials, rules, managed
configs, and agent-native telemetry. It is an internal deployment account, not
a benchmark; it reports no error rates. See [[guardrails]].

## Key points

- **Sandbox and approval policy are separate controls.** The sandbox sets
  where Codex can write, network reach, and protected paths. The approval
  policy sets when Codex must ask (for example, to leave the sandbox).
  Approvals can be once or per action type per session.
- **Auto-review mode** (`approvals_reviewer = "auto_review"`) sends the planned
  action and recent context to an auto-approval subagent. It approves low-risk
  actions, and high-risk actions with "sufficient level of user authorization";
  others still stop for the user.
- **Sandbox is mandatory via requirements:** `allowed_sandbox_modes =
  ["read-only", "workspace-write"]` removes full-access mode.
- **Network:** no open outbound access. A managed proxy allows expected
  domains, denies others (`pastebin.com`), and asks for unfamiliar ones; web
  search only from OpenAI's cache (`allowed_web_search_modes = ["cached"]`).
- **Credentials:** CLI and MCP OAuth tokens in the OS keyring; login forced
  through ChatGPT and pinned to one enterprise workspace, which routes activity
  to compliance logs.
- **Rules:** Starlark `prefix_rule` entries allow named read-only commands
  outside the sandbox (`gh pr view|list`, `kubectl get|describe|logs`) and can
  block or gate dangerous ones.
- **Managed configs:** cloud requirements, macOS managed preferences, and
  local requirement files; requirements cannot be overridden by users. One
  posture covers desktop app, CLI, and IDE extension.
- **Agent-native telemetry:** OpenTelemetry export of user prompts, approval
  decisions, tool results, MCP usage, and proxy allow/deny events. Endpoint logs
  say *what* happened; these logs add intent. An AI security triage agent reads
  them on alerts and hands its analysis to human analysts.

## Entities

[[openai]], [[openai-codex]]

## Concepts

[[guardrails]], [[agent-harness]], [[agent-steering]], [[model-context-protocol]]

## Notable claims & data

- The example network config allowlists `*.openai.com`. Anthropic reports an
  exfiltration through its own allowlisted API domain and calls an allowlist "a
  capability grant" ([[anthropic-eng-how-we-contain-claude]]). The OpenAI post
  does not discuss this risk class; recorded as an open question, not a
  contradiction.
- Auto-review may approve high-risk actions when user authorization is judged
  sufficient. Anthropic found that most auto-mode misses were exactly this
  judgment: the classifier decided an earlier user approval covered the blast
  radius ([[anthropic-eng-claude-code-auto-mode]]). Tension, see Connections.
- Third-party number from another source: in the Trajectory Labs test (720
  attempts) reported by Anthropic, GPT-5.6 Sol had 5.83% injection success
  under Codex Auto-review vs. 19.03% under Full Access. Caveats per that page:
  unequal effort settings, OpenAI browser safeguards not tested, and a new
  Auto-review shipped the week before ([[anthropic-auto-mode-default]]).
- Telemetry is also used to tune rollout (how often the network sandbox blocks
  or prompts).

## Connections

- **Agrees with** [[anthropic-eng-how-we-contain-claude]] and
  [[anthropic-eng-claude-code-sandboxing]]: sandbox first, network denied or
  allowlisted by default, credentials outside the agent's reach, approvals
  reserved for boundary crossings.
- **Parallels** [[anthropic-eng-claude-code-auto-mode]] and
  [[anthropic-auto-mode-default]]: both vendors put a model-based reviewer
  between per-action approval and full access. Anthropic's classifier is blind
  to tool results and agent prose; the OpenAI post says only "planned action and
  recent context", so whether tool output reaches the reviewer is not stated.
- Rules are the deterministic counterpart, like PreToolUse hooks in
  [[anthropic-steering-claude-code]] and [[anthropic-configure-hooks]]; narrow
  prefix allows fit Anthropic's advice to drop broad interpreter allow rules.
- Same vendor's broader Codex platform view: [[openai-codex-as-a-platform]],
  [[openai-codex-windows-sandbox]], OpenAI's "Agent security in the enterprise" white paper (Sep 2026; not ingested because it is behind a lead form).
- Security triage agent on logs: compare [[anthropic-cybersecurity-triage-agents]].
