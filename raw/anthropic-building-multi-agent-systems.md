# Building multi-agent systems: When and how to use them — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/building-multi-agent-systems-when-and-how-to-use-them
> Publisher: Anthropic (claude.com articles) · Date: 2026-01-23
> Captured: 2026-10-12 via curl (condensed).

Category: Best practices. Products: Claude Platform, Claude Code. Reading time
17 min. Written by Cara Phillips, with Paul Chen, Andy Schumeister, Brad Abrams,
and Theo Chu. First post in a series; the next post covers other coordination
patterns. Code examples use `claude-sonnet-4-5`.

## What is a multi-agent system?

- Definition: multiple LLM instances with separate conversation contexts,
  coordinated through code. Each handles a slice of the task. Benefits: context
  protection, parallel work, specialization.
- Other patterns exist (agent swarms, capability-based systems, message-bus
  architectures). This post covers only **orchestrator-subagent**: a lead agent
  spawns and manages specialized subagents. Recommended starting point.
- Anthropic observes multi-agent systems are often used where a single agent
  would do better; teams spent months on elaborate architectures, then matched
  the result with better prompting of one agent.
- Three situations where multiple agents consistently win: context pollution,
  parallelizable tasks, and specialization (tool selection or task focus).
  Elsewhere, coordination cost usually exceeds benefit.

## The case for starting with a single agent

- A single agent with good tools does more than most developers expect.
- Each added agent is another failure point, another prompt to maintain, another
  source of surprises.
- Failure seen: separate planning/execution/review/iteration agents lost context
  at each hand-off and spent more tokens coordinating than executing.
- In Anthropic's testing, multi-agent implementations typically use **3–10x more
  tokens** than single-agent ones for equivalent tasks. Sources: duplicated
  context, coordination messages, and hand-off summaries.

## A decision framework for multi-agent systems

Reserve multi-agent for constraints one agent cannot overcome. Managed
infrastructure can handle orchestration (multiagent orchestration in Claude
Managed Agents).

### Context protection

- Quality can degrade as context grows. Context pollution = information from one
  subtask that is irrelevant to later subtasks. Subagents give each subtask a
  clean context.
- Example: support agent that looks up order history while diagnosing a
  technical issue. Single-agent version: a tool result adds 2,000+ tokens of
  order history that stays in context during diagnosis.
- Multi-agent version: an `OrderLookupAgent` (own `messages`, `max_tokens=1024`,
  `get_order_details_tool`) returns a summary; the `SupportAgent` injects a
  one-line context string (status, date) and calls the model with
  `max_tokens=2048`. Main agent receives 50–100 tokens instead of the full
  history.
- Use isolation when: the subtask generates high volume (>1,000 tokens) mostly
  irrelevant to the main task; the subtask is well defined with clear extraction
  criteria; or it is a lookup/retrieval that needs filtering before use.

### Parallelization

- Parallel agents explore a larger search space; most valuable for search and
  research. References Anthropic's multi-agent research system: lead agent
  decomposes, subagents search facets in parallel, return distilled findings.
- Code shape: `AsyncAnthropic`; `lead_agent.decompose_query(query)` → list of
  facets → `asyncio.gather` over `research_subagent(facet)` (each with its own
  context, `max_tokens=4096`, tools `web_search`, `read_document`) →
  `lead_agent.synthesize(results)`.
- Cost: again 3–10x tokens. Parallelism cuts time vs running the same work
  sequentially, but multi-agent systems **often take longer overall** than a
  single-agent system because total computation rises.
- The main benefit is **thoroughness, not speed**.

### Specialization

Focused toolsets, prompts, or domain context per agent can improve reliability.

#### Tool set specialization

Three signals that tool specialization would help:
- Quantity: an agent with too many tools (often 20+) picks the wrong one.
- Domain confusion: tools span unrelated domains (database, API, filesystem).
- Degraded performance: adding tools hurts performance on existing tasks.

#### System prompt specialization

Conflicting personas or constraints (empathetic support vs critical code review;
rigid compliance vs creative brainstorming) are better split into agents with
their own system prompts. Each subagent prompt needs the same prompt-engineering
care as a single agent's.

