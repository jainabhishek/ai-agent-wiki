---
title: Agent Orchestration
type: concept
created: 2026-06-21
updated: 2026-10-13
tags: [orchestration, multi-agent, single-agent, patterns]
---

# Agent Orchestration

> How to structure execution once you've chosen an agent: the run loop, when to
> stay single-agent, OpenAI's two and Anthropic's five multi-agent patterns, and
> model routing. How people work with agents is on [[human-agent-teams]]. Both
> vendors agree:
> **maximize a single agent first.** (see [[openai-practical-guide-to-building-agents]],
> [[agent-design-principles]])

## The agent run loop

Every orchestration needs a **run** — a loop that lets the agent operate until an
**exit condition**: a final-output tool, a structured output of a given type, an
error, or a maximum number of turns. In the [[openai-agents-sdk]], `Runner.run()`
loops the LLM until a final-output tool fires or the model replies with no tool
calls. (see [[openai-practical-guide-to-building-agents]])

[[anthropic]]'s agents work the same way: plan → act via tools → observe
environmental ground truth → repeat, with stopping conditions and guardrails.
(see [[anthropic-building-effective-agents]])

In production, the loop is realized as a durable **session** — an append-only log
of every model call, tool call, and result — with the harness (brain) separated
from the execution sandbox (hands). See [[agent-harness]] and
[[anthropic-evolution-of-agentic-surfaces]].

## Single-agent systems

A single agent handles many tasks by **incrementally adding tools**, keeping
evaluation and maintenance simple. To manage complexity without splitting:
use a single flexible **prompt template** with policy variables rather than many
bespoke prompts. (see [[openai-practical-guide-to-building-agents]])

**When to split into multiple agents:**
- **Complex logic** — prompts full of if-then-else branches that don't scale.
- **Tool overload** — driven by tool *overlap*, not count (see [[tool-design]]).

**Subagents** are a lightweight form of multi-agent: they run in an isolated
context window and return only a final summary, keeping the main thread clean.
Use them for deep search, log analysis, or audits whose intermediate results you
won't reference again; they can nest several levels and orchestrate many
background agents, with plans/results held in script variables rather than
context. (see [[anthropic-steering-claude-code]], [[context-engineering]])
A subagent can also add a capability without adding a tool: Claude Code's docs-search
subagent searches in its own context and returns only the answer. (see
[[anthropic-seeing-like-an-agent]])

A subagent is also the way to **switch models** inside a session. Prompt caches are
per model, so switching the main thread's model mid-session pays for the whole
prefix again; a subagent on the other model with a hand-off message avoids that.
Claude Code's Explore agents run on a smaller model this way. (see
[[anthropic-prompt-caching-is-everything]])

**When subagents hurt.** Anthropic lists five cases where a subagent costs more
than it saves: sequential work where each step depends on the last, edits to the
same file, small tasks, a sprawling roster of specialists (automatic routing gets
less reliable; a handful is typical), and agents that must talk to each other,
because a subagent reports only to the main thread. (see
[[anthropic-subagents-in-claude-code]]) A subagent pays off for a job with much
disposable output; for a small job it is overhead. (see
[[anthropic-claude-code-session-cost]], [[anthropic-claude-code-session-management]])
Multi-agent systems typically use 3–10x the tokens of a single agent for the same
task. In a role split (planner, implementer, tester, reviewer), the subagents
spent more tokens on coordination than on work. Before splitting for tool
overload, try on-demand tool discovery; before splitting for context limits, try
compaction. (see [[anthropic-building-multi-agent-systems]]) The commerce-agents
authors report that one agent with skills beat a subagent-per-domain design on
quality, often at lower cost per task, because each handoff loses state and adds
tokens and latency. In their design a subagent fits only as a tool for
self-contained work, such as deep research that returns a compact answer. A hand-off
fits a domain that already has its own agent; the test is who owns the
conversation. (see
[[anthropic-anatomy-of-commerce-agents]], [[agent-skills]])

**Why split planning from execution.** One context that both plans and executes
shows three failure modes: *agentic laziness* (stopping partway through a long item
list), *self-preferential bias* (grading its own work), and *goal drift* (losing
requirements after compaction). Separate focused subagents counter all three. In
Claude Code's dynamic workflows the model writes a per-task orchestration script
with `agent`, `parallel`, and `pipeline` primitives; this costs more tokens, so it
suits complex, high-value tasks. (see [[anthropic-harness-for-every-task]],
[[workflow-patterns]], [[multi-agent-economics]])

