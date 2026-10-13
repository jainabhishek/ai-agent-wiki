# How Claude Code works in large codebases: Best practices and where to start — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start
> Publisher: Anthropic (claude.com articles) · Date: 2026-05-14
> Captured: 2026-10-12 via curl (HTML downloaded, text extracted locally; condensed).

No single author byline; acknowledgements credit Anthropic's Applied AI team
(Alon Krifcher, Charmaine Lee, Chris Concannon, Harsh Patel, Henrique Savelli,
Jason Schwartz, Jonah Dueck, Kirby Kohlmorgen) and Amit Navindgi (Zoox) for
feedback. Category: Best practices. Product: Claude Code. Reading time 18 min.
First article in the "Claude Code at scale" series.

## Introduction
- Claude Code runs in production in multi-million-line monorepos, decades-old
  legacy systems, distributed architectures across dozens of repos, and orgs with
  thousands of developers. Challenges include per-subdirectory build commands and
  legacy code with no shared root.
- "Large codebase" here covers all of those, including C, C++, C#, Java, PHP;
  the article says Claude Code performs better than teams expect in those
  languages, especially with recent models.

## How Claude Code navigates large codebases
- Navigates like an engineer: traverses the file system, reads files, greps,
  follows references. Runs locally; no codebase index to build, maintain, or
  upload.
- RAG tools embed the codebase and retrieve chunks; at scale the embedding
  pipelines can't keep up, so retrieval returns renamed or deleted code with no
  staleness signal.
- Agentic search avoids this: no central index; each instance works on the live
  code.
- Tradeoff: works best when Claude has enough starting context to know where to
  look; navigation quality depends on codebase setup (layered CLAUDE.md files and
  skills). A vague pattern search across a billion-line codebase hits
  context-window limits first.

## The harness matters as much as the model
- Common misconception: capability is defined only by the model. In practice the
  harness (ecosystem around the model) determines performance more than the model
  alone.
- Five extension points, built in order (each builds on the previous): CLAUDE.md
  files, hooks, skills, plugins, MCP servers. Plus two capabilities: LSP
  integrations and subagents.
- **CLAUDE.md first**: auto-read every session; root for big picture,
  subdirectory files for local conventions. Keep to what applies broadly, since
  they load regardless of task.
- **Hooks make the setup self-improving**: beyond blocking mistakes, their more
  valuable use is continuous improvement. A stop hook can reflect on the session
  and propose CLAUDE.md updates while context is fresh; a start hook can load
  team-specific context dynamically per module. For lint/format, hooks enforce
  deterministically, more consistent than an instruction.
- **Skills** keep expertise on demand via progressive disclosure (e.g. a
  security-review skill, a doc-update skill). Skills can be path-scoped (e.g. a
  payments team's deploy skill bound to its directory so it never auto-loads
  elsewhere in the monorepo).
- **Plugins** distribute what works: bundle skills, hooks, MCP configs into one
  installable package so a new engineer gets the same setup on day one; updates
  via managed marketplaces. Example: a large retailer built a skill connecting
  Claude to its internal analytics platform for business analysts and shipped it
  as a plugin before the broad rollout.
