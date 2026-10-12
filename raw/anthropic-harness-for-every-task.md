# A harness for every task: dynamic workflows in Claude Code — Anthropic (claude.dev blog) (raw capture)

> Source: https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/
> Publisher: Anthropic (claude.dev blog) · Date: 2026-06-02
> Captured: 2026-10-12 via WebFetch + curl of the page HTML (condensed).

Authors: Thariq Shihipar and Sid Bidasaria. Reading time 11 min. (Other dates on
the page belong to the related-posts list.)

## Introduction (untitled)

- Claude Code can write its own multi-agent harness for a given task: a
  **dynamic workflow**. Workflows are shareable and reusable.
- They can reproduce custom harnesses Anthropic previously hand-built for
  Research, security analysis, agent teams, and Code Review.
- They often use more tokens, so they suit complex, high-value tasks.

## Example prompts

- Reproduce a test that fails ~1 in 50 runs; form competing race-condition
  theories; continue until one survives the evidence.
- Mine the last 50 sessions for repeated corrections and turn them into
  `CLAUDE.md` rules.
- Search #incidents in Slack over six months for recurring root causes with no
  ticket.
- Investor, customer, and competitor agents critique a business plan.
- Rank 80 resumes for a backend role, double-check the top ten, and build the
  rubric via `AskUserQuestion`.
- Brainstorm CLI names; run a tournament for the top three.
- Rename the `User` model to `Account` everywhere.
- Verify every technical claim in a blog draft against the codebase.

## How dynamic workflows work

- A workflow is a **JavaScript file** built from three primitives (Fig A):
  - `agent(prompt, opts)` — spawn one subagent; only `prompt` required. Options:
    `schema` (validated JSON output), `model` (opus / sonnet / haiku),
    `isolation` (worktree / remote), `agentType` (which subagent).
  - `parallel()` — fan out and wait for all.
  - `pipeline()` — stream each item through every stage.
- Standard JS built-ins (JSON, Math, Array) available. Model and worktree
  isolation chosen per agent. An interrupted workflow continues when the session
  is resumed.

## Why dynamic workflows

One context window that both plans and executes shows three failure modes on
long, parallel, structured, or adversarial tasks:
- **Agentic laziness** — declares done after partial progress (e.g. 35 of 50
  items in a security review).
- **Self-preferential bias** — favors its own findings when verifying them.
- **Goal drift** — loses original requirements, especially after compaction.
Separate subagents with their own context and a focused goal counter these.

## Dynamic vs static workflows

- Static workflows (Claude Agent SDK, `claude -p`) must handle every edge case,
  so they are generic.
- "With Claude Opus 4.8 and dynamic workflows", Claude writes a harness tailored
  to each request (Fig B).
- Example — a checkout-service migration question: static harness = five web
  searches and a generic report; dynamic workflow reads billing code, checks
  features against the provider's docs, prices them at real volume, runs a
  devil's advocate, and gives a specific recommendation.

## Helpful patterns when using dynamic workflows

Start by asking for a workflow, or use the trigger word `ultracode`. Six
composable patterns (Fig C):
- **Classify-and-act** — a classifier routes to other agents or sets output
  type.
- **Fan-out-and-synthesize** — many clean-context steps, then merge structured
  outputs; synthesis waits for all fan-out agents.
- **Adversarial verification** — a separate agent checks each output against a
  rubric.
- **Generate-and-filter** — generate many ideas; filter by rubric/verification;
  dedupe.
- **Tournament** — N agents attempt the task with different approaches;
  pairwise judging picks a winner.
- **Loop until done** — repeat until a stop condition (no new findings, no
  errors in logs).

## Use cases

- **Migrations and refactors** — Bun was rewritten from Zig to Rust using
  workflows. Break work into units (callsites, failing tests, modules); one
  subagent per fix in a worktree; another agent reviews adversarially; merge.
  Tell agents to avoid resource-heavy commands so many can run in parallel.
- **Deep research** — `/deep-research` skill: fan out web searches, fetch
  sources, verify claims adversarially, produce a cited report. Also Slack
  status reports, tracing codebase features.
- **Deep verification** (Fig D) — claim extractor finds every factual claim; one
  checker agent per claim; optional source auditor.
- **Sorting** (Fig E) — for 1,000+ items: tournament bracket, pairwise
  comparison, or bucket-rank-then-merge. One agent per comparison, so no single
  context holds all items. Example: support tickets by bug severity.
- **Memory and rule adherence** (Fig F) — one verifier agent per rule in a clean
  context, then a skeptic agent filters false positives (example diff +142/−87
  checked against five rules, flags on lines 42 and 90). Reverse direction: mine
  sessions and review comments for repeated corrections, cluster, verify each
  candidate rule, distill survivors into `CLAUDE.md`.
- **Root-cause investigation** — independent hypotheses from disjoint evidence
  (logs, files, data); verifiers and refuters test each. Applies to sales drops,
  pipeline failures, post-mortems.
- **Triaging at scale** (Fig G) — quarantine: reader agents with read-only tools
  process untrusted content and emit structured summaries; a separate
  high-privilege actor agent acts only on those summaries (fix + open PR, or
  escalate to a human). Pair with `/loop` for continuous operation.
- **Exploration and taste** — many candidate designs/names judged by a review
  agent against a rubric or ranked by tournament.
- **Evals** — run agents in a worktree; comparison agents grade outputs against
  a rubric (e.g. refining a skill).
- **Model and intelligence routing** — a classifier agent researches the task
  (e.g. size/shape of the auth module) and routes to Sonnet or Opus by
  complexity.

## When not to use dynamic workflows

- New feature; can use significantly more tokens. Ask whether the task needs
  more compute — routine coding rarely needs e.g. a five-reviewer panel.
- Same logic as multi-agent vs single-agent: parallelism and specialization must
  pay for their coordination cost (links a related Anthropic post).

## Tips for building dynamic workflows

### Prompting
- Detailed prompts naming the patterns above work best. Workflows can be small —
  a "quick workflow" to adversarially review one assumption.

### Combine with /goal and /loop
- `/loop` for repeated runs (triage, research, verification); `/goal` for a hard
  completion requirement.

### Token usage budgets
- State a cap in the prompt, e.g. "use 10k tokens".

### Saving and sharing dynamic workflows
- Press `s` in the workflow menu to save a run; save to `~/.claude/workflows` or
  distribute via a skill. Skill folder example `~/.claude/skills/deep-verify/`
  with `SKILL.md`, `verify-claims.workflow.js`, `rubric.md`; reference the
  workflow from `SKILL.md`. Frame skill workflows as templates, not scripts to
  run verbatim.
- Dynamic workflows panel (Fig H) lists runs with agent count, tokens, duration:
  `review-changes` 14 agents / 482k tokens / 6m 12s; `find-flaky-tests` 6 agents
  (running); `deep-research` 22 agents / 1.1M tokens / 11m 3s. Keys: select,
  enter = view, `s` = save, `esc` = close.

## A new starting point for discovery

- Workflows are a new extension point for Claude Code. Related reading:
  Anthropic's post on three harness design patterns for building with Claude.
