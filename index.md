# Index

The content catalog for this wiki. The LLM updates this on every ingest. Each
page is listed with a wikilink and a one-line summary. When answering a query,
read this first to find relevant pages, then drill in.

## Overview

- [[overview]] — building effective LLM agents; current thesis + map of the wiki

## Sources

- [[anthropic-building-effective-agents]] — Anthropic's field guide: workflows vs.
  agents, five patterns, ACI, start-simple (Dec 2024)
- [[openai-practical-guide-to-building-agents]] — OpenAI's 34-page guide:
  components, orchestration, guardrails (2025)
- [[anthropic-steering-claude-code]] — seven mechanisms to steer an agent: CLAUDE.md, rules, skills, subagents, hooks, styles (Jun 2026)
- [[anthropic-lessons-building-claude-code-skills]] — skills best practices: gotchas, progressive disclosure, model-facing descriptions (Jun 2026)
- [[harnessing-claudes-intelligence]] — three patterns: use what Claude knows, stop doing, set boundaries (Apr 2026)
- [[anthropic-evolution-of-agentic-surfaces]] — brain–hands separation, sessions, harness–model co-evolution (Jun 2026)
- [[anthropic-eng-context-engineering]] — *primary source*: context rot, prompt altitude, just-in-time retrieval, compaction/memory/sub-agents
- [[anthropic-eng-writing-tools-for-agents]] — *primary source*: tool selection, namespacing, token efficiency, eval-with-agents
- [[anthropic-eng-effective-harnesses-long-running-agents]] — *primary source*: two-agent harness, JSON state, human-like verification
- [[anthropic-eng-demystifying-evals]] — *primary source*: grader types, real eval sets, pass@k vs pass^k, eval pitfalls
- [[anthropic-eng-multi-agent-research-system]] — *primary source*: orchestrator-worker, 90.2% gain, ~15× tokens, token-usage explains 80% of variance
- [[anthropic-eng-agent-skills]] — *primary source*: SKILL.md, three-level progressive disclosure, composability, cross-surface support
- [[cursor-agent-swarm-model-economics]] — *practitioner case study*: coding-swarm coordination, context isolation, review lenses, and model economics (Jul 2026)

### Harness, runtime, and containment

- [[anthropic-eng-scaling-managed-agents]] — Managed Agents internals: session, harness, sandbox behind small interfaces; vaulted credentials (Apr 2026)
- [[anthropic-eng-how-we-contain-claude]] — sandboxing Claude across products; environment first, model second; missed risks (May 2026)
- [[anthropic-eng-claude-code-auto-mode]] — auto mode: injection probe + transcript classifier; measured false blocks and misses (Mar 2026)
- [[anthropic-eng-harness-design-long-running-apps]] — planner / generator / evaluator for multi-hour builds; prune parts as models improve (Mar 2026)
- [[anthropic-harness-for-every-task]] — Claude Code writes per-task multi-agent harnesses; six composable patterns (Jun 2026)
- [[anthropic-prompt-caching-is-everything]] — Claude Code built around the prompt cache: prefix order, cache-safe compaction (Apr 2026)
- [[anthropic-claude-code-in-the-cloud]] — cloud sessions: one VM and branch per task, credentials outside the VM (Oct 2026)
- [[anthropic-building-effective-agent-automations]] — scheduled agent on Managed Agents: bookmarks, confirm-then-record, budget caps (Oct 2026)
- [[openai-agents-api-guide]] — Agents API vs. Agents SDK vs. Responses API; computer-use approvals; Aug–Oct 2026 changelog
- [[openai-codex-as-a-platform]] — the open Codex harness as an embeddable runtime: `codex exec`, SDK, app-server (Aug 2026)
- [[openai-one-year-of-responses]] — five Responses API case studies: background jobs, gather-then-reason, multi-agent (Mar 2026)

### Tools, MCP, and context

- [[anthropic-eng-advanced-tool-use]] — Tool Search, Programmatic Tool Calling, Tool Use Examples (Nov 2025)
- [[anthropic-eng-code-execution-with-mcp]] — MCP servers as code files in a sandbox; one task ~150K → ~2K tokens (Nov 2025)
- [[anthropic-seeing-like-an-agent]] — Claude Code tool-design case studies: AskUserQuestion, TodoWrite → Tasks, Grep over RAG (Apr 2026)
- [[anthropic-new-rules-context-engineering-claude-5]] — Claude Code system prompt cut >80% for the Claude 5 generation; judgement over rules (Jul 2026)
- [[openai-private-mcp-servers]] — Secure MCP Tunnel: outbound-only client for private MCP servers (Jun 2026)
- [[openai-automating-repetitive-work-codex]] — Codex + Runme notebooks: plan, approve, execute, keep the notebook as context (Aug 2026)

### Skills and evals

- [[openai-shell-skills-compaction]] — Responses API skills, hosted shell, server-side compaction: ten tips (Feb 2026)
- [[openai-skills-for-oss-maintenance]] — Agents SDK repos run on repo-local skills, `AGENTS.md` triggers, Codex in CI (Mar 2026)
- [[openai-testing-agent-skills-with-evals]] — skill evals: trigger tests, trace grading, schema-bound rubric grading (Jan 2026)
- [[anthropic-automating-eval-design-hillclimbing]] — four eval properties, the adversarial-sampling trap, train/test hillclimbing (Sep 2026)
- [[anthropic-eng-infrastructure-noise-evals]] — container limits alone move agentic eval scores up to 6 points (Feb 2026)