**Plan in one context, execute in a fresh one.** Sources from both vendors hand a
plan artifact to a fresh executor. Claude Code's large-codebase guidance has a
read-only subagent map a subsystem to a file before the main agent edits. (see
[[anthropic-claude-code-large-codebases]]) An Anthropic author hands a web of
exploration files and a plan to a fresh session, and the verification agent reads
the same files. (see [[anthropic-unreasonable-effectiveness-of-html]]) The Sora
Android team at OpenAI saved plans to files so that other Codex instances could
reuse them. (see [[openai-sora-android-with-codex]]) A case study reports the
same shape: CodeRabbit runs a planning layer that writes a requirements document
before Claude Code starts (see [[anthropic-coderabbit-agent-orchestration]]).
Planning with the user before the hand-off is on [[human-agent-teams]].

How readily a given model delegates is a per-model behavior, tuned in the prompt;
see axis 5 of [[prompt-tuning-axes]]. For example, OpenAI supplies a prompt for a
model that delegates less than desired, plus one that fixes errors in messages
between agents. (see [[openai-prompting-gpt-6-astra]])

## Multi-agent patterns (OpenAI)

- **Manager (agents as tools)** — a central manager LLM delegates to specialized
  agents via tool calls and synthesizes results. Best when one agent should keep
  control and user contact. Mirrors Anthropic's **orchestrator-workers**
  ([[workflow-patterns]]).
- **Decentralized (handoffs)** — peer agents transfer execution to one another; a
  handoff is a one-way tool call that passes conversation state. Best for triage
  and when a specialist should fully take over.

Both can be modeled as graphs (agents = nodes; edges = tool calls or handoffs).
The guiding principle across patterns: keep components **flexible, composable,
and driven by clear prompts.**

## Multi-agent coordination patterns (Anthropic)

[[anthropic-multi-agent-coordination-patterns]] (2026-04-10) names five patterns.
Start with orchestrator-subagent, which covers the most cases at the least
overhead. Move to another pattern only when a specific need appears. Production
systems often combine patterns.

| Pattern | Mechanism | Fits | Failure modes |
|---|---|---|---|
| **Generator-verifier** | a generator drafts; a verifier accepts or rejects against explicit criteria and returns feedback; loop to acceptance or a cap | — (the source gives no fit for this pattern) | a vague verifier rubber-stamps; loops oscillate. Mitigate with an iteration cap plus a fallback (see [[workflow-patterns]]) |
| **Orchestrator-subagent** | a lead plans, delegates bounded subtasks, and synthesizes | clear decomposition, low interdependence | the orchestrator is an information bottleneck; sequential dispatch adds tokens without speed |
| **Agent teams** | a coordinator spawns persistent workers that claim tasks from a shared queue and keep context across assignments | independent long-running work, such as a per-service migration | no sharing of intermediate findings; hard completion detection when durations vary; conflicting edits on shared resources |
| **Message bus** | agents publish and subscribe; a router delivers by topic; new agents join without rewiring | event-driven pipelines, such as security alert triage | hard tracing; silent drops or misroutes; an LLM router adds its own errors |
| **Shared state** | no coordinator; agents read and write a persistent store | findings that must flow between agents | duplicate or contradictory work; reactive loops. Locking, versioning, and partitioning fix write conflicts; loops need explicit termination (time budget, N cycles with no new findings, or a judge agent) |

Pairwise choice rules from the same source:
- Short, focused subtasks → orchestrator-subagent. Sustained context per worker →
  agent teams.
- A fixed sequence → orchestrator. Emergent, event-driven flow, where the
  orchestrator's conditionals multiply → message bus.
- Partitioned work → agent teams. Findings that flow between agents → shared
  state.
- A pipeline of stages → message bus. Accumulating knowledge → shared state.

How the five map to other pages: orchestrator-subagent is OpenAI's manager pattern
and the orchestrator-workers workflow; generator-verifier is evaluator-optimizer
([[workflow-patterns]]); agent teams are the peer option for agents that must
talk, which subagents cannot do ([[anthropic-subagents-in-claude-code]]). The
16-agent compiler below is shared state in practice. The OpenAI guide names only
the manager and handoff patterns; the message bus and shared state have no
counterpart in this wiki's OpenAI sources.

## Tiered model routing

