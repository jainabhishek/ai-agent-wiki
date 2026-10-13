---
title: "Anthropic: Claude Code in the Cloud (Field Guide to Cloud Sessions)"
type: source
created: 2026-10-12
updated: 2026-10-13
author: Addy Osmani (Anthropic, claude.dev blog)
date: 2026-10-06
source_url: https://claude.dev/blog/claude-code-in-the-cloud/
source_path: raw/anthropic-claude-code-in-the-cloud.md
tags: [claude-code, sandboxing, execution-environment, parallel-agents, sessions, verification, credentials]
---

# Anthropic: Claude Code in the Cloud (Field Guide to Cloud Sessions)

> A field guide to [[claude-code]] cloud sessions. Each task runs on its own
> disposable VM, holds no user secrets, and returns a branch. The design lessons
> cover per-task isolation, keeping credentials outside the VM, which configuration
> travels with the repo, and giving the agent a way to verify its own work.

## Summary

A local Claude Code session depends on the laptop in three ways. It shares the
working tree, so parallel sessions can collide on files and ports. It runs with
the user's credentials. It stops when the machine sleeps. A cloud session instead
gets a fresh VM per task, with the repo cloned onto a new branch and environment
setup already applied. The VM runs on Anthropic infrastructure or, with
self-hosted environments (beta), on the organization's own machines. The author
ran four real sessions against a sample Node repository. Three were parallel
tasks started within 16 s of each other, and all three finished 87 s after the
first started. In each session the agent ran repeated proof of its own work: the
test suite 40 times, the server plus a curl against each endpoint, and code
execution against sample data. Most of the post is product how-to (GitHub
connection paths, routines, teleport, the phone app). This page keeps the
agent-design content. See [[agent-harness]], [[guardrails]].

## Key points

### Harness and sandbox architecture
- **One task = one VM = one branch.** Sessions cannot touch each other's files or
  ports. The cost of this isolation is that sessions do not know about each other.
  In the demo, the logger session found the same cache race that a sibling session
  was fixing. It proposed the fix, left the code alone as out of scope, and said in
  its summary that the suite was not clean. Advice: split parallel tasks along file
  boundaries, merge in a sensible order, and expect duplicate problem reports. See
  [[agent-orchestration]].
- **Credentials stay outside the VM.** A proxy holds the GitHub token. The session
  gets a short-lived credential that can push only to its own working branch. On
  Pro and Max, environment "API credentials" attach a key to requests for named
  hosts outside the VM, so the key never sits in an environment variable.
  Environment variables are visible to every user of that environment.
- **Network as a policy dial.** The levels are None, Trusted (package registries,
  GitHub, and major cloud SDK hosts; the default), Custom, and Full. Choose the
  narrowest level that works. Even at None, traffic to the Anthropic API and a push
  to the session's own branch remain possible egress paths. A proxy logs the
  hostname of all outbound traffic. Changes reach running sessions within about one
  minute.
- **Untrusted code belongs in the disposable VM.** Contributor PRs, install
  scripts, and freshly cloned repos run away from SSH keys, cloud CLI sessions, and
  browser profiles.
- **Approval modes** in the cloud are limited to Auto, Accept edits, or Plan. There
  is no per-command approval. Routines run with no approval prompts and by default
  push to `claude/`-prefixed branches.

### Environment and configuration
- **Repo configuration travels; personal configuration does not.** `CLAUDE.md`,
  rules, skills, agents, commands, `.mcp.json`, and `.claude/settings.json` hooks
  come with the repo. `~/.claude` stays on the laptop. Corollary: test commands
  must be written into `CLAUDE.md`. See [[agent-steering]], [[agent-skills]].
- **Machine level vs project level setup.** The *setup script* runs as root before
  Claude Code starts. It must exit 0 and should finish in about 5 minutes, after
  which the environment is cached as a snapshot. The cache rebuilds when the script
  or allowed hosts change, and about every 7 days. A *SessionStart hook* in the
  repo runs the same steps locally and in the cloud. `CLAUDE_CODE_REMOTE` gates
  cloud-only steps. The snapshot caches files, not processes, so services such as
  postgres must be started per session.
