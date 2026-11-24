# Building security review into your SDLC with Codex Security — OpenAI developer blog (raw capture)

> Source: https://developers.openai.com/blog/building-security-review-into-your-sdlc-with-codex-security
> Publisher: OpenAI (developer blog) · Date: 2026-11-23 (byline "Nov 23, 2026")
> Author: Vanessa Sauter (Cyber Deployment Engineer at OpenAI)
> Captured: 2026-11-24 via curl of developers.openai.com/blog/llms-full.txt
> (markdown export); author and date read from the article HTML.
> Condensed paraphrase, not a copy. Headings, numbers, CLI flags, file names,
> and skill names are kept; example documents, policies, and workflow YAML are
> summarized by their key names. Screenshots are not captured.

## Intro

AI speeds up the SDLC and puts pressure on security workflows. Manual PR
security review cannot scale at the pace agents produce and revise code.
Application security used to move at human speed: a design review up front, a
hand review of the PRs judged riskiest, and occasional backlog triage. The
post argues for agentic security workflows that match the speed of an agentic
SDLC. It gives four principles, then shows the workflows in Codex Security and
its CLI.

## Four principles for agentic security workflows

1. **Give agents system-specific context.** Agents need the application's
   assets, trust boundaries, and security requirements. Threat models,
   repository security policies, and architecture documents supply them; keep
   them reviewed and current.
2. **Integrate review into development.** Feedback should reach developers while
   changes are in progress: local work, PRs, and CI, with clear triggers.
3. **Set review scope and reporting thresholds deliberately.** Diff scans,
   component assessments, and full-repo scans each answer a different question.
   Thresholds should reflect risk; sensitive areas such as authentication and
   billing get more attention.
4. **Make findings inspectable.** Reports should give code locations,
   reasoning, severity, confidence, and remediation, and state what was
   reviewed, excluded, or deferred.

## Seeding context for security reviews

### Differences among threat models, `AGENTS.md`, `SECURITY.md`, and knowledge bases

- `AGENTS.md` holds shared engineering instructions.
- A **threat model** records what is actually at stake and exposed: the assets,
  where input enters, which inputs an attacker controls, trust boundaries,
  assumptions about authentication, privileged operations, and risky parts. Commit it as
  `docs/security/threat-model.md` so Codex Security can use it in PR reviews and
  scans. The example threat model names untrusted JSON and file
  uploads, the boundary from the public API to internal billing and identity
  services, unauthenticated users or compromised tenant accounts as attackers,
  and tenant data, billing mutations, and service credentials as assets.
- `SECURITY.md` tells Codex how the organization wants that reality evaluated
  and reported. The example has sections `Security Invariants` (billing
  mutations authorized per tenant; bounded upload parsing; credentials never
  returned to clients), `Reportable Findings`, `Severity Context` (cross-tenant
  access = Critical; single-tenant unauthorized mutation = High), and
  `Out of Scope` (development-only tools).
- A **knowledge base** supplies supporting documents to particular scans
  (architecture, policies, extra threat models, operational context). The
  example `docs/security/payment-service-context.md` has sections: Purpose,
  Deployment and Exposure, Authentication and Authorization, Trust Boundaries
  (five numbered boundaries), Sensitive Assets and Operations, Important Data
  Flows (charge creation; webhook processing with signature check over raw
  bytes, a five-minute timestamp window, duplicate-ID suppression), Relevant
  Code, Security Assumptions, and Known Limitations. It includes details such as
  refunds above £1,000 needing a recorded approval and internal requests using
  workload identity rather than trusting network location. Endpoints named:
  `POST /api/payments` (internet-facing) and `POST /internal/refunds` (support
  service only); workers consume the `payment-events` queue. Relevant Code lists
  `src/http/payments.ts`, `src/http/refunds.ts`, `src/webhooks/provider.ts`,
  `src/workers/payment-events.ts`, `src/auth/tenant.ts`,
  `src/provider/client.ts`. Known Limitations include legacy refunds from before
  2025 lacking idempotency keys, region-local webhook replay protection, and a
  dev emulator that skips signature checks.
- Pass it to a scan: `npx @openai/codex-security scan . --knowledge-base
  docs/security/payment-service-context.md`.
- Suggested layout: `SECURITY.md` at root; `docs/security/` holding
  `threat-model.md`, `architecture.md`, `payment-service-context.md`,
  `authentication.md`, `deployment-boundaries.md`.

### Seeding a threat model

- Initialize one by invoking the threat model skill in Codex (example prompt
  uses `$codex-security:threat-model`; the short form `$threat-model` also
  works), then commit it under `/docs/security` and link it in the Codex Cloud
  settings for the repo. **If no threat model is specified, Codex regenerates
  one for every security review.**
- The example prompts are labelled with the model and effort used:
  "GPT-6.1 Sol · Extra High".
- Pay attention to assumptions that reading the code cannot confirm, for
  example controls elsewhere that compensate, or duties split with other
  services.
