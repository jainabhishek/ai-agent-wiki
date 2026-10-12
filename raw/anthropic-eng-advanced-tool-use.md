# Introducing advanced tool use on the Claude Developer Platform — Anthropic (Engineering blog) (raw capture)

> Source: https://www.anthropic.com/engineering/advanced-tool-use
> Publisher: Anthropic (Engineering blog) · Date: 2025-11-24
> Captured: 2026-10-12 via WebFetch (condensed).

Author: Bin Wu, with contributions from Adam Jones, Artur Renault, Henry Tay,
Jake Noble, Noah Picard, Sam Jiang, and the Claude Developer Platform team.

## Introduction (untitled)

- Three beta features let Claude discover, learn, and execute tools
  dynamically: **Tool Search Tool**, **Programmatic Tool Calling**, **Tool Use
  Examples**.
- Motivation: agents need hundreds or thousands of tools without loading every
  definition up front; definitions plus results can cost 50,000+ tokens before
  the request is read. Code fits orchestration better than one-call-per-turn
  natural language. JSON Schema cannot express usage patterns.
- Claude for Excel uses Programmatic Tool Calling to handle spreadsheets with
  thousands of rows.

## Tool Search Tool

### The challenge
- Five-server MCP setup (GitHub, Slack, Sentry, Grafana, Splunk) = 58 tools,
  ~55K tokens before the conversation starts. Adding Jira (~17K) pushes past
  100K. Anthropic has seen 134K tokens of definitions before optimization.
- Most common failures: wrong tool selection and wrong parameters, especially
  among similarly named tools.

### Our solution
- Tools are discovered on demand. Comparison: 191,300 tokens of context
  preserved vs 122,800 with the traditional approach.
- Traditional: ~77K tokens for 50+ tools. Search approach: ~8.7K (≈500 for the
  search tool + ≈3K for 3–5 discovered tools) — an 85% reduction.
- MCP-eval accuracy: Opus 4 49% → 74%; Opus 4.5 79.5% → 88.1%.

### How the Tool Search Tool works
- All tools are sent to the API; those marked `defer_loading: true` stay out of
  the initial context. Keep critical tools at `defer_loading: false`.
- Claude searches; matching tool definitions are expanded into context. Example
  tools: `github.createPullRequest`, `github.listIssues`.
- Whole MCP servers can be deferred via an `mcp_toolset` config, with selected
  tools (e.g. `search_files`) kept loaded.
- Platform ships regex-based and BM25-based search tools; custom search (e.g.
  embeddings) is supported. Attested type ID: `tool_search_tool_regex_20251119`
  (the BM25 variant's ID is not given in the post).
- Prompt caching is preserved because deferred tools are excluded from the
  initial prompt.

### When to use the Tool Search Tool
- Use: definitions > ~10K tokens; tool-selection accuracy problems; multiple MCP
  servers; 10+ tools.
- Less useful: < 10 tools; most tools used every session; compact definitions.

## Programmatic Tool Calling

### The challenge
- Intermediate results (e.g. a 10MB log file) flood context when only a summary
  is needed.
- Each tool call costs a full inference pass; a five-tool workflow = five passes
  plus manual synthesis.

### Our solution
- Claude writes Python that calls tools inside a sandboxed code-execution
  environment: parallel calls, filtering/transforming, error handling. Only the
  final output returns to Claude's context.

### Example: Budget compliance check
- Task: which of 20 engineers exceeded their Q3 travel budget, using
  `get_team_members`, `get_expenses`, `get_budget_by_level`.
- Traditional: 2,000+ expense line items (50KB+) land in context.
- Programmatic: ~200KB of raw data reduced to ~1KB of results naming the 2–3
  people over budget.
- Reported gains: average tokens 43,588 → 27,297 (−37%) on complex research
  tasks; 20+ calls in one code block remove 19+ inference passes (latency);
  internal knowledge retrieval 25.6% → 28.5%; "GIA benchmarks" (as written on
  the page) 46.5% → 51.2%.

### How Programmatic Tool Calling works
1. **Mark tools as callable from code** — add the `code_execution_20250825`
   tool and set `allowed_callers` on tools that code may call.
2. **Claude writes orchestration code** — the API exposes those tools as Python
   functions.
3. **Tools execute without hitting Claude's context** — tool requests issued
   from code carry a `caller` field; the developer returns results, which are
   processed inside the sandbox.
4. **Only final output enters context** — as `code_execution_tool_result`.

### When to use Programmatic Tool Calling
- Use: large datasets where only aggregates matter; 3+ dependent calls;
  filtering/transforming results; parallel operations across many items.
- Less useful: single calls; when Claude must reason over every intermediate
  result; quick lookups with small responses.

## Tool Use Examples

### The challenge
- JSON Schema defines structure, not usage. Example `create_ticket`: ambiguous
  date formats, ID conventions, when to fill nested contact details, how
  escalation fields relate to priority.

### Our solution
- An `input_examples` array in the tool definition holds concrete sample calls.
  Three examples convey date/ID formats, label conventions, nested-object
  patterns, and correlations (critical bugs carry full contact info and tight
  SLAs; feature requests omit them).
- Internal testing: accuracy on complex parameter handling 72% → 90%.

### When to use Tool Use Examples
- Use: complex nested structures; many optional parameters; domain-specific
  conventions; similar tools needing disambiguation (`create_ticket` vs
  `create_incident`).
- Less useful: simple tools; standard formats (URLs, emails); constraints better
  expressed in JSON Schema.

## Best practices

### Layer features strategically
- Context bloat from definitions → Tool Search Tool.
- Large intermediate results → Programmatic Tool Calling.
- Parameter errors → Tool Use Examples.

### Set up Tool Search Tool for better discovery
- Clear, descriptive names and descriptions (search matches on them) — e.g.
  `search_customer_orders` over `query_db_orders` with a vague description.
- Add system-prompt guidance naming the available tool categories.
- Keep the 3–5 most-used tools always loaded.

### Set up Programmatic Tool Calling for correct execution
- Document return formats precisely so Claude writes correct parsing code.
- Opt in tools that are parallel-safe or idempotent.

### Set up Tool Use Examples for parameter accuracy
- Realistic data, not placeholders.
- Show minimal, partial, and full specifications.
- 1–5 examples per tool, only where usage is not obvious from the schema.

## Getting started

- Beta header: `advanced-tool-use-2025-11-20`.
- Sample request uses `claude-sonnet-4-5-20250929` and combines
  `tool_search_tool_regex_20251119`, `code_execution_20250825`, and custom
  tools with `defer_loading`, `allowed_callers`, and `input_examples`.
- Docs and cookbook links per feature.
- Framing: dynamic discovery, efficient execution, reliable invocation.
  Acknowledged inspirations: LLMVM, Cloudflare's Code Mode, and Anthropic's
  Code Execution with MCP work.

## Acknowledgements

Contributor credits (listed above).