- **LSP integrations** give IDE-grade navigation ("go to definition", "find all
  references"): symbol-level precision, distinguishing same-named functions
  across languages; without it Claude pattern-matches text and can hit the wrong
  symbol. An enterprise software company deployed LSP org-wide before rollout to
  make C/C++ navigation reliable. Called one of the highest-value investments for
  multi-language codebases.
- **MCP servers** extend reach to internal tools, data, APIs. The most
  sophisticated teams exposed structured search as an MCP tool; others connect
  docs, ticketing, analytics.
- **Subagents** split exploration from editing: isolated instance, own context
  window, returns only the result. Pattern: a read-only subagent maps a subsystem
  and writes findings to a file; the main agent then edits with the full picture.

Summary table (component — what — when it loads — best for — common confusion):
- CLAUDE.md — auto-read context file — every session — project conventions,
  codebase knowledge — using it for reusable expertise that belongs in a skill.
- Hooks — scripts at key moments — on events — consistent automated behavior,
  capturing session learnings — using prompts for things that should run
  automatically.
- Skills — packaged task instructions — on demand — reusable expertise — loading
  everything into CLAUDE.md instead.
- Plugins — bundled skills/hooks/MCP configs — always once configured —
  distributing a working setup — letting setups stay tribal.
- LSP* — real-time code intelligence via language servers — always once
  configured — symbol navigation, automatic error detection in typed languages —
  assuming it is automatic.
- MCP servers — connections to external tools/data — always once configured —
  access to internal tools — building MCP before the basics work.
- Subagents* — separate instances for specific tasks — when invoked — split
  exploration/editing, parallel work — running exploration and editing in the same
  session.
(*LSP is accessed through the plugin layer; subagents are a delegation capability,
not a configured extension point.)

## Three configuration patterns from successful deployments

### Making the codebase navigable at scale
Too much always-loaded context degrades performance; too little leaves Claude
navigating blind. Patterns:
- Lean, layered CLAUDE.md files, loaded additively as Claude moves through the
  tree. Root = pointers and critical gotchas only.
- Initialize in subdirectories, not the repo root; Claude walks up the tree and
  loads every CLAUDE.md on the way, so root context is not lost.
- Scope test and lint commands per subdirectory in subdirectory CLAUDE.md files;
  full-suite runs cause timeouts and waste context. Harder in compiled-language
  monorepos with deep cross-directory dependencies (may need project-specific
  build configs).
- Use ignore files to exclude generated files, build artifacts, third-party code;
  commit `permissions.deny` rules in `.claude/settings.json` so exclusions are
  version-controlled and shared. Developers working on code generators can
  override locally.
- Build codebase maps when directory structure doesn't help: a lightweight
  markdown file at the root listing each top-level folder with a one-line
  description. For hundreds of top-level folders, layer it (root = top level;
  subdirectory CLAUDE.md files = next level). For simple cases, @-mention files or
  directories.
- Run LSP servers so Claude searches by symbol, not string: grep for a common
  name returns thousands of hits; LSP filters to references of the same symbol
  before Claude reads anything. Requires a code intelligence plugin for the
  language plus the language server binary.
- Caveat: edge cases where hierarchical CLAUDE.md breaks down (hundreds of
  thousands of folders and millions of files; non-git version control) are
  deferred to future installments.

### Actively maintaining CLAUDE.md files as model intelligence evolves
- Instructions written for the current model can work against a future one.
  Example: a rule to break every refactor into single-file changes helped an
  earlier model but blocks a newer one from coordinated cross-file edits.
- Skills and hooks compensating for model or tooling limitations become overhead
  once fixed. Example: a hook intercepting file writes to enforce `p4 edit` in a
  Perforce codebase became redundant once Claude Code added a native Perforce
  mode.
- Do a meaningful configuration review every three to six months, and after major
  model releases when performance seems to plateau.

### Assigning ownership for Claude Code management and adoption
- Fastest rollouts had dedicated infrastructure investment before broad access: a
  small team (sometimes one person) wired up tooling first. One company: a couple
  of engineers built plugins and MCPs available on day one. Another: a dedicated
  AI-coding-tools team had infrastructure in place before rollout.
- Owners usually sit in developer experience / productivity. Emerging role:
  "agent manager", a hybrid PM/engineer managing the Claude Code ecosystem.
  Minimum viable version: a DRI owning configuration, settings, permissions
  policy, plugin marketplace, CLAUDE.md conventions.
- Bottom-up adoption fragments without someone centralizing what works
  (standard CLAUDE.md hierarchy, curated skills/plugins); otherwise knowledge
  stays tribal and adoption plateaus.
- Governance in large/regulated orgs: who controls available skills/plugins, how
  to avoid thousands of engineers rebuilding the same thing, ensuring AI code goes
  through the same review as human code. Start with an approved skill set,
  required code review, limited initial access; expand as confidence builds.
- Smoothest deployments formed cross-functional working groups early
  (engineering, infosec, governance) to define requirements and a rollout
  roadmap.

## Applying these patterns to your organization
- Claude Code assumes conventional environments: engineers as main contributors,
  Git, standard directory structures. Non-traditional setups (game engines with
  large binary assets, unconventional version control, non-engineer
  contributors) need extra configuration. Anthropic's Applied AI team helps adapt
  the patterns.
