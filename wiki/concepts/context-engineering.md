---
title: Context Engineering
type: concept
created: 2026-06-21
updated: 2026-10-12
tags: [context, memory, caching, agents, best-practices, token-cost, sessions]
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

## Cost model: tokens × turns × contexts

Every item in the context is re-sent on every later turn. The cache makes each
re-send cheaper, but not free, and each re-sent item still adds to what the model
must reason over. Session volume is therefore the tokens in context × the turns
they stay × the contexts that run at once (see
[[anthropic-claude-code-session-cost]]).
- **Turn count sets cost.** Because each turn re-sends the prefix, turns and the
  cache hit rate dominate the bill. A check that the model can run (a test, a
  build, a script) cuts turns, because the model finds its mistakes earlier. A
  retry costs more than any saving from lower effort, a smaller model, or less
  context (see [[anthropic-what-a-task-costs-opus-5-5]]; model-specific prices
  and multipliers live on that page).
- **The unit is a finished task, not a token** (see
  [[anthropic-what-a-task-costs-opus-5-5]], [[anthropic-choosing-claude-model]]).
- **A long, durable thread costs more than a fresh one.** OpenAI's Codex white
  paper names this tradeoff for pinned workstream threads (see
  [[openai-codex-maxxing-long-running-work]]).
- **Where to look first,** in cost order: long sessions, too much in the context,
  a bigger model or higher effort than the task needs, and a broken prompt cache
  (see [[anthropic-claude-code-session-cost]]).

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
adding nested, progressive search (see [[anthropic-seeing-like-an-agent]]). The
Agent SDK guidance puts agentic file-system search first and adds semantic search
only when needed (see [[anthropic-building-agents-claude-agent-sdk]]). For large
codebases, embedding indexes lag active code and can return renamed or deleted
code without warning; agentic search on the live code avoids this but needs good
starting context (see [[anthropic-claude-code-large-codebases]]). An
OpenAI case study (Collxn) likewise found built-in web search plus custom tools
less complex than a full RAG system (see [[openai-one-year-of-responses]]).

**Gather, then reason.** Repo Prompt splits the two: a context-builder agent
assembles a structured context package, a separate model reasons over it with no
tool calls or retrieval, and a reviewer agent decides whether to loop (see
[[openai-one-year-of-responses]]). This parallels the search-subagent pattern
below.

**Large codebases.** [[anthropic-claude-code-large-codebases]] adds three
navigation aids:
- **LSP over grep** for symbol-level navigation, which avoids thousands of grep
  hits and wrong same-named symbols; the post calls it one of the
  highest-value investments for multi-language codebases (see [[tool-design]]).
- **Layered CLAUDE.md:** a lean root file with pointers and gotchas, plus
  per-directory files. Claude Code walks up from its start directory and loads
  every CLAUDE.md, so starting in a subdirectory scopes the context.
- **Exclusions and maps:** committed deny rules that keep generated and
  third-party code out of search, and a root codebase map when directory names do
  not explain themselves.

**Stage inputs as files, not prompt text.** OpenAI's hosted runtime stages inputs
in the container filesystem and lets the model choose what to open; structured
data goes into SQLite with a table description, so the model queries only the
rows it needs (see [[openai-responses-api-computer-environment]]).

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
Domain guidance belongs in a skill rather than the system prompt, so unrelated
requests carry none of its tokens (see
[[anthropic-improving-frontend-design-through-skills]]). Anthropic's skills guide
sets a size limit for `SKILL.md` and a threshold for reviewing how many skills are
enabled at once (see [[anthropic-complete-guide-building-skills]]). In production,
Vapi reports tool search over a catalog of more than 100 tools (see
[[claude-customer-vapi]]).

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
Memory that persists across runs and sessions (lessons logs, ledgers, memory
vaults, memory stores, write controls, and poisoning) is covered in
[[agent-memory]].

