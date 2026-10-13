# The AI-native SDLC playbook — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/the-ai-native-sdlc-playbook
> Publisher: Anthropic (claude.com articles) · Date: 2026-08-21
> Captured: 2026-10-12 via curl (HTML downloaded, text extracted locally; condensed).

Author: Louis Claxton. Category: Best practices. Products: Claude Enterprise,
Claude Code, Claude Tag. Reading time 40 min. A PDF version is offered (not
captured). Written from the Applied AI team's practice with customers.
Contributors thanked: Jim Blackhurst, Will Steuk, Jamal Arif.

## Code is no longer the bottleneck

- AI writes code far faster than a year ago, but approval gates, reviews,
  handoffs, and policies are unchanged, stalling gains.
- Traditional SDLC: six stages (plan, design, build, test, deploy, maintain),
  each owned by a different role (PM, architect, engineer, QA, release, ops), with
  handoffs by documents, tickets, sign-offs. Its heavy process (PRDs, estimation,
  security reviews) was designed when writing code was the costly step, and its
  controls assume humans do every step.
- When build runs faster than the process allows, three things become true:
  1. The bottleneck moves to the stages left and right of build — mainly plan,
     review/test, deploy — still at human speed.
  2. Controls stop matching reality: line-by-line human review cannot keep up
     once agents write most of the diff.
  3. Governance costs rise because exceptions still route through weekly or
     monthly committees.
- Example: security teams are sized for human output; with agent output, either
  the queue grows or code ships under-reviewed. Regulated orgs accept neither, so
  checks must keep pace with agents.

## What is an AI-native SDLC?

- Keeps the old control objectives with new enforcement. The flow becomes a loop
  with AI at each point and automated handover/triggering between stages. Also
  called agentic SDLC, AI SDLC, agentic software development.

### The shifts across the six stages

| Stage | Traditional | AI-native |
|---|---|---|
| Plan | Requirements by committee, workshops, sign-offs, written by hand | Claude synthesizes pain points from sources into `intent.md` (human readable, machine actionable) |
| Design | Analysts write spec, designers parse it | Requirements + design in one agent session, standards encoded as skills, versioned in git |
| Build | Handwritten tests/code; docs after | AI-generated tests and code; knowledge kept in versioned `CLAUDE.md` files and skills |
| Test | QA gates at stage boundaries | Continuous evals woven through implementation |
| Deploy | Humans review every line; governance in review cycles, inconsistent | Layers of agentic review; human review reserved for regulated/critical code; governance enforced as the AI acts, hooks as approval gates |
| Maintain | Humans watch production | Agents monitor deployments; a breached control band is diagnosed and written back as a new `intent.md` |

- Thread: the committed artifact. Each stage ends by committing one artifact
  (`intent.md`, `spec.md`, `plan.md`, diff + tests, PR with review findings,
  incident record) and the next stage starts by reading it. Markdown dominates
  early stages because product owner and agent can both act on it; from Build on,
  the artifact is code and its records. The commit chain is the audit trail (who
  asked, what the agent produced, who approved).
- Humans stay accountable for judgment calls; human attention follows the
  artifacts to review.

## Plays

- Plays are grouped in six non-linear stages. Each play: what changes, getting
  started, implementation steps, governance considerations, measurement
  (leading and lagging indicators). Modular; each names its prerequisites; a
  dependency graph orders adoption (start with plays that have no incoming
  arrows).
- Stage triggers: accepted `intent.md` → requirements/design pass; approved
  `spec.md` → plan mode; merged PR → pipeline; breached control band → next
  `intent.md`. Start by prompting each step by hand; end state is a loop where
  each accepted artifact fires the next gate and humans review what the agent
  flagged at gates.

## Stage 1 — Plan

### Capture as intent.md
- Intent enters from a person's idea, a ticket, or an incident alert (Stage 6).
  The originator brainstorms with Claude and produces a markdown proto-spec saved
  as `intent.md`; no PM translation step. The product owner reviews and corrects
  an agent-written `intent.md` before commit, whatever its origin.
