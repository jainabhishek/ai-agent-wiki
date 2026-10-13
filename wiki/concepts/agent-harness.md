---
title: Agent Harness
type: concept
created: 2026-06-21
updated: 2026-10-12
tags: [harness, architecture, agents, sessions, best-practices, agent-loop]
---

# Agent Harness

> The harness is the scaffolding around the model — the loop, tool wiring, context
> management, and execution environment that turn a model into an agent. Two
> ingested Anthropic sources argue the harness must **co-evolve with the model**
> and should stay as thin as the model allows.

## Definition

The code that calls the model, manages its context, executes its tool calls, and
decides when a run ends. Historically hand-rolled ("tokens in, tokens out"), then
tuned in SDKs ([[claude-agent-sdk]], [[openai-agents-sdk]]), then partly delegated
to managed platforms ([[claude-managed-agents]]). (see
[[anthropic-evolution-of-agentic-surfaces]])

## Brain–hands separation

A durable production pattern: run the **harness (brain)** separately from the
**sandbox (hands)** where code/tools execute, connected by a **session** — an
append-only log of every model call, tool call, and result. Yields latency wins
(mechanism disputed; see Contradictions), credential isolation (vaults outside
the sandbox), and resumable, auditable runs. This is the concrete form of the
run-loop / exit-condition idea in [[agent-orchestration]] and the persistence
idea in [[context-engineering]].

- **Interfaces are the stable part.** Because every harness component goes
  stale as models improve, [[claude-managed-agents]] fixes small interfaces
  instead of a harness (a "meta-harness"): one `execute(name, input) → string`
  call for every sandbox or tool, so a dead container is a tool error the model
  can handle, and a session log outside the harness, so a fresh harness can
  resume from the last event. Session storage stays separate from context
  management. (see [[anthropic-eng-scaling-managed-agents]]) OpenAI's Codex
  App Server makes the same bet: it collapses the harness's low-level events
  into a small set of stable, UI-ready notifications, keeps the protocol
  backward-compatible, and stores thread history apart from the model input
  that compaction rewrites. (see [[openai-codex-app-server-harness]],
  [[openai-unrolling-codex-agent-loop]])
- **Secrets stay outside the sandbox.** A proxy or vault holds the real
  credential and injects it on egress, only to allowlisted hosts; the sandbox
  sees a placeholder or a session token. Seen in Managed Agents (MCP OAuth
  vault, Git token used only at init), scheduled automations, and Claude Code
  cloud sessions (a branch-scoped push credential). (see
  [[anthropic-eng-scaling-managed-agents]],
  [[anthropic-building-effective-agent-automations]],
  [[anthropic-claude-code-in-the-cloud]], [[guardrails]]) Claude Tag stores
  credentials apart from the agent and injects them at the network boundary per
  request. (see [[anthropic-agent-identity-access-model]])
- **Independent convergence across vendors.** OpenAI's hosted Responses runtime
  has the same structure: the API service runs the loop, a container executes
  the shell commands, and a sidecar egress proxy enforces allowlists and
  injects secrets per domain, so the model and the container see only
  placeholders. Anthropic and OpenAI reached the brain–hands split and
  secrets-at-egress independently. (see
  [[openai-responses-api-computer-environment]],
  [[anthropic-eng-scaling-managed-agents]], [[anthropic-eng-how-we-contain-claude]])
- **Isolation strength follows oversight.** Anthropic matches the isolation
  pattern to how much the user can oversee: an ephemeral container where no one
  watches, an OS-level sandbox with a human in the loop, a sealed local VM for a
  desktop agent. Across deployments, standard primitives (hypervisors, syscall
  filters, container runtimes) held; custom glue around them failed. (see
  [[anthropic-eng-how-we-contain-claude]])
- **Resource headroom is part of the environment.** In one agentic coding
  benchmark, extra container resources up to about 3x the task spec fixed
  infrastructure errors without changing the score; beyond that, resources let
  the agent use different strategies, so the limit changes what is measured.
  Specify a guaranteed floor and a separate kill ceiling. (see
  [[anthropic-eng-infrastructure-noise-evals]], [[agent-evals]])

## Harness–model co-evolution

