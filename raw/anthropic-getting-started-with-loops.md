# Loop engineering: Getting started with loops — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/getting-started-with-loops
> Publisher: Anthropic (claude.com articles) · Date: 2026-06-30
> Captured: 2026-10-12 via curl (condensed).

Authors: Delba de Oliveira, Michael Segner. Category: Best practices,
Perspectives. Product: Claude Code. Reading time 2 min.

## Getting started with loops
- "Loop engineering" (designing loops instead of prompting) has many
  definitions online. The Claude Code team's definition: agents repeating
  cycles of work until a stop condition is met.
- Loop types are categorized by trigger, stop condition, Claude Code
  primitive, and best-fit task. Start with the simplest solution; use complex
  loops selectively.

## Turn-based loops
- Trigger: a user prompt. Stop: Claude judges it is done or needs more
  context. Best for: short, ad hoc tasks. Usage control: specific prompts and
  better verification via skills to cut turns.
- Every prompt starts a manual loop: gather context, act, check, repeat if
  needed, respond — "the agentic loop". Example: add a like button; Claude
  reads code, edits, runs tests, returns; you check and prompt again.
- Encode your manual checks as a `SKILL.md` so Claude verifies more of its own
  work end to end, with tools or connectors to see, measure, or interact with
  the result. More quantitative checks make self-verification easier. (Points
  to the steering-Claude-Code guide for skills vs hooks vs subagents.)
- Example skill `verify-frontend-change` ("Verify any UI change end-to-end
  before declaring it done"): never report a UI change done from a successful
  edit alone; steps — (1) start the dev server and open the page; (2) interact
  with the change, confirm the state change, screenshot before/after; (3)
  browser console shows zero new errors or warnings; (4) run a performance
  trace and audit Core Web Vitals with the Chrome DevTools MCP. On any
  failure, fix and rerun from step 1; no partially verified hand-backs.

## Goal-based loop (/goal)
- Trigger: a manual prompt in real time. Stop: goal achieved OR maximum turns
  reached. Best for: tasks with verifiable exit criteria. Usage control:
  specific completion criteria and explicit turn caps ("stop after 5 tries").
- `/goal` defines what done looks like, so Claude does not decide "good
  enough" and stop early. Each time Claude tries to stop, an evaluator model
  checks the condition and sends it back until met or the turn cap is hit.
  Deterministic criteria (tests passed, score threshold) work best.
- Example: `/goal get the homepage Lighthouse score to 90 or above, stop after
  5 tries.`

## Time-based loop (/loop and /schedule)
- Trigger: a time interval. Stop: you cancel, or the work completes (PR merges,
  queue empty). Best for: recurring work, or interfacing with external
  systems. Usage control: longer intervals, or react to events rather than
  time.
- Recurring work: same task, new inputs (e.g. morning Slack summary). External
  systems: poll on an interval and react (e.g. a PR getting reviews or failing
  CI).
- `/loop` re-runs a prompt on an interval, e.g. `/loop 5m check my PR, address
  review comments, and fix failing CI`. It runs on your computer and stops if
  the computer is off; `/schedule` moves it to the cloud as a routine.

## Proactive loops
- Trigger: an event or schedule, no human in real time. Stop: each task exits
  when its goal is met; the routine runs until turned off. Best for: recurring
  streams of well-defined work (bug reports, issue triage, migrations,
  dependency upgrades). Usage control: route routines to smaller, faster
  models; use the most capable model for judgment calls.
- Compose primitives plus auto mode and dynamic workflows (research preview):
  `/schedule` (research preview) to check for new reports; `/goal` for done,
  skills for how to verify; dynamic workflows to orchestrate triage, fix, and
  review agents; auto mode so it runs without permission prompts.
- Example prompt: schedule hourly checks of `#project-feedback`; goal: every
  report found this run is triaged, actioned, and answered; for bug fixes, use
  a workflow that explores three solutions in parallel worktrees with a judge
  reviewing them adversarially.

## Maintaining code quality
- Output quality depends on the surrounding system:
  - Keep the codebase clean; Claude follows existing patterns.
  - Give Claude a way to verify its work; encode "good" in skills.
  - Make docs easy to reach (frameworks' up-to-date best practices).
  - Use a second agent for code review: fresh context is less biased by the
    main agent's reasoning. Built-in `/code-review` skill or Code Review for
    GitHub. Loops that write code need loops that check it (points to the
    AI-native SDLC security post).
- When a result misses the standard, encode the fix into the system, not just
  the instance.

## Managing token usage
- Choose the right primitive and model; small tasks need no multi-agent loops;
  some tasks fit cheaper, faster models.
- Define clear success and stop criteria so Claude finishes sooner (but not
  too soon).
- Pilot before a large run: dynamic workflows can spawn hundreds of agents.
- Use scripts for deterministic work (e.g. a PDF skill ships a form-filling
  script instead of re-deriving code).
- Don't run routines more often than the watched thing changes.
- Review usage: `/usage` breaks down recent usage by skills, subagents, MCPs;
  `/goal` with no arguments shows turns and tokens so far; `/workflows` shows
  per-agent token usage and lets you stop agents.
- Model and effort choices are among the biggest cost levers.

## Getting started
- Summary table:
  - Turn-based — you hand off the check — when exploring or deciding — custom
    verification skills.
  - Goal-based — the stop condition — when you know what done looks like —
    `/goal`.
  - Time-based — the trigger — when work happens outside your project on a
    schedule — `/loop`, `/schedule`.
  - Proactive — the prompt — when work is recurring and well-defined — all of
    the above plus dynamic workflows.
- Pick one task where you are the bottleneck; ask which piece to hand off (the
  check, the goal, the schedule). Run, observe stalls and over-reach, iterate.
- Points to Claude Code docs (parallel agents, loop, schedule, goal, dynamic
  workflows) and the verification-loops-with-skills post.
