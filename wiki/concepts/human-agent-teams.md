---
title: Human-Agent Teams
type: concept
created: 2026-10-13
updated: 2026-10-13
tags: [orchestration, human-in-the-loop, teams, parallel-sessions, delegation, organizational-practice, feedback-loop]
---

# Human-Agent Teams

> How people and agents work together: the limit that human review capacity
> puts on agent work, the units in which work is delegated (tickets, tasks,
> channels, pull requests), agent teammates with written roles, context that
> agents can see, hand-off loops in which agents produce and humans decide,
> autonomy earned per task type, the changes to engineering organizations, and
> the loops that turn human feedback into agent changes. The multi-agent
> architecture itself is on [[agent-orchestration]]; approval mechanics are on
> [[guardrails]].

## Definition

A human-agent team is a group in which humans and agents share one work
surface (a chat channel, an issue tracker, a project board, or a repository).
Agents take assigned work, and humans set direction, review, and decide.
Anthropic calls agents that serve a whole team at once "multiplayer agents".
They need three capabilities: persistent memory, credentials that are not tied
to one human, and ongoing broad access to information. Anthropic's closing claim
is that the team norms are old human-team habits, and that agents make skipping
them more costly. (see [[anthropic-building-effective-human-agent-teams]])

## Human review capacity is the limit

- **Parallel sessions are not subagents.** Worktree-isolated sessions raise the
  number of tasks in flight; subagents keep each session focused. The ceiling on
  parallel sessions is what one person can review. Approval hooks belong at
  deploy gates, not in the build stage, or a person sits on the critical path of
  every parallel session. (see [[anthropic-ai-native-sdlc-playbook]])
- **Brooks' law applies to agent sessions.** On Sora for Android, OpenAI
  reports that parallel Codex sessions moved the bottleneck from writing code to
  human decisions, review, and integration, and each added session added
  coordination overhead. The findings are dated to a late-2025 model. (see
  [[openai-sora-android-with-codex]])
- **Three to five interactive sessions.** The Symphony team reports that an
  engineer could run three to five interactive sessions before context switching
  cut productivity. (see [[openai-symphony-codex-orchestration]])
- **Human QA capacity.** In OpenAI's repository with no hand-written code, human
  QA capacity became the bottleneck. The team answered by making the
  application legible to the agent (per-worktree app boot, browser driving,
  logs, and metrics). (see [[openai-harness-engineering]])
- **Budget human attention on purpose.** Anthropic's agents batch questions,
  restate key context, and limit the items that each human sees. Some teams set
  daily caps on agent output so that human review stays sustainable. The best
  long-running agents check their own work with tests, rubrics, and style
  guides before a human sees it, for example in a Doer-Verifier harness. (see
  [[anthropic-building-effective-human-agent-teams]], [[agent-verification]])
- **Scale reported by Block.** Block reports engineers working with about 45
  concurrent agents, a number that single-conversation tools do not scale to.
  (see [[anthropic-block-orchestrates-fable]])

## Units of delegated work

The common move is to stop supervising sessions and to delegate work items that
already exist in the team's system of record.

- **The ticket (Symphony).** A service polls the issue tracker, creates a
  workspace per active issue, and runs an agent there until the issue leaves an
  active state. Humans review at hand-off states such as `Human Review`. One
  issue can yield several PRs or none. Agents decompose large work into a task
  graph with blockers, only unblocked tasks dispatch, and agents file follow-up
  issues for out-of-scope findings. The scheduler is deterministic code and
  only reads the tracker; ticket changes are agent tool calls. Treating the
  agents as rigid nodes in a state machine failed; the agents get objectives
  plus tools instead. OpenAI self-reports a 500% increase in landed PRs for
  some teams. Ambiguous or judgment-heavy work stays in interactive sessions.
  (see [[openai-symphony-codex-orchestration]], [[agents-vs-workflows]])
- **The task queue as a backlog.** OpenAI engineers send tangents and drive-by
  fixes to Codex as background tasks and review the PRs later. OpenAI sizes a
  good task at about one hour of human work or a few hundred lines of code;
  the page describes the 2025 cloud Codex.
  (see [[openai-how-openai-uses-codex]])
- **The project task (Asana).** People talk unstructured inputs through with
  Claude, then log actionable items as projects and tasks that agents pick up.
  Agents receive task assignments, post messages, and appear in activity feeds.
  (see [[anthropic-asana-coachable-agents]])
- **The board item (monday.com).** People assign work to agents by triggers
  and mentions on the existing boards. In the coding integration, the agent
  posts its results back to the ticket. (see
  [[anthropic-monday-agent-first-platform]])
