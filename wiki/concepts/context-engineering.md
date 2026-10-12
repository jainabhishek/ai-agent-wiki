---
title: Context Engineering
type: concept
created: 2026-06-21
updated: 2026-10-12
tags: [context, memory, caching, agents, best-practices]
---

# Context Engineering

> Managing what goes into (and stays out of) the model's context window — load the
> right information at the right time, let the agent prune and persist context
> itself, and structure prompts for cache efficiency. A through-line across the
> ingested Anthropic sources.

## Definition & why it matters

[[anthropic-eng-context-engineering]] defines it as "curating and maintaining the
optimal set of tokens (information) during LLM inference" — the evolution beyond
prompt engineering, spanning system instructions, tools, external data, and
message history. It matters because of **context rot**: "as the number of tokens
in the context window increases, the model's ability to accurately recall
information from that context decreases" (n² attention + sparse training on long
sequences). Treat context as **finite and precious**. Governing maxim: **find the
smallest set of high-signal tokens that maximize the likelihood of your desired
outcome.**

## System-prompt altitude

Aim between **brittle** (hardcoded if-else in the prompt) and **vague** (overly
general). Organize into sections (XML tags / Markdown headers); start minimal with
your best model and add only to fix identified failures; "minimal does not
necessarily mean short." Closely related to [[agent-steering]] and
[[agent-instructions]].

**Conflicting instructions across layers.** The system prompt, CLAUDE.md, skills,
and the user request all land in one context and can contradict each other; the
model then spends reasoning reconciling them. Anthropic found such conflicts in
[[claude-code]] transcripts and recommends auditing the layers for
over-constraint and conflict; it also keeps tool-usage guidance in the tool
description only, not repeated elsewhere (see
[[anthropic-new-rules-context-engineering-claude-5]]). Layer roles and
precedence are covered in [[agent-instructions]].

## Retrieval: just-in-time vs pre-loading

- **Just-in-time** — hold lightweight identifiers (paths, queries, URLs) and load
  at runtime; metadata (folders, names, timestamps) guides behavior; progressive
  disclosure. e.g. Claude Code uses `head`/`tail` instead of loading whole files.
- **Pre-loading** (embeddings) — faster but risks staleness/indexing complexity.
- **Hybrid (recommended)** — some upfront, the rest explored autonomously.
This is the same "persistent curated artifact > re-retrieve raw context" intuition
behind the LLM-wiki idea this repo implements.

**Agentic search over pre-retrieval.** Claude Code replaced a pre-indexed RAG
vector store with a Grep tool so the model builds its own context, with skills
adding nested, progressive search (see [[anthropic-seeing-like-an-agent]]). An
OpenAI case study (Collxn) likewise found built-in web search plus custom tools
less complex than a full RAG system (see [[openai-one-year-of-responses]]).

**Gather, then reason.** Repo Prompt splits the two: a context-builder agent
assembles a structured context package, a separate model reasons over it with no
tool calls or retrieval, and a reviewer agent decides whether to loop (see
[[openai-one-year-of-responses]]). This parallels the search-subagent pattern
below.

## Core practices

**Load on demand, not all at once (progressive disclosure).**
Use [[agent-skills]] whose bodies load only when invoked; path-scope rules; keep
CLAUDE.md lean. (see [[agent-steering]], [[anthropic-steering-claude-code]])
Tool definitions follow the same rule: defer most definitions and load them via
tool search, keeping the 3–5 most-used tools always resident (see
[[anthropic-eng-advanced-tool-use]]); or expose [[model-context-protocol]]
servers as a file tree of code wrappers the agent browses on demand (see
[[anthropic-eng-code-execution-with-mcp]]). Always-loaded metadata still costs
context: with many skills installed, [[openai-codex]] shortens skill descriptions
to fit, and selection gets worse (see
[[openai-rethinking-skills-prompts-gpt-6-astra]]). Templates placed inside skills
cost nothing until invoked (see [[openai-shell-skills-compaction]]).