The central best practice: **re-test your harness assumptions with every model
upgrade, and delete scaffolding the model has outgrown.**
- Example: Sonnet 4.5 "context anxiety" (rushing near the context limit) led teams
  to add context resets; Opus 4.5 removed the behavior, making those resets pure
  overhead. (see [[anthropic-evolution-of-agentic-surfaces]])
- The general rule from [[harnessing-claudes-intelligence]]: "Assumptions about
  what Claude can't do need to be re-tested with each step change in its
  capability." Prefer general-purpose tools and let the model do more
  ([[tool-design]], [[agent-design-principles]]).

- **Every component encodes an assumption** about what the model cannot do.
  When a new model ships, remove components one at a time and re-measure; in
  the planner / generator / evaluator case study some components became
  unnecessary while others still paid off. (see
  [[anthropic-eng-harness-design-long-running-apps]],
  [[anthropic-eng-scaling-managed-agents]])
- **Tools are harness too.** Claude Code retired tools and reminders that had
  helped earlier models but constrained later ones. (see
  [[anthropic-seeing-like-an-agent]], [[tool-design]])
- **Limits sized for weak models truncate strong ones.** Dust reports that its
  old tool-call defaults (three per run, maximum eight) cut results short once
  models could chain more steps; it redesigned the loop to allow up to 24.
  Spotify reports removing an LLM judge that had raised PR success early on,
  once models and the harness improved. (see [[claude-customer-dust]],
  [[claude-customer-spotify-boris-office-hours]])
- **Per-model tuning has a real cost.** Cognition reports that moving a model
  into a different part of its workflow forces changes to prompts, tool
  definitions, context management, trajectory monitoring, and guardrails; about
  50–70 engineers work on that surface. (see [[claude-customer-cognition]])
- **Re-review on a schedule.** Anthropic's guidance for large codebases is to
  review Claude Code configuration every three to six months and after major
  model releases. Its CISO guide adds that controls built into elaborate
  scaffolds and prompts disappear when those scaffolds become obsolete, so
  durable controls belong in identity, permissions, and monitoring. (see
  [[anthropic-claude-code-large-codebases]], [[anthropic-ciso-guide-agentic-ai]],
  [[guardrails]])

**Implication:** delegate harness tuning to the platform/SDK where you can, and
spend your effort on domain expertise, tools, and context — not on maintaining a
custom loop. Several case studies report this move. Greptile chose the
[[claude-agent-sdk]] over a homegrown harness, citing model–harness coupling,
and put its effort into review tools. Caylent rebuilt a brittle homegrown
harness on the SDK. LG CNS reports a thin, layered harness, arguing that a thick
harness that guards every failure constrains the model and costs tokens. (see
[[claude-customer-greptile]], [[claude-customer-caylent]],
[[claude-customer-lg-cns]])

The harness moves scores as much as the model does: on one fixed optimization
task, the same model scored from 1790 down to 1363 cycles (lower is better)
depending on the harness and the time budget. (see [[anthropic-eng-ai-resistant-evaluations]])

## Harness as a reusable runtime

- **The agent loop is the reusable part; the product is separate.** OpenAI
  presents the open-source [[openai-codex]] harness (conversation state,
  streaming, tool use, sandbox and approval policies) as a runtime to embed. The
  host application owns the UI, the context and tools exposed, where the agent
  runs, which actions need approval, and how results return. Harness settings
  alone (retained reasoning plus compaction) more than doubled one model's
  ARC-AGI-3 score with sixfold fewer output tokens (secondary figure). (see
  [[openai-codex-as-a-platform]])
- **Who runs the loop** is a choice: a vendor-managed harness
  ([[openai-agents-api]], [[claude-managed-agents]]), an SDK in your app
  ([[openai-agents-sdk]], [[claude-agent-sdk]]), or your own loop over a raw
  model API. OpenAI's rule trades integration effort against control of
  deployment, storage, and approvals. (see [[openai-agents-api-guide]])
- **The responsibility split repeats across deployments.** The platform or SDK
  owns the loop, sessions, and context gathering; the builder owns prompts,
  tools, triggers, policy, permissions, monitoring, review, and outcome
  feedback. ABC Legal (Managed Agents), Cresta (Agent SDK), Balyasny, and
  JetBrains each report this split; JetBrains and Balyasny put the safety net in
  the harness and infrastructure, not in the model. (see
  [[anthropic-abc-legal-managed-agents]], [[anthropic-cresta-agent-builder]],
  [[anthropic-balyasny-evaluates-fable-5]], [[anthropic-jetbrains-evaluates-fable-5]])