- Traditional vs AI-native: backlog entries, stories, points, refinement
  meetings with ownership transferred at each handoff vs the originator's own
  words captured once; repeat processes encoded as skills.
- Prerequisites: none. Infrastructure: Claude access for non-engineers
  (claude.ai or Cowork); an agreed `intent.md` template; a shared,
  version-controlled intent home the product owner watches — simplest is an
  `intent/` folder in the product repo; a dedicated intent repo only when intent
  spans many repos; in a monorepo, a directory. Platform team sets it up once and
  decides write access. Non-git users commit via a version-control connector
  (e.g. GitHub) from claude.ai or Cowork.
- Steps: originator describes the problem in their own words → brainstorm until
  concrete (Claude asks analyst questions: scope, users, constraints, success) →
  Claude writes `intent.md` from the org template (can be a skill, signed off by
  a lead): problem, proposed outcome, affected users/systems, constraints, open
  questions → originator corrects → commit to the intent home.
- Example `intent.md`: "claims status self-service" — contact-center handlers
  spend about a third of call time on status-only queries; outcome: portal shows
  status, next step, expected date; constraints: no new PII in the portal
  session, existing authentication only; open question about third-party loss
  adjusters.
- Governance: the commit (author, timestamp, revision history) is the evidence;
  the product owner's accept/reject is recorded as merge or closed review.
- Measure — leading: time from first conversation to committed `intent.md`
  (expected: multi-week cycle → hours). Lagging: survival rate (share accepted
  into Design); number of `intent.md` changes after the first `spec.md` commit.

## Stage 2 — Design

### Requirements and design
- Claude turns the accepted `intent.md` into a requirements-and-design spec,
  guided by the org's skills for brand, security, compliance, UX. The product
  owner reviews but does not write it. Goal: a spec engineering can plan against,
  with concerns flagged.
- Front-end example: product owner mocks the design in Claude Design (beta) from
  `intent.md`, iterates, exports to Claude Code.
- Prerequisites: `intent.md`; brand/security/compliance/UX policies as skills.
  Infrastructure: a product owner with Claude access; no engineering skill
  needed.
- Steps: open a session with org skills and the `intent.md` → prompt names
  constraints and demands flagged concerns; run by hand first, then codify as an
  org-level slash command, then trigger it from the merge of `intent.md` via a
  non-interactive job that commits `spec.md` as a PR → product owner checks the
  spec against the idea and open questions → resolve flagged concerns with each
  policy owner before engineering sees it → commit `spec.md` next to `intent.md`
  → a human decides whether to progress to build (tech lead for higher-risk);
  acceptance starts the plan-mode play.
- Example prompt (paraphrased): read `intent.md`, produce a requirements and
  design spec for the existing codebase, apply available skills (brand, security,
  UX), save as `spec.md`, and describe areas of concern, especially contradicting
  policies.
- Governance: live policy applied while the spec is written, not weeks later in
  review. Spec, prompt, and skill versions in force are logged in version
  control; product owner signs off; concerns routed to named policy owners.
- Measure — leading: time between `intent.md` and `spec.md` commits. Lagging:
  `spec.md` commits dated after the first `plan.md` commit (requirements rework).

## Stage 3 — Build

### Claude Code plan mode as the default starting point
- Engineers start in plan mode with the approved `spec.md`; Claude interviews
  them; iterate until satisfied. In plan mode Claude reads the codebase without
  changing anything and cannot edit files until the plan is accepted.
- Prerequisites: `intent.md`/`spec.md` if they exist; `CLAUDE.md` helps.
  Infrastructure: Claude Code with repo access.
- Steps: start in plan mode → give `intent.md` and `spec.md`, ask for a plan
  naming files that change, order of work, and proving tests → interrogate (what
  could break, riskiest step, rejected alternatives) → iterate until an engineer
  who never saw the conversation could implement from the plan alone → commit as
  `plan.md` (PR review later checks the diff against it) → let Claude implement
  (often a single pass) → when implementation departs from the plan, update
  `plan.md` in the same commit; consider a hook to enforce sync.
