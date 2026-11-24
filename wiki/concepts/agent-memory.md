---
title: Agent Memory
type: concept
created: 2026-10-12
updated: 2026-11-24
tags: [memory, agents, context, persistence, security, governance]
---

# Agent Memory

> State that an agent keeps across runs and sessions: what it learned, what it
> already did, and what its users prefer. Memory is distinct from the context
> window (what the model sees in one request) and from skills (procedures that
> humans write and change on purpose).

## Definition

Memory is the part of an agent's state that outlives one run. The context window
is rebuilt on every request and is lost when a session ends, is compacted, or is
cleared (see [[context-engineering]]). Memory is what the next run reads back.

Three boundaries define the concept:

- **Memory versus the context window.** Compaction, trimming, and the memory tool
  discard or move content out of the window; a durable store outside the window
  is what survives (see [[anthropic-eng-scaling-managed-agents]],
  [[anthropic-eng-context-engineering]]). Within-run durable state, such as a task
  list that survives summarization, is covered in [[context-engineering]].
- **Memory versus skills.** Warp separates the two: skills are procedural,
  stable, and changed on purpose by humans; memory is written by the agent at
  inference time and changes constantly (see
  [[anthropic-warp-builds-self-improving-agents]]). The boundary is porous in
  practice: Cresta reports that its Conductor agent turns a build's patterns,
  business rules, and eval approaches into a memory artifact that it shares as a
  skill (see [[anthropic-cresta-agent-builder]]), and the CI on-call agent
  promotes recurring lessons into its skill (see [[anthropic-ai-ci-cd-on-call]]).
  See [[agent-skills]].
- **Memory versus instructions.** [[anthropic-new-rules-context-engineering-claude-5]]
  replaces the habit of writing memory into CLAUDE.md by hand (the `#` key) with
  auto-memory. CLAUDE.md now holds a brief purpose plus codebase gotchas, and
  auto-memory handles remembering (see
  [[anthropic-eng-claude-code-best-practices]], [[agent-instructions]],
  [[agent-steering]]).

## Memory as files

The recurring design across vendors is memory as plain files that the agent reads
at the start of each run and updates at the end. Files are inspectable, diffable,
and survive compaction.

- **Lessons log.** Anthropic's CI on-call agent appends each resolved incident to
  `lessons.md` and reads it at the start of every investigation (see
  [[anthropic-ai-ci-cd-on-call]]).
- **Bookmarks, ledger, and run records.** Anthropic's automations guide keeps
  per-source bookmarks (newest-item timestamp) instead of fixed time windows, a
  `ledger.md` keyed by stable IDs, and per-run records `runs/<date>.md`. User
  preferences are re-read every run, never baked into the prompt; if the agent
  cannot read them, it stops rather than running on defaults (see
  [[anthropic-building-effective-agent-automations]]).
- **Project memory files.** OpenAI's long-horizon Codex run used four Markdown
  files as "durable project memory": a frozen spec, a milestone plan with
  validation commands, a runbook, and a status and audit log (see
  [[openai-run-long-horizon-tasks-codex]]).
- **Memory vault.** OpenAI's Codex white paper says message history is not
  enough. A vault holds people, decisions, open loops, and project state. If the
  vault lives in GitHub, memory diffs become a review surface. The memory
  instruction asks Codex to record what changed and each decision with its
  reason, not vague impressions (see [[openai-codex-maxxing-long-running-work]]).
- **Context repository.** The MacCoss Lab reports that it keeps all AI context in
  a separate, versioned repository so it applies across branches; plans and
  to-do lists do not persist, recorded context does (see
  [[anthropic-onboarding-claude-code-legacy-codebase]]).
- **Filesystem plus bash.** Outtake reports that a filesystem with bash gives
  memory that survives compaction (see [[anthropic-outtake-cyber-investigator]]).
- **Transcripts as a knowledge base.** Anthropic's CLUE team stores every
  investigation transcript; the transcripts serve as audit and as a knowledge base
  Claude can query (see [[anthropic-cybersecurity-triage-agents]]).
