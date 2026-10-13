# Building agents with Skills: Equipping agents for specialized work — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/building-agents-with-skills-equipping-agents-for-specialized-work
> Publisher: Anthropic (claude.com articles) · Date: 2026-01-22
> Captured: 2026-10-12 via curl (condensed).

Category: Best practices. Product: Claude Code. Reading time 12 min.
Acknowledgments: Barry Zhang, Mahesh Murag, Keith Lazuka, Ryan Whitehead.

## Intro

- Over the past year MCP became the connectivity standard, Claude Code launched
  as a general-purpose coding agent, and the Claude Agent SDK shipped a
  production-ready agent.
- Recurring gap: agents have intelligence and capabilities but not always
  expertise. Agent Skills are organized collections of files packaging domain
  expertise (workflows, best practices, scripts). The post explains why
  Anthropic "stopped building specialized agents" and builds skills instead.

## The new paradigm: code is all you need

- Earlier assumption: each domain (coding, research, finance, marketing) needs
  its own agent, tools, scaffolding. Anthropic converged instead on code as a
  general interface for nearly any digital work.
- Claude Code is a general agent that works through code. Financial-report
  example: call APIs, store data on the filesystem, analyze with Python,
  synthesize — scaffolding reduces to bash plus a filesystem.

## The missing piece: domain expertise

- Analogy: a math genius vs an experienced tax professional; people pick the
  professional for expertise, not intelligence.
- Agents lack context, cannot easily absorb an organization's expertise, and do
  not automatically learn from repeated tasks. Skills package expertise for
  progressive access.

## What are Agent Skills?

- Example folder `anthropic_brand/` with `SKILL.md`, `docs.md`,
  `slide-decks.md`, `apply_template.py`.
- Files are a deliberate universal primitive: version with Git, store in Google
  Drive, share with a team. Non-engineers (PMs, analysts, domain experts) build
  skills.

## Progressive disclosure

- At runtime only metadata (YAML frontmatter `name`, `description`) is shown.
  If Claude judges the skill relevant it reads the full `SKILL.md`; a
  `references/` directory holds further docs loaded on demand.
- Token sizes per tier: metadata ~50 tokens; full SKILL.md ~500 tokens;
  reference files 2,000+ tokens, loaded only when needed. Lets an agent hold
  hundreds of skills.

## Skills can include scripts as tools

- Problems with traditional tools: poorly written instructions, model cannot
  modify or extend them, they bloat context. Code is self-documenting,
  modifiable, and need not be in context.
- Example: Claude repeatedly wrote the same script to apply Anthropic slide
  styling, so it was asked to save it as `apply_template.py` (python-pptx;
  prints a usage line and exits if not given one pptx argument). `slide-decks.md`
  lists colors (intro/outro background `#141413`, foreground oat; section slides
  background `#da7857`, foreground `#141413`) and points to the script for
  in-place updates.

## The skills ecosystem

### Foundational skills
- Core capabilities: documents, spreadsheets, presentations; in the public repo.
### Partner skills
- Companies make services agent-accessible: K-Dense, Browserbase, Notion, others.
### Enterprise skills
- Proprietary skills encoding internal processes, compliance requirements,
  institutional knowledge.

## Trends we see

### Increasing complexity
- Simple: "Status report writer" (~100 lines) — templates, formatting.
- Intermediate: "Financial model builder" (~800 lines) — data retrieval, Excel
  modeling with Python.
- Complex: "RNA sequencing pipeline" (2,500+ lines) — coordinates HISAT2,
  StringTie, DESeq2.
### Skills and MCP
- They combine: e.g. a competitive-analysis skill coordinating web search,
  internal databases via MCP, Slack history, and Notion pages.
### Non-developer adoption
- PMs, analysts, domain experts can create and test a first skill in under 30
  minutes with the interactive skill-creator tool.

## The complete architecture

Four layers: **agent loop** (reasons, decides next step), **agent runtime**
(execution environment: code, filesystem), **MCP servers** (connections to
external tools/data), **skills library** (domain expertise, procedural
knowledge). Loop reasons, runtime executes, MCP connects, skills guide; each
layer evolves independently. Example: the frontend design skill adds typography,
color, and animation guidance and loads only when building web interfaces.

## Deploying skills to new verticals

### Financial Services
- Skills: DCF model builder (WACC, sensitivity analysis); comparable company
  analysis; earnings analysis; initiation coverage; due diligence (M&A
  frameworks); pitch materials.
### Healthcare & Life Sciences
- Bioinformatics bundles (scVI-tools, Nextflow); clinical trial protocol
  generation; scientific problem selection; FHIR development; prior
  authorization review.

## Standardizing Agent Skills

- Agent Skills published as an open standard; like MCP, skills should be
  portable across tools and platforms. Anthropic reports collaboration with
  ecosystem members and early adoption.

## Getting started

- Resources listed: talk "Don't Build Agents, Build Skills Instead" (YouTube),
  skills docs, GitHub repo, skills cookbook, using skills in Claude, Skills API
  quickstart, skills best-practices docs.
