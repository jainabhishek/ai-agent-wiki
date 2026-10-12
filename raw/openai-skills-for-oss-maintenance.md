# Using skills to accelerate OSS maintenance — OpenAI (raw capture)

> Source: https://developers.openai.com/blog/skills-agents-sdk
> Publisher: OpenAI (Developers blog) · Date: 2026-03-09
> Captured: 2026-10-12 via the OpenAI blog full-text export plus curl of the page for byline (condensed).

Author: Kazuhiro Sera. Category tag: Codex.

## Introduction

OpenAI maintains the OpenAI Agents SDK repos (`openai-agents-python`,
`openai-agents-js`) with Codex, using repo-local skills, `AGENTS.md`, and
GitHub Actions to turn recurring work (verification, release prep, example
integration tests, PR review) into repeatable workflows. Reported throughput:
1 Dec 2025 – 28 Feb 2026 the two repos merged 457 PRs, versus 316 in
1 Sep – 30 Nov 2025 (Python 182 to 226; TypeScript 134 to 231). Scale (30-day
windows as of 2026-03-06): about 14.7M PyPI downloads (Python), about 1.5M
npm downloads (TypeScript).

Setup:
- repository policy in `AGENTS.md`;
- repo-local skills in `.agents/skills/`;
- optional scripts and references inside skills;
- the Codex GitHub Action when the same workflow should run in CI.
(The post also mentions a Codex for OSS programme for eligible maintainers.)

## Keep workflows in the repo

A skill is a small package of operational knowledge: `SKILL.md` plus optional
`scripts/`, `references/`, `assets/`. Progressive disclosure: the agent sees
`name` and `description` first, loads `SKILL.md` only when selected, and reads
references or runs scripts only when needed.

Python repo skills:
- `code-change-verification` — formatting, lint, type-check, tests when code
  or build behavior changes.
- `docs-sync` — audits docs against code for missing/incorrect/outdated docs.
- `examples-auto-run` — runs examples in auto mode with logs and rerun
  helpers.
- `final-release-review` — compares previous release tag with the release
  candidate; checks readiness.
- `implementation-strategy` — decides compatibility boundary and approach
  before runtime/API edits.
- `openai-knowledge` — pulls current OpenAI docs via the official Docs MCP.
- `pr-draft-summary` — branch-name suggestion, PR title, draft description at
  handoff.
- `test-coverage-improver` — runs coverage, finds largest gaps, proposes tests.

JavaScript repo adds:
- `changeset-validation` — changesets and bump levels must match the package
  diff.
- `integration-tests` — publishes to a local Verdaccio registry and verifies
  install-and-run across runtimes.
- `pnpm-upgrade` — updates pnpm toolchain, `packageManager`, and CI pins
  together (instead of broad search-and-replace).

Pattern: each skill has a narrow contract, a clear trigger, and a concrete
output. `docs-sync` and `test-coverage-improver` are report-first: they
inspect, prioritize, and ask for approval before editing. In Python,
`docs-sync` treats source docstrings and comments as the source of truth for
generated reference docs.

## Make workflows mandatory

`AGENTS.md` holds repository-level instructions that apply before the agent
starts; keep it small, highest-value rules at the top. Both repos use short
if/then rules: before runtime/API edits call `$implementation-strategy`; if
SDK code, tests, examples, or build behavior change call
`$code-change-verification`; if a JS package change affects release metadata
call `$changeset-validation`; for OpenAI API/platform work call
`$openai-knowledge`; at handoff call `$pr-draft-summary`. A compact sample
`AGENTS.md` has sections: Project overview (code under `src/agents/` or
`packages/*/src/`, tests under `tests/` or `packages/*/test/`, samples under
`examples/`); Mandatory skill usage; Build and test commands (Python:
`make format`, `make lint`, `make typecheck`, `make tests`; TypeScript:
`pnpm i`, `pnpm build`, `pnpm -r build-check`, `pnpm lint`, `pnpm test`);
Compatibility rules (preserve positional compatibility of public constructors
and dataclass fields). The Python file also says: append new optional
parameters at the end where possible; add compatibility tests if reordering is
unavoidable.

### Verification rules

`$code-change-verification` is conditional and mandatory: run it when runtime
code, tests, examples, or build/test behavior changed, and do not mark work
complete until it passes; docs-only work stays light. Python stack:
`make format`, `make lint`, `make typecheck`, `make tests`. JS stack, exact
order: `pnpm i`, `pnpm build`, `pnpm -r build-check`,
`pnpm -r -F "@openai/*" dist:check`, `pnpm lint`, `pnpm test`. The skill
encodes the repo's definition of "verified"; `AGENTS.md` makes it enforceable.

### Changeset validation

JS only, built on Changesets. When `packages/` or `.changeset/` changes, the
model must create or update the right changeset, validate the bump level, and
confirm it matches the diff. Codex judges the git diff; validation rules sit in
a shared prompt so local runs and GitHub Actions use the same logic. Policy
encoded: reuse the branch's existing changeset; one-line Conventional Commit
summary; before 1.0 avoid major bumps for normal features, treat labeled
preview-only additions as patch if behavior is unchanged; validate bump level
against actual package changes.

