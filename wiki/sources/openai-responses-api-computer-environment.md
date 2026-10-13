---
title: "OpenAI (Eng): From model to agent — equipping the Responses API with a computer environment"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Bo Xu, Danny Zhang, Rohit Arunachalam (OpenAI)
date: 2026-03-11
source_url: https://openai.com/index/equip-responses-api-computer-environment/
source_path: raw/openai-responses-api-computer-environment.md
tags: [openai, responses-api, shell, containers, compaction, skills, network-security, agent-harness, primary-source]
---

# OpenAI (Eng): From model to agent — equipping the Responses API with a computer environment

> OpenAI's engineering explanation of the hosted agent runtime behind the
> Responses API: a server-side loop, the shell tool, a hosted container,
> native compaction, an egress proxy, and skill loading.

## Summary

The post names the practical problems of building agents: where intermediate
files go, how to avoid pasting large tables into prompts, how to allow network
access safely, and how to handle timeouts and retries. OpenAI's answer is a
set of platform primitives. With custom tools, the Responses API hands control
back to the client's harness; with hosted tools, the API runs the loop itself.
It forwards the model's shell commands to a container runtime, streams output
back, and repeats until the model stops issuing commands. The shell tool
requires a model trained to propose shell commands: **GPT-5.2 and later**, as
of the 2026-03-11 post. See [[agent-harness]].

## Key points

- **Shell over code interpreter.** Standard Unix tools (`grep`, `curl`,
  `awk`) and any runtime (Go, Java, NodeJS), not only Python.
- **Concurrent commands.** The model can propose several commands in one step;
  the API runs them in separate container sessions and multiplexes the
  streams into structured tool outputs.
- **Bounded output.** The model sets an output cap per command; the API keeps
  the head and tail and marks the truncated middle. See [[tool-design]].
- **Native compaction.** Models are trained to emit an encrypted compaction
  item; the next window holds it plus high-value recent items. Server-side
  mode compacts at a configured threshold and tolerates small overages just
  before compaction; a standalone `/compact` endpoint also exists. See
  [[context-engineering]].
- **Files and SQLite, not prompt stuffing.** Stage inputs in the container
  filesystem and let the model choose what to open; put structured data in
  SQLite and give the model a table description so it queries only the rows
  it needs.
- **Egress proxy with secret placeholders.** All outbound traffic passes a
  sidecar proxy that enforces allowlists and stays observable. Secrets are
  injected per domain at egress; the model and container see only
  placeholders. See [[guardrails]].
- **Deterministic skill loading.** Skills are versioned bundles stored by ID.
  Before the model call, the API fetches skill metadata, copies and unpacks the
  bundle into the container, and adds metadata and path to context; the model
  then reads `SKILL.md` and runs scripts via shell. See [[agent-skills]].

## Entities

[[openai]], [[openai-codex]]

## Concepts

[[agent-harness]], [[context-engineering]], [[agent-skills]], [[guardrails]],
[[tool-design]], [[agent-core-components]]

## Notable claims & data

- Codex helped build the compaction system: when one Codex instance hit a
  compaction error, a second instance was started to investigate it.
- The post frames the full agent as five parts: orchestration (Responses API),
  actions (shell), runtime context (container), reusable workflow (skills),
  and longevity (compaction).

## Connections

- **Engineering companion** to the developer-facing
  [[openai-shell-skills-compaction]] (2026-02-11), which gives usage tips for
  the same three primitives (`domain_secrets`, network allowlists,
  `/responses/compact`). No conflicts found.
- **Brain–hands separation, converged.** The API service runs the loop while
  the container executes commands, and credentials are injected at egress
  outside the sandbox. This is the same structure as
  [[anthropic-eng-scaling-managed-agents]] and the containment patterns in
  [[anthropic-eng-how-we-contain-claude]].
- The compaction mechanism is the server side of what
  [[openai-unrolling-codex-agent-loop]] describes from the Codex client.
- Context for the API design: [[openai-why-we-built-responses-api]],
  [[openai-one-year-of-responses]].
