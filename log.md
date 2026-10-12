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

## [2026-07-21] ingest | Cursor — Agent Swarms and the New Model Economics
- summary: wiki/sources/cursor-agent-swarm-model-economics.md
- touched: [[cursor]], [[multi-agent-economics]], [[agent-orchestration]],
  [[agent-harness]], [[context-engineering]], [[agent-evals]],
  [[workflow-patterns]], [[agent-design-principles]], [[agent-instructions]],
  [[overview]], index, README
- source note: live web source; `raw/` remains unchanged per repository policy

## [2026-08-06] schema | model-scoped pages: `models:` + `as_of:` frontmatter
- updated: CLAUDE.md, templates/source.md
- summary: prompting guidance is a per-model contract, not shared theory —
  cross-vendor/cross-generation synthesis of prompting advice is not filed.
  Model-specific claims must declare exact API model IDs and a verification
  date; scope follows the vendor's own current/legacy split; values live in
  sources, never in concepts.
- touched: [[overview]], index

## [2026-08-06] ingest | Model-scoped prompting guidance (Claude 5 series, GPT-5.6)
- summaries: wiki/sources/anthropic-prompting-claude-opus-5.md,
  wiki/sources/anthropic-prompting-claude-sonnet-5.md,
  wiki/sources/anthropic-prompting-claude-fable-5.md,
  wiki/sources/openai-prompt-guidance-gpt-5-6.md
- new concept: wiki/concepts/prompt-tuning-axes.md — the durable re-tuning axes,
  deliberately holding no values
- touched: [[prompt-tuning-axes]], [[agent-instructions]],
  [[agent-design-principles]], [[overview]], index, CLAUDE.md
- contradiction flagged: `reasoning_extraction` refusals on Claude Fable 5 put
  the older implementation of the Transparency principle (prompt the model to
  narrate its reasoning) in tension with current model behavior; recorded on
  [[agent-design-principles]]
- scope: excludes Anthropic 4.x (incl. Haiku 4.5), GPT-4.1, GPT-5 — per the
  per-model-contract rule, superseded generations are not carried forward
- source note: live web sources; `raw/` remains unchanged per repository policy

## [2026-08-06] ingest | raw captures added for model-scoped prompting sources
- corrects the "source note" on the model-scoped prompting ingest above, which
  claimed `raw/` should stay unchanged. That generalized a one-off note from the
  Cursor ingest into a policy; the dominant precedent is the opposite — every
  other `raw/` file is an agent-written WebFetch capture, added across four
  ingest commits (37691df, 307ccd8, b804204).
- added: raw/anthropic-prompting-claude-opus-5.md,
  raw/anthropic-prompting-claude-sonnet-5.md,
  raw/anthropic-prompting-claude-fable-5.md,
  raw/openai-prompt-guidance-gpt-5-6.md
- `source_path:` added to all four source pages.
- rationale: every cited URL moved host during capture (`docs.claude.com` →
  `platform.claude.com` 302; `cookbook.openai.com` → `developers.openai.com`
  308; one OpenAI help-center URL returned 403). Without a capture there is
  nothing to re-check a page against when a link rots.
- also: the fuller OpenAI capture surfaced sections the first condensed fetch
  missed — contradiction review, PTC handoff design and `program_output` testing,
  long-running workflow state and prompt caching, check-work-before-finishing,
  and effort-as-second-resort. [[openai-prompt-guidance-gpt-5-6]] expanded
  accordingly.
- touched: [[openai-prompt-guidance-gpt-5-6]],
  [[anthropic-prompting-claude-opus-5]],
  [[anthropic-prompting-claude-sonnet-5]],
  [[anthropic-prompting-claude-fable-5]]