- **The shared channel.** At Slack, humans and agents triage in one channel,
  and humans set priority. An emoji reaction adds an item that an agent picks
  up. (see [[anthropic-slack-human-agent-teams]]) Anthropic's CI on-call agent
  works in the on-call Slack channel and reads every alert there. (see
  [[anthropic-ai-ci-cd-on-call]])
- **The pull request.** ABC Legal's stated rule is to make a decision look like
  a pull request: every agent change gets review, version history, rollback,
  and an audit trail. (see [[anthropic-abc-legal-managed-agents]])
- **The committed artifact.** Anthropic's SDLC playbook turns the lifecycle into
  a loop of committed files (`intent.md`, `spec.md`, `plan.md`, the diff, the
  PR, the incident record). Each accepted artifact triggers the next stage, and
  a human product owner accepts each one. (see
  [[anthropic-ai-native-sdlc-playbook]])

## Agent teammates: roster and roles

- **One roster with written roles.** Anthropic puts every human and agent in
  one roster, each with a written role, a scope, and the right tools. Skill
  files define agent roles, so others can stand up the same agent type. Without
  roles, people run side fleets of personal agents that duplicate work and
  fragment context. (see [[anthropic-building-effective-human-agent-teams]],
  [[agent-skills]])
- **Agents as coworkers with focus areas.** Slack reports that it routes routine transactional
  tasks (help-desk tickets, weekly metrics) to a general agent and retires an
  agent whose purpose people cannot state. (see
  [[anthropic-slack-human-agent-teams]])
- **Role first, then build.** Asana reports that it defines the purpose, instructions, and owned
  jobs before it builds an agent. Each agent has a profile page that lists its
  users, admins, skills, integrations, and permissions. The team that owns the
  standard, for example brand voice, administers the agent. (see
  [[anthropic-asana-coachable-agents]])
- **Agents with names and board presence.** monday.com reports that it gives each agent a name,
  an avatar, permissions, and board presence. Its reason: enterprises stall when
  AI chat runs parallel to the real workflow. monday.com calls its earlier
  bolt-on features "AI dust". (see [[anthropic-monday-agent-first-platform]])
- **Role-specialized agents on one repo.** Warp reports that it runs separate spec-writing,
  review, and triage agents across its open-source repository. (see
  [[anthropic-warp-builds-self-improving-agents]])
- **An identity of its own.** A team-wide agent needs a principal that is not
  one human. Under Anthropic's agent-identity model, Claude Tag has its own
  principal per channel, and access and memory are isolated per channel. (see
  [[anthropic-agent-identity-access-model]], [[agent-identity-and-access]])

## Working in public: context that agents can see

- **Agents know only what is written and searchable.** Anthropic sets a few
  workspace-level security boundaries and lets context flow freely inside each
  boundary. New channels default to org-public, and teams write meeting notes
  for agents as primary readers. Private work goes through DMs or personal MCP
  connectors. (see [[anthropic-building-effective-human-agent-teams]],
  [[context-engineering]])
- **A private channel is a blind spot.** Slack reports that it defaults
  channels to public,
  because decisions in DMs or private threads are invisible to every agent that
  reports on that work. Slack also uses agents to reconstruct why a decision was
  made, not only what was decided. (see [[anthropic-slack-human-agent-teams]])
- **If the agent cannot see it, it does not exist.** OpenAI's harness team
  moves Slack threads, documents, and tacit knowledge into the repository, which
  is the system of record. (see [[openai-harness-engineering]])
- **Agent work is visible too.** Per Asana, its agent posts its plan and steps on the
  shared task, so reviewers can coach the agent, not only fix the output. (see
  [[anthropic-asana-coachable-agents]])
- **Visibility is an access grant.** Anthropic's data team treats Slack channel
  membership as an access grant that the data team owns, because anyone who can
  mention the bot inherits the bot's access. (see
  [[anthropic-claude-tag-analytics-in-slack]]) Block captures individuals'
  skills and knowledge centrally, so every agent run gets them. (see
  [[anthropic-block-orchestrates-fable]])

## Hand-off loops: agents produce, humans decide

- **The basic loop.** Slack reports agents that draft, summarize, monitor, and
  prepare; a human reviews, decides, and redirects at the end of each loop.
  Examples include an agent-built Monday briefing and meeting briefings. (see
  [[anthropic-slack-human-agent-teams]])
- **Humans set the north star.** Humans write the team's north star and name
  which agents may propose new workstreams. (see
  [[anthropic-building-effective-human-agent-teams]])
