---
title: Tool Design
type: concept
created: 2026-06-21
updated: 2026-10-13
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

- **When tool count justifies specialist agents.** Anthropic's multi-agent guide
  names tool count (often 20+), tools that span unrelated domains, and new tools
  that degrade old tasks as signals for specialization. It advises trying
  on-demand tool discovery first. Its split of 40+ tools into specialists of
  8–10 tools is an illustrative example, not a measurement (see
  [[anthropic-building-multi-agent-systems]]).
- **Fewer, non-overlapping tools in practice.** OpenAI reports that fewer,
  non-overlapping tools made its in-house data agent more reliable (see
  [[openai-in-house-data-agent]]). Caylent reports that each stage agent in its
  migration pipeline gets only the tools that its stage needs (see
  [[claude-customer-caylent]]).

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
  [[context-engineering]]. For symbol navigation in large multi-language
  codebases, Anthropic calls LSP integration one of the highest-value
  investments, because grep returns thousands of hits and same-named symbols
  (see [[anthropic-claude-code-large-codebases]]). The two complement each
  other: search builds context, and LSP resolves symbols.
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

- **The "think" tool, absorbed by the model.** In Mar 2025 Anthropic proposed a
  no-op `think` tool that gave the model a scratchpad between tool calls, with
  gains on policy-heavy, sequential tool use (measured on Claude 3.7 Sonnet). A
  Dec 2025 banner on the post recommends built-in extended thinking instead in
  most cases; interleaved and adaptive thinking now reason between tool calls
  without a tool. This is a worked example of retiring a tool once the model
  does the job itself. (see [[anthropic-eng-think-tool]])
- **Revisit loop limits as well as tools.** Dust reports that its old defaults
  (three tool calls per run, maximum eight) truncated results once models could
  chain more steps, so it redesigned the loop to allow up to 24 calls. The same
  page also says tool-call depth rose "with no engineering changes", so the
  attribution is unclear (see [[claude-customer-dust]], [[agent-harness]]).

### Tool calls versus one-shot output, and recovery

- **Discrete tool calls for a rare, strict format.** n8n reports that one-shot
  generation of a whole workflow JSON failed, because the model had to hold the
  schema, every node definition, and all connections at once. Discrete calls
  (add node, connect, configure) worked. n8n lists code generation as its next
  experiment (see [[claude-customer-n8n]]).
- **A tool loop needs correct stopping and error recovery.** Genspark reports
  that a model-driven loop over 150+ tools failed for two years through
  infinite loops and repeated errors. It worked once a model generation (early
  2025) stopped correctly and tried an alternative after a tool error (see
  [[claude-customer-genspark]], [[agent-design-principles]]).
- **Invest in domain tools, and let the agent ask for more.** Greptile reports
  that a small team used a vendor SDK for the loop and put its effort into
  specialized review tools (see [[claude-customer-greptile]]). Outtake reports a
  loop in which the agent reports missing tools, a separate coding agent writes
  each tool and a test scenario, and a human judges only the outcome (see
  [[anthropic-outtake-cyber-investigator]]). Anthropic's security-review post
  advises letting the model ask for or build its own tools (see
  [[anthropic-llms-secure-source-code]]).

## Deterministic tools for exact work

The model interprets and plans; deterministic code does retrieval, arithmetic,
and strict validation.

- **Guidance.** Anthropic's skills guide says to bundle a script for critical
  validations, because "Code is deterministic; language interpretation isn't"
  (see [[anthropic-complete-guide-building-skills]]). Scripts in a skill act as
  tools that need not sit in context; Claude kept rewriting a slide-styling
  script, so it was saved as `apply_template.py` (see
  [[anthropic-building-agents-with-skills]]). Scaffold and bundle scripts in a
  frontend skill cut tokens and raised reliability (see
  [[anthropic-improving-frontend-design-through-skills]]). See also "Script the
  deterministic parts" below and [[agent-skills]].
- **Kepler (case study).** Kepler reports that Claude decomposes the analyst's
  question, while a query engine retrieves and a formula engine computes. No
  number is model-generated, and each figure links to a filing line item (see
  [[anthropic-kepler-verifiable-ai]]).
- **Caylent (case study).** Caylent reports splitting work so that scripts do
  the exact tasks and Claude does reasoning and language (see
  [[claude-customer-caylent]]).