- Example `plan.md` sections: Files that change; Order of work; Risks (e.g.
  claims-core API rate-limits at 50 rps, so the panel must cache); Proof (tests
  cover four claim states; screenshot matches approved mock).
- Governance: design review happens before code exists. Plan and revisions
  logged with acceptor; routine changes approved by the engineer, higher risk by
  tech lead/architect.
- Measure — leading: share of changes merging from the first implementation
  pass; time from plan approval to merged PR. Lagging: rework cycles per change;
  how often the merged diff still matches `plan.md`.

### Claude Code on auto mode
- After plan approval, auto mode applies each change without per-edit prompts.
  As guardrails mature (tuned `CLAUDE.md`, policy skills, blocking hooks, a test
  suite Claude can run), auto-accept becomes the default for routine work: tight
  `spec.md`, small blast radius, code already covered by tests.
- Review shifts from watching edits to reviewing artifacts after longer
  autonomous sessions. With worktrees it enables parallelism and underpins the
  autonomous loop of Stage 6.

### Sidebar: Legacy systems and the source of truth
- Existing artifacts live in Jira, regulated requirements tools, Figma, change
  boards — accepted by auditors, hard to displace. For every artifact name one
  source of truth; everything else holds a copy or link. Options:
  - Repo as source of truth: markdown is authoritative; the legacy system
    references commits. Cleanest for engineering-led orgs (one tool, one
    timestamp authority).
  - Legacy system as source of truth (Jira, ServiceNow, requirements tool):
    markdown is a working copy; Claude reads the record at session start and
    writes the outcome back via an MCP connector in the same session.
  - Linkage as the minimum bar: artifacts note the record ID; legacy records
    hold the commit SHA. A good starting point, accepting two sources of truth.

### The CLAUDE.md
- Gives Claude what a new joiner needs: conventions, commands, architecture,
  frequent mistakes. Maintained by the team; updated when mistakes happen.
- Prerequisites: none. Infrastructure: a repo, Claude Code, one engineer who
  knows the codebase.
- Steps: run `/init` → cut to day-one essentials (build/test/lint commands, key
  conventions, things Claude gets wrong) → check in at repo root, review changes
  like code → rule: when Claude makes a mistake twice, the correction goes in
  `CLAUDE.md` → keep it under a page (Claude reads all of it each session; stale
  text wastes context).
- Example (payments service): sections Commands (`make build`, `make test`,
  `make itest` needs docker, `make lint`), Conventions (Java 21, Spring Boot 3,
  no new Lombok, money always BigDecimal, every endpoint needs an integration
  test), Architecture (api/, core/, adapters/; Kafka schemas in schemas/, never
  edit generated classes), Things Claude gets wrong (don't bump dependency
  versions; legacy v1/ frozen, changes go in v2/).
- Governance: version-controlled, reviewable, code owners approve changes.
- Measure — leading: how often Claude repeats a mistake `CLAUDE.md` should catch.
  Lagging: time to first merged PR for a new team member.

### Skills as institutional knowledge
- Skills make institutional knowledge operational: explicit, versioned, broadly
  applied, centrally updated. Rule of thumb: a skill for knowledge that must be
  applied consistently; not for what belongs in `CLAUDE.md` or a prompt.
- Prerequisites: none (`CLAUDE.md` helps). Infrastructure: one policy with a
  named owner and written source of truth.
- Steps: pick knowledge enforced inconsistently today (security standard, API
  convention, brand rule) → write a skill: folder with `SKILL.md`, frontmatter
  says when it triggers, body says what to do; an engineer writes it from the
  policy owner's source with Claude's help → store at `.claude/skills/<name>/`
  or distribute org-wide via a plugin → test triggering by asking for the task in
  different ways → on policy change, update the skill with policy-owner sign-off
  → engineers get the new version next session.
- Example `.claude/skills/secure-api-review/SKILL.md`: triggers on creating or
  modifying external endpoints, reviewing API code, generating OpenAPI specs.
  Rules: every endpoint requires the gateway JWT (no anonymous routes outside
  /health); validate bodies against the OpenAPI schema and reject unknown
  fields; state-changing endpoints emit an audit event (actor, action, entity,
  timestamp); fields tagged pii never appear in logs/errors; run
  `scripts/check-endpoints.sh` and include its output.