- **Plan with the human, then hand off.** Shortcut reports that it plans with the user, then
  hands the approved plan to a fresh agent so that its context stays clean.
  (see [[claude-customer-shortcut]]) On Sora for Android, Codex summarized the
  code, humans corrected the summary, and the two co-wrote a mini design doc
  before Codex executed it. (see [[openai-sora-android-with-codex]]) The general
  plan-then-execute pattern is on [[agent-orchestration]].
- **One human decision at the end of a pipeline.** monday.com reports that it chains a
  Strategist Agent, a Landing Page Builder, and a Brand Reviewer; a human then
  makes one decision: publish or refine. (see
  [[anthropic-monday-agent-first-platform]])
- **Multiplayer triage.** In Anthropic's CI on-call channel, humans steer or add
  hypotheses in the same Slack thread while Claude investigates. Most fixes
  arrive as PRs that the on-call engineer reviews and merges. (see
  [[anthropic-ai-ci-cd-on-call]])
- **Hand off with the whole conversation.** Anthropic's inbound sales agent ends
  in a purchase, a quick answer, or a hand-off to a rep with the full
  conversation. The agent states why it hands off. (see
  [[anthropic-sales-inbound-managed-agents]])
- **Ambiguity goes to humans.** In OpenAI's Tax AI loop, unclear evidence goes
  back to the product team, and engineers own architecture and shipping. (see
  [[openai-self-improving-tax-agents-codex]])
- **Digests for decision-makers.** Asana reports a daily at-risk-renewal digest
  in three buckets to the CCO, the CRO, and regional leaders. (see [[anthropic-asana-coachable-agents]])

## Earned autonomy per task type

The team-level rule is to track autonomy per task type and widen it with
evidence. Approval gates, approval placement, and the full set of practices are
on [[guardrails]] (Human-in-the-loop, Earned autonomy).

- **Start with full review.** Anthropic engineers have sent agents to fix 500
  bugs independently; they started with full human review of every agent
  decision. Grant autonomy in proportion to demonstrated reliability, and
  retest as models change, because old guardrails can constrain a stronger
  model. In one backlog, a weekly "lessons and missteps" report helped the team
  expand agent scope. (see [[anthropic-building-effective-human-agent-teams]])
- **Recommendation mode first.** Each ABC Legal agent first posts
  recommendations. It moves to automation mode only after it matches or beats
  humans on that task, and it stays under the same measurement afterward. (see
  [[anthropic-abc-legal-managed-agents]])
- **Expand with evidence, not by friction.** OpenAI's security paper warns that
  friction that blocks legitimate work drives users to less governed tools. It
  advises a narrow start, expansion as evidence shows the limits work, and a
  check before each expansion that monitoring and recovery still cover the new
  authority. (see [[openai-agent-security-enterprise]])
- **Routine work first.** Anthropic's SDLC playbook makes auto mode the default
  only for routine, well-tested work with a small blast radius, once guardrails
  mature. (see [[anthropic-ai-native-sdlc-playbook]])

## How engineering organizations change

- **Planning moves to prototypes.** At Claude Code, a six-month roadmap was out
  of date by month three. Planning moved from design docs to PRs and
  prototypes that internal users try. (see
  [[anthropic-running-ai-native-engineering-org]]) Asana reports that automated
  feedback-to-PR loops bloated its cycles; in Command, agents fill an unplanned
  board and people decide what enters a cycle. (see
  [[anthropic-asana-coachable-agents]])
- **Ask Claude, not the author.** Every PR on the Claude Code team is
  Claude-assisted, so the team asks Claude what it needs to know, then asks
  whether the question can be automated. (see
  [[anthropic-running-ai-native-engineering-org]])
- **A review split.** Claude handles style, linting, bug catching, and test
  addition; humans review legal risk, trust boundaries, security-sensitive
  code, and product taste. Fung says to re-evaluate this split as models
  improve. (see [[anthropic-running-ai-native-engineering-org]]) The SDLC
  playbook runs the same AI review on every PR and forbids the authoring agent
  from approving its own work. (see [[anthropic-ai-native-sdlc-playbook]])
  OpenAI's harness team goes further: agents review each other's PRs, and human
  review is optional. (see [[openai-harness-engineering]])
- **Quality gates stay.** Anthropic's CI team reports that engineers ship 8x as
  much code per quarter as in 2021–2025, with gates unchanged: a named human
  owner per PR, approval to merge, and the same CI checks. (see
  [[anthropic-ai-ci-cd-on-call]])
- **The engineer's job becomes the environment.** OpenAI's harness team fixes
  agent failures by adding the missing capability to the environment, and runs
  recurring cleanup agents instead of manual cleanup days. (see
  [[openai-harness-engineering]]) Block runs recurring maintenance agents that
  sweep its codebase daily or weekly. (see [[anthropic-block-orchestrates-fable]])
  On Sora for Android, humans hand-built the architecture and a few
  representative features first. (see [[openai-sora-android-with-codex]])
