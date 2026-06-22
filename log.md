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

## [2026-06-21] ingest | Anthropic Eng — Effective Context Engineering for AI Agents
- source: wiki/sources/anthropic-eng-context-engineering.md (primary source)
- touched: [[context-engineering]], [[tool-design]], [[agent-harness]], [[agent-orchestration]], [[agent-design-principles]], [[claude]], [[claude-code]], [[anthropic]], index

## [2026-06-21] ingest | Anthropic Eng — Writing Effective Tools for Agents
- source: wiki/sources/anthropic-eng-writing-tools-for-agents.md (primary source)
- touched: [[tool-design]], [[agent-evals]] (new), [[context-engineering]], [[claude]], [[anthropic]], index

## [2026-06-21] ingest | Anthropic Eng — Effective Harnesses for Long-Running Agents
- source: wiki/sources/anthropic-eng-effective-harnesses-long-running-agents.md (primary source)
- touched: [[agent-harness]], [[agent-evals]], [[agent-orchestration]], [[claude-agent-sdk]], [[anthropic]], index
- new concept: [[agent-evals]]

## [2026-06-21] ingest | Anthropic Eng — Demystifying Evals for AI Agents
- source: wiki/sources/anthropic-eng-demystifying-evals.md (primary source)
- touched: [[agent-evals]] (major expansion), [[anthropic]], [[claude]], index

## [2026-06-21] lint | partial ingest — 2 of 6 engineering posts pending
- fetched + ingested: context-engineering, writing-tools, harnesses, demystifying-evals
- PENDING (transient WebFetch limit): multi-agent-research-system → enrich [[agent-orchestration]];
  agent-skills (eng) → enrich [[agent-skills]]
- skipped tangential eng posts: postmortems, SWE-bench, infra-noise, eval-awareness,
  contain-claude, C-compiler, contextual-retrieval, desktop-extensions, auto-mode, sandboxing

## [2026-06-21] ingest | Anthropic Eng — How We Built Our Multi-Agent Research System
- source: wiki/sources/anthropic-eng-multi-agent-research-system.md (primary source)
- touched: [[agent-orchestration]] (multi-agent evidence), [[anthropic]], [[claude]], index

## [2026-06-21] ingest | Anthropic Eng — Equipping Agents with Agent Skills
- source: wiki/sources/anthropic-eng-agent-skills.md (primary source)
- touched: [[agent-skills]] (SKILL.md + 3-level disclosure), [[claude-code]], [[claude-agent-sdk]], [[anthropic]], [[claude]], index

## [2026-06-21] lint | all 6 core engineering posts ingested
- complete: building-effective-agents, context-engineering, writing-tools, harnesses,
  demystifying-evals, multi-agent-research-system, agent-skills
- wiki now ~21 sources/concepts/entities pages added across this thread; next gaps:
  MCP concept page; OpenAI-side harness/context depth; non-lab perspectives

## [2026-06-22] query | Obsidian graph analysis
- filed synthesis: wiki/synthesis/obsidian-graph-analysis.md
- summary: wiki-only graph has 35 pages, one connected component, 407 directed
  wikilinks, 130 reciprocal link pairs, no unresolved internal links, and no
  wiki-only inbound orphans
- touched: [[obsidian-graph-analysis]], [[overview]], index

## [2026-06-22] query | bottom-right Obsidian graph component
- updated synthesis: wiki/synthesis/obsidian-graph-analysis.md
- summary: identified the bottom-right full-vault component as template/schema
  placeholder links plus a nearby isolated raw source capture
- touched: [[obsidian-graph-analysis]]

## [2026-06-22] schema | remove placeholder wikilinks from templates
- updated: CLAUDE.md, templates/source.md, templates/entity.md,
  templates/concept.md, templates/synthesis.md
- summary: converted fake placeholder wikilinks to plain placeholders so
  Obsidian no longer creates unresolved graph nodes for template examples
- touched: [[obsidian-graph-analysis]]
