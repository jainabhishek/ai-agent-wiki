---
title: Tool Design
type: concept
created: 2026-06-21
updated: 2026-10-12
tags: [tools, aci, best-practices, agents]
---

# Tool Design

> Both guides treat tools as the highest-leverage surface to get right. Anthropic
> calls it the **Agent-Computer Interface (ACI)** and gives it equal weight to
> the human-computer interface; OpenAI emphasizes standardized, well-documented,
> testable tools and warns against tool *overlap*.

## Tool types (OpenAI)

| Type | Purpose | Examples |
|------|---------|----------|
| **Data** | Retrieve context | Query a CRM/DB, read PDFs, web search |
| **Action** | Take actions in systems | Send email, update a record, hand off a ticket |
| **Orchestration** | Other agents used as tools | Refund agent, research agent (see [[agent-orchestration]]) |

Each tool should have a **standardized definition**, enabling many-to-many
relationships between tools and agents. Well-documented, tested, reusable tools
improve discoverability, simplify versioning, and prevent redundant definitions.
(see [[openai-practical-guide-to-building-agents]])

## ACI best practices (Anthropic)

- Give the model **enough tokens to think** before it commits to output.
- Keep formats close to **text seen naturally on the internet**.
- Avoid **formatting overhead** (line counting, heavy escaping).
- Write tool descriptions as if for a new engineer: **example usage, edge cases,
  input formats, clear boundaries.** (Later Anthropic guidance disagrees on
  example usage — see Contradictions below.)
- Apply **poka-yoke** (mistake-proofing) — shape arguments so misuse is hard.
- **Test extensively** and iterate on definitions in a workbench.
(see [[anthropic-building-effective-agents]])

## Clarity over count

OpenAI's key finding: the problem isn't the *number* of tools but their
**similarity/overlap**. Some teams handle 15+ distinct, well-defined tools; others
struggle with fewer than 10 overlapping ones. Improve names, parameters, and
descriptions first; only split into multiple agents if clarity doesn't help. (see
[[openai-practical-guide-to-building-agents]], [[agent-orchestration]])

Anthropic's [[claude-code]] team states the cost side: each new tool is one more
choice for the model, so Claude Code keeps about 20 tools and a high bar for
adding more. It adds capability without new tools through progressive disclosure
in [[agent-skills]] or a docs-search subagent that returns only the answer (see
[[anthropic-seeing-like-an-agent]]). Near-duplicate tools (`create_ticket` vs
`create_incident`) are one of the cases Anthropic lists for worked input examples
(see [[anthropic-eng-advanced-tool-use]]).

## Use what the model already knows

A complementary Anthropic principle: prefer **general-purpose tools the model is
already good at** (bash, a text editor) over bespoke interfaces — they keep
improving as the model improves. "Claude 3.5 Sonnet reached 49% on SWE-bench
Verified with only a bash tool and a text editor tool." Higher-level capabilities
(programmatic tool calling, [[agent-skills]], memory) compose from these
foundations. Add **declarative/dedicated tools strategically** — for
security-sensitive actions, UX presentation, or observability — and re-evaluate
their necessity as the model advances. (see [[harnessing-claudes-intelligence]],
[[agent-harness]])

- **Retire tools as models improve.** Claude Code's TodoWrite list plus periodic
  reminders helped early models but constrained later ones; a task tool with
  dependencies shared across subagents replaced it. Old tools can limit new
  models (see [[anthropic-seeing-like-an-agent]]). Same direction as removing
  harness components one at a time in [[agent-harness]].
- **Let the agent search instead of pre-retrieving.** Claude Code replaced a
  pre-indexed RAG vector store with a Grep tool so the model builds its own
  context (see [[anthropic-seeing-like-an-agent]]). An OpenAI Responses API
  builder (Collxn) found built-in web search plus 16 custom tools less complex
  than a full RAG system (see [[openai-one-year-of-responses]]). See
  [[context-engineering]].
- **Structured tool over format instructions for UI-parsed output.** A prompt that
  specified a markdown question format was unreliable; a dedicated blocking
  question tool with structured options gave guaranteed options and composed
  with the SDK and skills (see [[anthropic-seeing-like-an-agent]]). This is the
  "UX presentation" case for a dedicated tool.