- **Repo-level configuration is the portable part.** In Claude Code cloud
  sessions, `CLAUDE.md`, rules, skills, agents, commands, `.mcp.json`, and
  project hooks travel with the repo; per-user config (`~/.claude`) does not.
  Test commands must therefore live in repo config. (see
  [[anthropic-claude-code-in-the-cloud]], [[agent-steering]])
- **Model-written harnesses.** Claude Code can write a task-specific
  multi-agent harness per request (dynamic workflows); static harnesses such as
  an SDK must stay generic. (see [[anthropic-harness-for-every-task]],
  [[workflow-patterns]])

## The core loop

- **Gather → act → verify → repeat.** Anthropic frames the agent loop as
  gather context, take action, verify work, and repeat. It ranks verification
  methods by robustness: rules-based feedback (for example linting) first,
  visual feedback (screenshots) second, and an LLM judge last, with a latency
  cost. Claude Code's turn-based, goal, time-based, and proactive loops all run
  this same cycle. (see [[anthropic-building-agents-claude-agent-sdk]],
  [[anthropic-getting-started-with-loops]], [[agent-core-components]])
- **OpenAI's long-horizon version** is plan → edit → run tools → observe →
  repair → update docs → repeat. In OpenAI's 25-hour Codex experiment, the
  harness supplied repo metadata, the file tree, diffs, command output, and a
  "done when" routine, and validation ran after each milestone. (see
  [[openai-run-long-horizon-tasks-codex]])
- **Doer–Verifier.** Anthropic's name for a harness that gives one agent the
  task and a second agent the check, so work is verified before human review.
  (see [[anthropic-building-effective-human-agent-teams]], [[agent-evals]])

## Loop mechanics in production

- **Cache hit rate is a production metric.** The Claude Code team lays out the
  request static-first, sends changing state as messages, never swaps models or
  tool sets mid-session, and treats hit-rate drops as incidents (SEVs). (see
  [[anthropic-prompt-caching-is-everything]], [[context-engineering]]) Greptile
  reports about 90% cache hits; Dust reports cache reads rising from about 30%
  to 65% of input tokens after a three-tier cache. (see
  [[claude-customer-greptile]], [[claude-customer-dust]])
- **OpenAI reached the same cache rules independently.** The Codex loop grows
  each request so the old prompt is an exact prefix of the new one. OpenAI
  lists the cache-miss causes as changing the tools, the model, the sandbox
  configuration, the approval mode, or the working directory mid-conversation,
  and Codex sends a config change as a new appended message instead of editing
  earlier ones. These match the Claude Code team's rules. (see
  [[openai-unrolling-codex-agent-loop]], [[anthropic-prompt-caching-is-everything]])
- **Faster inference exposes per-request overhead.** OpenAI reports that once
  inference got fast, API work on each follow-up request (reprocessing the full
  conversation) became the bottleneck. Its fix keeps prior response state in a
  cache scoped to one WebSocket connection, and reports agent loops about 40%
  faster end to end. OpenAI rejected a lower-overhead prototype (one Response
  per rollout) because its API shape broke drop-in compatibility. (see
  [[openai-websockets-agentic-workflows]])
- **Append-only history.** Return assistant turns exactly as received and never
  edit earlier turns; add reminders by appending them (for example as
  turn-scoped system messages) and leaving them in place, never by inserting and
  later deleting. Edits that break the prompt cache also invalidate preserved
  thinking. Exact API behaviors are model-scoped; see
  [[anthropic-prompting-claude-fable-5-1]],
  [[anthropic-prompting-claude-opus-5-5]],
  [[anthropic-prompting-claude-sonnet-5-5]].
- **Message placement affects injection resistance.** Never put user text inside
  a tool result; append mid-turn user words after the last tool result; keep
  harness notices in a separate system message; cap repeated harness reminders,
  because frequent harness text after tool results can look like injection.
  (see [[anthropic-prompting-claude-sonnet-5-5]], [[guardrails]])
