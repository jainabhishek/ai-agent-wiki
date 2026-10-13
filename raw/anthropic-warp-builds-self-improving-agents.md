# How Warp builds self-improving agents on Claude — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/how-warp-builds-self-improving-agents-on-claude
> Publisher: Anthropic (claude.com articles) · Date: 2026-08-26
> Captured: 2026-10-12 via curl (condensed).

Byline: Michael Segner. Category: Best practices. Product: Claude Platform.
Stated reading time: 10 min. Part of a startup series; customer case study,
figures are self-reported by Warp / Anthropic.

## Company facts (from the "quick pitch" box)

- Warp: AI terminal and agentic development environment. Founded 2020; CEO Zach
  Lloyd. Stack: Rust, Go, GitHub Actions, an internal agent orchestration
  platform called Oz, Claude Platform.
- Stated growth: $73M raised; 800K monthly developers; 56% of the Fortune 500
  use Warp; 10M Claude Code sessions run inside Warp to date (400K+ per week);
  40M total Warp Agent conversations.

## Problem

- Recurring agent tasks need reliability: a first-pass prompt that is 80%
  right still produces a noisy experience.
- Warp's internal code review agent drew complaints: unhelpful comments,
  low-quality output.
- Stopgaps tried: manually rewriting the prompt after observed failures (more
  usable, did not scale); improving context files such as `AGENTS.md` (helped,
  incomplete).
- Diagnosis: feedback given to an agent vanishes when the session ends, so it
  never re-enters the loop. Fix: a skills-based framework where feedback
  compounds.

## Agent self-improvement loops built on skills

- Two skills with human feedback between them.
- **Inner / base skill**: domain knowledge and instructions. E.g. when a PR
  opens, the code review agent runs with the base skill.
- **Human feedback**: anything from a thumbs-up to a detailed reason; the more
  explicit, the better. Lloyd's example: explaining that a suggested variable
  rename conflicts with the codebase's naming convention for a type of global.
- **Outer / improver skill**: an observer agent on a schedule, not per task. It
  pulls accumulated feedback, compares agent suggestions with human responses,
  and proposes a small, focused edit to the base skill.
- Skills are plain files, so agents edit them well; the edit is a PR that goes
  through normal review; once merged, the next base-skill run inherits it.
- Warp runs this across its whole open-source repo with separate spec-writing,
  review, and triage agents, each with its own loop.
- Lloyd: skills encode knowledge outside the prompt as something the agent
  looks up; the framework is just a base skill plus an improver skill.

## How to write self-improving skills for agents (Warp's tips)

1. **Principles, not rules** — instruct as for a smart person; "look for
   repeated code" beats exhaustive naming rules.
2. **Explain the why** — rationale lets the agent reason and generalize.
3. **Make feedback effortless** — capture it where people already work (PR or
   issue comments), automatically, no extra submission step. Low friction keeps
   signal flowing.
4. **Small skills, progressive disclosure** — skill file references resource
   files and scripts rather than loading everything into context.
5. **Quality over volume, but volume helps** — a little detailed
   domain-expert feedback beats much binary thumbs up/down, which lacks the why.
   Warp's repo: hundreds of contributors, thousands of code reviews.
6. **Invest in the improver skill** — it is reusable across agents; the code
   review improver is not very different from any other agent's improver.

## The loop in action: Warp's issue triage agent

- Trigger: a new GitHub issue fires a GitHub Action that runs an agent to assess
  complexity and feasibility, assign labels, and suggest a fix direction. The
  inner skill holds what each label means and how to research the codebase.
- Sample issue: the inner skill missed the `ready to spec` label (signals a
  contributor may start product and technical specs). A maintainer commented on
  the issue saying what he expected and why.
- The improver runs in Oz as a scheduled "update triage" agent: authenticates to
  GitHub, runs a Python script bundled with the skill to pull recent issues with
  feedback, summarizes them into a JSON file, reads it back into context.
  Bundling the script is called a best practice (reuse instead of writing fresh
  code each run).
- It extracted the concrete signals and proposed the smallest edit: a PR
  changing the inner skill to apply `ready to spec` when an issue describes a
  real problem even if the UI/UX shape is undefined. The PR description named
  the triggering signals and the change.
- A human reviews, approves, merges; the next triage run inherits it. The human
  merge step keeps a person in control.

## Best practices from the Warp team (Q&A box)

- **Skills vs memory**: skills are procedural, stable, run-agnostic, changed
  deliberately; memory is auto-written by the agent at inference time and
  changes constantly.
- **One improver or one per agent?** A templated base loop for shared parts plus
  domain-specific layers; a handful of improvers can each own one agent, a
  hundred agents should share.
- **Wrong feedback**: assume it happens. Do not accept feedback blindly; give
  the agent context to sanity-check, filter whose input counts, keep a human at
  the filtering or final-review stage.
- **Verifiable domain**: build the verification harness first — reference
  corpus, compare output, fix, repeat.
- **Non-verifiable domain**: use deterministic evals against golden outputs
  where possible; restrict human feedback to domain experts.
- **Is the system improving?** Track global metrics humans already watch (time
  to merge, contributor count, cost) and feed them to the improver agents.
  Roll out crawl-walk-run.

Closes by pointing to a webinar with a live demo.