## [2026-10-12] lint | new Anthropic and OpenAI agent guidance since 2026-08-06
- stale by construction: all four model-scoped source pages. Anthropic's models
  overview lists `claude-opus-5`, `claude-sonnet-5`, and `claude-fable-5` under
  "Legacy models"; current is `claude-fable-5-1`, `claude-opus-5-5`,
  `claude-sonnet-5-5`, `claude-haiku-5-5`. OpenAI's models page lists
  `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6-luna`; plain `gpt-5.6` is gone (only the
  `gpt-5.6-cyber` specialist remains). Pages: [[anthropic-prompting-claude-opus-5]],
  [[anthropic-prompting-claude-sonnet-5]], [[anthropic-prompting-claude-fable-5]],
  [[openai-prompt-guidance-gpt-5-6]]. Not yet re-verified or retired — awaiting
  the human's decision.
- replacements confirmed to exist (HTTP 200): `prompting-claude-opus-5-5`,
  `prompting-claude-sonnet-5-5`, `prompting-claude-haiku-5-5`,
  `prompting-claude-fable-5-1` under platform.claude.com/docs/en/build-with-claude/
  prompt-engineering/. OpenAI publishes a prompting section only for GPT-6 Astra
  (developers.openai.com/api/docs/guides/latest-model/gpt-6-astra); none for
  GPT-6.1 Sol or GPT-6 Luna.
- new since 2026-08-06, not ingested (Anthropic, claude.dev/blog): building
  effective agent automations (2026-10-08); Claude Code in the cloud
  (2026-10-06); automating eval design and hillclimbing (2026-09-28); building
  with Claude Sonnet 5.5 (2026-09-28); getting the most out of Opus 5.5
  (2026-09-22).
- new since 2026-08-06, not ingested (OpenAI, developers.openai.com/blog):
  rethinking skills and prompts for GPT-6 Astra (Sep 2026); automating
  repetitive work at OpenAI with Codex (2026-08-25); Codex as a platform (page
  metadata says 2026-07-07, page text says 2026-08-19 — date unresolved).
- OpenAI platform changes, from the official API changelog: Assistants API shut
  down 2026-08-26; GPT-6 Astra released 2026-09-03; Agents API (managed Codex
  harness) public beta 2026-09-10; GPT-6 Sol and Luna 2026-09-22; GPT-6.1 Sol
  2026-09-29; computer use in the Agents API 2026-09-29.
- older candidates, never ingested (previously out of scope, not misses):
  Anthropic engineering — how we contain Claude (2026-05-25), scaling Managed
  Agents (2026-04-08), Claude Code auto mode (2026-03-25), harness design for
  long-running apps (2026-03-24), infrastructure noise in agentic evals
  (2026-02-05), advanced tool use (2025-11-24), code execution with MCP
  (2025-11-04). claude.dev — new rules of context engineering for Claude 5
  (2026-07-24), a harness for every task (2026-06-02), prompt caching is
  everything (2026-04-30), seeing like an agent (2026-04-10). OpenAI — shell +
  skills + compaction (2026-02-11), testing agent skills with evals
  (2026-01-22), skills for OSS maintenance (2026-03-09), one year of Responses
  (2026-03-11), private MCP servers (2026-06-26).
- touched: log.md only

## [2026-10-12] schema | legacy status for model-scoped pages
- added to CLAUDE.md: a third option beside re-verify and retire. A page whose
  model the vendor no longer lists as current keeps its claims and gets
  `status: legacy`, `superseded_by: [...]`, a dated banner, and a place in the
  "Legacy" subsection of `index.md`.
- added `status:` and `superseded_by:` to `templates/source.md`.
- applied to [[anthropic-prompting-claude-opus-5]],
  [[anthropic-prompting-claude-sonnet-5]], [[anthropic-prompting-claude-fable-5]],
  [[openai-prompt-guidance-gpt-5-6]] (see the 2026-10-12 lint entry above).

## [2026-10-12] ingest | Anthropic and OpenAI agent guidance, Nov 2025 – Oct 2026 (30 sources)
- trigger: the 2026-10-12 lint above. The human asked to keep the legacy
  prompting pages and add everything the lint listed as missing.
- model-scoped (current models): [[anthropic-prompting-claude-fable-5-1]],
  [[anthropic-prompting-claude-opus-5-5]], [[anthropic-prompting-claude-sonnet-5-5]],
  [[anthropic-prompting-claude-haiku-5-5]], [[anthropic-building-with-sonnet-5-5]],
  [[anthropic-getting-most-out-of-opus-5-5]], [[openai-prompting-gpt-6-astra]],
  [[openai-rethinking-skills-prompts-gpt-6-astra]]