### Use current docs

`$openai-knowledge` is a thin wrapper around the OpenAI Docs MCP: look up
current docs (Responses API, tools, streaming, Realtime, MCP) instead of
answering from memory; if the MCP server is not configured, point to the Docs
MCP quickstart and the official endpoint.

### Prepare the PR handoff

`$pr-draft-summary` triggers only when work is effectively finished and
touched meaningful code, tests, examples, behavior-affecting docs, or build
config. It collects branch name, working-tree status, changed files, diff
stats, and recent commits, then outputs a rigid block: branch-name
suggestion, PR title, draft description (example: a fix for lazy tracing
initialization to avoid import-time fork hazards, resolving issue #2489).

## Write better descriptions

`description` is part of the routing contract — structural, not stylistic.
The Agent Skills specification makes `name` and `description` the required
frontmatter and loads only those at startup; the Codex docs and the "Skills
in OpenAI API" cookbook describe the same (hosted shell reads `name`,
`description`, and path first). Examples:
- `code-change-verification`: the vague version says only what it does; the
  actual version adds *when* (changes affecting runtime code, tests, or
  build/test behavior) and that it is mandatory.
- `pr-draft-summary`: the actual version says it is end-of-task, for
  moderate-or-larger changes (runtime code, tests, build config,
  behavior-affecting docs), and that output is a PR-ready block.
Lesson: if routing feels unreliable, fix metadata before adding code.

## Put mechanics in scripts

Split: interpretation, comparison, and reporting stay with the model;
deterministic repeated shell work goes in `scripts/`. The cookbook recommends
skill scripts be tiny CLIs: run from the command line, deterministic stdout,
fail loudly with usage/error messages, write outputs to known paths. Model
work: read source to infer intent, compare logs with intent, judge whether a
release diff carries real compatibility risk, write an actionable
explanation. Script work: run verification in fixed order; start example
runs, collect per-example logs, write rerun files; fetch the previous release
tag; helper commands `start`, `stop`, `status`, `logs`, `tail`, `collect`,
`rerun`. Heuristic: if the model rediscovers the same shell recipe each time,
make it a script.

## Automate integration tests

Two layers. (1) `examples-auto-run` (both repos). The runner came first:
non-interactive execution support that auto-answers common prompts;
auto-approves HITL, MCP, `apply_patch`, and shell actions where supported;
keeps unsuitable examples (realtime, Next.js apps) on an auto-skip list;
writes structured per-example logs; generates rerun files. Python wraps
`uv run examples/run_examples.py --auto-mode --write-rerun --main-log ...
--logs-dir ...`; JS wraps build checks then `pnpm examples:start-all`. Codex
then reads each example's source, infers intended flow, opens the matching
log, and compares intended vs. actual stdout/stderr — for every successful
example. A zero exit code is not enough for examples that call real APIs or
produce structured output. (2) JS `integration-tests`: publish to local
Verdaccio, install and run in Node.js, Bun, Deno, Cloudflare Workers, and a
Vite React app — catches post-publish/install/runtime problems.

## Add release checks

Release review: find previous release tag, diff against latest `main`, have
Codex inspect for backward-compatibility issues in public APIs and behavior,
regressions, and missing migration or release notes; then make a readiness
call. Example (openai-agents-python PR #2480): overall green with the Python
3.9 drop flagged as moderate risk (38 files changed, +1450/−789;
`requires-python = ">=3.10"`), with a release-note action. Gate rule: start
from "safe to release"; switch to blocked only on concrete evidence; every
blocked call carries a specific unblock checklist.

## Run workflows in CI

Move a skill to CI with the Codex GitHub Action once it is stable locally.
For public repos, trigger design matters as much as the skill. The Action's
security checklist: limit who can start the workflow; prefer trusted events
or explicit approvals; sanitize prompt inputs from PRs, commits, issues, or
comments; protect `OPENAI_API_KEY` with `drop-sudo` or an unprivileged user;
run Codex as the last step of the job. Risk in write-capable workflows on
untrusted input is mainly in triggers, input handling, and runtime
privileges.

## Use Codex in PR review

Codex GitHub PR auto review is used on most changes. For straightforward bugs,
regressions, and missing tests, OpenAI says relying on Codex as the required
review path is now safe enough in practice. Human review remains essential
for choices among valid options: API/architecture changes, behavior changes
affecting product expectations, compatibility promises or rollout; naming,
migration, release communication; cross-team alignment. `AGENTS.md` can
encode what matters for correctness review. This split was a significant
throughput contributor.

## Final thoughts

`AGENTS.md` says which workflows are required; `description` says when to
route into them; `scripts/` does the deterministic parts; the model does the
contextual parts; the Codex GitHub Action carries stable workflows into CI.