A multi-agent design lets each role run on a different model class. The sources
show three shapes. Benchmark figures are model-scoped and stay on the source
pages; cost trade-offs are on [[multi-agent-economics]].
- **Frontier planner, cheaper workers.** Block reports that a frontier model
  designs data models and specs and directs up to dozens of cheaper workers that
  edit files and run tests; frontier tokens concentrate in upfront planning. (see
  [[anthropic-block-orchestrates-fable]]) CodeRabbit reports that its largest
  model runs the orchestration loop, a mid-size model sequences planning steps,
  and the smallest does narrow work such as context distillation; eval results on
  cost and latency set the routing. (see [[anthropic-coderabbit-agent-orchestration]])
  Caylent reports a small model for high-volume parsing and a mid-size model for
  synthesis, and gives each stage agent only the tools that its stage needs. (see
  [[claude-customer-caylent]], [[tool-design]])
- **Cheap classifier, specialist subagents.** Rocket Money reports a cheap
  classifier that routes each request to a single-responsibility subagent, plus
  one formatter subagent that writes every reply, so that each failure traces to
  one classifier or call. (see [[claude-customer-rocket-money]], routing in
  [[workflow-patterns]])
- **Advisor (the inverse of orchestrator-worker).** A cheap executor model runs
  the whole loop and consults a frontier advisor model only at a decision that it
  cannot resolve. The advisor reads the shared context and returns a plan, a
  correction, or a stop signal. It never calls tools and never writes
  user-facing output. There is no decomposition, worker pool, or orchestration
  code. Evaluate three configurations: the executor alone, the executor plus the
  advisor, and the advisor model alone. (see [[anthropic-advisor-strategy]],
  [[anthropic-choosing-claude-model]])

A routing rule for any of these shapes: give a small model only work where a
misread is cheap to spot, such as lookups and log reading, not code edits. The
main model pays for every detour that a misread causes. (see
[[anthropic-what-a-task-costs-opus-5-5]])

## Trust and checks at the subagent boundary

- **Subagent output is an injection path.** An orchestrator that trusts subagent
  output more than raw tool output gives injected content a route to escalate
  trust; Anthropic lists this as an open containment problem. (see
  [[anthropic-eng-how-we-contain-claude]], [[guardrails]])
- **Check at both crossings.** Claude Code's auto-mode classifier checks the
  handoff on delegation, where it can deny (inside a subagent the orchestrator's
  instruction looks like a user message), and on return, where it only warns.
  (see [[anthropic-eng-claude-code-auto-mode]])
- **The orchestrator verifies subagent evidence.** For fan-out audits, migrations,
  and large reviews, tell the orchestrator to check each subagent's evidence
  before accepting it. (see [[anthropic-getting-most-out-of-opus-5-5]]) The
  architecture form is adversarial verification: a separate agent checks the work
  against a rubric. (see [[anthropic-harness-for-every-task]])
- **Isolate the verifier.** Give a verification subagent the artifact, the
  success criteria, and tools, not the build history. Feed its issues back to the
  implementer in a retry loop with a cap. (see
  [[anthropic-building-multi-agent-systems]]) In security scanning, discovery
  agents that also verified their own findings self-censored true positives. The
  verifier runs in a fresh container with no shared filesystem or conversation
  history, sees only the finding and the codebase, and is prompted to assume that
  the finding is a false positive. Partners report that this roughly halved
  non-exploitable findings. (see [[anthropic-llms-secure-source-code]])
- **The early victory problem.** A verifier tends to declare success after one or
  two tests. Counter it with concrete criteria, edge cases, negative tests, and an
  explicit instruction to run the complete suite. (see
  [[anthropic-building-multi-agent-systems]])
- **Many narrow reviewers, and no self-approval.** Anthropic's CI runs several
  reviewer agents on every PR, each scoped to one concern, instead of one
  mega-prompt. The stated reasons: they do not share blind spots, one can catch
  another's compromise or mistake, and effort is not spread thin. Each finding
  needs a written proof. (see [[anthropic-securing-ai-native-sdlc]]) The authoring
  agent cannot approve its own PR (separation of duties). (see
  [[anthropic-ai-native-sdlc-playbook]])
