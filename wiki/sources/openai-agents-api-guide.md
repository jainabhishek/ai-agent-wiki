---
title: "OpenAI: Agents guide, Agents API, and API changelog (Aug–Oct 2026)"
type: source
created: 2026-10-12
updated: 2026-10-12
author: OpenAI
date: accessed 2026-10-12
source_url: https://developers.openai.com/api/docs/guides/agents
source_path: raw/openai-agents-api-guide.md
tags: [openai, agents-api, agents-sdk, responses-api, managed-agents, computer-use, human-in-the-loop, changelog]
---

# OpenAI: Agents guide, Agents API, and API changelog (Aug–Oct 2026)

> OpenAI's runtime-selection guide (Agents API vs Agents SDK vs Responses API),
> the Agents API docs (a managed Codex harness), and the agent-related API
> changelog entries from 2026-08-01 to 2026-10-12.

## Summary

The **Agents API** ([[openai-agents-api]]) entered public beta on 2026-09-10. It
runs the [[openai-codex]] harness as an OpenAI-managed service. OpenAI handles
sessions, orchestration, context compaction, and recovery. The application
supplies tools and chooses an execution environment: an OpenAI-hosted sandbox,
a self-hosted sandbox connected through an executor, or no sandbox. The capture
covers two assigned pages (the Agents guide and the changelog). Facts on core
concepts, architecture, and the computer-use approval model come from three
linked Agents API pages (overview, architecture, tools/computer-use).

## Key points

### Choosing a runtime (OpenAI's rule)
| | Agents API | [[openai-agents-sdk]] | Responses API |
|---|---|---|---|
| Who runs the loop | OpenAI (managed Codex harness) | SDK in your app | Your app |
| Integration effort | Low | Medium | High |
| State | Saved sessions (config, turns, items) | Your storage / SDK sessions | Manual history, chaining, Conversations |
| Environment | Hosted sandbox, self-hosted, or none | Your runtime + sandbox providers | Your own |

- Agents API: for long-running tasks where OpenAI manages the agent and saves
  its progress. It bundles compaction, multi-agent orchestration, programmatic
  tool calling, and MCP.
- Agents SDK: for when your app must control deployment, storage, approvals, and
  runtime.
- Responses API: for calling models directly or building an agent from scratch.
- Sessions, SDK sessions, Responses conversations, and sandboxes are separate
  resources with separate cleanup. See [[agent-harness]].

### Agents API model
- Four concepts: **Agent** (model, instructions, tools, MCP servers),
  **Environment** (optional sandbox), **Session** (a durable agent instance),
  and **Events/items**.
- `environment.type`: `none` (no Bash, apply-patch, or workspace files; remote
  MCP and function tools still work), `openai_hosted`, or `self_hosted` (your
  executor runs the commands; you own the lifecycle).
- Multi-agent: `multi_agent: { enabled, max_concurrent_subagents }`. Skills load
  from `capability_directories`. See [[agent-orchestration]], [[agent-skills]].
- Progress arrives by streaming and/or webhooks. A missing function-tool handler
  leaves the agent waiting.
- US data residency only; no Zero Data Retention, even with a self-hosted
  sandbox.

### Computer-use approval model (added 2026-09-29)
- The hosted browser asks for user approval for **each new website origin**,
  public sites included. Network access settings do not grant this approval, and
  origin approval does not override the network policy.
- **Origin approval does not confirm individual actions.** To guarantee
  confirmation before purchases or destructive changes, OpenAI says to restrict
  the browser to resources that cannot perform them, or to run your own browser
  runtime. A confirmation function tool works only if the agent calls it.
  Website content is untrusted and cannot grant permission. See [[guardrails]].
- **Sign-in** goes through a dedicated `browser_authentication` request. The
  values never enter model input or history. Only the main agent may request
  sign-in; subagents cannot. Auth requests expire after 5 minutes. Passkeys and
  QR-code sign-in are not supported.
- Clarifying questions use an app-defined function tool. Its results are
  visible to the model, so it must never carry credentials.

### Changelog milestones
- 2026-08-26 Assistants API shut down (migrate to Responses + Conversations).
- 2026-09-03 GPT-6 Astra; async tool calling, mid-turn steering, mid-conversation
  effort change ([[openai-prompting-gpt-6-astra]]).
- 2026-09-10 Agents API public beta.
- 2026-09-22 GPT-6 Sol and GPT-6 Luna.
- 2026-09-29 GPT-6.1 Sol with Multi-agent beta in Responses; computer use in
  the Agents API.
- 2026-10-06 Decisions API beta (`gpt-6-luna`; typed answers, stated as 10x
  faster than Responses).

## Notable claims & data

- Integration effort: Agents API low, Agents SDK medium, Responses high
  (OpenAI's own rating).
- Auth submission limits: 6 fields, 16,384 characters each, 120 KiB total.
- AWS Bedrock Managed Agents is built on the Agents API.

## Entities

[[openai]], [[openai-agents-api]], [[openai-agents-sdk]], [[openai-codex]]

## Concepts

[[agent-harness]], [[agents-vs-workflows]], [[agent-orchestration]],
[[guardrails]], [[agent-skills]], [[context-engineering]], [[tool-design]]

## Connections

The managed counterpart of the open harness described in
[[openai-codex-as-a-platform]]. It is architecturally parallel to
[[claude-managed-agents]]: both are vendor-hosted harnesses with durable
sessions and sandboxes. The origin-versus-action approval split refines the
human-in-the-loop guidance in [[openai-practical-guide-to-building-agents]].

## Contradictions / open questions

- [[openai-practical-guide-to-building-agents]] presents the Agents SDK as
  OpenAI's agent-building path. OpenAI now offers a managed alternative and
  places the SDK at "medium" integration effort. This is a scope change, not a
  contradiction. The entity page [[openai-agents-sdk]] should note it.
- No existing wiki page mentions the Assistants API, so its 2026-08-26
  shutdown makes no page stale.