**Let the agent manage its own context.**
- Give code execution so the agent **orchestrates actions** and filters/pipes tool
  results without pushing them all through context. One MCP task fell from about
  150K to about 2K tokens (98.7%) when tools were called from code (see
  [[anthropic-eng-code-execution-with-mcp]]); the pattern is productized as
  Programmatic Tool Calling (see [[anthropic-eng-advanced-tool-use]]).
- Use **context editing** to remove stale information.
- Use **subagents** for isolated work whose intermediate results don't return;
  e.g. Claude Code's docs-search subagent returns only the answer (see
  [[anthropic-seeing-like-an-agent]]).
(see [[harnessing-claudes-intelligence]], [[agent-orchestration]])

**Let the agent persist context.**
Append-only logs, memory folders, compaction, and strategic summarization let the
agent choose what to remember across sessions — rather than relying solely on
retrieval/RAG infrastructure. The **session** (append-only event log) in
[[claude-managed-agents]] is the durable form of this. (see [[agent-harness]])

**The session is not the context window.** Compaction, memory tools, and trimming
discard irreversibly. A durable session log outside the harness lets the harness
resume, rewind, or reread positional slices, and transform events before they
enter context; storage (session) is separate from context management (harness)
(see [[anthropic-eng-scaling-managed-agents]]).

**Durable state in files.** State that must survive fresh sessions or
summarization lives in files the agent reads each run, not in the prompt:
- Per-source **bookmarks** (newest-item timestamp) instead of fixed time windows;
  a **ledger** keyed by stable IDs; per-run records; user preferences re-read
  every run, never baked into the prompt (see
  [[anthropic-building-effective-agent-automations]]).
- A **task list** in a file (e.g. `TASKS.md`) survives Claude Code's summarization
  of older turns (see [[anthropic-getting-most-out-of-opus-5-5]]).
- A **per-run notebook** holding goal, plan, commands, outputs, and decisions,
  indexed so later runs can find it (see [[openai-automating-repetitive-work-codex]]).
- Intermediate results and saved working functions written to the sandbox
  filesystem, which can grow into skills (see
  [[anthropic-eng-code-execution-with-mcp]]).

Cursor's Field Guide is a multi-agent variant: agents curate surprising
discoveries into a shared, size-bounded index injected into later runs. Its task
tree also isolates context by role—planners retain intent while workers retain
only a narrow implementation leaf. (see
[[cursor-agent-swarm-model-economics]], [[agent-orchestration]])

## The three long-horizon techniques

For work exceeding a single context window ([[anthropic-eng-context-engineering]]):
1. **Compaction** — summarize near the limit and reinitialize; preserve decisions,
   open bugs, key details; discard redundant tool outputs. Tune recall-first, then
   precision. Clearing old tool-call results is the lightest touch.
   - Run compaction as a **cache-safe fork**: reuse the parent's exact prefix and
     append the compaction instruction as a new message; a separate summarizer
     call pays the full uncached price for the whole conversation (see
     [[anthropic-prompt-caching-is-everything]]).
   - OpenAI advises compaction **by default** for long runs, not as a fallback,
     and offers it server-side (see [[openai-shell-skills-compaction]]).
   - A compaction instruction can list the categories to preserve and keep the
     user's words near-verbatim (see [[anthropic-prompting-claude-fable-5-1]]).
   - Whether compaction suffices, or a full context reset with a handoff is
     needed, has changed across model generations (see
     [[anthropic-eng-harness-design-long-running-apps]],
     [[anthropic-eng-scaling-managed-agents]]). A single agent that plans and
     executes can lose requirements after compaction (goal drift); focused
     subagents counter it (see [[anthropic-harness-for-every-task]]).
2. **Structured note-taking (agentic memory)** — persist notes outside context and
   reload on demand (e.g. the file-based memory tool; Claude playing Pokémon
   tracking objectives/maps across resets). See "Durable state in files" above.
3. **Sub-agent architectures** — sub-agents explore with large context and return
   ~1–2k-token summaries to a focused coordinator. See [[agent-orchestration]].