- **Identity at agent-to-agent boundaries.** When work is split across agents,
  each agent needs its own ID and its own credentials; shared credentials defeat
  the split. Before an agent accepts a delegated task, it verifies the delegating
  agent's identity and authorization. Each step is authorized again, and every
  inter-agent message is logged. (see [[anthropic-zero-trust-for-ai-agents]])
  Anthropic's Deputy CISO reports that a model swap alone, in an incident-response
  agent, produced new agent-to-agent behavior: the agent asked a code-writing
  Claude instance over Slack for a fix, which still went through human PR review.
  The lesson drawn: draw boundaries around access and actions, including access to
  other agents, not around what the current model is believed to do. (see
  [[anthropic-ciso-guide-agentic-ai]], [[guardrails]])
- **Quarantine untrusted input.** Read-only reader agents summarize untrusted
  content into structured output; a separate privileged actor acts only on the
  summaries. (see [[anthropic-harness-for-every-task]])
- **Some powers stay with the main agent.** In OpenAI's Agents API only the main
  agent may request browser sign-in; subagents cannot. (see
  [[openai-agents-api-guide]])

## Harness signals for parallel work

Two current Anthropic harness patterns change how a lead agent paces subagents.
Both are model-scoped; the source pages hold the details.
- **Elapsed-time budget.** A line on each message stating elapsed time against an
  advisory budget let a lead agent pace and parallelize, and teams finished sooner
  at comparable quality. Keep a hard timeout as well. (see
  [[anthropic-prompting-claude-opus-5-5]]) Contrast the warning against showing a
  remaining-*token* countdown, recorded on [[prompt-tuning-axes]].
- **Non-blocking subagent start.** A subagent-start tool that returns at once,
  plus a separate wait tool, lowered average time to completion at similar
  quality, tokens, and cost. (see [[anthropic-prompting-claude-fable-5-1]])
- An unattended lead agent must wait for background subagents before it treats a
  task as complete. (see [[anthropic-prompting-claude-opus-5-5]])

## Evidence from Anthropic's multi-agent research system

[[anthropic-eng-multi-agent-research-system]] quantifies the tradeoff:
- A lead-agent + parallel-subagent system **beat single-agent Opus 4 by 90.2%**
  on breadth-first research; parallelism (3–5 subagents, 3+ parallel tool calls
  each) cut research time up to 90%. The baseline is the same subagents spawned
  serially, not a single agent (see Contradictions / open questions).
- But **token usage alone explains ~80% of performance variance** — the gain
  comes from spreading work across separate context windows
  ([[context-engineering]]), not orchestration complexity itself.
- It's expensive (~15× chat tokens) and **fails when context must be shared**
  (e.g. most coding), so it isn't a default — consistent with single-agent-first
  and [[agents-vs-workflows]].
- Prompt the orchestrator with **effort-scaling rules** (agent count by query
  complexity) and **explicit delegation** (objective, output format, boundaries).

## Decomposition and coordination

**Decompose by context, not by role.** [[anthropic-building-multi-agent-systems]]
makes context-centric decomposition its main design rule. A problem-centric split
divides work by type (feature writer, test writer, reviewer). It loses context at
each handoff, and the agents play a "telephone game". A context-centric split
follows context boundaries. Good boundaries: independent research paths,
components with a clean API contract, and blackbox verification. Bad boundaries:
sequential phases of one piece of work, tightly coupled components, and shared
state. The same guide accepts only three reasons to go multi-agent: context
protection, parallelizable work, and specialization.

**Partition, then fan out.** A first pass partitions the search space, parallel
agents search each partition, and a final system-level pass uses their findings.
Adding agents without partitions gave mostly duplicates. (see
[[anthropic-llms-secure-source-code]]) The cloud-sessions advice below, to split
along file boundaries, is the same principle. Fan-out units in the sources:
- One executor subagent per source of truth (Grafana, logs, PagerDuty, GitHub,
  Kubernetes, Slack), merged by the orchestrator into one situation report. (see
  [[anthropic-ai-ci-cd-on-call]])
- Parallel query sub-agents in security alert triage, with a synthesized
  summary. (see [[anthropic-cybersecurity-triage-agents]])
- One subagent per spreadsheet sheet, reported by Shortcut. (see
  [[claude-customer-shortcut]])
- Several frontier models planning in parallel, with Claude reconciling the
  plans, reported by Genspark. (see [[claude-customer-genspark]])
- A memory sub-agent that retrieves team standards and learned codebase quirks,
  reported by Greptile. (see [[claude-customer-greptile]], [[agent-memory]])
- One clean-context agent per eval run, so that runs do not contaminate each
  other. (see [[anthropic-improving-skill-creator]])
- Best-of-N: several candidates in parallel, then pick one or combine parts.
  (see [[openai-how-openai-uses-codex]])