- **Unattended loops need explicit stop handling.** A text-only end of turn can
  be a progress report rather than completion. Pattern: a model-updated
  checklist; a continuation message naming open items when no blocker is
  stated; optionally a small model judging a stated completion condition; a cap
  of two or three automatic continuations; wait for background commands and
  subagents. (see [[anthropic-prompting-claude-opus-5-5]])
- **Detect stalls by pattern, not by turn count.** Twilio reports treating the
  same tool with the same input three times as a stall, alternating calls as
  oscillation, and no file changes as idle. Safety floors on budgets and
  sandbox mode follow, plus a phase retry that keeps partial progress. (see
  [[claude-customer-twilio]])
- **The client must be able to see progress.** On some current models,
  between-tool notes arrive as thinking blocks that a text-only client does not
  show unless it opts in. Check the model-scoped page before assuming a silent
  agent is idle. (see [[anthropic-prompting-claude-opus-5-5]],
  [[anthropic-prompting-claude-sonnet-5-5]])

## Concrete long-running patterns

From the case study in [[anthropic-eng-effective-harnesses-long-running-agents]]:
- **Two-agent pattern** — a one-time **initializer** (environment, spec file, git,
  progress file) and a per-session **coding agent** doing one feature at a time.
- **Structured JSON state** the agent only partially edits (flip a "passes" field)
  — models inappropriately edit Markdown more readily than JSON.
- **Session startup sequence** — `pwd` → read git log + progress → pick top
  incomplete feature → smoke-test → implement, to avoid re-establishing context.
- **Verify like a human user** (e.g. browser automation), but only reliably once
  *explicitly* prompted. See [[agent-evals]].
- **Failure modes to design against:** premature completion, half-finished
  features, undocumented progress, code-only (non-end-to-end) verification.

- **The verifier is the steering wheel.** An autonomous agent solves whatever
  the tests define, so the tests must be nearly perfect, and a CI gate should
  block any commit that breaks existing tests. Write test output for the model:
  a few lines on screen and details in a log file, `ERROR` and its reason on one
  line that grep can find, summary statistics already computed, and a fast
  sampled mode that is stable for one agent and varies across agents. (see
  [[anthropic-eng-building-c-compiler]])
- **A concrete target to iterate against** — tests, a visual mock, or expected
  output — is the most reliable way to get good results from a coding agent.
  (see [[anthropic-eng-claude-code-best-practices]])
- **Move invariants from the prompt into the harness.** Outtake reports that in
  long runs, prompt rules are eventually ignored, so it hard-codes the
  always-do steps at the orchestration layer; this also frees context. A
  filesystem plus bash gives memory that survives compaction. (see
  [[anthropic-outtake-cyber-investigator]], [[agent-memory]], [[guardrails]])
- **Fix the environment, not the prompt.** OpenAI's harness-engineering team
  treats every agent failure as a missing capability to add to the
  environment and make legible and enforceable. Knowledge the agent cannot see
  in the repo does not exist for it; custom linters carry remediation
  instructions in their error messages. OpenAI also reports that a startup
  script, environment variables, and internet access cut Codex's error rate.
  (see [[openai-harness-engineering]], [[openai-how-openai-uses-codex]])
- **Garbage-collection agents.** Agents copy existing patterns, good or bad.
  OpenAI reports that a manual weekly cleanup did not scale, so it encodes
  "golden principles" and runs recurring background Codex tasks that find
  deviations and open small refactor PRs. (see [[openai-harness-engineering]])
- **Bounded task environments.** Thrive's tax-agent setup gives Codex a
  writable worktree (instructions, task files, scoped product code, eval
  suites, graders, skills) and reads production traces and source documents
  only through read-only tools, so the agent cannot change the evidence. (see
  [[openai-self-improving-tax-agents-codex]])

## Coordination-bearing harnesses

At multi-agent coding scale, the harness also becomes the coordination system.
Cursor placed design ownership, decision reconciliation, merge mediation,
modularity enforcement, review, and shared memory around the models; its new
harness outperformed the old one under every tested model mix. This reinforces
harness-model co-evolution: model swaps and prompt reuse must be evaluated as a
system, including downstream worker behavior. (see
[[cursor-agent-swarm-model-economics]], [[multi-agent-economics]])

## Related concepts

- [[agent-orchestration]], [[context-engineering]], [[agent-design-principles]],
  [[tool-design]], [[agent-core-components]], [[agent-evals]], [[guardrails]],
  [[agent-memory]]

