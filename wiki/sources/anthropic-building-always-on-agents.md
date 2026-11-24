---
title: "Anthropic: Building always-on agents"
type: source
created: 2026-11-24
updated: 2026-11-24
author: William Hu (Anthropic)
date: 2026-11-13
source_url: https://claude.com/resources/articles/building-always-on-agents
source_path: raw/anthropic-building-always-on-agents.md
models: [claude-opus-5-5, claude-opus-5]
as_of: 2026-11-24
tags: [always-on, proactive-agents, event-driven, memory, permissions, harness, architecture]
---

# Anthropic: Building always-on agents

> Anthropic's reference architecture for stateful, proactive agents: five primitives (event inbox, timers, memory, permissions, outbox) around an ordinary agent loop.

## Summary

Anthropic published this guide on claude.com on 2026-11-13. William Hu wrote it. The post defines an always-on agent as stateful and proactive. The agent keeps context across sessions and acts without direct supervision. The core loop is the same as in other agents. The difference is the architecture around the loop.

"Always on" describes the user experience, not the runtime. The agent sleeps most of the time. It wakes for a **run**: it receives an event, does the task, and saves what happened. A run happens inside a **session**. The session is the record of messages and tool calls. Five primitives control when the agent wakes, what it remembers, what it may do, and how results reach the user.

## Key points

- **Event inbox.** Every event source writes to an inbox, and the event sources do not call the agent directly. Direct calls let two events start competing runs, and a crash can lose an event. The minimal inbox has a durable event table, an HTTP handler that writes events, and a worker that reads events. (see [[agent-harness]])
- **Inbox rules.** The handler acknowledges events fast, because webhook providers treat slow replies as failures. Deep checks, such as prompt-injection screening, run inside the run. The inbox is the source of truth, so a new worker can retry an event after a crash. Each inbox has one active worker. The worker batches pending events into one run. (see [[prompt-injection]])
- **Sessions.** An event that continues earlier work, such as a user reply, resumes the existing session. Other events start a new session. The post recommends one inbox per user as a start.
- **Timers.** A follow-up is a deadline that the agent chooses for itself. A schedule recurs on a known cadence. Timers live in a separate store. A scheduler polls the store, marks follow-ups done, moves schedules to the next due time, and writes an event into the inbox.
- **Memory.** Memory is a directory of files on durable storage, so memories outlive the worker. Store only what the agent cannot look up again, and store pointers for the rest. The post lists four memory types: user instructions, user notes, past messages, and task progress. Large note sets load only an index at the start of a run. Dreaming curates memory across runs. (see [[agent-memory]])
- **Context overhead.** The system prompt, tool definitions, and memory files load on every run. The post says to keep this overhead small and to use prompt caching. Compaction and new sessions both lose detail, so the agent saves lasting facts to memory during the run. (see [[context-engineering]])
- **Permissions.** A proxy outside the agent's environment injects credentials into outgoing requests. Auto-mode classifiers review higher-risk actions, and the user still reviews the most important decisions. A deferred tool call ends the run and saves the session mid-call. The user's answer returns as an inbox event, which resumes the session. (see [[agent-identity-and-access]], [[guardrails]])
- **Outbox.** A run ends in one of three ways: a message, a decision to send nothing, or a deferred tool call. A simple "send" tool is enough for most agents. A formal outbox table with a dispatcher is needed only to pace messages or to recover from errors.
- **Message volume.** Too many messages make noise, and too few messages miss things. The post recommends evals to tune volume. It says the agent starts quiet and earns more of the user's attention over time. (see [[agent-evals]], [[human-agent-teams]])

## Notable claims & data

- Model-specific claim, as of 2026-11-24: Opus 5.5 was 78% cheaper than Opus 5 per solved task on one long-horizon coding benchmark. On typical workloads the saving was 40%. The post does not name the benchmark. The 40% figure matches the "40% cheaper for typical workloads" estimate in [[anthropic-what-a-task-costs-opus-5-5]].
- The post gives two reasons for renewed interest in always-on agents: better model judgment about user intent and check-ins, and cheaper intelligence for long-horizon tasks.
- Claude Code's auto memory and the Messages API memory tool both store memory as a directory of files.
- Deferred tool calls can show the request to the user as an interactive card built with MCP Apps. (see [[model-context-protocol]])

## Entities

[[anthropic]], [[claude]], [[claude-code]].

## Concepts

[[agent-harness]], [[agent-memory]], [[context-engineering]], [[agent-identity-and-access]], [[guardrails]], [[prompt-injection]], [[agent-evals]], [[human-agent-teams]], [[model-context-protocol]].

## Connections

- Memory types and dreaming: [[anthropic-eng-components-of-agent-memory]].
- Auto-mode classifiers: [[anthropic-eng-claude-code-auto-mode]].
- OpenAI's persistent-agent security account reviews every action of an always-on agent, while this post reviews only higher-risk actions: [[openai-securing-persistent-agents-openclaw]].
- Events that arrive while the agent works: [[openai-time-awareness-async-input-agents]].
- Credential proxy outside the sandbox, as in [[claude-managed-agents]] and [[anthropic-self-hosted-managed-agents]].
- Scheduled and recurring agents: [[anthropic-building-effective-agent-automations]].