**Coding swarms.** Cursor's SQLite experiment shows that shared-context coding is not categorically
incompatible with multi-agent work, but the harness must carry coordination that
ordinary Git workflows leave to humans. Its new swarm assigned shared design
decisions to planners, delegated disjoint leaves, reconciled decision documents,
used neutral conflict resolution, decomposed contested megafiles, and stacked
independent review lenses. The authors attribute scaling primarily to context
efficiency rather than parallelism. (see
[[cursor-agent-swarm-model-economics]], [[multi-agent-economics]])

Isolation has the opposite cost. In Claude Code cloud sessions each task gets its
own VM and branch, so parallel sessions cannot see each other's fixes: one session
found the same bug a sibling session was fixing. The advice is to split parallel
tasks along file boundaries, merge in a sensible order, and expect duplicate
problem reports. (see [[anthropic-claude-code-in-the-cloud]])

- **Sixteen agents with no orchestrator.** A C compiler that builds the Linux
  kernel was written by 16 parallel agents of one model, coordinating only
  through git and lock files in a shared task directory (an agent claims a
  task by writing a file; git rejects a duplicate claim). This worked while
  failures were independent. All agents then stalled on the single kernel-build
  task, until a known-good reference compiler (GCC) let them split it into
  independent parts. The finding supports this page's view that the limit is
  how well the task decomposes, and it is a replication on an ordinary git
  repository. (see [[anthropic-eng-building-c-compiler]])
- **Writer and reviewer in separate contexts.** One instance writes and a
  second, fresh instance reviews; this often beats one instance doing both.
  (see [[anthropic-eng-claude-code-best-practices]],
  [[anthropic-subagents-in-claude-code]], [[anthropic-getting-started-with-loops]])
  Verifier isolation is covered under the subagent boundary above.
- **More searchers, more shortcuts.** On BrowseComp, multi-agent runs found
  unintended solutions 3.7 times as often as single-agent runs (0.87% vs.
  0.24%). Anthropic attributes this to more tokens and more parallel
  searchers, not to a change in the model's tendency. (see [[anthropic-eng-eval-awareness-browsecomp]])

## Parallel sessions and human-agent teams

The number of parallel agent sessions is limited by how much work one person can
review, not by how many agents can run. Some teams delegate whole tickets to
agents instead of supervising sessions, and some teams give every human and
agent a written role in one roster. These topics are on [[human-agent-teams]].

## Declarative vs. code-first

OpenAI contrasts **declarative graph** frameworks (define every branch/loop
upfront) with the [[openai-agents-sdk]]'s **code-first** approach (express logic
with normal programming constructs). Echoes Anthropic's caution about framework
abstraction in [[agent-design-principles]].

## Related concepts

- [[workflow-patterns]], [[agent-core-components]], [[tool-design]],
  [[agent-design-principles]], [[guardrails]], [[agent-harness]],
  [[context-engineering]], [[prompt-tuning-axes]], [[multi-agent-economics]],
  [[agent-skills]], [[agent-memory]], [[agents-vs-workflows]],
  [[human-agent-teams]]

## Key entities

- [[openai]], [[openai-agents-sdk]], [[anthropic]], [[claude-code]],
  [[claude-managed-agents]]

## Appears in

