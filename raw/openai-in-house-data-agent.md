# Inside OpenAI's in-house data agent — OpenAI (Engineering) (raw capture)

> Source: https://openai.com/index/inside-our-in-house-data-agent/
> Publisher: OpenAI (Engineering) · Date: 2026-01-29 · Authors: Bonnie Xu, Aravind Suresh, Emma Tang
> Captured: 2026-10-12 via built-in browser (get_page_text) (condensed). openai.com returns HTTP 403 to curl and WebFetch.

Case study of an internal-only tool; all results are self-reported by OpenAI.
Page headings: Why we needed a custom tool · How it works · Context is
everything (Layers #1–#6) · Built to think and work like a teammate · Moving
fast without breaking trust · Agent security · Lessons learned (#1–#3) · Same
vision, new tools.

## Intro

- Internal-only AI data agent (not an external product) built around OpenAI's
  data, permissions, and workflows. Built with Codex, GPT-5 (flagship), the
  Evals API, and the Embeddings API.
- Claim: question to insight in minutes, not days. Used by Engineering, Data
  Science, Go-To-Market, Finance, Research. Combines Codex-derived table-level
  knowledge with product and org context; memory improves it each turn.

## Why we needed a custom tool

- Platform scale: **3.5k+ internal users**, **600+ PB**, **70k datasets**.
  Finding the right table is a major time sink (many similar tables; some
  include logged-out users, some do not; overlapping fields).
- Even with the right table, failure modes silently invalidate results:
  many-to-many joins, filter pushdown errors, unhandled nulls. An example SQL
  statement is 180+ lines.

## How it works

- Powered by **GPT-5.2**. Available as a Slack agent, a web UI, inside IDEs,
  in Codex CLI via MCP, and in OpenAI's internal ChatGPT app via an MCP
  connector.
- Handles open-ended questions end-to-end (example on a test dataset: most
  unreliable NYC taxi pickup-to-dropoff ZIP pairs and when variability occurs).
- Self-evaluates progress: if an intermediate result looks wrong (e.g. zero
  rows from a bad join/filter) it investigates, adjusts, and retries, keeping
  full context. Iteration moves from the user into the agent.
- Covers discovery, SQL, and publishing notebooks and reports; uses internal
  knowledge, web search, learned usage, and memory.

## Context is everything — six layers

1. **Table Usage** — schema metadata (column names, types) and table lineage
   (upstream/downstream); historical queries teach query style and common
   joins.
2. **Human Annotations** — expert-curated table/column descriptions: intent,
   semantics, business meaning, known caveats.
3. **Codex Enrichment** — Codex derives a code-level definition of each table:
   uniqueness of values, update frequency, scope/granularity, derivation from
   analytics events, and usage beyond SQL (Spark, Python). Distinguishes
   look-alike tables (e.g. only first-party ChatGPT traffic). Refreshed
   automatically.
4. **Institutional Knowledge** — Slack, Google Docs, Notion (launches,
   incidents, codenames, canonical metric definitions). Ingested, embedded,
   stored with metadata and permissions; a retrieval service does access
   control and caching at runtime.
5. **Memory** — saves corrections and discovered nuances; aims at
   non-obvious corrections, filters, and constraints not inferable from other
   layers. Example: filtering an experiment needed matching a specific string
   from an experiment gate, not fuzzy matching. The agent prompts the user to
   save a memory after a correction; users can create and edit memories;
   scopes are **global** and **personal**.
6. **Runtime Context** — live queries to the warehouse when context is
   missing or stale; can query other Data Platform systems (metadata service,
   Airflow, Spark).
- A **daily offline pipeline** merges usage, annotations, and Codex enrichment
  into one normalized representation, embeds it (Embeddings API), and stores
  it. At query time the agent retrieves only the most relevant context (RAG)
  rather than scanning raw metadata, keeping latency predictable across tens
  of thousands of tables. Live warehouse queries run as needed.

## Built to think and work like a teammate

- Conversational and always-on; carries full context across turns; users can
  interrupt mid-analysis and redirect.
- Asks clarifying questions when instructions are unclear; with no reply,
  applies sensible defaults (e.g. last 7 or 30 days for an unspecified growth
  question).
- **Workflows** package recurring analyses into reusable instruction sets
  (e.g. weekly business reports, table validations).

## Moving fast without breaking trust

- Without a tight feedback loop, regressions are inevitable and invisible;
  systematic evaluation is the answer. Uses the **Evals API**.
- Evals: curated question-answer pairs; each question has a manually authored
  **golden SQL**. Send the question to the query-generation endpoint, run the
  generated SQL, compare with the golden SQL's result.
- No naive string matching: compare both SQL and result data (tolerating
  syntactic differences and extra columns), feed signals to the Evals grader,
  which outputs a score and explanation.
- Evals run continuously in development like unit tests, and as canaries in
  production.

## Agent security

- Pure interface layer inheriting existing permissions and guardrails. Access
  is strictly **pass-through**: users can only query tables they already may
  access; when access is missing it flags it or falls back to authorized
  datasets.
- Transparency: summarizes assumptions and execution steps with each answer;
  links to underlying query results for verification.

## Lessons learned

1. **Less is More** — exposing the full tool set caused confusion from
   overlapping functionality; they restricted and consolidated tool calls.
2. **Guide the Goal, Not the Path** — highly prescriptive prompting degraded
   results; higher-level guidance plus GPT-5's reasoning worked better.
3. **Meaning Lives in Code** — schemas and query history show shape and usage;
   true meaning (assumptions, freshness, business intent) lives in pipeline
   code. Crawling the codebase with Codex improves "what's in here" and "when
   can I use it" answers.

## Same vision, new tools

- Ongoing work: ambiguous questions, stronger validation, deeper workflow
  integration; the agent should blend into existing work, not be a separate
  tool.
