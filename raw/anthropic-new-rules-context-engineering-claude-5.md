# The new rules of context engineering for Claude 5 generation models — Anthropic (claude.dev blog) (raw capture)

> Source: https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/
> Publisher: Anthropic (claude.dev blog) · Date: 2026-07-24
> Captured: 2026-10-12 via WebFetch + curl of the page HTML (condensed).

Author: Thariq Shihipar, member of technical staff. Section: Engineering.
Reading time 7 min. (Other dates on the page belong to the related-posts list.)

## Introduction (untitled)

- The user prompt is a small part of what Claude receives; most context comes
  from the system prompt, Skills, CLAUDE.md files, memory, and other sources.
  Context is reused across many requests, so it cannot be as specific as a
  prompt.
- Headline result: Anthropic removed **over 80% of Claude Code's system prompt**
  for "models like Claude Opus 5 and Claude Fable 5" with **no measurable loss**
  on its coding evaluations. No API model IDs are given; the post frames its
  guidance for the "Claude 5 generation".
- The practices are built into `claude doctor` — run `/doctor` in Claude Code to
  rightsize skills and CLAUDE.md files.

## Unhobbling Claude

- Anthropic was over-constraining Claude Code via its system prompt, CLAUDE.md
  files, and skills.
- Internal transcripts showed conflicting messages in one request (e.g. a
  "leave documentation as appropriate" style instruction alongside an
  all-caps no-comments rule). Claude can usually infer intent but must spend
  extra reasoning reconciling clashes.
- Constraints once needed to avoid worst-case behavior can now largely be
  deleted; the model uses surrounding context and judgement instead.
- Claude Code now has more context channels — memory, artifacts, skills — so
  CLAUDE.md is no longer the sole source of memory and guidance.

## Then and now

Six earlier best practices that "had become myths":

### Then: Give Claude rules → Now: Let Claude use judgement
- Early Claude Code system prompt carried strong blanket rules to avoid worst
  cases: default to no comments, at most one short comment line, no multi-line
  docstrings, no planning/analysis documents unless asked (paraphrased).
- These were wrong for a subset of prompts (user documentation preferences,
  complex code needing multi-line comments) but were an accepted trade-off for
  older models.
- New system prompt instead tells Claude to write code that matches the
  surrounding code's comment density, naming, and idiom (paraphrased).

### Then: Give Claude examples → Now: Design interfaces
- Previously the top tool-use rule was to give usage examples. With the newest
  models, examples constrain Claude to a narrow exploration space.
- Instead design the tools, scripts, and files: make parameters expressive.
- Figure: the TodoWrite tool description went from ~9,100 characters of
  when-to-use lists and worked examples to a one-line description plus a
  `status` enum (`pending`, `in_progress`, `completed`) and one rule — only one
  task `in_progress` at a time.

### Then: Put it all upfront → Now: Use progressive disclosure
- Code-review and verification instructions used to sit in the system prompt;
  they are now separate skills Claude calls selectively.
- Progressive disclosure also applies to tools: some tools are deferred-loading
  and must be found via `ToolSearch` before use, so more tools (e.g. the Task
  tools) cost no context until needed.
- Do not make CLAUDE.md / SKILL.md a central repository of every practice; use a
  tree of files loaded at the right time.

### Then: Repeat yourself → Now: Simple tool descriptions
- Earlier models sometimes needed repeated instructions and weighted
  end-of-context instructions more, so tools were referenced in both the system
  prompt and the tool description.
- Now: delete repeats; put tool-usage guidance in the tool description only.

### Then: Memory in CLAUDE.md files → Now: Auto-memory
- Users were told to save memories to CLAUDE.md with the `#` hotkey. Claude now
  saves relevant memories automatically.

### Then: Simple specs → Now: Rich references
- Plan mode relied on markdown plan files; specs were stored in the repo.
- Claude now handles richer references: HTML artifacts (artifacts feature),
  detailed test suites, a function in another codebase to port.
- Rubrics are references that encode taste (e.g. what good API design looks
  like); Claude applies them via dynamic workflows that spin up verifier agents.

## Applying this to your context

Context as a stack (figure): user prompt on top; references (@-mentioned files,
specs, mockups, codebases, artifacts); then system prompt, CLAUDE.md, skills,
memory.

### System prompt
- Tied to the product: tells Claude what product it is in and what it is doing.
- Claude Code users will likely never modify it; builders of their own agent
  harness should invest most effort here.

### CLAUDE.md
- Lightweight: briefly say what the repo is for; spend most tokens on codebase
  gotchas (e.g. "all types live in one monolithic file").
- Omit what Claude can discover from the file system or repo.
- Use progressive disclosure — e.g. a verification skill referenced from
  CLAUDE.md.

### Skills
- Lightweight guides to help Claude find information when needed; avoid
  over-constraining except in highly important areas.
- Split long skills into many files.
- Best for opinions, knowledge, or practices particular to you, your team, or
  your product.

### References
- @-mention files to include them (specs, mockups, whole codebases).
- Prefer references that are code: high-fidelity and in a language Claude
  knows; an HTML mockup generally beats a prose description or a screenshot.

## Try simplifying

- Audit system prompt, skills, and CLAUDE.md for over-constraint and conflicts.
- `claude doctor` (`/doctor`) helps do this automatically.
- Points to the "Fable field guide" for prompting more advanced models.