- Example: Backstage's published threat model. A generated model could assume
  the auth plugin and the catalog plugin are isolated since each runs on its
  own host. Backstage's own model says host separation is not a security
  boundary if the catalog plugin can still reach the authentication plugin's
  database. With the model fixed, a review can check deployment config and access
  grants, so the assumption becomes a stated requirement. Any change to database
  access, shared caches, or where plugins are placed should re-open review of
  that boundary.
- Update the threat model whenever entry points, trust boundaries, or
  privileged operations move.

### Seeding a `SECURITY.md`

- The `$define-security-policy` skill (prompt form
  `$codex-security:define-security-policy`) seeds a policy. The example prompt
  is for a fictional "Northstar Bank API".
- The example policy (summarized) has four sections: **Authentication and
  Authorization** (authenticate every non-public endpoint; validate tokens for
  issuer, audience, signature, expiry, revocation, context; fail closed;
  authorize before every read, mutation, transaction, export, or admin action;
  an identifier is not proof of authorization; tenant isolation across list,
  detail, search, bulk, export, and indirect references; no trust in
  client-supplied roles or prices; least privilege), **Transaction and ledger
  integrity** (server-side validation of amounts and limits; replay, race, and
  idempotency-key protection; atomic balance checks; immutable ledger entries
  corrected by compensating entries; no ambiguous state without
  reconciliation), **Data protection** (encryption, approved secret
  management, no credentials in logs, equal protection for exports and backups,
  no internals in errors, retention per governance), and **Input and output
  handling** (treat headers, bodies, uploads, webhooks, third-party responses,
  and stored content as untrusted; validation; parameterized queries;
  restricted outbound requests; bounded parsers; output encoding).
- Example: Apache Superset's `SECURITY.md` says asynchronous jobs grant no extra
  data access of their own: a queued job is just the tail of an action that was
  already authorized, the initiating route must run the same checks, and
  the worker runs under the initiating principal's effective identity. The post
  says this sharpens reports, since it pins down the invariant that has to hold
  when work hops from the request handler to a worker.

## Codex Security

Choose a review workflow that fits the team: local review (before a PR),
automatic PR review (team checkpoint), or the CLI (explicit targets, saved
artifacts, custom CI). Start with one workflow, inspect results on a change the
team understands, then expand.

### Codex Security Review in GitHub Cloud

- Fastest path: the **Security Review** feature in ChatGPT, on the same settings
  surface as Codex Code Review (`chatgpt.com/codex/cloud/settings/code-review`).
- Security Review reads the PR diff plus surrounding repo context and any threat
  model or security guidance that has been configured.

#### Difference between Code Review and Security Review

- **Code Review**: broad engineering review of code quality (control flow, data
  loss, compatibility regressions, API behavior); audience is developers.
- **Security Review**: deeper security assessment of the same PR (authn/authz
  bypass, cross-tenant access, injection and unsafe parsing, sensitive data
  exposure); audience is developers who fix vulnerabilities and application
  security engineers.

#### Configuring security reviews

- **Auto-review reporting** sets which findings Codex posts when Security Review
  runs automatically. Default: **High** (High and Critical posted).
- **Manual review** sets which findings are posted when someone requests a
  review. Default: **Medium** (Medium, High, Critical).
- Set automatic thresholds to what the team can investigate consistently; use
  manual review for targeted investigations.

#### Setting path overrides

- Path-based overrides change the minimum severity posted per path: lower for
  authentication, authorization, payments, cryptography, CI workflows,
  infrastructure; higher for low-risk or noisy areas. Configured in Codex Cloud
  repo settings. Screenshot example: `src/**` at Low; GitHub workflow and
  dependency changes at Medium.
- Start by mapping sensitive operations to paths and owners, and pick a
  threshold that reflects the cost of a missed issue.
- Superset example: repo-wide **High**, with overrides `superset/security/` →
  Low; `superset/row_level_security/` → Low; `superset/sqllab/` and
  `superset/commands/sql_lab/` → Medium; `superset/embedded/` → Medium.

### Codex Security Review in Codex Desktop

- Interactive review of PRs or uncommitted changes from the **security tab**
  (scan type "Changes"), or by prompting the skill
  `$codex-security:security-diff-scan` on the current branch.
- Most useful while the implementation is fresh, so the developer can check a
  finding (for example an authorization assumption) immediately.

### Codex Security Review in the CLI

#### Reviewing uncommitted local work

- Setup sets shell variables for the repo root (`git rev-parse --show-toplevel`),
  the `docs/security` knowledge base, and a temp results dir.
- `npx @openai/codex-security scan <repo> --working-tree --base HEAD
  --knowledge-base <SECURITY.md> --knowledge-base <docs/security>
  --output-dir <dir>` reviews staged and unstaged changes against `HEAD`.
- Confirm the working tree holds only the intended change; unrelated edits
  widen the investigation.