## Key entities

- [[anthropic]], [[claude]], [[claude-agent-sdk]], [[claude-managed-agents]],
  [[claude-code]], [[openai-codex]], [[openai-agents-api]]

## Appears in

- [[anthropic-evolution-of-agentic-surfaces]]
- [[harnessing-claudes-intelligence]]
- [[anthropic-eng-effective-harnesses-long-running-agents]]
- [[anthropic-eng-context-engineering]]
- [[cursor-agent-swarm-model-economics]]
- [[anthropic-eng-scaling-managed-agents]]
- [[anthropic-eng-harness-design-long-running-apps]]
- [[anthropic-eng-how-we-contain-claude]]
- [[anthropic-eng-infrastructure-noise-evals]]
- [[anthropic-prompt-caching-is-everything]]
- [[anthropic-seeing-like-an-agent]]
- [[anthropic-harness-for-every-task]]
- [[anthropic-building-effective-agent-automations]]
- [[anthropic-claude-code-in-the-cloud]]
- [[anthropic-prompting-claude-opus-5-5]]
- [[anthropic-prompting-claude-sonnet-5-5]]
- [[anthropic-prompting-claude-fable-5-1]]
- [[openai-codex-as-a-platform]]
- [[openai-agents-api-guide]]
- [[anthropic-eng-building-c-compiler]]
- [[anthropic-eng-claude-code-best-practices]]
- [[anthropic-eng-ai-resistant-evaluations]]
- [[openai-unrolling-codex-agent-loop]]
- [[openai-codex-app-server-harness]]
- [[openai-harness-engineering]]
- [[openai-responses-api-computer-environment]]
- [[openai-websockets-agentic-workflows]]
- [[openai-run-long-horizon-tasks-codex]]
- [[openai-how-openai-uses-codex]]
- [[openai-self-improving-tax-agents-codex]]
- [[anthropic-building-agents-claude-agent-sdk]]
- [[anthropic-getting-started-with-loops]]
- [[anthropic-building-effective-human-agent-teams]]
- [[anthropic-agent-identity-access-model]]
- [[anthropic-claude-code-large-codebases]]
- [[anthropic-ciso-guide-agentic-ai]]
- [[anthropic-outtake-cyber-investigator]]
- [[anthropic-abc-legal-managed-agents]]
- [[anthropic-cresta-agent-builder]]
- [[anthropic-balyasny-evaluates-fable-5]]
- [[anthropic-jetbrains-evaluates-fable-5]]
- [[claude-customer-twilio]]
- [[claude-customer-dust]]
- [[claude-customer-cognition]]
- [[claude-customer-greptile]]
- [[claude-customer-caylent]]
- [[claude-customer-lg-cns]]
- [[claude-customer-spotify-boris-office-hours]]

## Contradictions / open questions

- Otherwise strongly consistent with the start-simple / prune-complexity theme.
- **Mechanism of the brain–hands latency win.**
  [[anthropic-evolution-of-agentic-surfaces]] (2026-06-10) says reasoning starts
  while the sandbox spins up in parallel;
  [[anthropic-eng-scaling-managed-agents]] (2026-04-08) says containers are
  provisioned only when a tool call needs one. Both report the same figures.
  Recorded in full on [[claude-managed-agents]].
- **Does a Codex Web thread survive container loss?** (open, 2026-10-12)
  [[openai-codex-app-server-harness]] (2026-02-04) says Codex Web runs the App
  Server inside the workspace container and relies on persisted thread history
  for reconnection. [[anthropic-eng-scaling-managed-agents]] (2026-04-08)
  describes that co-located layout as the first design that became a "pet" and
  moved the harness out of the sandbox. The OpenAI post does not say whether a
  thread survives the loss of its container. A layout difference, not a
  contradiction of fact.
- **Scope of blocking CI gates.** (scoped difference, 2026-10-12)
  [[anthropic-eng-building-c-compiler]] says a CI gate should block any commit
  that breaks existing tests. [[openai-harness-engineering]] (2026-02-11) runs
  minimal blocking gates, short-lived PRs, and re-runs for flaky tests. The
  OpenAI author limits that rule to agent throughput far above human attention,
  calls it irresponsible in a low-throughput setting, and still enforces
  mechanical lints and structural tests.