- **Shared index across agents.** Cursor's agents curate surprising discoveries
  into a shared, size-bounded index injected into later runs (see
  [[cursor-agent-swarm-model-economics]], [[agent-orchestration]]).

These files match the progress-file pattern in
[[anthropic-eng-effective-harnesses-long-running-agents]] and the structured
note-taking technique in [[anthropic-eng-context-engineering]].
- **Agent-maintained wiki.** Linked pages that an agent builds during dreaming
  act as a map of memory. In Anthropic's tests they helped most when combined
  with search, and on questions that need several documents. They gave no clear
  gain when one document answers the question. A wiki can also grow larger than
  its sources without abstracting anything. This repository follows the same
  pattern. (see [[anthropic-eng-components-of-agent-memory]])

## Platform memory

- **Auto-memory in Claude Code.** Replaces manual CLAUDE.md memory notes (see
  [[anthropic-new-rules-context-engineering-claude-5]], [[claude-code]]).
- **Memory stores in Managed Agents.** Stores mount into the sandbox, for
  example a user-owned preferences store that is read-only to the agent and an
  agent-owned state store that is read-write (see
  [[anthropic-building-effective-agent-automations]],
  [[claude-managed-agents]]). ABC Legal reports that the platform owns the loop,
  sessions, and memory, and that its agents keep memory configuration as code
  (see [[anthropic-abc-legal-managed-agents]]).
- **Per-channel memory in Claude Tag.** Access and memory are isolated per
  channel identity, and memory writes are logged (see
  [[anthropic-agent-identity-access-model]]). Anthropic lists persistent memory
  as one of three capabilities that multiplayer agents need (see
  [[anthropic-building-effective-human-agent-teams]]).

## Write and read design

- **Extract asynchronously, read in layers.** Anthropic's commerce-agent
  reference stores facts as typed records in the company's own database. An
  asynchronous extractor reads only user and assistant text; it gave 13% higher
  recall than a save-memory tool that the agent calls. Reads happen in three
  layers: always in context, prefetched per turn, and behind a lookup tool. A
  validator on the write path, user deletion, a retention period, and a
  per-deployment switch govern the data (see
  [[anthropic-anatomy-of-commerce-agents]]).
- **Offer to save corrections.** OpenAI's data agent offers to save a memory after
  a non-obvious correction. Memories are global or personal and user-editable;
  memory is one of six context layers (see [[openai-in-house-data-agent]]).
- **Retrieve through a subagent.** Greptile reports a memory subagent that
  retrieves team standards, learned codebase quirks, and instruction files (see
  [[claude-customer-greptile]]).
- **Store what the environment does not show.** State that the agent can re-read
  every turn goes stale in memory and wastes effort. Strategy, plans, and tested
  rules exist only if the agent writes them down. In Anthropic's tests, a small
  curated memory beat an archive of everything. (see
  [[anthropic-eng-components-of-agent-memory]])
- **Keep the injected layer small, as an index.** Notes that the harness
  preloads into every session cost tokens and carry any error into every
  session, and loading them does not guarantee that the agent follows them. Keep
  the top layer an index and move details down, with links left behind. (see
  [[anthropic-eng-components-of-agent-memory]],
  [[cursor-agent-swarm-model-economics]])
- **One writer per page.** In Anthropic's tests, several agents writing one
  shared summary table lost facts by overwriting each other. One page per
  document, written by one agent that quotes source terms word for word, kept
  every fact. (see [[anthropic-eng-components-of-agent-memory]],
  [[anthropic-multi-agent-coordination-patterns]])
- **Tell the agent what memory is for, not how to use it.** Fixed write rules
  such as "record only failures" reduced the memory gain for stronger models;
  per-model detail is on the source page. (see
  [[anthropic-eng-components-of-agent-memory]])