- Governance: a skill is an advisory control — it makes compliance likely but
  nothing forces it. A policy that must always hold needs something
  deterministic behind it (a blocking hook or a PR-review re-check): the skill
  makes violations rare, the hook makes them near-impossible. Skill invocations
  are logged in session traces; policy owner reviews skill changes like code.
- Measure — leading: time from policy approval to skill merge. Lagging: PR
  review findings citing the policy should fall toward zero; if not, the skill
  isn't triggering or has drifted from the policy.

### Hooks as build-time guardrails
- Hook = deterministic layer behind the advisory skill. Build is where hooks fire
  most (file edits, shell commands). Uses: block edits to protected paths
  (generated classes, frozen package); run formatter/linter after edits; keep
  credentials out of the diff. Back any skill whose policy must hold without
  exception.
- Build hooks run on every matching action, so keep them fast and scoped to the
  changed file; heavy checks (full test suite) belong at commit or PR.
- Hooks that ask a human for approval belong at Stage 5 gates; an approval prompt
  during build puts a person on the critical path of all parallel sessions.

### Parallel sessions and subagents
- Parallel session: a full Claude Code instance on a separate task in its own git
  worktree, unaware of the others. Subagent: a scoped helper inside one session
  with its own context window and tool limits, for recurring jobs (e.g.
  verifying the app runs).
- Prerequisites: `CLAUDE.md`; the feedback loop (Stage 4) reduces supervision.
  Infrastructure: git repo (worktrees for isolation); permission settings tuned
  so sessions don't wait on prompts for commands the org deems safe.
- Steps: split work into tasks touching different files using `plan.md`; tasks
  sharing files run sequentially in one session → one worktree per task, e.g.
  `claude --worktree feature-auth` and `claude --worktree fix-rate-limit` → start
  with two or three sessions; ceiling = how many streams one person can review;
  add sessions only while review keeps up → turn repeated jobs into subagents in
  `.claude/agents/` (name, when-to-use description, allowed tools): code
  simplifier, verifier, researcher; check them into git.
- Example `.claude/agents/verifier.md`: tools `Bash, Read`; start the app with
  `make run`, exercise the changed behavior and the two nearest neighboring
  flows, report what was run/seen and mismatches with `plan.md`; report only,
  do not fix.
- Governance: controls come from repo configuration (hooks, permissions apply to
  all sessions); session activity logged and attributed to the engineer.
- Measure — leading: concurrent sessions per engineer while review quality holds
  (from the OpenTelemetry export); share of day steering vs waiting. Lagging:
  changes merged per engineer per week alongside rework rate.

## Stage 4 — Test

### Give Claude a feedback loop
- Always give Claude a way to verify its own work (tests, build, screenshot
  diff). Distinct from the verifier subagent: the loop runs throughout the task;
  the verifier is a final check in a fresh context window so the verdict is not
  colored by the assumptions that produced the code.
- Prerequisites: none. Infrastructure: test suite and build each runnable with
  one command; for UI, a browser tool or screenshot utility via MCP.
- Steps: wrap multi-step checks in one target (`make test`, `npm test`) exiting
  non-zero on failure → list each command in `CLAUDE.md` Commands with an example
  of healthy output → state a quantifiable target (e.g. all tests in a file pass,
  screenshot matches mock, endpoint returns 200 with the new field) → for bug
  fixes, write the failing test first, confirm it fails for the expected reason,
  commit it, then have Claude make it pass without editing the test → for UI,
  iterate implement/screenshot/compare (two or three rounds normal) → make
  verification part of "done" in `CLAUDE.md` (run tests, show output) → protect
  the loop: a hook blocks edits to test files during a fix task (or reject test
  changes in review).
- Example `CLAUDE.md` verification block: build must end with "Build succeeded";
  tests all green, never skip or delete a failing test; lint zero warnings; run
  all three before reporting done and paste the output; fix the code, not the
  test.