- **Sessions are ephemeral, conversations persist.** Idle VMs are reclaimed.
  Reopening a session gives a fresh VM with the conversation restored, so the agent
  should commit as it goes.
- **Command timeouts.** Foreground commands time out after 2 min by default (10 min
  max), then continue in the background for up to 30 more minutes. The variables
  `BASH_DEFAULT_TIMEOUT_MS` and `BASH_MAX_TIMEOUT_MS` change these limits. The
  stated rationale: a long test loop inside one command costs little usage, so ask
  for thorough proof (for example, 200 runs or a bisect across 50 commits).

### Verification and task framing
- **Give sessions a way to check their own work.** "Without that, you review
  changes nobody has run." Most of the demo's value came from Claude running
  things. See [[agent-verification]], [[agent-design-principles]].
- **Write each task as a self-contained ticket**: what is wrong, what done looks
  like, and the command that proves it. The flaky-test prompt asked for at least 30
  runs; the agent ran 40.
- **Habits.** One task per session. Ask for evidence. Read the summary before the
  diff. Commits carry a `Claude-Session` trailer that links to the transcript.
  Parallel sessions consume plan limits in parallel (5 sessions ≈ 5x the rate).

### Sessions and handoff (brief)
- `claude --cloud "<task>"` clones the GitHub remote at the current branch, so the
  user must push first. `claude --teleport` pulls a cloud session's branch and its
  full conversation into the local terminal. `claude -p "<msg>" --cloud <id>`
  queues a follow-up from any machine, including CI.
- Routines (research preview) start cloud sessions from a schedule (at most
  hourly), an HTTP call, or a GitHub event. Projects (beta) run a coordinator that
  starts and tracks sessions and can start up to 200 new threads a day.
- GitHub access needs two separate grants: sign-in (identity) and the Claude
  GitHub App (private repo visibility). Auto-fix, GitHub-triggered routines, and
  projects require the App.

## Notable claims & data

- The VM has about 4 vCPU, 16 GB RAM, and 30 GB disk.
- Stay local for local-only resources (real local data, VPN, GPU, simulators,
  hardware), for tight visual loops, and under Zero Data Retention, which disables
  cloud sessions.
- In the demo, repo recreation took roughly a third to just over half of each
  61–72 s run. That overhead is absent with a real GitHub clone.

## Entities

[[anthropic]], [[claude-code]], [[claude]]

## Concepts

[[agent-harness]], [[guardrails]], [[agent-orchestration]], [[agent-steering]],
[[agent-skills]], [[agent-evals]], [[agent-verification]], [[agent-design-principles]], [[context-engineering]]

## Connections

- The credential-proxy design (secret held outside the execution sandbox and
  injected on egress) is the same pattern as the Managed Agents vault in
  [[anthropic-building-effective-agent-automations]]. It likely relates to
  [[anthropic-eng-how-we-contain-claude]].
- "Repo config travels, user config doesn't" makes [[anthropic-steering-claude-code]]'s
  mechanisms (CLAUDE.md, rules, skills, hooks) the portable layer of the harness.
- Verification-by-running and committing as you go echo
  [[anthropic-eng-effective-harnesses-long-running-agents]] (progress in git,
  end-to-end checks).
- Parallel isolated sessions with branch merges are a coarse-grained form of
  the parallelization in [[workflow-patterns]]. The duplicate-discovery cost is the
  coordination cost discussed in [[multi-agent-economics]].
- Fresh disposable environments complement the eval guidance on isolating trials in
  [[anthropic-eng-demystifying-evals]].

## Contradictions / open questions

- _None recorded._ The post states that the cloud approval modes exclude
  per-command approval. The post does not say how that interacts with
  [[guardrails]] advice to require human approval for high-risk actions. For
  cloud sessions, the containment burden moves to the VM, the network policy, and
  the branch-scoped credential.