- **For always-on agents, store pointers, not copies.** Store only what the
  agent cannot look up again, and pointers to everything else. Anthropic's
  design keeps four file types (user instructions, user notes, past messages,
  task progress) and loads only an index for large note sets. (see
  [[anthropic-building-always-on-agents]])

### Offline consolidation (dreaming)

Notes written during a session record what seemed important at the time. They
can be wrong from the start, or drift. Anthropic calls an offline pass between
sessions **dreaming**: the agent reviews its transcripts, corrects notes against
what actually happened, builds linked pages, promotes a small index, and fills
gaps that no single session could see. Dreaming costs compute. Open choices are
how often to run it (for example, by how often a memory is read) and whether to
focus it on facts that change. (see
[[anthropic-eng-components-of-agent-memory]])

## Write controls

Shared memory changes the behavior of an agent for everyone who uses it, so
writes need an owner.

- Asana reports that anyone can give task-level feedback, but only named admins
  and editors can commit feedback to an agent's shared permanent memory or delete
  it. The team that owns the standard administers the agent (see
  [[anthropic-asana-coachable-agents]]).
- Keep user-owned preferences read-only to the agent; the agent proposes
  preference changes in its own store instead (see
  [[anthropic-building-effective-agent-automations]]).
- Write-path validation, user deletion, and retention periods (see
  [[anthropic-anatomy-of-commerce-agents]]).

## Integrity and poisoning

Memory is a persistence channel for attacks. An injected instruction that lands in
memory runs again in every later session.

- **Open problem.** Anthropic names persistent memory poisoning through
  cross-session state (memory, CLAUDE.md, scheduled-agent state) as unsolved (see
  [[anthropic-eng-how-we-contain-claude]], [[guardrails]]).
- **The agent's own notes as a vector.** In the automations guide, a planted
  instruction can still alter the brief through the agent's own notes; the
  authors limit the damage with read-only tokens, a read-only preferences store,
  and a host allowlist (see [[anthropic-building-effective-agent-automations]],
  [[prompt-injection]]).
- **Zero Trust safeguards.** Anthropic's Zero Trust framework lists memory-based
  privilege retention, RAG and shared-context poisoning, and slow memory drift as
  threats. Its controls: isolate memory per session and per user; validate
  integrity at every retrieval, not only at storage, by hashing each element,
  tagging its source, and storing hashes apart from content; give unverified
  memory a TTL; keep versioned stores for rollback (see
  [[anthropic-zero-trust-for-ai-agents]]).
- **Isolation by identity.** Per-channel memory compartments in Claude Tag (see
  [[anthropic-agent-identity-access-model]]) and per-user access bounds in Asana
  (see [[anthropic-asana-coachable-agents]]) limit what one context can leak into
  another.

- OpenAI's white paper lists context and memory poisoning as a threat class:
  harmful influence that persists across tasks or users. Its control is to
  isolate and review persistent context so it cannot silently redirect
  sensitive actions. (see [[openai-agent-security-enterprise]])

- **Inference, not a source claim:** dreaming against transcripts corrects
  honest errors and drift, but a poisoned transcript would also confirm a
  poisoned note. Neither [[anthropic-eng-components-of-agent-memory]] nor
  [[anthropic-zero-trust-for-ai-agents]] tests this.
- **Stale cautions build up.** Cautions collect in memory, notes, and
  instruction files over many sessions. A model that follows instructions
  closely keeps obeying stale rules such as "never retry". Prune them regularly,
  rewrite absolute rules with their scope and reason, and restart a stuck system
  with trimmed memory. (see [[anthropic-prompting-claude-fable-5-2]])

## Why it matters

Long-running and scheduled agents fail silently when memory goes stale or wrong
(see [[anthropic-building-effective-agent-automations]]). Memory is also the
mechanism by which an agent improves between runs without retraining, which makes
its write path a governance and security surface, not only a storage choice.

## Related concepts

