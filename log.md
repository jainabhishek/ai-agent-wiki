# Log

Append-only, chronological record of activity. Newest at the bottom. Each entry
starts with `## [YYYY-MM-DD] <type> | <title>` so the log is greppable:

```
grep "^## \[" log.md | tail -5
```

Event types: `ingest`, `query`, `lint`, `schema`.

---

## [2026-06-21] schema | wiki initialized
- Scaffolded the research-wiki structure per the LLM Wiki pattern.
- Created: CLAUDE.md (schema), index.md, log.md, templates/, tools/search.py.
- Ready to ingest the first source.

## [2026-06-21] ingest | Anthropic — Building Effective Agents
- source: wiki/sources/anthropic-building-effective-agents.md (raw/anthropic-building-effective-agents.md)
- touched: [[anthropic]], [[agents-vs-workflows]], [[workflow-patterns]], [[tool-design]], [[agent-design-principles]], [[agent-orchestration]], overview, index

## [2026-06-21] ingest | OpenAI — A Practical Guide to Building Agents
- source: wiki/sources/openai-practical-guide-to-building-agents.md (raw/openai-practical-guide-to-building-agents.txt)
- touched: [[openai]], [[openai-agents-sdk]], [[agent-core-components]], [[agent-instructions]], [[guardrails]], [[agent-orchestration]], [[tool-design]], overview, index

## [2026-06-21] query | best practices shared by Anthropic and OpenAI
- filed synthesis: wiki/synthesis/agent-building-best-practices-anthropic-vs-openai.md
- comparison table + distilled checklist across both guides