- Governance: enforced — verification before "done" and the test-file block, as
  hooks where guaranteed behavior is wanted. Evidence — literal toolchain output.
  Logged — session transcript (OpenTelemetry export to observability stack) and
  the PR check run. Approver — the code owner, who focuses on intent and risk.
- Measure — leading: first-pass CI success rate for agent changes. Lagging:
  review time per PR; change failure rate.

### Continuous evals in CI
- Evals are the AI-native equivalent of stage-gate QA: a suite that runs when the
  agent's configuration changes (new model, rewritten prompt). Live suite: as
  models improve, cases stop discriminating; add new ones from monitoring. Some
  teams run evals offline on a cadence instead.
- Prerequisites: `CLAUDE.md` and the feedback loop. Infrastructure: CI that runs
  Claude Code non-interactively; an API key with eval budget.
- Steps: platform engineer collects 20 to 50 real recent tasks with accepted
  outcomes → each becomes an eval (prompt + checks: tests pass, lint clean,
  behavior unchanged, policy followed) → run non-interactively in CI on a
  schedule and on any change to `CLAUDE.md`, skills, or hooks → gate config
  changes on results (a skill change that drops the pass rate is reviewed before
  merge) → every production incident gets an eval written by the owning team,
  kept as a regression test.
- Example `.github/workflows/agent-evals.yml`: triggers on pull_request paths
  `CLAUDE.md` and `.claude/**` and a nightly cron `0 2 * * *`; installs
  `@anthropic-ai/claude-code`; loops over `evals/*.json`, runs `claude -p` with
  the eval prompt, `--allowedTools "Read,Edit,Bash(make test)"`,
  `--output-format json`, and checks results with `./evals/check.sh`.
- Governance: pass-rate threshold enforced as a merge check; runs logged for
  comparison; config-owning team approves.
- Measure — leading: pass rate over time; time for an incident to become an
  eval. Lagging: regressions caught in CI vs found in production.

## Stage 5 — Deploy

Principle: the agent does everything up to the production gate and nothing past
it.

### AI in the PR review loop
- Claude reviews incoming PRs against org policy and addresses review comments
  on its own PRs; human review moves up to intent and risk. All PRs get identical
  review passes with severity-ranked findings.
- Prerequisites: updated `CLAUDE.md`; skills if passes enforce written policy;
  defined subagents. Infrastructure: managed Code Review (research preview,
  admin-enabled per repo) or `claude-code-action` in your own CI, with model calls
  via AWS Bedrock, Google Vertex, or Microsoft Foundry where needed; branch
  protection requiring code-owner approval.
- Steps: managed Code Review is the fastest start; use `claude-code-action` for
  pipeline control or routing through your cloud agreement → tech lead writes
  `REVIEW.md` at repo root with passes: bugs/logic; security; compliance against
  `spec.md`, `plan.md`, and design principles; defines Important vs Nit and what
  to skip → findings neither approve nor block alone; branch protection still
  needs a code owner; a platform engineer can gate merges on the severity tally
  the check run publishes → tagging `@claude` on a review comment makes Claude
  fix and push (via `claude-code-action`); in the managed service `@claude review`
  requests a fresh review; for Claude-opened PRs, a custom slash command can
  "babysit" the PR — sweep unresolved comments and failing checks until green and
  waiting only on code-owner approval → a mistake flagged a second time goes into
  `CLAUDE.md`; review also flags when a change makes `CLAUDE.md` stale → monthly,
  the tech lead rates findings and caps Nit volume; generated paths and anything
  CI enforces are excluded.
- Example `REVIEW.md`: three tagged passes (Bugs, Security, Compliance);
  Important reserved for breaking behavior, leaking data, breaching policy;
  at most five nits per review, the rest summarized as a count; skip
  `src/gen/` and CI-enforced items.
- Governance: separation of duties — the authoring agent cannot approve its own
  code; the PR history is the audit record; humans approve via branch
  protection. Links to "securing an AI-native SDLC at Anthropic".
