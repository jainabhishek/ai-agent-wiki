# Claude Code in the cloud: a field guide to cloud sessions — Anthropic (claude.dev blog) (raw capture)

> Source: https://claude.dev/blog/claude-code-in-the-cloud/
> Publisher: Anthropic (claude.dev blog) · Date: 2026-10-06
> Author: Addy Osmani. Category: Playbooks. 18 min read.
> Captured: 2026-10-12 via curl + local HTML-to-text (condensed, paraphrased;
> product how-to compressed, agent-environment details kept).

## Intro

A local Claude Code session depends on the laptop in three ways: it shares the
working tree (two sessions on one repo can edit the same files and contend for the
same port), it runs with the user's credentials, and it stops when the machine
sleeps or loses network. A cloud session runs Claude Code on its own machine: each
task gets a fresh VM with the repo cloned onto a new branch and the environment's
setup already applied. Start from claude.ai/code, mobile app, Desktop, terminal, or
Slack; follow from browser, mobile, Desktop. Output is a branch (optionally a PR).
Included in Pro, Max, Team, Enterprise with no separate compute charge; draws on
the same Claude Code usage limits; an org owner may need to enable it. The author
ran four real cloud sessions against a made-up sample repo; transcripts, diffs,
timings are reported.

## Three tasks, one repository, three machines