- **Modes as tools, not tool-set swaps.** Tool definitions sit in the
  prompt-cache prefix, so Claude Code never adds or removes tools mid-session.
  Plan mode is itself a pair of enter/exit tools, so the model can enter it
  autonomously without breaking the cache (see
  [[anthropic-prompt-caching-is-everything]]).

## Scaling to large tool libraries

Anthropic's [[model-context-protocol]] work reports that a five-server MCP setup
already costs ~55K tokens of definitions. Its advice is to choose the technique
by bottleneck, not to enable everything (see [[anthropic-eng-advanced-tool-use]],
Nov 2025):

| Bottleneck | Technique | Use when |
|------------|-----------|----------|
| Definition bloat | **Tool search with deferred loading** | 10+ tools, >~10K definition tokens, several MCP servers, selection errors |
| Intermediate-result bloat | **Programmatic tool calling** | 3+ dependent calls, large data where only aggregates matter, parallel fan-out |
| Parameter errors | **Worked input examples** | nested structures, many optional params, domain conventions, near-duplicate tools |

- **Tool search / deferred loading.** Deferred tools stay out of the initial
  context; the model searches and only matching definitions load. Keep the 3–5
  most-used tools always loaded. Names and descriptions become search keys, so
  make them search-friendly (`search_customer_orders`, not `query_db_orders`).
  Reported ~85% fewer definition tokens with prompt caching preserved (see
  [[anthropic-eng-advanced-tool-use]]). Claude Code defers MCP schemas as
  name-only stubs in fixed order and loads full schemas on selection — **defer,
  don't remove**, to keep the cache prefix stable (see
  [[anthropic-prompt-caching-is-everything]],
  [[anthropic-new-rules-context-engineering-claude-5]]). See
  [[context-engineering]].
- **Programmatic tool calling.** The model writes code that calls tools, filters
  results, and returns only the final output to context. Not for tasks where the
  model must reason over every intermediate result. Document return formats
  precisely, and expose to model-written code only parallel-safe / idempotent
  tools (see [[anthropic-eng-advanced-tool-use]]).
- **Tools as code files.** The design basis: present each MCP server as a
  directory of generated code wrappers inside a code-execution sandbox. The agent
  discovers tools by browsing files or a search tool with a detail-level option,
  then writes a script that moves data between tools without it entering
  context — one task ~150K → ~2K tokens. The execution layer can tokenize PII
  before the model sees it. Saved working functions plus a `SKILL.md` become
  [[agent-skills]]. Trade-off: agent-written code needs a sandbox, resource
  limits, and monitoring (see [[anthropic-eng-code-execution-with-mcp]],
  [[guardrails]]). Cloudflare's "Code Mode" reported a similar result
  independently.

## Tool reach and placement

- **Private MCP connectivity.** [[openai]]'s Secure MCP Tunnel lets hosted
  products reach [[model-context-protocol]] servers inside enterprise networks
  through an outbound-only, customer-run client that forwards only to an
  explicitly configured local server. OpenAI rejected public endpoints,
  third-party tunnels, and VPN/peering as too broad (see
  [[openai-private-mcp-servers]], [[guardrails]]).
- **Browser-side tools.** Runme, a static client-side app, registers tools in
  the browser through WebMCP instead of running an MCP server, which would add
  infrastructure and change where notebook data is handled (see
  [[openai-automating-repetitive-work-codex]]).
- **One tool interface for every "hand".** Anthropic's Managed Agents harness
  calls every sandbox or tool through one `execute(name, input) → string`
  interface; a dead container surfaces as a tool error the model can handle (see
  [[anthropic-eng-scaling-managed-agents]]).
- **Host owns the tool surface.** In OpenAI's Codex platform the host application,
  not the harness, decides which context and tools (including app-owned MCP
  servers) are exposed and which actions need approval (see
  [[openai-codex-as-a-platform]]).

## Tool output and safety

- **Trusted tool output is still an injection channel.** Remote tools can change
  after approval, so output from trusted tools needs live inspection; a small fast
  classifier can do it (see [[anthropic-eng-how-we-contain-claude]],
  [[guardrails]]).
- **Approval tools work only if called.** In OpenAI's Agents API a confirmation
  function tool helps only when the agent calls it, and clarifying-question tool
  results are visible to the model, so they must never carry credentials (see
  [[openai-agents-api-guide]]).