- Measure — leading: time to first review (minutes); share of comments resolved
  without a human touching the branch. Lagging: defects/vulnerabilities caught
  pre-merge vs escaping to production.

### Hooks as approval gates
- Build hooks allow or block with no human. A hook can also ask: pause until a
  named person approves — what release gating needs. Hooks run wherever Claude
  acts (e.g. block migration/infra edits without a change ticket in Build; block
  test-file edits during fixes in Test).
- Prerequisites: none. Infrastructure: a written list of approvals the change
  process requires.
- Steps: leadership with change management and compliance list gates that must
  survive (change sign-off, release authorization, protected-path edits) →
  platform engineer expresses each as a hook that can allow, ask, or block →
  team hooks in `.claude/settings.json` in git; non-negotiable hooks in managed
  settings owned by platform/IT, which engineers cannot switch off → a block
  explains itself (reason and approval route shown in Claude's output).
- Example: `.claude/settings.json` registers a `PreToolUse` hook with matcher
  `Bash` running `${CLAUDE_PROJECT_DIR}/.claude/hooks/production-gate.sh`. The
  script reads `.tool_input.command` from stdin with `jq`; if the command
  contains both "deploy" and "production" and `RELEASE_APPROVAL` is unset, it
  prints a message to stderr and exits 2 (exit 2 blocks; the message goes to
  Claude); otherwise exit 0.
- Governance: gate condition enforced every time for everyone; allow/block
  decisions logged with timestamps; the gate defines what counts as approval.

### Worked example: Managed settings for a regulated enterprise
Deployed by the platform team via MDM or the admin console; engineers cannot
edit or override. Keys and values in the example:
- `permissions.deny`: `Read(.env*)`, `Read(./secrets/**)`, `WebFetch`,
  `Bash(curl *)`, `Bash(wget *)`.
- `permissions.allow`: `Bash(git *)`, `Bash(make build)`, `Bash(make test)`,
  `Bash(make lint)`.
- `permissions.disableBypassPermissionsMode`: `"disable"`.
- `allowManagedPermissionRulesOnly`: true.
- `sandbox`: `enabled: true`, `failIfUnavailable: true`,
  `allowUnsandboxedCommands: false`, `network.allowedDomains`
  [`git.internal.example.com`, `registry.npmjs.org`], `credentials.files` deny
  `~/.ssh` and `~/.aws/credentials`, `credentials.envVars` deny `GITHUB_TOKEN`.
- `allowManagedHooksOnly`: true. `disableSideloadFlags`: true.
  `allowManagedMcpServersOnly`: true.
- `strictKnownMarketplaces`: [{source: github, repo:
  example-corp/approved-plugins}].
- `requiredMinimumVersion`: "2.1.193".
What each buys:
- deny keeps secrets out of context and blocks tool-level egress; allow
  pre-approves the safe inner loop so the deny list doesn't cause prompt fatigue.
- `disableBypassPermissionsMode` + `allowManagedPermissionRulesOnly`: no engineer,
  project file, or CLI flag can widen rules.
- `sandbox` closes what permissions cannot: a WebFetch deny doesn't stop a shell
  command reaching the network; the OS-level domain allowlist blocks egress.
- `failIfUnavailable` + `allowUnsandboxedCommands: false` make the sandbox a gate:
  Claude Code refuses to start if the sandbox can't initialize, and a command
  failing in the sandbox can't be retried outside it.
- `credentials`: `permissions.deny` governs Claude's file tools, but a sandboxed
  shell command could still read `~/.ssh`/`~/.aws/credentials` by default; this
  block denies those reads and strips named secrets from sandboxed command
  environments.
- `allowManagedHooksOnly`: only the managed approval gates run.
- `disableSideloadFlags` + `strictKnownMarketplaces`: every skill, agent, hook,
  MCP server arrived via the approved marketplace.
- `allowManagedMcpServersOnly`: tool surface is a platform-owned allowlist.
- `requiredMinimumVersion`: refuses to start below the assessed version floor.
- A starting point, not a copy-paste recommendation: every deny trades against
  capability; balance by the repo's data classification. Settings reference:
  code.claude.com/docs/en/settings.
- Measure (hooks) — leading: wait time per approval gate (every hook decision is
  written to the OpenTelemetry export with timestamp and verdict). Lagging: gate
  violations reaching production before vs after hooks.

### CI/CD integration and deployment
- Run Claude Code non-interactively in CI/CD, sandbox execution, expose
  deployment via MCP, rehearse rollback in advance.
- Prerequisites: PR review loop and hooks as approval gates (gates must exist
  before automation accelerates through them). Infrastructure: CI with
  `claude-code-action` or any runner calling `claude -p`; model access via API or
  Bedrock/Foundry/Vertex; MCP servers for deployment targets; a sandbox profile
  for agent jobs with no standing production credentials.
- Steps: start with read-only judgment steps (`claude -p` to triage a failed
  build, summarize a flaky test, draft a changelog) → add write steps behind
  existing gates (fix lint, update generated docs, address `@claude` comments);
  all agent writes arrive as PRs; no route to push to main → sandbox: containers,
  network policy, short-lived scoped tokens, no production credentials by default
  → expose deploy/status/rollback as MCP tools scoped per environment (an
  allowlist, not a shell script with credentials) → tier autonomy by environment:
  dev deploys freely; production — agent prepares, release manager authorizes, a
  hook enforces; staging in between → rollback is the most rehearsed path: one
  command the agent can run, exercised regularly in staging (Stage 6 calls it).
- Example pipeline step: on failure, `claude -p` reads `out/build.log`,
  identifies the likely cause, says flaky vs real, writes a three-line PR summary
  appended to `triage.md`.
- Governance: branch protection makes agent writes PRs; production deploy hook
  blocks until a named release manager authorizes; each non-interactive run acts
  under the agent's own identity so logs separate agent actions from the
  triggering engineer; per-environment permission tiers.
- Measure — leading: share of pipeline failures triaged without paging a human.
  Lagging: DORA metrics.

## Stage 6 — Maintain

### Maintenance and closing the loop
- Earlier stages need a human to start them; this stage runs Claude autonomously.
  E.g. a monitoring agent creates `intent.md` from a bug ticket and flows through
  requirements, plan, build, test, review headless, with an independent
  confidence gate between stages (a deterministic check or an adversarial
  reviewing agent) deciding continue vs escalate to a human.
- Traditional: reactive; alerts at 3 a.m. missed; tickets sit; post-mortem
  actions may never reach the code. AI-native: a trigger (control-band breach,
  ticket, channel message, schedule) invokes Claude with no person in the path;
  Claude diagnoses, acts only via gated routes, writes `intent.md`.

### Closing the loop
- A deterministic script watches production and invokes Claude on a control-band
  breach.
- Prerequisites: `intent.md` format; accelerated PR review; hooks as action
  boundary; a CI/CD rollback path. Infrastructure: a metrics store (Prometheus,
  CI API, etc.); repo read access; non-interactive Claude Code in CI or the Agent
  SDK for a webhook-receiving service.
- Steps: pick one metric with a stable rolling baseline (CI test failure rate,
  post-deploy 5xx rate, PR cycle time) → detection script: mean and standard
  deviation over a rolling window with Western Electric (or similar) rules to
  catch drift and spikes; version-controlled, unit-tested, fully deterministic,
  no model → response tiers in version-controlled `bands.yaml`: 1σ log only; 2σ
  invoke Claude read-only to diagnose; 3σ Claude may act, only by opening a PR
  into the review gate or triggering a pre-approved runbook → trigger layer:
  scheduled GitHub/GitLab workflow, monitoring webhook, or in-network cron;
  Claude runs stateless as a CI step or Agent SDK service in a sandboxed
  container → agent writes its diagnosis as `intent.md` (anomaly and evidence,
  proposed outcome, affected systems, open questions) → service owner or on-call
  triages (fix now, schedule, dismiss); dismissals tune the bands → when a fix
  ships, add an eval for the incident.
- Example `bands.yaml`: metric `ci_test_failure_rate`, baseline `rolling_30d`,
  rules `western_electric`; tiers 1sigma log; 2sigma diagnose with tools
  `Read,Grep,Bash(gh run view *)`; 3sigma propose with routes `pull_request` and
  `runbook:rollback-deploy`.
- Governance: tier boundaries from versioned config; permissions and managed
  settings deny production access; invocations, findings, triage logged; service
  owner approves; runbooks pre-approved.
- Measure — leading: time from breach to `intent.md` in the triage queue.
  Lagging: share of findings becoming merged fixes; repeat incidents of the same
  class.
- Examples: CI failure rate > 3σ → quarantine flaky test or open revert PR;
  post-deploy 5xx > 3σ with a deploy in the window → trigger existing rollback
  pipeline; PR cycle time drift → report to engineering leadership (process
  metrics too).
- Detection stays deterministic; Claude is invoked on breach; the tier sets what
  it may do.

### Recurring codebase scans
- A security scan is a point-in-time statement about a codebase under a given
  model; both go stale (code changes weekly; each model generation finds what the
  last missed). Run scans on a schedule, no human in the invocation path, with
  findings through the same gates as any change.
- Claude Security: hosted scheduled scanning. Connect a GitHub repo; scans run on
  Claude Mythos 5 in Anthropic's infrastructure; each finding validated before
  reporting with a confidence rating; suggested patches reviewed/applied in
  Claude Code on the web; the org gets findings without model access.
- Prerequisites: PR review gate and hooks as approval gates; `intent.md` format
  for large findings. Infrastructure: Claude Enterprise (public beta); Anthropic
  GitHub App on target repos (cloud github.com); Claude Code on the Web enabled;
  Extra Usage on with a spend limit; premium seats for scan runners; admin
  switch at `claude.ai/admin-settings/claude-code`. Billed on consumption at
  Mythos 5 rates.
- Steps: security lead connects repos and groups them into projects (repo,
  service, team) for clear ownership → first full scan of most critical repos as
  baseline, including previously scanned ones (expect findings in "clean" code)
  → schedule per project; weekly default for active services; scope to a
  directory/branch for large or mixed repos → triage with confidence rating;
  dismiss with a reason so findings don't return as new → bounded finding: open
  the suggested patch in Claude Code on the Web, review, send through the PR
  gate (the proposing agent cannot approve) → wider issues become `intent.md` →
  after a fix ships, add an eval for the vulnerability class → export findings
  as CSV/Markdown or via webhooks so existing trackers stay the system of record.
- Governance: admin controls set connected repos, scan seats, spend limit; every
  finding has validation result and confidence; every dismissal has a reason.
  Fixes reach production only via PR review and branch protection. Augments,
  does not replace, static analysis and dependency scanning, which stay in CI.
- Measure — leading: share of repos on a schedule; time from finding to patch in
  PR review. Lagging: vulnerabilities found by scans vs in production/external
  reports; findings per scan trend on repeatedly scanned repos.

### Claude on call with Claude Tag
- Incidents also arrive via Slack/Teams. Claude Tag (public beta, in Slack) makes
  Claude a channel member under its own identity — a first responder for each
  incident. Anyone in the channel can guide the response; channel history adds
  auditability. Via MCP, Claude verifies the metric is back to baseline, confirms
  in-thread, and writes the post-mortem to a version-controlled lessons file
  future investigations read.
- Also picks up tickets (via MCP) or channel requests: small fixes arrive as PRs
  through the review gate; larger work becomes `intent.md`.

## Closing thoughts
- Models and harnesses now allow transforming the whole SDLC, not only code
  production, while keeping human judgment central and meeting enterprise
  governance.

### Resources and acknowledgments
Docs list in rollout order (code.claude.com/docs/en/...): admin-setup, settings,
server-managed-settings, permissions, sandboxing, hooks-guide, hooks, skills,
plugin-marketplaces, managed-mcp, third-party-integrations, network-config,
monitoring-usage, analytics, security; plus platform.claude.com Compliance API.