#### Reviewing PRs or branch commits

- Compute the merge base with `origin/main`, then `scan <repo> --diff <base>
  --head HEAD --knowledge-base ... --output-dir ...`.
- A diff scan evaluates proposed changes only, not the whole repo.
- Output files: `report.md` (readable review); `scan-manifest.json` (exact base,
  head, target, artifacts); `findings.json` (severity, confidence, locations,
  remediation); `coverage.json` (reviewed surfaces, exclusions, deferred work,
  completeness).

#### Scanning monorepos

- Put engineering guidance in `AGENTS.md` and security expectations in
  `SECURITY.md`; example tree has `packages/auth/` and `services/billing/`,
  `services/reporting/`.
- Use ownership and build metadata to connect components to dependencies,
  consumers, and tests. A change to `packages/auth` may need review of both
  services. **The organization maintains this scope mapping; adding Codex does
  not configure it.**
- **Component assessment:** repeat `--path` to scan a shared library and its
  consumers together; only the selected paths are scanned.
- **PR and diff scanning:** use exact base and head SHAs (`BASE_SHA`,
  `HEAD_SHA`; the scan uses their merge base as `BASE_REVISION`) from
  authenticated GitHub metadata; both must be in the checkout; example adds `--auth chatgpt`.
  For a shared-library change, also run a component assessment on a clean
  checkout of the PR head. `--diff` and `--path` are separate modes and cannot
  be combined.

#### Scanning alerts from GitHub

- `npx @openai/codex-security import github <owner/repo> --format json` imports
  open code-scanning alerts (or a subset with repeated `--github-alert <n>`; the example picks alerts 12
  and 18).
- `npx @openai/codex-security validate <alerts.json>` run from the local repo;
  the post's comment says imported contents are data.

### GitHub Actions workflows

- Custom CI can run the CLI; OpenAI packages it as a GitHub Action,
  `openai/codex-security` (pinned by commit SHA, `action-v0.3.0`).
- Example workflow `.github/workflows/codex-security-repository.yml` (summary):
  triggers `workflow_dispatch` and a weekly cron (`23 7 * * 1`, Mondays 07:23
  UTC); `permissions: contents: read`; runs on `ubuntu-24.04`; first step
  installs `bubblewrap` and `apparmor-profiles` and loads the
  `bwrap-userns-restrict` AppArmor profile ("Set up the Ubuntu sandbox");
  `actions/checkout` pinned by SHA with `persist-credentials: false`; the action
  is called `with: model: gpt-5.6-sol, effort: high`; the API key comes from a
  repo secret `CODEX_SECURITY_API_KEY` as `OPENAI_API_KEY`.
- The same approach works for GitLab, BitBucket, or Jenkins (docs page "Run
  Codex Security in CI").

## Managing supply chain risk in CI/CD

The CLI can assess dependencies when one is added or bumped.

### Validating Dependabot alerts

- The skill `$codex-security:triage-finding` imports and triages third-party
  vulnerability alerts (including Dependabot) for **reachability and
  exploitability**, and returns a ledger with a verdict and reason per alert.
- Superset example: a webpack-dev-server advisory (`GHSA-f5vj-f2hx-8m93`)
  reached through the docs toolchain (Docusaurus). Codex traced the dependency, found the reviewed
  lockfile (`docs/yarn.lock`, lines L15019–L15021) resolved version 5.2.6, which the advisory lists as patched, and
  concluded that revision was not affected. Before closing the alert, the post says
  to check that the alert's version and revision match this evidence and to
  confirm what is actually installed.

### Running scans when package versions change

- Example workflow `.github/workflows/codex-security-dependency.yml` (summary):
  trigger `pull_request` on `package.json` and `package-lock.json`; runs only
  when the PR head repo equals the base repo (no forks); `contents: read`;
  `timeout-minutes: 45`; same sandbox setup step; Node `26` and Python `3.14`;
  installs `@openai/codex-security` under `$RUNNER_TEMP` with `--prefix`,
  `--ignore-scripts`, `--no-audit`, `--no-fund`; verifies the binary
  (`CODEX_SECURITY_BIN`, `--version`); checks out the PR head SHA with `fetch-depth: 0` and
  `persist-credentials: false`; `npm ci --ignore-scripts`; runs a **full
  repository scan** (env `CODEX_SECURITY_STATE_DIR`, `SCAN_DIR` in the runner
  temp dir) with `--auth api-key`, `--fail-on-severity high`, and
  `--json`; uploads results as an artifact with `retention-days: 7`.

## Wrapping up

- As agents write more code, security teams must build scaffolding for agents to
  reason across the codebase and enforce gates before insecure code is
  committed.
- Start with a few critical repositories; commit threat models and security
  policies; review PRs to judge how well the agent reasons with enterprise
  context; expand to more repos and pipelines once confident.
- Pointers: OpenAI security use cases in the developer docs, and the "Daybreak
  Defense Factory" for continuous security reviews.