- **Tolerate near-miss tool names in the harness.** For one current model,
  Anthropic recommends accepting case-only name mismatches or returning an error
  that names the exact tool (see [[anthropic-prompting-claude-sonnet-5-5]];
  model-scoped).

## Anthropic engineering specifics

From [[anthropic-eng-writing-tools-for-agents]] (the primary-source deep dive):
- **Choose the right tools** — "more tools don't always lead to better outcomes."
  Prefer `search_contacts` over `list_contacts`; consolidate operations (a
  `schedule_event` that finds availability *and* books).
- **Namespace** related tools by common prefix (`asana_search`, `jira_search`);
  prefix vs suffix has measurable eval effects.
- **Return meaningful context** — semantic over technical (`name` not `uuid`); add
  a `response_format` parameter (`concise`/`detailed`).
- **Token efficiency** — pagination, filtering, truncation with helpful messages;
  actionable errors over opaque codes.
- **Human clarity test** (also in [[anthropic-eng-context-engineering]]): "if a
  human engineer can't definitively say which tool should be used, an AI agent
  can't be expected to do better."
- **Evaluate with the agent in the loop** — realistic multi-call tasks; paste
  transcripts into the model to auto-optimize tools. See [[agent-evals]].
- **Guidance lives once, in the description.** Tool-usage guidance belongs only
  in the tool description, not repeated across the system prompt and other
  layers; conflicting layers cost the model reasoning (see
  [[anthropic-new-rules-context-engineering-claude-5]]).
- **Script the deterministic parts.** If the model keeps rediscovering the same
  shell recipe, make it a tiny script with deterministic output that fails
  loudly (OpenAI, see [[openai-skills-for-oss-maintenance]]).

## Why it matters

Most agent failures trace back to ambiguous tools or instructions, not model
capability. Investing here pays off before any orchestration complexity. See
[[agent-design-principles]].

## Related concepts

- [[agent-core-components]], [[agent-instructions]], [[agent-orchestration]],
  [[agent-skills]], [[agent-harness]], [[agent-evals]], [[context-engineering]],
  [[model-context-protocol]], [[guardrails]]

## Key entities

- [[anthropic]], [[openai]], [[claude]], [[claude-code]]

## Appears in

- [[anthropic-building-effective-agents]]
- [[openai-practical-guide-to-building-agents]]
- [[harnessing-claudes-intelligence]]
- [[anthropic-eng-writing-tools-for-agents]]
- [[anthropic-eng-context-engineering]]
- [[anthropic-eng-advanced-tool-use]]
- [[anthropic-eng-code-execution-with-mcp]]
- [[anthropic-new-rules-context-engineering-claude-5]]
- [[anthropic-seeing-like-an-agent]]
- [[anthropic-prompt-caching-is-everything]]
- [[anthropic-eng-how-we-contain-claude]]
- [[anthropic-eng-scaling-managed-agents]]
- [[anthropic-prompting-claude-sonnet-5-5]]
- [[openai-one-year-of-responses]]
- [[openai-private-mcp-servers]]
- [[openai-automating-repetitive-work-codex]]
- [[openai-codex-as-a-platform]]
- [[openai-agents-api-guide]]
- [[openai-skills-for-oss-maintenance]]

## Contradictions / open questions

- **Worked examples in tool definitions (Anthropic, appears generation-dependent).**
  Three Anthropic sources disagree:
  1. Dec 2024: tool descriptions should include example usage
     ([[anthropic-building-effective-agents]]).
  2. Nov 2025: worked input examples in the tool definition raised accuracy on
     complex parameters from 72% to 90%
     ([[anthropic-eng-advanced-tool-use]]).
  3. Jul 2026: for Claude 5-generation models, usage examples narrow the model's
     exploration; make parameters expressive instead (Claude Code's TodoWrite
     description shrank from ~9,100 characters to one line plus a status enum)
     ([[anthropic-new-rules-context-engineering-claude-5]]).
  The later post does not retract the earlier measurements; it scopes its advice
  to newer models. Read as model-generation dependent; re-test per model before
  adding or removing examples.
- OpenAI on tool taxonomy and Anthropic on interface craft remain complementary.
