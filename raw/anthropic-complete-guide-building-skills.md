# The Complete Guide to Building Skills for Claude — Anthropic (guide PDF) (raw capture)

> Source: https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
> Landing page: https://claude.com/resources/articles/complete-guide-to-building-skills-for-claude
> Publisher: Anthropic (guide PDF) · Date: 2026-01-29 (landing-page byline; the 33-page PDF carries no date, but its distribution chapter is headed "January 2026")
> Captured: 2026-10-12 via curl (PDF downloaded; text extracted with macOS PDFKit) (condensed). Section-complete: every chapter and subsection of the PDF appears below.

## Landing page (claude.com article, 2026-01-29, 3 min)

- Since skills launched in October (2025), interest came from developers wanting
  consistent workflows, power users automating repeatable tasks, teams
  standardizing Claude, and MCP connector builders.
- Expect ~15–30 minutes to build and test a first skill with skill-creator if
  you know your top 2–3 workflows. Body of the guide is the PDF.

## Contents (PDF page numbers)
Introduction 3 · Fundamentals 4 · Planning and design 7 · Testing and iteration
14 · Distribution and sharing 18 · Patterns and troubleshooting 21 · Resources and
references 28 · Reference A–C (30–32).

## Introduction (p.3)

- A skill is a set of instructions packaged as a folder that teaches Claude a
  task or workflow; teach once instead of re-explaining every conversation.
- Good fits: repeatable workflows — frontend designs from specs, research with
  consistent methodology, documents in a team style, multi-step processes.
  Works with built-in code execution and document creation; for MCP builders,
  skills turn raw tool access into reliable workflows.
- Audience: developers, power users, teams standardizing Claude.
- Two paths: standalone skills → Fundamentals, Planning and design, categories
  1–2. MCP enhancement → "Skills + MCP" section and category 3.
- Goal: a functional skill in one sitting; 15–30 min with skill-creator.

## Chapter 1 — Fundamentals (pp.4–6)

### What is a skill?
Folder containing: `SKILL.md` (required; Markdown with YAML frontmatter);
`scripts/` (optional; Python, Bash, etc.); `references/` (optional; docs loaded as
needed); `assets/` (optional; templates, fonts, icons used in output).

### Core design principles
- **Progressive disclosure**, three levels: (1) YAML frontmatter, always in the
  system prompt, enough to know when to use the skill; (2) SKILL.md body, loaded
  when Claude judges the skill relevant; (3) linked files in the skill directory,
  navigated only as needed.
- **Composability**: Claude can load several skills at once; a skill should not
  assume it is the only capability.
- **Portability**: skills work identically across Claude.ai, Claude Code, and the
  API, provided the environment supports the skill's dependencies.

### For MCP builders: Skills + Connectors
- Skills are the knowledge layer over a working MCP server.
- Kitchen analogy: MCP is the professional kitchen (tools, ingredients,
  equipment); skills are the recipes.