- new since 2026-08-06: [[anthropic-building-effective-agent-automations]],
  [[anthropic-claude-code-in-the-cloud]],
  [[anthropic-automating-eval-design-hillclimbing]],
  [[openai-automating-repetitive-work-codex]], [[openai-codex-as-a-platform]],
  [[openai-agents-api-guide]]
- older, never ingested: [[anthropic-eng-how-we-contain-claude]],
  [[anthropic-eng-scaling-managed-agents]], [[anthropic-eng-claude-code-auto-mode]],
  [[anthropic-eng-harness-design-long-running-apps]],
  [[anthropic-eng-infrastructure-noise-evals]], [[anthropic-eng-advanced-tool-use]],
  [[anthropic-eng-code-execution-with-mcp]],
  [[anthropic-new-rules-context-engineering-claude-5]],
  [[anthropic-harness-for-every-task]], [[anthropic-prompt-caching-is-everything]],
  [[anthropic-seeing-like-an-agent]], [[openai-shell-skills-compaction]],
  [[openai-testing-agent-skills-with-evals]], [[openai-skills-for-oss-maintenance]],
  [[openai-one-year-of-responses]], [[openai-private-mcp-servers]]
- new pages: [[model-context-protocol]] (concept), [[openai-agents-api]],
  [[openai-codex]] (entities)
- corrections to the lint entry: "Codex as a platform" is dated 2026-08-19 by
  its byline; the 2026-07-07 was a linked changelog URL. "Rethinking skills and
  prompts for GPT-6 Astra" is dated 2026-09-11 by its byline.
- scoping decisions: [[openai-prompting-gpt-6-astra]] is scoped to all three
  GPT-6 model IDs, because OpenAI calls its practices a starting point for the
  whole family. [[anthropic-prompting-claude-fable-5-1]] includes
  `claude-mythos-5-1` from the page metadata only.
  [[anthropic-new-rules-context-engineering-claude-5]] has no `models:` field,
  because it names models only as examples of a generation.
- method: six helpers wrote the source pages in parallel; six more merged their
  notes into shared pages, each checking every claim against its source page.
  `raw/` captures are condensed paraphrase (the repo is public).
- touched: index, overview, [[agent-building-best-practices-anthropic-vs-openai]],
  [[anthropic]], [[openai]], [[openai-agents-sdk]], [[claude]], [[claude-code]],
  [[claude-managed-agents]], [[claude-agent-sdk]], and the concept pages
  [[agent-harness]], [[guardrails]], [[agent-steering]], [[context-engineering]],
  [[agent-instructions]], [[agent-evals]], [[workflow-patterns]],
  [[multi-agent-economics]], [[agents-vs-workflows]], [[tool-design]],
  [[agent-core-components]], [[agent-skills]], [[agent-orchestration]],
  [[prompt-tuning-axes]], [[agent-design-principles]]
- contradictions recorded (both claims kept, with sources and dates):
  [[claude-managed-agents]] — where the latency win came from (sandbox spins up
  in parallel, Jun 2026, vs. containers created only on first tool call, Apr
  2026); [[tool-design]] — worked examples in tool descriptions (Dec 2024 and
  Nov 2025 for, Jul 2026 against); [[agent-evals]] — "target weaknesses" vs.
  the failure-fingerprint warning (Sep 2026); [[agent-instructions]] —
  step-level instructions (2025) vs. judgement over blanket rules (2026);
  [[agent-steering]] — auto-memory narrows `CLAUDE.md` (Jul 2026);
  [[guardrails]] — cloud sessions and scheduled agents have no per-command
  approval; [[prompt-tuning-axes]] — three settings reversed between the 5 and
  5.x generations; [[agent-orchestration]] — separate verifier subagents vs.
  "no reviewer subagents unless asked"; [[openai]] — no Terra tier in GPT-6;
  [[anthropic-getting-most-out-of-opus-5-5]] — blog and docs disagree in four
  places.
