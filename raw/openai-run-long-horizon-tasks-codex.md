# Run long horizon tasks with Codex — OpenAI (Developers blog) (raw capture)

> Source: https://developers.openai.com/blog/run-long-horizon-tasks-with-codex
> Publisher: OpenAI (Developers blog) · Date: 2026-02-23 · Author: Derrick Choi
> Captured: 2026-10-12 via curl (condensed). Body text taken from the developers blog llms-full Markdown export; byline date and author taken from a curl of the live page HTML ("Feb 23, 2026"); figures spot-checked against the live page.

## Intro

- Timeline given by the author: GPT-5-Codex (Sep 2025) was the first GPT-5 variant tuned for agentic coding; the 5.2 release (Dec 2025) is described as the point where autonomous coding agents started to seem reliable, with a large jump in how long the model follows instructions.
- Experiment: a blank repository, full access, one task — build a design tool from scratch. Model GPT-5.3-Codex at "Extra High" reasoning.
- Result: about 25 hours uninterrupted, about 13M tokens, about 30k lines of code.
- The author frames it as an experiment, not a production rollout; it did well on spec-following, staying on task, running verification, and repairing failures.
- Screenshot only: the resulting "Design Desk" UI.

## What a long-run Codex session looks like

- Screenshots only: a session-summary page Codex generated from its own session data, and CLI session stats with token usage.
- Point made: agentic coding is shifting toward time horizon rather than one-shot intelligence.

## The real shift is time horizon

- The practical change: agents stay coherent longer, finish larger end-to-end chunks, and recover from errors without losing the thread.
- Cites METR's time-horizon work: the length of software tasks frontier agents finish at ~50% and 80% reliability is rising, with a rough ~7-month doubling time (METR, "Measuring AI Ability to Complete Long Tasks", 2025-03-19). Chart only.
- GPT-5.3-Codex launch claims two practical gains: (1) better multi-step execution (plan → implement → validate → repair); (2) easier mid-run steering — corrections do not wipe progress.
- Cites Cursor's "Scaling agents" browser-building post, where Cursor said OpenAI models were better at extended autonomous work (following instructions, focus, avoiding drift, complete implementation).

## Why Codex can stay coherent on long tasks

- Long runs depend on the agent loop more than on one large prompt. Codex loop: 1. Plan 2. Edit code 3. Run tools (tests/build/lint) 4. Observe results 5. Repair failures 6. Update docs/status 7. Repeat.
- The loop supplies: real feedback (errors, diffs, logs); externalized state (repo, files, docs, worktrees, outputs); steerability over time.
- Codex models work better on Codex surfaces than in a generic chat because the harness provides structured context (repo metadata, file tree, diffs, command outputs) and enforces a "done when" routine. Links OpenAI's "Unrolling the Codex agent loop" article.
- Codex app features listed: parallel threads across projects; Skills (standardize plan/implement/test/report); Automations (background routine work); Git worktrees (isolate runs, reviewable diffs). Screenshot only.

## My setup for the test

- A design tool chosen as an unforgiving test: UI, data model, editing operations, many edge cases; wrong architecture breaks fast.
- A substantial spec; "Extra High" reasoning; ~25 h uninterrupted; verification (tests, lint, typecheck) after every milestone.

## The key idea: durable project memory

Most important technique: spec, plan, constraints, and status kept in Markdown files the agent rereads, which prevented drift and fixed the definition of "done". Repository: github.com/derrickchoi-openai/design-desk (`docs/`).

### Prompt.md (spec + deliverables)
- Purpose: freeze the target so the agent does not build something impressive but wrong.
- Sections: goals and non-goals; hard constraints (perf, determinism, UX, platform); deliverables; "Done when" (checks + demo flow).
- The kickoff prompt told Codex to treat this file as the full specification and produce a milestone plan (screenshot only).

### Plan.md (milestones + validations) — file is `docs/plans.md`
- Purpose: convert open-ended work into checkpoints the agent can finish and verify.
- Sections: milestones small enough for one loop; acceptance criteria and validation commands per milestone; stop-and-fix rule (repair before moving on when validation fails); decision notes to avoid oscillation; intended architecture.
- Note in post: Codex app, CLI, and IDE extension now have a native plan mode, toggled with the `/plan` slash command; Codex asks follow-up questions if it needs clarification.

### Implement.md (execution instructions referencing the plan)
- Purpose: the runbook for how Codex operates.
- Sections: plans file is the source of truth, milestone by milestone; run validation after each milestone and fix failures immediately; keep diffs scoped; update the documentation file continuously.
- A prompt told Codex to read `implement.md` as its execution instructions (screenshot only).

### Documentation.md (status + decisions as it shipped)
- Purpose: shared memory and audit log, so the human can step away for hours.
- Sections: current milestone status; decisions and reasons; how to run and demo (commands, smoke tests); known issues and follow-ups.
- Screenshots only: milestone status updates; verification commands run.

### Verification at every milestone
- After milestones Codex ran verification commands and repaired failures before continuing. Instructed quality commands covered lint, typecheck, tests, build, and export (screenshot only). Example shown: Codex fixing issues after `npm run lint` (screenshot only).

## What the agent built

Not production-ready but real and testable; the bar was instruction-following and working behavior, not compiling. Ten capabilities:
1. Canvas editing (frames, groups, shapes, text, images/icons, buttons, charts)
2. Live collaboration (presence, cursors, selections, cross-tab edit sync)
3. Inspector controls (geometry, styling, text)
4. Layers management (search, rename, lock/hide, reorder)
5. Guides, alignment, snapping
6. History snapshots and restore
7. Replay timeline and branching from a prior point
8. Prototype mode (hotspots, flow navigation)
9. Comments (pinned threads, resolve/reopen)
10. Export (save/import/export; CLI export to JSON and React + Tailwind)

## Takeaways for long-horizon Codex tasks

Success came from the combination, not one clever prompt: clear target and constraints (spec file); checkpointed milestones with acceptance criteria (`plans.md`); a runbook (`implement.md`); continuous verification (tests/lint/typecheck/build); a live status and audit log (`documentation.md`). Direction stated: less babysitting, more delegation with guardrails.

## Try Codex on your own long-running task

Promotional close: humans steer at milestones; Codex aims for stronger teammate behavior, tighter real-context integration, and guardrails (plans, validations, previews, rollbacks); non-developers will build too. Links: Codex overview, quickstart, models, features.
