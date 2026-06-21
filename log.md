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

## [2026-06-21] ingest | Anthropic blog — Steering Claude Code
- source: wiki/sources/anthropic-steering-claude-code.md
- touched: [[claude-code]], [[agent-steering]], [[agent-skills]], [[context-engineering]], [[agent-orchestration]], [[guardrails]], [[anthropic]], index

## [2026-06-21] ingest | Anthropic blog — Lessons from Building Claude Code (skills)
- source: wiki/sources/anthropic-lessons-building-claude-code-skills.md
- touched: [[agent-skills]], [[claude-code]], [[agent-steering]], [[anthropic]], index

## [2026-06-21] ingest | Anthropic blog — Harnessing Claude's Intelligence
- source: wiki/sources/harnessing-claudes-intelligence.md
- touched: [[agent-harness]], [[context-engineering]], [[tool-design]], [[agent-design-principles]], [[claude]], [[anthropic]], index

## [2026-06-21] ingest | Anthropic blog — The Evolution of Agentic Surfaces
- source: wiki/sources/anthropic-evolution-of-agentic-surfaces.md
- touched: [[agent-harness]], [[agent-orchestration]], [[context-engineering]], [[guardrails]], [[claude-managed-agents]], [[claude-agent-sdk]], [[anthropic]], index

## [2026-06-21] ingest | new entities/concepts + cross-link sweep
- new entities: [[claude]], [[claude-code]], [[claude-agent-sdk]], [[claude-managed-agents]]
- new concepts: [[agent-skills]], [[agent-steering]], [[context-engineering]], [[agent-harness]]
- updated synthesis with Anthropic operational depth; updated overview + index
- scope note: ingested only the engineering/best-practice posts from claude.com/blog;
  skipped pure product announcements (managed-agents launches, hackathons, connectors auth, etc.)