### Model-scoped prompting guidance

Per-model contracts, not general theory. Each carries `models:` + `as_of:`. When a
vendor stops listing a model as current, its page moves to "Legacy" below with
`status: legacy` and a pointer to its replacement (see `CLAUDE.md`).

- [[anthropic-prompting-claude-fable-5-1]] — Fable 5.1 / Mythos 5.1: append-only history, call batching, finish-whole-task, compaction (as of Oct 2026)
- [[anthropic-prompting-claude-opus-5-5]] — Opus 5.5: effort-only thinking control, unattended early stops, pasted-text tags, time budgets (as of Oct 2026)
- [[anthropic-prompting-claude-sonnet-5-5]] — Sonnet 5.5: initiative and scope vary with effort, `between_tools`, mid-turn messages, refusals (as of Oct 2026)
- [[anthropic-prompting-claude-haiku-5-5]] — Haiku 5.5: first Haiku with effort, date-grounded search, JSON with tools, chatbot adherence (as of Oct 2026)
- [[anthropic-building-with-sonnet-5-5]] — Sonnet 5.5 launch playbook: choosing vs. Opus, migration steps, effort re-sweep (Sep 2026)
- [[anthropic-getting-most-out-of-opus-5-5]] — Opus 5.5 in Claude apps and Claude Code: define done, name the stops; differs from docs in four places (Sep 2026)
- [[openai-prompting-gpt-6-astra]] — GPT-6 family (observed on Astra): initiative, instruction precedence, style, delegation, testing; migration checklist (as of Oct 2026)
- [[openai-rethinking-skills-prompts-gpt-6-astra]] — audit skills, `AGENTS.md`, and boundary language for GPT-6 Astra (Sep 2026)

#### Legacy (vendor no longer lists the model as current)

- [[anthropic-prompting-claude-opus-5]] — Opus 5: verbosity, over-verification, subagent caps (as of Aug 2026; legacy since Oct 2026)
- [[anthropic-prompting-claude-sonnet-5]] — Sonnet 5: literal instruction following, effort remapping, new tokenizer (as of Aug 2026; legacy since Oct 2026)
- [[anthropic-prompting-claude-fable-5]] — Fable 5 / Mythos 5: long-horizon autonomy, memory, `reasoning_extraction` refusals (as of Aug 2026; legacy since Oct 2026)
- [[openai-prompt-guidance-gpt-5-6]] — GPT-5.6 Sol/Terra/Luna: outcome-first prompts, staged migration (as of Aug 2026; legacy since Oct 2026)

## Entities

- [[anthropic]] — AI lab; *Building Effective Agents* + operational blog posts
- [[openai]] — AI lab; *A Practical Guide to Building Agents*
- [[openai-agents-sdk]] — OpenAI's code-first agent library (run loop, handoffs, guardrails)
- [[openai-agents-api]] — OpenAI's hosted agent runtime on the Codex harness (beta Sep 2026)
- [[openai-codex]] — OpenAI's coding agent and open-source agent harness
- [[claude]] — Anthropic's LLM family; current: Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5
- [[claude-code]] — Anthropic's agentic coding tool (steering + skills example)
- [[claude-agent-sdk]] — Anthropic's tuned agent harness (2025)
- [[claude-managed-agents]] — Anthropic's managed agent platform (2026)
- [[cursor]] — AI coding product; practitioner research on coding-agent swarms

## Concepts

- [[agents-vs-workflows]] — when to use a dynamic agent vs. a predefined workflow
- [[agent-design-principles]] — start simple, eval, prune scaffolding, design for cache hits
- [[agent-core-components]] — Model, Tools, Instructions
- [[tool-design]] — ACI craft + tool types; clarity beats count; use general-purpose tools
- [[model-context-protocol]] — MCP at scale: deferred loading, tools as code, credentials and private servers
- [[workflow-patterns]] — Anthropic's five: chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer
- [[agent-orchestration]] — run loop; single-agent first; manager vs. decentralized; subagents
- [[agent-instructions]] — unambiguous, action-oriented instructions from real SOPs
- [[guardrails]] — layered safety: classifiers, PII, moderation, tool safeguards, hooks, human-in-the-loop
- [[agent-skills]] — on-demand procedural know-how; gotchas, progressive disclosure
- [[agent-steering]] — choosing the right instruction mechanism (CLAUDE.md/rules/skills/hooks/...)
- [[context-engineering]] — load on demand, let the agent manage/persist context, design for cache hits
- [[agent-harness]] — brain–hands separation, sessions, harness–model co-evolution; two-agent long-running pattern
- [[agent-evals]] — measure beyond accuracy; realistic multi-call tasks; human-like verification; eval-with-agents
- [[multi-agent-economics]] — optimize cost per accepted outcome across planner, workers, review, and coordination
- [[boundary-contracts]] — the bug class tests can't catch: wrong models of external systems; ground-truth-before-code, fail-loud, ratchet
- [[prompt-tuning-axes]] — the knobs you re-tune on a model migration; axes only, no values (those expire)

## Synthesis

- [[agent-building-best-practices-anthropic-vs-openai]] — where the two guides
  agree/differ + a distilled best-practices checklist
- [[obsidian-graph-analysis]] — current wiki graph topology, hubs, caveats, and
  recommended Obsidian filters
