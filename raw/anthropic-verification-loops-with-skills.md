# Building verification loops in Claude Code with skills — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/building-verification-loops-in-claude-code-with-skills
> Publisher: Anthropic (claude.com articles) · Date: 2026-07-22
> Captured: 2026-10-12 via curl (condensed).

Byline: Delba de Oliveira (Claude Code team). Category: Best practices.
Product: Claude Code. Stated reading time: 5 min.

## Intro

- An agentic coding session cycles through three steps: gather context, take
  action, verify results; on failure it loops back to gather more context.
- Claude already verifies against deterministic signals in the codebase: type
  checkers, linters, tests, runtime errors. Whatever Claude cannot infer is
  left as manual checks the developer performs.
- Thesis: convert those manual checks into verification loops (Claude checks
  and attempts to fix its own work) packaged as skills, so Claude closes its
  own feedback loop while the developer works elsewhere.
- Points newcomers to the companion article "getting started with loops".

## What is a verification loop?

- Definition: a repeating cycle in which the agent checks its own work (tests,
  linters, custom checks) and fixes failures before moving on.
- Packaged as a skill, every session applies the same checks automatically
  instead of depending on a human to remember them.

## Built-in verification loops

Built-in support listed by the article:

- **`/verify` skill** — builds, runs, and observes the change in the app.
- **Toolchain** — Claude acts on error codes and warnings from any tool you
  provide (e.g. a linter). Recommended practice: list exact build and test
  commands in `CLAUDE.md` so Claude need not infer them.
- **Code Review (research preview)** — managed multi-agent service that runs an
  automated review on PRs in enabled repos. Fix the finding by hand, or close
  the loop by commenting `@claude` on the finding (needs GitHub Actions set up).
- **GitHub Actions** — a job invokes Claude with a verification skill, so local
  checks also fire on every push or PR.
- **Spec validation** — a skill that checks each change against a markdown spec
  in the repo and tries to fix violations.
- **Rubrics in Claude Managed Agents (beta)** — outcomes graded against a rubric
  by a separate grader agent; failures loop back for rework automatically.

## Writing verification loops

- Trigger: you keep making the same small corrections each time Claude builds a
  feature. First step: write down everything you do every time.
- New project: write the best-practice version in plain English, as for a new
  teammate on day one.
- If you cannot articulate the check, ask Claude for best practices and edit;
  your points of difference are what to capture.
- Checks need not be qualitative. Example of a project-specific deterministic
  rule no generic linter catches: reject a migration that drops a column
  without a backfill step. Anything enforced by hand repeatedly qualifies.

## Make it a skill

- Fastest path: install the `skill-creator` plugin and let Claude interview you,
  e.g. `/skill-creator Create a skill for verifying frontend changes end-to-end.
  Interview me about my workflow.`
- Or hand-write a markdown file under `.claude/skills/` in the project.
- Minimal example, `.claude/skills/verify-log-hygiene/SKILL.md`: frontmatter
  `name: verify-log-hygiene`, a `description` saying error logs must include the
  request ID and never the request body, to be used when the diff touches error
  handling or logging, and `allowed-tools: [Read, Edit, Grep]`. Body: read
  error-handling paths in the diff; for each error-path log call confirm the
  request ID is present and no body, headers, or user payload is passed; report
  each violation as `file:line`, then fix it.
- Full schema: Anthropic's complete guide to building skills.

## Match the check to where it runs

Four trigger placements: standalone, embedded, chained, on every PR.

### Standalone

- Invoked deliberately after the artifact exists. Suits cross-cutting checks
  that should not fire on every change: pre-commit security scan, pre-PR
  accessibility audit, license-header check across a repo.
- Cost: each run is a turn you must remember. Signal you have outgrown it: you
  run it after every change. Then embed or chain it.

### Embedded

- Runs automatically as a step of the producing skill; the check belongs to one
  workflow.
- Simplest form: append one line to the producing skill. Example
  `.claude/skills/scaffold-component/SKILL.md` (`allowed-tools: [Read, Write,
  Edit, Bash, Glob]`) scaffolds `src/components/<Name>/` with `<Name>.tsx`,
  `<Name>.test.tsx` (React Testing Library mount test), and `index.ts`,
  following `src/components/Button/` and the `@/components/...` alias; the
  appended line says to run eslint on the new file and fix errors before
  reporting completion.
- Confirm the embed by running the skill on a fresh task; if the step does not
  run, the description or earlier instructions are not pulling it in.
- Only for skills you can edit (your own, or project-level SKILL.md under your
  control). Not for built-in or plugin-managed skills that updates overwrite;
  chain those instead.
- Skip for checks spanning workflows (use standalone).

### Chained

- One skill calls another at its end; several verified handoffs run end to end.
- Anthropic Claude Code team members chain: `/code-review` (bugs) →
  `/simplify` (clean the diff) → a `/verify` skill (end-to-end behavior) → a
  custom `/design` skill checking a `DESIGN.md` file when UI changed.
- Chaining adds verification to a skill you cannot modify: a wrapper skill,
  e.g. `.claude/skills/safe-refactor/SKILL.md`, runs `/simplify` first, then
  invokes `/verify-no-public-api-changes`.
- Turns a habit into a contract; the developer steps in only on escalation.
- Skip when steps are independent and sometimes run alone — chaining trades
  flexibility for automation. Chains can raise token spend; test before broad
  rollout.

### On every PR

- Once a chain is stable for your own changes, run the same skills and rubrics
  on every PR so teammates' changes pass the same gates regardless of whether
  they remembered to invoke them.
- Verification moves from personal to team infrastructure. Hold off on
  PR-wide gates while the chain is still changing, because each tweak becomes
  visible to the whole team.

## Closing process (six steps)

1. Pick the manual follow-up you did most often this week.
2. Try the built-in `/verify` skill first.
3. Write the procedure in plain English for a day-one teammate.
4. Hand it to `skill-creator`, or put the markdown file in `.claude/skills/`.
5. Invoke it on a new task; confirm the check runs; iterate.
6. Experiment with chaining for an end-to-end verification flow.

Claim: the more you encode, the more often Claude's first response lands close
to what you want.