Selection: compaction for heavy back-and-forth; note-taking for milestone-based
iterative work; multi-agent for complex parallel research.

## Design for cache hits

Prompt caching is a prefix match, so any change early in the request invalidates
everything after it. Claude Code is built around this and treats cache hit-rate
drops as incidents (see [[anthropic-prompt-caching-is-everything]],
[[harnessing-claudes-intelligence]]).
- **Static content first:** system prompt and tools → project instructions →
  session context → conversation. Past breakages: a detailed timestamp in the
  system prompt, non-deterministic tool ordering.
- **Byte-stable prefix:** render volatile values such as today's date once per
  conversation so the system prompt and tools stay byte-identical (see
  [[anthropic-prompting-claude-haiku-5-5]]).
- **Updates as messages:** send changed state (time, edited files) in the next
  message or tool result, not as prompt edits.
- **Append-only history:** return assistant turns as received and never edit
  earlier turns. The same edits that break the cache invalidate thinking blocks
  on current Claude models (see [[anthropic-prompting-claude-fable-5-1]],
  [[anthropic-building-with-sonnet-5-5]]).
- **Stable tools and models:** do not add or remove tools or switch models
  mid-session; model modes (e.g. plan mode) become tools, and a model switch
  becomes a subagent handoff. **Defer tool definitions instead of removing them**
  — name-only stubs in fixed order, full schemas loaded by tool search, which
  preserves the cache (see [[anthropic-prompt-caching-is-everything]],
  [[anthropic-eng-advanced-tool-use]]).
- **Forks share the prefix:** compaction, summarization, and skill execution reuse
  the parent's prefix (see above).
- A durable session log lets the harness reshape events before they enter context,
  e.g. for cache hit rate (see [[anthropic-eng-scaling-managed-agents]]).

## Why it matters

Context is the scarce resource in long-running agents. Good context engineering is
what lets a single agent scale (see [[agent-orchestration]]) and is the mechanism
behind "let Claude manage context" — a key part of [[agent-design-principles]].
It also connects back to the LLM-wiki idea this repo is built on: a persistent,
curated artifact beats re-retrieving raw context every turn.

## Related concepts

- [[agent-skills]], [[agent-steering]], [[agent-harness]], [[agent-orchestration]],
  [[agent-design-principles]], [[tool-design]], [[agent-instructions]],
  [[model-context-protocol]]

## Key entities

- [[anthropic]], [[claude]], [[claude-managed-agents]], [[claude-code]],
  [[openai]], [[openai-codex]]

## Appears in

- [[anthropic-eng-context-engineering]]
- [[harnessing-claudes-intelligence]]
- [[cursor-agent-swarm-model-economics]]
- [[anthropic-steering-claude-code]]
- [[anthropic-evolution-of-agentic-surfaces]]
- [[anthropic-new-rules-context-engineering-claude-5]]
- [[anthropic-seeing-like-an-agent]]
- [[openai-one-year-of-responses]]
- [[anthropic-eng-advanced-tool-use]]
- [[anthropic-eng-code-execution-with-mcp]]
- [[openai-rethinking-skills-prompts-gpt-6-astra]]
- [[openai-shell-skills-compaction]]
- [[anthropic-eng-scaling-managed-agents]]
- [[anthropic-building-effective-agent-automations]]
- [[anthropic-getting-most-out-of-opus-5-5]]
- [[openai-automating-repetitive-work-codex]]
- [[anthropic-prompt-caching-is-everything]]
- [[anthropic-prompting-claude-fable-5-1]]
- [[anthropic-eng-harness-design-long-running-apps]]
- [[anthropic-harness-for-every-task]]
- [[anthropic-prompting-claude-haiku-5-5]]
- [[anthropic-building-with-sonnet-5-5]]

## Contradictions / open questions

- _Primary source now ingested ([[anthropic-eng-context-engineering]]). Remaining
  depth would come from the memory-tool and compaction feature docs._