Sample repo `tidepool` (small Node tide-prediction API) with three problems: a test
failing ~1 run in 4, API docs describing parameters the code no longer reads, and a
logger building lines by string concatenation. Three sessions started within 16
seconds (programmatically; each recreated the repo from its prompt because it
wasn't on GitHub). Terminal form is `claude --cloud "<prompt>"`. Prompts
(paraphrased): find and fix the flaky test's root cause in code not test, prove by
running the suite at least 30 times consecutively; rewrite `docs/API.md` to match
`src/server.js`, start the server and run each curl example; make `src/logger.js`
emit one JSON object per line, keep `LOG_LEVEL`, log method/path/status/
`duration_ms`, add a test.
- Durations 61, 65, 72 s; all done 87 s after first start; repo recreation took
  roughly a third to just over half of each run.
- Flaky test: race in `TtlCache.get` (value stored only after loader finished, so a
  concurrent `get` re-invoked the loader). Fix: cache the in-flight promise, evict
  on load failure. Ran `npm test` 40 times, zero failures.
- Docs: started server, curled every endpoint, found five discrepancies (fields
  never returned, ignored `days` param, feet vs metres, missing `/next-high`,
  missing error responses). Found malformed `from=` returns empty list with 200 and
  documented it as a caveat rather than changing server code outside its task.
- Logger: JSON logger + five tests. Its commit had one failing test; it reran the
  cache test 8 times, saw 5 failures, traced it to the same race, proposed the same
  fix but left the cache alone (out of scope) and stated the suite wasn't clean.
- Lesson: isolation (own repo copy, processes, branch) means no file/port
  collisions — the docs and logger sessions each started the server independently —
  but also no visibility into sibling sessions' fixes. Split parallel tasks along
  file boundaries, merge branches in a sensible order, expect duplicate problem
  reports.

## Under the hood of a Claude Code cloud session

A Claude Code session on Anthropic-managed infrastructure, or on the org's own
machines with a self-hosted environment. Everything the agent can touch is inside
the VM; the GitHub token and network policy sit outside. Four takeaways:
- Every task gets its own machine: fresh VM, repo cloned onto a new branch;
  sessions can't touch each other's files or ports.
- The GitHub token never enters the VM: a proxy holds it; the session gets a
  short-lived credential that can push only to its own working branch.
- Repo Claude config travels (`CLAUDE.md`, rules, skills, agents, commands);
  personal `~/.claude` does not.
- Idle VMs are reclaimed; reopening gives a fresh VM with the conversation
  restored, so commit work you care about.

## Local or cloud?

Comparison table (condensed):
- Runs on: local machine vs fresh VM per task.
- Laptop asleep/offline: local stops vs cloud continues.
- Several tasks on one repo: separate worktrees/ports/care vs one VM + branch per task.
- Agent reach: local = anything the user account can reach (SSH keys, cloud CLIs,
  `~/.claude`); cloud = the repo, the configured network level, enabled connectors,
  a session-scoped GitHub credential.
- Start/follow from: local machine (or phone via remote control) vs browser, phone,
  Desktop, terminal, Slack, API call, or schedule.
- Approvals: local any mode incl. per-command vs cloud Auto, Accept edits, or Plan.
- Ends with: working-tree changes vs a branch (+ PR on request).
- Compute: own machine vs no separate charge, plan limits.
Stay local when the task needs something only the local machine has (DB with real
local data, VPN service, GPU, phone simulator, hardware), for tight visual loops,
and under Zero Data Retention (which disables cloud sessions). In-between options:
remote control (session stays local, steered remotely) and self-hosted environments
(beta, Team/Enterprise; cloud sessions on org infrastructure, can reach private
networks).

## Seven workflows that suit cloud sessions

### 1. Clear a backlog in parallel
Start N sessions, review N branches. `claude --cloud` clones the GitHub remote at
the current branch — push local commits first. CLI shows a live setup checklist and
queues typed input. Write each task as a self-contained ticket: what's wrong, what
done looks like, how to prove it (the flaky-test prompt named its proof — 30 runs;
the session ran 40). Projects (public beta, Pro/Max) run a coordinator conversation
that starts and tracks cloud sessions, grouped as working / waiting on you / ready
for review.

### 2. Let it prove the fix
Repeated proof without tying up the local machine. Ask for thorough proof: run the
suite 200 times, bisect across 50 commits, run slow integration tiers, start the
app and curl it. Each turn counts toward plan usage but a long test run inside one
command costs little. Foreground commands time out after 2 minutes by default (10
max), then continue in background up to 30 more minutes; raise defaults with
`BASH_DEFAULT_TIMEOUT_MS` and `BASH_MAX_TIMEOUT_MS` in the environment variables.

### 3. Plan at your desk, build in the cloud, finish in your terminal
Agree the plan locally in plan mode (`claude --permission-mode plan`), commit and
push it (e.g. `docs/migration-plan.md`), then `claude --cloud "Execute the migration
plan in ..."`. Pull back with `claude --teleport [<session-id>]` (or `/teleport`,
`/tp`, `/tasks` then `t`): checks same repo, fetches and checks out the session's
branch, loads the full conversation; needs a clean working tree (offers to stash)
and a pushed branch. Desktop "Open in" sends a local session to the cloud.

### 4. Check in from your phone
Claude app Code tab connects to the same sessions: start, follow, steer, answer
questions, watch a PR. A fourth session answered a phone-style question about how
tidepool predicts tides; it ran code to verify and found a real bug (loop never
examines first/last sample, so a high tide exactly at window start is missed),
changing no files.

### 5. Hand CI failures and review comments to Claude
With the Claude GitHub App installed, a session can watch a PR: Auto-fix in the CI
bar, `/autofix-pr` in terminal, mobile, or paste the PR URL. Claude pushes clear
fixes for failing checks and review comments, explains changes, asks about
ambiguous/architectural ones. Review-thread replies post under the user's GitHub
username, labeled Claude Code. Not notified of merge conflicts — ask it to rebase.
Its comments can trigger comment-driven automation (e.g. Atlantis).

### 6. Start work without starting it yourself
Routines (research preview): saved prompt + repos + connectors + environment; each
run is a cloud session started by a trigger — schedule (at most hourly), HTTP call
to the routine's endpoint, or GitHub event (PR opened, release). Created at
claude.ai/code/routines, Desktop, or `/schedule`. Routines run without approval
prompts and by default push to `claude/`-prefixed branches. Queue a follow-up into
a running session from any logged-in machine incl. CI:
`claude -p "<message>" --cloud <session-id>`. Prefilled-session URLs:
`claude.ai/code?prompt=...&repositories=<owner>/<repo>`.

### 7. Run code you don't fully trust
Untrusted PRs, install scripts, freshly cloned repos run, locally, next to SSH
keys, cloud CLI sessions, browser profile. In the cloud they run in a disposable VM
without those, with a session-scoped GitHub credential and a narrowable network.
Network level None is strictest; Trusted allows package registries, GitHub, major
cloud SDK hosts. Even at None, Claude Code still talks to the Anthropic API (a data
egress path) and can push to its own branch. All outbound traffic passes a proxy
that logs hostnames.

## Connecting GitHub without getting stuck

Most first-session failures are GitHub. Two separate permissions: signing in with
GitHub (identity) and installing the Claude GitHub App on an account/org (which
private repos are visible). Public repos need only the first. Auto-fix,
GitHub-triggered routines, and projects require the App. Paths: (A) browser —
claude.ai/connect-github then install the App (org owner approval usually needed;
SAML SSO step must be authorized or org repos are hidden); (B) `/web-setup` sends
the local `gh` token, reaching whatever that token can, without the App (Team/
Enterprise owners must enable Quick setup); (C) no GitHub — `claude --cloud` in a
repo without GitHub remote/App uploads a bundle; push-back only if the GitHub
connection has push access. Team/Enterprise owner checklist: enable GitHub
connector, allow cloud sessions, install App on org repos, decide on Quick setup;
IP allowlists and GitHub Enterprise Server need extra steps. Troubleshooting table
covers: private repo missing (App not installed/repo excluded), owner-only error
(pending App permission request, IP allow list, SAML), org repos missing (skipped
SAML authorization), all sessions failing auth (IP allowlisting — ask support to
exempt Anthropic-hosted services).

## Give sessions what they need to check their own work

A session that can run tests checks its work before handing it back; otherwise the
user reviews changes nobody ran. Most demo value came from Claude running things.
Ten minutes of environment setup enables this:
- Default environment: Trusted network, no variables, no setup script — enough for
  most JS, Python, Go, Rust repos.
- Setup script (machine level): runs as root before Claude Code starts (`apt
  install` works); must exit 0 or the session won't start; should finish within
  ~5 minutes so the environment is cached. New sessions then start from a snapshot.
  Cache rebuilds when the script or allowed hosts change, and about every 7 days.
- SessionStart hook (project level): put `npm install` etc. in a hook in the repo's
  `.claude/settings.json` so it runs identically locally and in the cloud; check
  `CLAUDE_CODE_REMOTE` for cloud-only steps. Repo hooks load in single-repo sessions.
- Start services per session: the cache stores files, not running processes (e.g.
  `service postgresql start` via Claude or a SessionStart hook).
- Narrowest network level that works: Trusted for common registries; Custom to add a
  private registry; Full only when open internet is needed. Changes reach running
  sessions within ~1 minute.
- Secrets out of shared variables: environment variables are visible to anyone
  using the environment. On Pro/Max, environment API credentials attach a key to
  requests for named hosts outside the VM, so the key never sits in a variable.
- Put commands in CLAUDE.md: `~/.claude` doesn't reach the VM, so the repo must say
  how to run e.g. integration tests.

## Habits that pay off

- One task, one session (easier to review, cheaper to discard).
- Ask for evidence: name the command that proves done; read the summary before the diff.
- Push before `claude --cloud` (VM clones from GitHub).
- Commit as you go on long tasks (idle VMs reclaimed).
- Review in the diff view; inline comments batch into the next message; Create PR
  offers full PR, draft, or GitHub compose page.
- Steer mid-run: messages queue; a queued one can be retracted.
- Share the session (Team/Enterprise visibility = Team); cloud commits carry a
  `Claude-Session` trailer linking to the transcript.
- Watch limits: parallel sessions consume plan limits in parallel (5 sessions ≈ 5x
  rate); routines have hourly caps; projects can start up to 200 new threads/day.

## Common questions

- Eligibility: Pro, Max, Team, Enterprise (premium or Chat + Claude Code seat),
  signed in with claude.ai; not with Console API key or third-party provider.
- Data: Anthropic stores the transcript (retention depends on plan and
  model-improvement setting); VMs reclaimed after inactivity; deleting a session
  removes its data. Training policy same as rest of Claude Code (no training on
  Team/Enterprise/API unless opted in; Free/Pro/Max per setting).
- VM size: about 4 vCPUs, 16 GB RAM, 30 GB disk; put heavy installs in the setup
  script so they land in the cached snapshot.
- GitLab/Bitbucket: bundle upload works, no push-back; GitHub Enterprise Server
  supported on Team/Enterprise.
- Parallel branch conflicts: sessions don't know about each other; merge one, then
  send the next `claude -p "rebase on main and fix any conflicts" --cloud <id>`.
- Local tools: user-level config doesn't travel — commit skills/commands under
  `.claude/`, project MCP servers in `.mcp.json`, test commands in `CLAUDE.md`.

## Start in five minutes

1. Open claude.ai/code or `/login` with a claude.ai account.
2. Connect GitHub and install the App where the repo lives.
3. Pick the repo and the Default environment.
4. Give one backlog task with a command that proves it's done.
5. Close the tab; check in from phone; review the diff and create the PR.