- **Blurred roles and a flat team.** PMs code, and engineers take on content and
  design. The Claude Code team mandates three things: dogfood relentlessly,
  keep the team flat, and give explicit permission to kill obsolete processes.
  (see [[anthropic-running-ai-native-engineering-org]])
- **Metrics.** Fung tracks onboarding ramp time, PR cycle time, and
  Claude-assisted commits, and warns that throughput is not success. (see
  [[anthropic-running-ai-native-engineering-org]]) Slack makes the same point:
  token usage and message counts show activity, not results. (see
  [[anthropic-slack-human-agent-teams]])
- **Adoption spreads by example.** DeLanghe cites Salesforce's public "How I
  Slackbot" channel and a Slack PM's "what I did and how" canvas that other PMs
  copied. (see
  [[anthropic-slack-human-agent-teams]]) monday.com reports that the mental model
  was harder to change than the technology, and that adoption depends on trust as
  much as on capability. (see [[anthropic-monday-agent-first-platform]]) ABC
  Legal reports that its main hurdle was teaching business users git, not AI.
  (see [[anthropic-abc-legal-managed-agents]])

## Coaching agents: feedback into the agent

Feedback that stays in a chat session disappears when the session ends. The
sources route feedback into a durable, reviewed artifact.

- **Use is separate from training.** Asana reports that anyone can give task-level
  feedback, but only admins and editors can commit feedback to the agent's
  shared permanent memory, or delete it. (see
  [[anthropic-asana-coachable-agents]], [[agent-memory]])
- **Feedback becomes a pull request.** ABC Legal reports that its Harvester agent turns Slack
  thread replies and emoji reactions into labels, and a weekly Tuner agent
  drafts a prompt or config change as a PR that a human merges. (see
  [[anthropic-abc-legal-managed-agents]]) Warp reports that its scheduled
  improver skill compares agent output with human comments and opens a PR with the smallest
  edit to the base skill. Warp assumes some feedback is wrong, filters whose
  input counts, and keeps a human at the filtering or final-review stage. (see
  [[anthropic-warp-builds-self-improving-agents]])
- **Corrections become evals after review.** OpenAI reports that its Tax AI loop groups
  practitioner corrections and turns only repeated, reviewed patterns into eval
  targets. (see [[openai-self-improving-tax-agents-codex]], [[agent-evals]])
- **A lessons log.** Anthropic's CI on-call agent appends each resolved incident
  to `lessons.md` and reads it at the start of every investigation; recurring
  patterns move into the skill. Human taste still sets the status-report
  format, which took several iterations. (see [[anthropic-ai-ci-cd-on-call]])
- **Escalation reasons as the signal.** Anthropic's sales team reports that
  fixing the common hand-off reasons halved the share of conversations that
  needed a human. Sales and content leads edit the prompt themselves, and every
  change is a version. (see [[anthropic-sales-inbound-managed-agents]])
- **Instrument every answer.** Anthropic's data team logs reactions,
  corrections, and the loaded skill versions for each answer in Slack. (see
  [[anthropic-claude-tag-analytics-in-slack]])

## Case studies

All results are self-reported by the named organization; the sections above
cite the details.

| Team | Work surface | What it reports |
|---|---|---|
| Anthropic (team norms) | Slack | Four norms: work in public, one roster, human north star, earned autonomy. [[anthropic-building-effective-human-agent-teams]] |
| Slack | Shared channels | Public-by-default context, hand-off loops, adoption by example; no metrics. [[anthropic-slack-human-agent-teams]] |
| Asana | Work Graph tasks | Role-first agents, editor-only memory, planning as the bottleneck; no metrics. [[anthropic-asana-coachable-agents]] |
| monday.com | Boards | Agents as assignable teammates; 5M+ agent interactions after launch. [[anthropic-monday-agent-first-platform]] |
| Anthropic CI team | On-call channel | Median 14 minutes to first evidence-grounded analysis. [[anthropic-ai-ci-cd-on-call]] |
| Anthropic data team | Slack | Over 75% of questions in one channel answered unprompted. [[anthropic-claude-tag-analytics-in-slack]] |
| Claude Code team | Repo and PRs | Every commit Claude-assisted; new engineers ship in week one. [[anthropic-running-ai-native-engineering-org]] |
| ABC Legal | Git and Slack | 50+ agents; one review agent at ~98% agreement with compliance. [[anthropic-abc-legal-managed-agents]] |
| Anthropic sales | Buying agent with rep hand-off | Escalated leads convert more than 2x as often as form leads. [[anthropic-sales-inbound-managed-agents]] |
| OpenAI Symphony | Issue tracker | +500% landed PRs on some teams in three weeks. [[openai-symphony-codex-orchestration]] |
| OpenAI Sora Android | Repo | Four engineers, 28 days, about 85% of code by Codex. [[openai-sora-android-with-codex]] |
| OpenAI harness team | Repo | About 1,500 merged PRs with no hand-written code. [[openai-harness-engineering]] |