- [[openai-practical-guide-to-building-agents]]
- [[anthropic-building-effective-agents]]
- [[anthropic-steering-claude-code]]
- [[anthropic-evolution-of-agentic-surfaces]]
- [[anthropic-eng-context-engineering]]
- [[anthropic-eng-effective-harnesses-long-running-agents]]
- [[anthropic-eng-multi-agent-research-system]]
- [[cursor-agent-swarm-model-economics]]
- [[anthropic-seeing-like-an-agent]]
- [[anthropic-prompt-caching-is-everything]]
- [[anthropic-harness-for-every-task]]
- [[anthropic-eng-how-we-contain-claude]]
- [[anthropic-eng-claude-code-auto-mode]]
- [[anthropic-getting-most-out-of-opus-5-5]]
- [[anthropic-claude-code-in-the-cloud]]
- [[anthropic-prompting-claude-opus-5-5]]
- [[anthropic-prompting-claude-fable-5-1]]
- [[openai-agents-api-guide]]
- [[openai-prompting-gpt-6-astra]]
- [[anthropic-eng-building-c-compiler]]
- [[anthropic-eng-claude-code-best-practices]]
- [[anthropic-eng-eval-awareness-browsecomp]]
- [[anthropic-multi-agent-coordination-patterns]]
- [[anthropic-building-multi-agent-systems]]
- [[anthropic-subagents-in-claude-code]]
- [[anthropic-advisor-strategy]]
- [[anthropic-choosing-claude-model]]
- [[anthropic-what-a-task-costs-opus-5-5]]
- [[anthropic-coderabbit-agent-orchestration]]
- [[anthropic-block-orchestrates-fable]]
- [[anthropic-anatomy-of-commerce-agents]]
- [[anthropic-claude-code-session-cost]]
- [[anthropic-claude-code-session-management]]
- [[anthropic-claude-code-large-codebases]]
- [[anthropic-unreasonable-effectiveness-of-html]]
- [[anthropic-llms-secure-source-code]]
- [[anthropic-securing-ai-native-sdlc]]
- [[anthropic-ai-native-sdlc-playbook]]
- [[anthropic-zero-trust-for-ai-agents]]
- [[anthropic-ciso-guide-agentic-ai]]
- [[anthropic-ai-ci-cd-on-call]]
- [[anthropic-cybersecurity-triage-agents]]
- [[anthropic-improving-skill-creator]]
- [[anthropic-getting-started-with-loops]]
- [[claude-customer-shortcut]]
- [[claude-customer-caylent]]
- [[claude-customer-genspark]]
- [[claude-customer-greptile]]
- [[claude-customer-rocket-money]]
- [[openai-sora-android-with-codex]]
- [[openai-how-openai-uses-codex]]
- [[anthropic-prompting-claude-fable-5]]
- [[anthropic-prompting-claude-sonnet-5-5]]

## Contradictions / open questions

- [[anthropic-eng-multi-agent-research-system]] reports that multi-agent systems
  are a poor fit when agents must share context, including most coding.
  [[cursor-agent-swarm-model-economics]] demonstrates a counterexample at extreme
  scale using a custom VCS and explicit coordination mechanisms. The practical
  boundary appears to be harness capability and task partitionability, not a
  categorical research-versus-coding distinction; replication on ordinary Git
  repositories remains open.
- **Separate verifier agents: architecture pattern vs model default.**
  [[anthropic-harness-for-every-task]] (written when Claude Opus 4.8 was current)
  builds adversarial verification from separate agents, and the legacy
  [[anthropic-prompting-claude-fable-5]] page recommended fresh-context verifier
  subagents. [[anthropic-prompting-claude-sonnet-5-5]] (2026-10-12) says not to let
  the model launch reviewer subagents unless asked, because they raised cost with
  no quality change. The two may not conflict — one is a harness the developer
  designs, the other is the model's unprompted habit — but no source tests when a
  separate verifier still pays for itself on current models. See
  [[prompt-tuning-axes]]. Newer architecture sources weigh on the harness side:
  the multi-agent guide (2026-01-23) recommends a verification subagent across
  domains ([[anthropic-building-multi-agent-systems]]); the source-code security
  guide (2026-05-27) reports that an isolated adversarial verifier roughly halved
  non-exploitable findings ([[anthropic-llms-secure-source-code]], partner-reported);
  and Anthropic's CI uses several narrow reviewer agents
  ([[anthropic-securing-ai-native-sdlc]], 2026-07-21). None of them measures the
  cost of the verifier against a single agent on a current model.
- **Does parallelism buy speed?** The research-system post (2025) reports that
  parallel subagents cut research time up to 90%
  ([[anthropic-eng-multi-agent-research-system]]). The multi-agent guide
  (2026-01-23) says that parallelism buys thoroughness, not speed, and that a
  multi-agent run often takes longer overall than a single agent
  ([[anthropic-building-multi-agent-systems]]). The baselines differ: the 90%
  figure compares 3–5 subagents spawned at once with the same subagents spawned
  serially; the guide compares a multi-agent system with one agent, and it agrees
  that parallelism cuts time against sequential work. So the two claims are
  compatible. No source measures wall-clock time for multi-agent against
  single-agent on the same research task.
- **Multi-agent gains on BrowseComp carry a contamination caveat.** The 2025
  research-system post reports multi-agent gains on BrowseComp
  ([[anthropic-eng-multi-agent-research-system]]). The Mar 2026 eval-awareness
  post finds that multi-agent runs on the same benchmark had 3.7 times the rate
  of unintended solutions ([[anthropic-eng-eval-awareness-browsecomp]]). This qualifies, not reverses, the gain.