- [[context-engineering]] — within-run context; memory is the cross-run layer.
- [[agent-skills]] — procedural knowledge that humans curate; memory is
  agent-written.
- [[agent-instructions]], [[agent-steering]] — CLAUDE.md and AGENTS.md versus
  auto-memory.
- [[agent-harness]] — where memory reads and writes are wired in.
- [[guardrails]], [[prompt-injection]] — write controls and poisoning.
- [[agent-orchestration]] — memory subagents and shared indexes.

## Key entities

- [[anthropic]], [[claude-code]], [[claude-managed-agents]], [[openai]],
  [[openai-codex]], [[cursor]]

## Appears in

- [[anthropic-anatomy-of-commerce-agents]]
- [[anthropic-ai-ci-cd-on-call]]
- [[anthropic-asana-coachable-agents]]
- [[anthropic-building-effective-agent-automations]]
- [[anthropic-warp-builds-self-improving-agents]]
- [[anthropic-cresta-agent-builder]]
- [[anthropic-new-rules-context-engineering-claude-5]]
- [[anthropic-eng-claude-code-best-practices]]
- [[anthropic-zero-trust-for-ai-agents]]
- [[anthropic-eng-how-we-contain-claude]]
- [[anthropic-agent-identity-access-model]]
- [[anthropic-building-effective-human-agent-teams]]
- [[anthropic-abc-legal-managed-agents]]
- [[anthropic-outtake-cyber-investigator]]
- [[anthropic-cybersecurity-triage-agents]]
- [[anthropic-onboarding-claude-code-legacy-codebase]]
- [[anthropic-eng-scaling-managed-agents]]
- [[anthropic-eng-context-engineering]]
- [[anthropic-eng-effective-harnesses-long-running-agents]]
- [[anthropic-prompting-claude-fable-5]]
- [[claude-customer-greptile]]
- [[cursor-agent-swarm-model-economics]]
- [[openai-codex-maxxing-long-running-work]]
- [[openai-run-long-horizon-tasks-codex]]
- [[openai-in-house-data-agent]]
- [[openai-agent-security-enterprise]]
- [[anthropic-prompting-claude-fable-5-1]]
- [[anthropic-eng-components-of-agent-memory]]
- [[anthropic-prompting-claude-fable-5-2]]
- [[anthropic-building-always-on-agents]]

## Contradictions / open questions

- **Model-scoped lesson-file guidance.** The Fable 5 prompting guide recommended a
  lesson-file memory system with a note discipline and a bootstrap prompt (see
  [[anthropic-prompting-claude-fable-5]]). The Fable 5.1 guide does not repeat it
  (see [[anthropic-prompting-claude-fable-5-1]]). Fable 5 is now legacy. It is
  unclear whether the guidance was superseded or only dropped from the page, so it
  is not stated here as a general rule.
- **Memory versus CLAUDE.md (recorded 2026-10-12).** Earlier sources framed
  CLAUDE.md as a memory store; [[anthropic-new-rules-context-engineering-claude-5]]
  (Jul 2026) moves that role to auto-memory. See [[agent-steering]] for the full
  note.
- **Extractor versus tool.** The 13% recall gain of an asynchronous extractor over
  a save-memory tool comes from one reference design
  ([[anthropic-anatomy-of-commerce-agents]]). No second source measures it.
- **Open:** no source yet compares auto-memory, Managed Agents memory stores, and
  hand-maintained files on the same task.
- **Agent-written notes plus dreaming, a third write design (recorded
  2026-11-24).** [[anthropic-eng-components-of-agent-memory]] (2026-11-06) uses
  notes that the agent writes during the session, then corrects them offline. It
  reports that newer models judge what to save well when they are left free. No
  source compares this with the asynchronous extractor or the save-memory tool
  on the same task.
- **Wiki versus search (2026-11-24).**
  [[anthropic-eng-components-of-agent-memory]] now compares an agent-built wiki,
  search, and both. The auto-memory versus memory stores versus hand-maintained
  files comparison is still open.