- Table: MCP = connectivity (connects Claude to a service such as Notion, Asana,
  Linear; real-time data and tool invocation; "what Claude can do"). Skills =
  knowledge (how to use the service; workflows and best practices; "how Claude
  should do it").
- Without skills: users connect the MCP and do not know what next; support
  tickets ask "how do I do X"; every conversation starts from scratch;
  inconsistent results from varied prompting; users blame the connector when the
  issue is workflow guidance.
- With skills: pre-built workflows activate automatically; consistent tool use;
  embedded best practices; lower learning curve.

## Chapter 2 — Planning and design (pp.7–13)

### Start with use cases
- Identify 2–3 concrete use cases before writing code. Example definition:
  "Project Sprint Planning" — trigger phrases ("help me plan this sprint",
  "create sprint tasks"); steps: fetch project status from Linear via MCP,
  analyze velocity/capacity, suggest prioritization, create labeled and
  estimated tasks in Linear; result: planned sprint.
- Questions: what the user wants; which multi-step workflows; which tools
  (built-in or MCP); what domain knowledge to embed.

### Common skill use case categories
- **Category 1: Document & Asset Creation** — consistent output (documents,
  presentations, apps, designs, code). Example: `frontend-design` skill (also
  docx, pptx, xlsx). Techniques: embedded style guides/brand standards, template
  structures, quality checklists before finalizing, no external tools needed.
- **Category 2: Workflow Automation** — multi-step processes with consistent
  method, including multi-MCP coordination. Example: `skill-creator`.
  Techniques: step-by-step workflow with validation gates, templates, built-in
  review and improvement suggestions, iterative refinement loops.
- **Category 3: MCP Enhancement** — workflow guidance over MCP tool access.
  Example: `sentry-code-review` (Sentry) — analyzes and fixes bugs in GitHub PRs
  using Sentry error data via MCP. Techniques: sequence multiple MCP calls, embed
  domain expertise, supply context users would otherwise give, handle common MCP
  errors.

### Define success criteria
Described as aspirational, rough benchmarks with some "vibes-based" assessment;
Anthropic says it is developing better measurement guidance.
- Quantitative: skill triggers on 90% of relevant queries (run 10–20 queries that
  should trigger; count auto-loads vs explicit invocations); completes workflow
  in X tool calls (compare with/without skill; count tool calls and tokens);
  0 failed API calls per workflow (watch MCP server logs, retry rates, error
  codes).
- Qualitative: users need not prompt about next steps (count redirections; beta
  feedback); workflows complete without correction (run the same request 3–5
  times, compare structure and quality); consistent across sessions (can a new
  user succeed first try).

### Technical requirements
- **File structure**: `your-skill-name/` with `SKILL.md`, `scripts/` (e.g.
  `process_data.py`, `validate.sh`), `references/` (e.g. `api-guide.md`,
  `examples/`), `assets/` (e.g. `report-template.md`).
- **Critical rules**:
  - File must be exactly `SKILL.md` (case-sensitive; not `SKILL.MD`, `skill.md`).
  - Folder name in kebab-case (`notion-project-setup`); no spaces, underscores,
    or capitals.
  - No `README.md` inside the skill folder; docs go in SKILL.md or
    `references/`. A repo-level README for humans is still fine for GitHub
    distribution.
- **YAML frontmatter** — "the most important part": it is how Claude decides
  whether to load the skill. Minimal format: `name` + `description` ("What it
  does. Use when user asks to [specific phrases].") between `---` delimiters.
- **Field requirements**:
  - `name` (required): kebab-case, no spaces/capitals, should match folder name.
  - `description` (required): must include both what it does and when to use it
    (trigger conditions); under 1024 characters; no XML tags (`<` or `>`);
    include phrases users might say; mention file types if relevant.
  - `license` (optional): for open source; common MIT, Apache-2.0.
  - `compatibility` (optional): 1–500 characters; environment requirements
    (intended product, system packages, network access).
  - `metadata` (optional): custom key-value pairs; suggested `author`,
    `version`, `mcp-server` (example: author ProjectHub, version 1.0.0,
    mcp-server projecthub).
- **Security restrictions**: forbidden in frontmatter — XML angle brackets;
  names containing "claude" or "anthropic" (reserved). Reason: frontmatter
  appears in the system prompt, so malicious content could inject instructions.

### Writing effective skills — the description field
- Cites Anthropic's engineering blog: metadata gives just enough for Claude to
  know when to use a skill — first level of progressive disclosure.
- Structure: [What it does] + [When to use it] + [Key capabilities].
- Good examples (paraphrased): a Figma handoff skill naming `.fig` uploads and
  phrases like "design specs"; a Linear workflow skill naming "sprint", "Linear
  tasks", "create tickets"; a PayFlow onboarding skill naming "onboard new
  customer", "set up subscription".
- Bad examples: too vague ("Helps with projects."); missing triggers
  ("Creates sophisticated multi-page documentation systems."); too technical,
  no user triggers (an entity-model implementation description).

### Writing the main instructions
- Recommended template after frontmatter: `# Skill Name` → `## Instructions` →
  numbered steps (each with explanation, example command such as
  `python scripts/fetch_data.py --project-id PROJECT_ID`, expected output) →
  `Examples` (user says / actions / result) → `Troubleshooting` (Error / Cause /
  Solution).

### Best practices for instructions
- **Be specific and actionable**: name the command
  (`python scripts/validate.py --input {filename}`) and list common failures
  (missing required fields; invalid date formats → use YYYY-MM-DD), rather than
  "Validate the data before proceeding."
- **Include error handling**: e.g. a "MCP Connection Failed" section for
  "Connection refused": verify server running (Settings > Extensions), confirm
  API key, reconnect.
- **Reference bundled resources clearly**: e.g. consult
  `references/api-patterns.md` for rate limits, pagination, error codes.
- **Use progressive disclosure**: keep SKILL.md to core instructions; move
  detail to `references/`.

## Chapter 3 — Testing and iteration (pp.14–17)

- Rigor levels: manual testing in Claude.ai (fast, no setup); scripted testing
  in Claude Code (repeatable across changes); programmatic testing via the
  skills API (evaluation suites on defined test sets). Match rigor to audience
  size (small internal team vs thousands of enterprise users).
- **Pro tip — iterate on a single task first**: iterate on one hard task until
  Claude succeeds, then extract the winning approach into a skill; uses
  in-context learning and gives faster signal; then broaden test cases.

### Recommended testing approach
1. **Triggering tests** — loads at the right times: triggers on obvious tasks,
   on paraphrases, not on unrelated topics. Example suite for a "ProjectHub"
   skill: three should-trigger prompts; should-not-trigger prompts such as a
   weather question, "Help me write Python code", "Create a spreadsheet" (unless
   the skill handles sheets).
2. **Functional tests** — correct outputs: valid outputs, API calls succeed,
   error handling works, edge cases covered. Given/When/Then example: create
   project "Q4 Planning" with 5 tasks → project created, 5 tasks with correct
   properties, all linked, no API errors.
3. **Performance comparison** — skill vs baseline. Illustrative: without skill
   — instructions each time, 15 back-and-forth messages, 3 failed API calls,
   12,000 tokens; with skill — automatic execution, 2 clarifying questions, 0
   failed calls, 6,000 tokens.

### Using the skill-creator skill
- Available in Claude.ai via the plugin directory or as a download for Claude
  Code. With an MCP server and top 2–3 workflows: functional skill in one
  sitting, often 15–30 minutes.
- Creating: generates skills from natural-language descriptions, formats
  SKILL.md with frontmatter, suggests trigger phrases and structure.
- Reviewing: flags vague descriptions, missing triggers, structural problems;
  identifies over/under-triggering risk; suggests test cases.
- Iterative improvement: bring edge cases/failures back to skill-creator.
- Invocation: ask Claude to use the skill-creator skill for a use case.
- Note in the guide: skill-creator helps design and refine but does not execute
  automated test suites or produce quantitative evaluation results.

### Iteration based on feedback
- Undertriggering signals: does not load when it should; users enable it
  manually; support questions about when to use it. Fix: more detail and
  keywords (especially technical terms) in the description.
- Overtriggering signals: loads for irrelevant queries; users disable it;
  confusion about purpose. Fix: negative triggers; more specificity.
- Execution issues: inconsistent results, API failures, user corrections. Fix:
  better instructions, error handling.

## Chapter 4 — Distribution and sharing (pp.18–20)

- Skills give an MCP integration an edge over MCP-only alternatives.

### Current distribution model (January 2026)
- Individuals: download the folder; zip if needed; upload via Claude.ai
  Settings > Capabilities > Skills; or place in the Claude Code skills directory.
- Organizations: admins deploy skills workspace-wide (shipped 2025-12-18);
  automatic updates; centralized management.

### An open standard
- Agent Skills published as an open standard, portable like MCP. Platform-
  specific skills can say so in the `compatibility` field.

### Using skills via API
- `/v1/skills` endpoint to list and manage skills; add skills to Messages API
  requests via the `container.skills` parameter; versioning and management in the
  Claude Console; works with the Claude Agent SDK.
- Surface table: end users, manual testing, ad-hoc workflows → Claude.ai /
  Claude Code. Programmatic apps, production at scale, automated pipelines and
  agent systems → API.
- Skills in the API require the Code Execution Tool beta (secure environment).
- Pointers: Skills API Quickstart; Create Custom Skills; Skills in the Agent SDK.

### Recommended approach today
1. Host on GitHub — public repo, README with install instructions (separate from
   the skill folder), example usage and screenshots.
2. Document in your MCP repo — link the skill, explain why both together, quick
   start.
3. Create an installation guide — clone or download ZIP; Claude.ai > Settings >
   skills > "Upload skill" (zipped folder); toggle it on and ensure the MCP
   server is connected; test with a sample request.

### Positioning your skill
- Describe outcomes, not features (e.g. "workspace set up in seconds instead of
  30 minutes" beats "a folder with YAML frontmatter").
- Tell the MCP + skills story: MCP gives access; skills teach the workflow.

## Chapter 5 — Patterns and troubleshooting (pp.21–27)

Patterns came from early adopters and internal teams; not prescriptive templates.

### Choosing your approach: problem-first vs tool-first
- Home Depot analogy. Problem-first: user describes an outcome; the skill
  orchestrates the MCP calls. Tool-first: user has e.g. Notion MCP connected; the
  skill teaches optimal workflows. Most skills lean one way.

### Pattern 1: Sequential workflow orchestration
- Use when steps must run in a specific order. Example "Onboard New Customer":
  `create_customer` (name, email, company) → `setup_payment_method` (wait for
  verification) → `create_subscription` (plan_id, customer_id from step 1) →
  `send_email` (welcome_email_template).
- Techniques: explicit ordering, inter-step dependencies, validation at each
  stage, rollback instructions for failures.

### Pattern 2: Multi-MCP coordination
- Example design-to-development handoff: Phase 1 Figma MCP (export assets,
  specs, manifest) → Phase 2 Drive MCP (folder, upload, share links) → Phase 3
  Linear MCP (tasks, attach links, assign) → Phase 4 Slack MCP (post summary to
  #engineering).
- Techniques: clear phase separation, data passing between MCPs, validation
  before the next phase, centralized error handling.

### Pattern 3: Iterative refinement
- Example report generation: draft (fetch via MCP, first draft, temp file) →
  quality check (`scripts/check_report.py`; missing sections, formatting, data
  errors) → refinement loop (fix, regenerate, re-validate, repeat to threshold)
  → finalization.
- Techniques: explicit quality criteria, iteration, validation scripts, knowing
  when to stop.

### Pattern 4: Context-aware tool selection
- Example file storage decision tree: >10MB → cloud storage MCP; collaborative
  docs → Notion/Docs MCP; code → GitHub MCP; temporary → local. Then call the
  tool, apply metadata, generate a link, explain the choice to the user.
- Techniques: clear decision criteria, fallbacks, transparency about choices.

### Pattern 5: Domain-specific intelligence
- Example payment processing with compliance: before processing, fetch details,
  check sanctions lists, jurisdiction, risk, document decision; process only if
  compliant, else flag and open a compliance case; audit trail of all checks and
  decisions.
- Techniques: domain expertise in logic, compliance before action,
  documentation, governance.

### Troubleshooting
- **Skill won't upload**:
  - "Could not find SKILL.md in uploaded folder" → file not named exactly
    `SKILL.md`; rename; check with `ls -la`.
  - "Invalid frontmatter" → YAML problem (missing `---` delimiters, unclosed
    quotes).
  - "Invalid skill name" → spaces or capitals (`My Cool Skill` → `my-cool-skill`).
- **Skill doesn't trigger**: revise the description; checklist — too generic?
  includes real trigger phrases? mentions file types? Debug by asking Claude when
  it would use the skill; it quotes the description back.
- **Skill triggers too often**: add negative triggers (e.g. "Do NOT use for
  simple data exploration (use data-viz skill instead)"); be more specific
  ("Processes PDF legal documents for contract review" not "Processes
  documents"); clarify scope.
- **MCP connection issues** (skill loads, calls fail): verify server connected
  (Claude.ai Settings > Extensions shows "Connected"); check auth (keys valid,
  scopes, OAuth refreshed); test the MCP without the skill — if that fails the
  MCP is at fault; verify tool names (case-sensitive).
- **Instructions not followed**: (1) too verbose → concise, bullets, move detail
  to references; (2) buried → critical instructions at top, `## Important` /
  `## Critical` headers, repeat key points; (3) ambiguous → explicit checks
  (e.g. before `create_project` verify non-empty name, ≥1 member, start date not
  past). Advanced: for critical validations bundle a script — code is
  deterministic, language interpretation is not (see the Office skills).
  (4) Model "laziness" → add explicit encouragement (thoroughness over speed,
  do not skip validation); the guide notes this works better in user prompts
  than in SKILL.md.
- **Large context issues** (slow or degraded): causes — skill too large, too
  many skills enabled, no progressive disclosure. Fixes — keep SKILL.md under
  5,000 words, move docs to `references/`; evaluate if more than 20–50 skills are
  enabled at once; selective enablement; skill "packs".

## Chapter 6 — Resources and references (pp.28–29)

- Start with the Best Practices Guide, then API docs. Listed: Skills
  Documentation, API Reference, MCP Documentation; blog posts (Introducing Agent
  Skills; Engineering Blog: Equipping Agents for the Real World; Skills
  Explained; How to Create Skills for Claude; Building Skills for Claude Code;
  Improving Frontend Design through Skills).
- Example skills: GitHub `anthropics/skills`.
- skill-creator: built into Claude.ai, available for Claude Code; generates and
  reviews skills.
- Support: Claude Developers Discord; bug reports to `anthropics/skills/issues`
  with skill name, error, repro steps.

## Reference A: Quick checklist (p.30)
- Before: 2–3 use cases; tools identified; guide and examples reviewed; folder
  structure planned.
- During: kebab-case folder; `SKILL.md` exact spelling; `---` delimiters; `name`
  kebab-case; description has WHAT and WHEN; no `<` `>` anywhere; clear
  instructions; error handling; examples; references linked.
- Before upload: trigger tests (obvious, paraphrased, unrelated); functional
  tests; tool integration; compressed as .zip.
- After upload: real conversations; monitor under/over-triggering; collect
  feedback; iterate description and instructions; bump metadata version.

## Reference B: YAML frontmatter (p.31)
- Required: `name`, `description`.
- All optional fields: `license` (e.g. MIT); `allowed-tools` (e.g.
  `"Bash(python:*) Bash(npm:*) WebFetch"`, restricts tool access); `metadata`
  (author, version, mcp-server, category, tags, documentation, support).
- Allowed: standard YAML types, custom metadata fields, descriptions up to 1024
  characters. Forbidden: XML angle brackets; code execution in YAML (safe YAML
  parsing); names with a "claude" or "anthropic" prefix (reserved). (Chapter 2
  says names *containing* these words; Reference B says *prefix*.)

## Reference C: Complete skill examples (p.32)
- Document skills (PDF, DOCX, PPTX, XLSX); example skills (workflow patterns);
  partner skills directory (Asana, Atlassian, Canva, Figma, Sentry, Zapier, and
  more). Clone and adapt as templates.