**The session is not the context window.** Compaction, memory tools, and trimming
discard irreversibly. A durable session log outside the harness lets the harness
resume, rewind, or reread positional slices, and transform events before they
enter context; storage (session) is separate from context management (harness)
(see [[anthropic-eng-scaling-managed-agents]]). OpenAI's Codex design converges
on the same split: compaction rewrites only the model input, while the thread's
event history is stored separately for resume and reconnect (see
[[openai-unrolling-codex-agent-loop]], [[openai-codex-app-server-harness]]).

**Durable state in files.** State that must survive compaction, summarization, or
a fresh session lives in files the agent reads, not in the prompt. Cross-run
records (bookmarks, ledgers, run records, per-run notebooks, preferences) are
covered in [[agent-memory]] (see [[anthropic-building-effective-agent-automations]],
[[openai-automating-repetitive-work-codex]]). Within a run:
- A **task list** in a file (e.g. `TASKS.md`) survives Claude Code's summarization
  of older turns (see [[anthropic-getting-most-out-of-opus-5-5]]).
- A **spec, plan, runbook, and status-log stack.** OpenAI's long-horizon Codex run
  froze the target in one file, kept milestones with validation commands in a
  second, a runbook in a third, and a status and audit log in a fourth (see
  [[openai-run-long-horizon-tasks-codex]]).
- **Filesystem plus bash.** Outtake reports that this gives memory that survives
  compaction and lets the agent work around failing tools (see
  [[anthropic-outtake-cyber-investigator]]).
- **File-chained stages.** LG CNS reports that each stage of its migration
  pipeline writes files the next stage reads; it keeps this pattern even with
  1M-token windows, because context taxonomy matters more than raw window size
  at its scale (see [[claude-customer-lg-cns]]).
- Intermediate results and saved working functions written to the sandbox
  filesystem, which can grow into skills (see
  [[anthropic-eng-code-execution-with-mcp]]).

Cursor's Field Guide is a multi-agent variant: agents curate surprising
discoveries into a shared, size-bounded index injected into later runs. Its task
tree also isolates context by role—planners retain intent while workers retain
only a narrow implementation leaf. (see
[[cursor-agent-swarm-model-economics]], [[agent-orchestration]])

- **A checklist file as a scratchpad.** For large multi-step jobs such as
  migrations or lint backlogs, have the agent keep a Markdown checklist and work
  through it item by item. (see [[anthropic-eng-claude-code-best-practices]])

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
     and offers it server-side (see [[openai-shell-skills-compaction]]). Its
     compaction endpoint replaces the input with an opaque, encrypted compaction
     item plus high-value recent items, and models are trained to emit that item
     (see [[openai-unrolling-codex-agent-loop]],
     [[openai-responses-api-computer-environment]]). The Responses API also keeps
     encrypted reasoning state on the server across turns (see
     [[openai-why-we-built-responses-api]]).
   - **Compact early, with a hint.** Autocompact fails when the model cannot
     predict where the work goes next, and the model is at its least capable at
     compaction time because of context rot. Compact proactively and say what
     comes next (see [[anthropic-claude-code-session-management]]). Compact
     before a break, not after it, when the cache has expired (see
     [[anthropic-what-a-task-costs-opus-5-5]],
     [[anthropic-opus-5-5-long-coding-sessions]]).
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

## Session management

Every finished turn is a branching point with five options (see
[[anthropic-claude-code-session-management]]):

| Option | When |
|---|---|
| Continue | The context is still useful. |
| Rewind | The approach failed; return to just after the useful reads. |
| Compact with a hint | Mid-task, but the context is bloated. |
| Clear | A new task; carry forward only a user-written brief. |
| Subagent | The output is noisy and only the conclusion matters. |

- **Rewind instead of correcting.** Re-prompt from just after the useful file
  reads with the lesson learned, rather than append a correction on top of the
  failed attempt (see [[anthropic-claude-code-session-management]]). Rewind
  trims only the end of the conversation, so the earlier turns stay cached;
  compaction rewrites the whole context (see
  [[anthropic-claude-code-session-cost]]).