## Related concepts

- [[agent-orchestration]] — the multi-agent architecture that these teams run on.
- [[agents-vs-workflows]] — Symphony keeps judgment-heavy work interactive.
- [[guardrails]] — approval gates, earned autonomy, and human-in-the-loop mechanics.
- [[agent-identity-and-access]] — identity and access for agents that serve a team.
- [[agent-verification]] — self-checks that reduce what humans must review.
- [[context-engineering]] — why work must be written down for agents to see it.
- [[agent-skills]] — skill files as written agent roles and as the target of feedback loops.
- [[agent-memory]] — who may write to an agent's shared memory.
- [[agent-evals]] — reviewed corrections that become eval targets.
- [[multi-agent-economics]] — the cost side of running many agents in parallel.

## Key entities

- [[openai]], [[openai-codex]], [[anthropic]], [[claude]], [[claude-code]],
  [[claude-managed-agents]]

## Appears in

- [[anthropic-abc-legal-managed-agents]]
- [[anthropic-agent-identity-access-model]]
- [[anthropic-ai-ci-cd-on-call]]
- [[anthropic-ai-native-sdlc-playbook]]
- [[anthropic-asana-coachable-agents]]
- [[anthropic-block-orchestrates-fable]]
- [[anthropic-building-effective-human-agent-teams]]
- [[anthropic-claude-tag-analytics-in-slack]]
- [[anthropic-monday-agent-first-platform]]
- [[anthropic-running-ai-native-engineering-org]]
- [[anthropic-sales-inbound-managed-agents]]
- [[anthropic-slack-human-agent-teams]]
- [[anthropic-warp-builds-self-improving-agents]]
- [[claude-customer-shortcut]]
- [[openai-agent-security-enterprise]]
- [[openai-harness-engineering]]
- [[openai-how-openai-uses-codex]]
- [[openai-self-improving-tax-agents-codex]]
- [[openai-sora-android-with-codex]]
- [[openai-symphony-codex-orchestration]]

## Contradictions / open questions

- **Which human stage is the new bottleneck: framing, not conflict.** Asana
  names planning (deciding what enters a cycle) as the new bottleneck
  ([[anthropic-asana-coachable-agents]]). Fung names verification, code review,
  and security ([[anthropic-running-ai-native-engineering-org]]). Sora names
  decisions, review, and integration ([[openai-sora-android-with-codex]]), and
  the harness team names human QA ([[openai-harness-engineering]]). All agree
  that code generation stopped being the constraint and that a human-speed
  stage binds next; the SDLC playbook lists plan, review/test, and deploy
  together ([[anthropic-ai-native-sdlc-playbook]]). Each source names the stage
  that bound in its own setting. Fung also moved planning to prototypes, so
  her talk does not deny a planning cost.
- **Human review of every PR: scoped difference.** Anthropic's CI team keeps a
  named human owner and approval for every PR
  ([[anthropic-ai-ci-cd-on-call]]), and Fung keeps humans on trust boundaries
  and security ([[anthropic-running-ai-native-engineering-org]]). OpenAI's
  harness team makes human review optional
  ([[openai-harness-engineering]]), and the author scopes this to agent
  throughput far above human attention. Record this as a scoped difference.
- **Whose permissions bound a team agent: open design question.** Asana bounds
  an agent's effective access by the permissions of the person who triggers it
  ([[anthropic-asana-coachable-agents]]). Claude Tag gives the agent its own
  principal per channel, so a member can ask it to read a repo that the member
  cannot read ([[anthropic-agent-identity-access-model]]); Anthropic's data
  team notes that anyone who can mention the bot inherits its access
  ([[anthropic-claude-tag-analytics-in-slack]]). Anthropic plans an overlay
  that also checks the requesting user's permissions, which would narrow the
  gap. Detail is on [[agent-identity-and-access]].
- **Where team context lives.** Anthropic and Slack move agents to where the
  conversation is (public channels); OpenAI's harness team moves the
  conversation into the repository. Both rules share one premise: an agent
  cannot use what it cannot see. The sources do not compare the two choices.