- **Datadog (case study).** Datadog reports that each Temper capability has a
  machine-parseable data contract that an agent can discover without docs, next
  to behavior and authorization contracts (see
  [[anthropic-datadog-universal-machine-tool]], [[boundary-contracts]]).

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
  [[context-engineering]]. Anthropic's multi-agent guide says to try tool search
  before splitting work into specialist agents (see
  [[anthropic-building-multi-agent-systems]]). Vapi reports that its Composer
  agent loads only the tools relevant to the current turn from a catalog of
  100+ tools (see [[claude-customer-vapi]]).
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
  independently. Anthropic's MCP production post recommends the same shape for
  large server surfaces: a thin tool that accepts a script run in a server-side
  sandbox. Its example is Cloudflare's server, where two tools (`search`,
  `execute`) cover ~2,500 endpoints in ~1K tokens (see
  [[anthropic-agents-production-systems-mcp]]).

## Tool reach and placement

Where a tool runs and who owns it now has its own page: [[tool-placement]]. It
covers hosted versus client-side tools, API or connector before computer use,
IDE and browser-side tools, and private MCP reach. It also covers the host
application that owns the tool surface and approvals, and output caps on tool
results.

## Tool output and safety

- **Trusted tool output is still an injection channel.** Remote tools can change
  after approval, so output from trusted tools needs live inspection; a small fast
  classifier can do it (see [[anthropic-eng-how-we-contain-claude]],
  [[guardrails]]).
- **Least agency.** Anthropic's Zero Trust eBook extends least privilege to what
  each tool can do, how often, and where: for example, a read-only database
  tool, or an email summarizer with no send or delete rights (see
  [[anthropic-zero-trust-for-ai-agents]], [[guardrails]]). The same eBook names
  tool poisoning, rug pulls, and tool chaining as threats; see
  [[model-context-protocol]] and [[prompt-injection]].
- **Write the connection and auth path into the skill.** Anthropic's data team
  reports documenting the connection and authentication path in the analytics
  skill, so that the agent fails cleanly when access breaks (see
  [[anthropic-claude-tag-analytics-in-slack]]).
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
  `schedule_event` that finds availability *and* books). For MCP servers,
  Anthropic says to group tools by intent, not by endpoint: one
  `create_issue_from_thread` beats four primitive calls (see
  [[anthropic-agents-production-systems-mcp]]).
- **Namespace** related tools by common prefix (`asana_search`, `jira_search`);
  prefix vs suffix has measurable eval effects.
- **Return meaningful context** — semantic over technical (`name` not `uuid`); add
  a `response_format` parameter (`concise`/`detailed`).
- **Token efficiency** — pagination, filtering, truncation with helpful messages;
  actionable errors over opaque codes. Anthropic's commerce-agent post applies
  this: tools call the existing search, cart, and inventory systems, trim
  fields, and return instructions instead of error codes on failure (see
  [[anthropic-anatomy-of-commerce-agents]]).
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
  [[model-context-protocol]], [[guardrails]], [[tool-placement]]

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
- [[anthropic-prompting-claude-sonnet-5-5]]
- [[openai-one-year-of-responses]]
- [[openai-agents-api-guide]]
- [[openai-skills-for-oss-maintenance]]
- [[anthropic-eng-think-tool]]
- [[anthropic-building-multi-agent-systems]]
- [[openai-in-house-data-agent]]
- [[claude-customer-caylent]]
- [[anthropic-claude-code-large-codebases]]
- [[claude-customer-dust]]
- [[claude-customer-n8n]]
- [[claude-customer-genspark]]
- [[claude-customer-greptile]]
- [[anthropic-outtake-cyber-investigator]]
- [[anthropic-llms-secure-source-code]]
- [[anthropic-complete-guide-building-skills]]
- [[anthropic-building-agents-with-skills]]
- [[anthropic-improving-frontend-design-through-skills]]
- [[anthropic-kepler-verifiable-ai]]
- [[anthropic-datadog-universal-machine-tool]]
- [[claude-customer-vapi]]
- [[anthropic-agents-production-systems-mcp]]
- [[anthropic-anatomy-of-commerce-agents]]
- [[anthropic-zero-trust-for-ai-agents]]
- [[anthropic-claude-tag-analytics-in-slack]]

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
- **Where long tool guidance belongs.** The think-tool post (Mar 2025) found
  that long guidance for the tool worked better in the system prompt than in
  the tool description ([[anthropic-eng-think-tool]]). The Jul 2026 context-engineering post keeps
  tool guidance only in the tool description
  ([[anthropic-new-rules-context-engineering-claude-5]]). The two posts target
  different model generations.