- **Compact versus clear.** Compaction is lossy and model-written; clearing with
  a user-written brief takes more work but controls exactly what carries forward
  (see [[anthropic-claude-code-session-management]]).
- **One session per task.** Clear between unrelated tasks; compact between
  phases (see [[anthropic-claude-code-session-cost]],
  [[anthropic-claude-code-session-management]]).
- **Plan in one session, implement in a fresh one.** Seed the implementation
  session with the planning artifacts (spec, prototype), and have the agent log
  forced deviations in a notes file (see [[anthropic-fable-field-guide-unknowns]]).
  A fresh session can receive several plan and exploration files, and a
  verification agent reads the same files (see
  [[anthropic-unreasonable-effectiveness-of-html]]).

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
- **Segment the prefix by scope and lifetime.** Anthropic's commerce-agent
  reference orders the prefix as global, then session, then volatile content;
  skills load as tool results, so they extend the cache instead of breaking it,
  and the cache breakpoint rolls forward each turn (see
  [[anthropic-anatomy-of-commerce-agents]]). Dust reports a three-tier cache:
  globally shared instructions on the longest lifetime, workspace and per-user
  context on shorter ones; cache reads rose from about 30% to 65% of input
  tokens (see [[claude-customer-dust]]).
- **User-side cache breakers.** Switching model, changing some session settings,
  connecting or disconnecting a tool server, compaction, and cache expiry each
  force a re-prefill. The cheap moments to switch are the session start or right
  after a clear (see [[anthropic-claude-code-session-cost]],
  [[anthropic-what-a-task-costs-opus-5-5]]). Which settings break the cache, and
  the cache lifetimes, change by model and access path; see the source pages and
  the open questions below.
- OpenAI's Codex CLI follows the same rules: the old prompt is an exact prefix of
  the new one, configuration changes become new messages, and changing tools,
  model, sandbox, or working directory mid-conversation causes a cache miss (see
  [[openai-unrolling-codex-agent-loop]]).

## Legibility: what the agent can see

**Information the agent cannot read does not exist for it.** Two independent
sources state this. OpenAI's harness-engineering team says Slack threads, Google
Docs, and tacit knowledge must move into the repository, which becomes the
system of record (see [[openai-harness-engineering]]). Anthropic says agents know
only what is written and searchable: decisions in DMs or private channels are
blind spots, so new channels default to public and teams write notes with agents
as primary readers (see [[anthropic-building-effective-human-agent-teams]],
[[anthropic-slack-human-agent-teams]]).
- **Keep the knowledge base current mechanically.** OpenAI reports a short
  `AGENTS.md` that points into a structured `docs/` directory, linters and CI
  that check docs are current and cross-linked, and a recurring doc-gardening
  agent that opens PRs to fix stale docs. The post cautions that its results
  depend on one repository's structure (see [[openai-harness-engineering]]).
- **Context as a versioned artifact.** The MacCoss Lab reports keeping all AI
  context in its own repository and growing it like code (see
  [[anthropic-onboarding-claude-code-legacy-codebase]], [[agent-memory]]).
- **Consistent code is context.** Agents copy patterns from nearby code, good or
  bad; Spotify and OpenAI each report that standardized code improves agent
  output (see [[claude-customer-spotify-boris-office-hours]],
  [[openai-harness-engineering]]).
- **Structure before agents act.** Asana reports logging actionable items as
  tasks and projects that agents pick up, rather than handing agents
  unstructured input (see [[anthropic-asana-coachable-agents]]).

**Internal context is the signal.** Anthropic's CLUE triage platform enriches
each alert with Slack, internal docs, code repositories, and warehouse data before
a human sees it, and names internal context as the differentiator over external
tools (see [[anthropic-cybersecurity-triage-agents]]). OpenAI's data agent uses six
context layers, including Codex reading the pipeline code that builds each table;
a daily job merges and embeds three of them, and the agent retrieves at query
time (see [[openai-in-house-data-agent]]). n8n reports that an in-product
assistant that sees the user's real workflow diagnoses better than an external
chatbot (see [[claude-customer-n8n]]).