#### Domain expertise specialization

Deep domain context (case law, clinical-trial methodology) can overwhelm a
generalist; specialized agents carry only their domain.

Example: integration across CRM, marketing automation, and messaging, each with
10–15 relevant endpoints. One agent with 40+ tools confuses similar operations.
Split into `CRMAgent` and `MarketingAgent` (each a focused system prompt and
8–10 tools) under an `OrchestratorAgent` whose only tools are
`delegate_to_crm`, `delegate_to_marketing`, `delegate_to_messaging`, with routing
rules in its system prompt. Cost: routing complexity (misrouting gives poor
results) and more prompts to maintain. Works best when domains are clearly
separable and routing is unambiguous.

## Outgrowing single-agent architectures

Concrete signals:
- **Approaching context limits** with degrading performance. Compaction is
  reducing this limit for single agents.
- **Managing many tools** (15–20+). First try the Tool Search Tool (on-demand
  tool discovery), which can cut token use by up to 85% and improve selection
  accuracy.
- **Parallelizable subtasks** (multi-source research, tests for many components).

These thresholds will shift as models improve; they are guidelines, not limits.

## Context-centric decomposition

- The most important design decision is how to divide work. Teams often get it
  wrong.
- **Problem-centric** (by work type: feature writer, test writer, reviewer) is
  often counterproductive. Each hand-off loses context; the tester does not know
  why decisions were made. Agents play a "telephone game" that degrades fidelity.
  In one experiment with planner/implementer/tester/reviewer agents, subagents
  spent more tokens on coordination than on work.
- **Context-centric** (by context boundary) usually works: the agent that builds
  a feature also writes its tests. Split only when context truly isolates.
- Good boundaries: independent research paths (Asia vs Europe market trends);
  separate components with a clean API contract (frontend vs backend); blackbox
  verification (a verifier that only runs tests).
- Bad boundaries: sequential phases of the same work (plan, implement, test one
  feature); tightly coupled components; work that needs shared state.

## The verification subagent pattern

- A dedicated agent whose only job is to test or validate the main agent's work;
  works across domains.
- More capable orchestrators (Claude Opus 4.5 named) can increasingly evaluate
  subagent work directly. Verifiers remain useful with less capable
  orchestrators, when verification needs special tools, or to enforce explicit
  checkpoints.
- Works because verification needs little context transfer; it avoids the
  telephone game.

### Implementating a multi-agent system (heading as published)

- Main agent finishes a unit of work, then spawns a verifier with the artifact,
  clear success criteria, and verification tools. The verifier need not know why
  the artifact was built that way.
- Code shape: `CodingAgent.implement_feature` (tools `read_file`, `write_file`,
  `list_directory`) returns code and `files_changed`. `VerificationAgent`
  (tools `run_tests`, `execute_code`, `read_file`) gets requirements and changed
  files, is told to run the full suite (`pytest --verbose`) and pass only if all
  tests pass. `implement_with_verification(requirements, max_attempts=3)` loops:
  on failure it appends the verifier's issues to the requirements; after 3
  failures it raises.

### Multi-agent system applications

Verifiers suit: quality assurance (tests, lint, schema validation); compliance
checking; output validation against specs; factual verification of claims and
citations.

### The early victory problem

Main failure mode: the verifier runs one or two tests, sees them pass, declares
success. Mitigations:
- Concrete criteria ("run the full test suite and report all failures", not
  "make sure it works").
- Comprehensive checks across scenarios and edge cases.
- Negative tests: inputs that should fail, confirmed to fail.
- Explicit instructions such as "You MUST run the complete test suite before
  marking as passed." Without them, verifiers take shortcuts.

## Choosing between single-agent and multi-agent systems

Before adding agents, confirm: (1) a genuine constraint exists (context limits,
parallelism, specialization); (2) decomposition follows context, not problem
type; (3) clear verification points exist that do not need full context. Start
with the simplest approach; add complexity only when evidence supports it.

Further reading named: Building effective agents; Effective context engineering
for AI agents; How we built our multi-agent research system.

## Acknowledgements

Cara Phillips (author); contributors Paul Chen, Andy Schumeister, Brad Abrams,
Theo Chu.