- checks: `tools/search.py --orphans` reports no orphans; every `[[link]]` in
  wiki/, index.md, and log.md resolves to a page.

## [2026-10-12] query | refresh Obsidian graph analysis
- updated synthesis: [[obsidian-graph-analysis]]
- summary: the wiki-only graph grew from 35 pages and 408 links (June) and 44
  pages and 516 links (`main`, August) to 77 pages and 1,255 links, with 419
  reciprocal pairs, one connected component, no unresolved links, and no pages
  without a `wiki/` inbound link. Concept hubs grew most:
  [[context-engineering]] and [[agent-harness]] 18–19 → 51 inbound links,
  [[guardrails]] 14 → 45. OpenAI coverage roughly doubled; Anthropic sources
  still outnumber OpenAI about 3 to 1.
- method: a script collects wikilinks from every page under `wiki/`, drops
  self-links and duplicates, and computes components on the undirected graph.
  The August column reruns it on `main`.
- touched: [[obsidian-graph-analysis]], index

## [2026-10-12] schema | agent-written raw captures are paraphrase
- added to CLAUDE.md (Ingest): web pages the agent captures into `raw/` are
  condensed paraphrase. Headings, numbers, parameter names, and identifiers
  stay exact; prose and example prompts are paraphrased; quotes stay under 15
  words. The header records the fetch method actually used.
- why: the repo is public and the sources are copyrighted. The human asked
  whether to keep paraphrase or copy prompts verbatim; paraphrase stays.
- the three Aug 2026 Anthropic prompting captures that quote prompt blocks
  verbatim are left unchanged, because `raw/` is immutable.

## [2026-10-12] ingest | six Anthropic Engineering backlog posts
- summaries: [[anthropic-eng-claude-code-sandboxing]] (Oct 2025),
  [[anthropic-eng-claude-code-best-practices]] (Apr 2025),
  [[anthropic-eng-think-tool]] (Mar 2025), [[anthropic-eng-building-c-compiler]]
  (Feb 2026), [[anthropic-eng-ai-resistant-evaluations]] (Jan 2026),
  [[anthropic-eng-eval-awareness-browsecomp]] (Mar 2026)
- trigger: the human asked to add the six posts that the earlier 2026-10-12
  ingest named as not yet ingested.
- superseded content: the best-practices URL now redirects to a maintained docs
  page (modified 2026-10-06); the raw capture holds the 2025 text from the
  Wayback Machine plus a labeled second capture of the successor page. A Dec
  2025 banner on the think-tool post recommends extended thinking instead.
- no `models:` field on any of the six; each names the model and date its
  findings were measured on.
- contradictions recorded: [[guardrails]] — "an injection inside the sandbox
  cannot impact user security" (Oct 2025) vs. exfiltration through an
  allowlisted domain (May 2026); [[agent-evals]] — starting a test where the
  current model struggles vs. the failure-fingerprint warning;
  [[tool-design]] — long tool guidance in the system prompt (Mar 2025) vs. in
  the tool description only (Jul 2026); [[agent-orchestration]] — multi-agent
  BrowseComp gains vs. 3.7x unintended solutions; [[multi-agent-economics]] —
  no-planner design vs. planner-plus-workers advice.
- resolved: the open question in [[agent-orchestration]] about replication on
  ordinary git repositories now has one data point ([[anthropic-eng-building-c-compiler]]).
- touched: index, overview, [[anthropic]], [[claude-code]], [[guardrails]],
  [[agent-evals]], [[agent-orchestration]], [[agent-harness]], [[tool-design]],
  [[multi-agent-economics]], [[context-engineering]], [[model-context-protocol]]

## [2026-10-12] query | refresh Obsidian graph analysis (after backlog ingest)
- updated synthesis: [[obsidian-graph-analysis]]
- summary: 83 pages, 53 of them sources; 1,364 unique directed links; 445
  reciprocal pairs; one connected component; no unresolved links; no pages
  without a `wiki/` inbound link. Same script as the earlier refresh today.
- touched: [[obsidian-graph-analysis]], index
