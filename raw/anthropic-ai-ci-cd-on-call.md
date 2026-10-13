# Claude on call: How Claude Tag serves as Anthropic's first responder for CI/CD failures — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/ai-ci-cd-on-call
> Publisher: Anthropic (claude.com articles) · Date: 2026-08-18
> Captured: 2026-10-12 via curl (condensed).

Page labels: Category Best practices · Product Claude Tag · Author Sachin Malhotra (Continuous Integration team, Anthropic), contributions from Michael Segner · Reading time 13 min. No model version is named. All figures are self-reported by Anthropic about its own internal use. The page links an "on-call setup kit" on GitHub.

## AI incident response for CI/CD: Claude on call at Anthropic

- Opening example: an on-call engineer is told at 10pm that ~44 tests on a new service are not firing. He asks @Claude in Slack. Claude finds that a feature flag turned on that morning removed the tests and that a revert is safe. After the revert, Claude reports 3 minutes later that the skip rules are gone and the error rate is back to baseline.
- Claude Tag has been the CI/CD on-call first responder "for the last several months". Claude wrote the first situation report (SITREP) in every recent incident that had one, typically within 15 minutes.

## Our Claude on call setup

- An on-call agent needs four things: memory (what was done), connections and access (to investigate and act), schedules (when to resume work), and instructions (what to do).
- Claude Tag is the backbone. It holds memory across the on-call Slack channel, takes per-turn instructions during an incident, reacts in real time to channel events, and runs scheduled "routines" set in natural language (example: "run CI handoff every Monday at 9:00am EST").
- Claude Tag has its own service account with the tools a CI engineer uses (Datadog, Grafana). An administrator set this up once for the channel.
- Claude also watches other channels where Claude Tag is a member, for service alerts, config changes, and PR updates.
- Standing instructions are markdown skill files in a GitHub repository, so teammates iterate on them like code. The repo also holds routing instructions, policies, and a lessons-learned log for self-improvement.
- Setup took "hours, not days". The setup kit converts a team's incident history into triage playbooks and leaves a read-only Claude in the incident channel that diagnoses, escalates, and learns; a demo runs against a fictional team's history in ~10 minutes.
- TL;DR steps: (1) Claude Team or Enterprise plan; (2) org owner adds Claude to the on-call channel via Claude Tag; (3) org owner connects Claude in that channel to connectors and the GitHub repo and sets up Claude Code Remote; (4) add Claude to the incident channel and tell it to monitor and triage immediately.

## Detection

- Failure mode 1: humans cannot set perfect alert rules and thresholds up front, especially with little traffic data. Claude analyses data and alerts during a new service's first few days and suggests new rules or tightens/loosens existing ones.
- Failure mode 2: alert fatigue. Claude checks every alert in the alert channels against criteria in a root `oncall.md` file and decides page-now versus wait-until-morning. Example tuned rule: page if error rate > 2% for > 5 minutes and not a known deploy window; otherwise write it to `lessons.md`.
- Two other triggers: a CI team member reports an issue in the on-call channel; or anyone opens an incident via an internal page, and if it is a CI infrastructure incident a Slack channel is provisioned and the on-call Claude picks it up.
- Takeaway: alerting is deterministic; escalation has deterministic and agentic paths.

## Triage

- Claude posts its first evidence-grounded analysis a median 14 minutes after an incident opens; fastest cases name the root cause within 4 minutes in the first report.
- Claude Tag starts a dynamic workflow: an orchestration agent spins up executor subagents, one per dependency or source of truth (Grafana, the log store, PagerDuty, GitHub, Kubernetes, Slack incident channels — all via MCP connectors). Executors report to the orchestrator, which writes a SITREP. Parallel leads reduce MTTR.
- Agents follow an investigation skill with reference markdown per bug class. Example: a 617-line skill for shadow-divergence bugs, created by troubleshooting one incident turn by turn with Claude and then asking Claude to write the file.
- `lessons.md` is a running log of every resolved incident (what happened, root cause, fix, gotcha). Claude appends to it automatically and reads it at the start of each investigation. Patterns that recur enough are promoted into the investigation skill. One entry Claude wrote: query the data before theorizing; config shows what could fail, metrics show what did.
- Claude is not always right first time; Claude Tag makes triage multiplayer, so humans can steer or add hypotheses in the thread in real time.

## Resolution

- Most team deploys sit behind feature flags. The author built a separate Claude Code agent, running with his permissions, that does progressive deployment behind each flag: it manages canary traffic, monitors, and ramps the flag up or down (not detailed further).
- Other resolution help from Claude Tag: advising when to drain or cordon parts of the Kubernetes cluster; instructions to scale infrastructure in demand surges (rare); and, most often, a fix PR that the on-call reviews, merges, and deploys.

## Verification, communication, and handoff

- Claude verifies fixes with the same MCP connectors used for the investigation. Per `oncall.md`, it writes a post-mortem to `lessons.md` and a handoff SITREP.
- A `ci-weather` agent compiles incident channels, build metrics, merge-queue stats, and deploy lag into a newsroom-style report in one public company channel, so engineers check it instead of pinging the CI team about whether to hold merges.
- The report format took several iterations: Claude can one-shot a status-report skill, but readability depends on team-specific taste.
- Claude also writes daily and weekly human handoff summaries (weekly on Mondays).

## From monitoring incidents to monitoring an incident response system

- Anthropic engineers ship on average 8x as much code per quarter as in 2021–2025. Quality gates stay: every PR has a named human owner, every change needs approval to merge, every change passes the same CI gates. The author's claim: keeping up with agentic coding requires agentic CI.
- Claude absorbs after-hours disruption and incident comms; the engineer focuses on longer-term reliability architecture. The process stays in Slack.
- "How to get started" repeats the four TL;DR steps.