## Why it matters

Context is the scarce resource in long-running agents. Good context engineering is
what lets a single agent scale (see [[agent-orchestration]]) and is the mechanism
behind "let Claude manage context" — a key part of [[agent-design-principles]].
It also connects back to the LLM-wiki idea this repo is built on: a persistent,
curated artifact beats re-retrieving raw context every turn.

## Related concepts

- [[agent-skills]], [[agent-steering]], [[agent-harness]], [[agent-orchestration]],
  [[agent-design-principles]], [[tool-design]], [[agent-instructions]],
  [[model-context-protocol]], [[agent-memory]], [[multi-agent-economics]]

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
- [[anthropic-eng-claude-code-best-practices]]
- [[anthropic-claude-code-session-cost]]
- [[anthropic-claude-code-session-management]]
- [[anthropic-opus-5-5-long-coding-sessions]]
- [[anthropic-what-a-task-costs-opus-5-5]]
- [[anthropic-choosing-claude-model]]
- [[anthropic-fable-field-guide-unknowns]]
- [[anthropic-unreasonable-effectiveness-of-html]]
- [[anthropic-onboarding-claude-code-legacy-codebase]]
- [[anthropic-claude-code-large-codebases]]
- [[anthropic-building-agents-claude-agent-sdk]]
- [[anthropic-anatomy-of-commerce-agents]]
- [[anthropic-improving-frontend-design-through-skills]]
- [[anthropic-complete-guide-building-skills]]
- [[anthropic-outtake-cyber-investigator]]
- [[anthropic-building-effective-human-agent-teams]]
- [[anthropic-slack-human-agent-teams]]
- [[anthropic-asana-coachable-agents]]
- [[anthropic-cybersecurity-triage-agents]]
- [[claude-customer-dust]]
- [[claude-customer-vapi]]
- [[claude-customer-lg-cns]]
- [[claude-customer-n8n]]
- [[claude-customer-spotify-boris-office-hours]]
- [[openai-codex-maxxing-long-running-work]]
- [[openai-run-long-horizon-tasks-codex]]
- [[openai-why-we-built-responses-api]]
- [[openai-unrolling-codex-agent-loop]]
- [[openai-codex-app-server-harness]]
- [[openai-responses-api-computer-environment]]
- [[openai-harness-engineering]]
- [[openai-in-house-data-agent]]

## Contradictions / open questions

- _Primary source now ingested ([[anthropic-eng-context-engineering]]). Remaining
  depth would come from the memory-tool and compaction feature docs._
- **Superseded: effort changes and cache lifetime (recorded 2026-10-12).**
  [[anthropic-claude-code-session-cost]] (2026-08-14) says a mid-session effort
  change breaks the Claude Code cache and that API-key caches last five minutes
  by default. [[anthropic-opus-5-5-long-coding-sessions]] (2026-09-24) says that
  on Opus 5.5 and Fable 5.1 an effort change no longer resets the cache, and that
  API-key and cloud-provider users can set a one-hour lifetime.
  [[anthropic-what-a-task-costs-opus-5-5]] (2026-09-25) adds an exception that
  the 09-24 post omits: on Amazon Bedrock, Google Cloud's Agent Platform, or a
  Claude apps gateway, an effort change still clears the cache. The source pages
  treat this as supersession for the named models, not a conflict; the August
  rule may still hold for other models.
- **Tradeoff: server-held state versus stateless requests.**
  [[openai-shell-skills-compaction]] recommends carrying state on the server
  between requests for long runs. Codex CLI deliberately keeps requests stateless
  to support Zero Data Retention and carries only encrypted reasoning across turns
  (see [[openai-unrolling-codex-agent-loop]]).
- **Open:** when the Codex harness runs inside the workspace container, does a
  thread survive loss of that container? [[openai-codex-app-server-harness]]
  relies on persisted thread history for reconnection but does not say.
  [[anthropic-eng-scaling-managed-agents]] argues against co-locating the harness
  with the sandbox.
