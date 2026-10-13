# How Block orchestrates Claude Fable across thousands of pull requests — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/how-block-orchestrates-claude-fable-across-thousands-of-pull-requests
> Publisher: Anthropic (claude.com articles) · Date: 2026-10-08
> Captured: 2026-10-12 via curl (condensed).

Category: Perspectives. Product: Claude Enterprise. Interview format, no author
byline; speaker is Bradley Axen, Head of AI Capabilities at Block. Block builds
Square and Cash App; Axen's team builds AI products including Buzz, an
open-source workspace for human-agent teams. Models discussed: Claude Opus 5,
Claude Fable 5 (CTA links to Fable 5.1). Customer perspective; claims
self-reported.

## How has this technology impacted how you work?

Biggest impact is on how Block builds. In 2025 Claude Code needed much more
manual intervention. Engineering work has shifted toward designing migrations,
reviewing agent behavior, and customer features. Next phase: AI in Block's
products, possibly interfaces built on demand for specific customer problems.

## What can your team do now that it couldn't a few months ago?

- Scale: company-wide code migrations with AI, which rarely worked in 2025.
  Before Fable 5, frontier models needed a well-shaped problem.
- A migration can mean hundreds or thousands of PRs across multiple repos and
  millions of lines. Previously humans coordinated and models handled one or a
  few PRs.
- Now Fable orchestrates across many sessions. A human engineer steers; Fable
  does higher-level design (data models, API specs, algorithms) and directs up to
  dozens of cheaper models (Opus or Sonnet) to make file edits and run tests.
- Economics: early results show frontier tokens spent on upfront planning, then a
  higher share of tokens going to worker models, without quality loss.
- Runs on Buzz (shared channels and threads for humans and agents), which gives
  visibility into progress. A single migration may merge a thousand
  Fable-orchestrated PRs.

## When do you use Claude Fable models over other options?

- Other models (including Opus) have narrowed the gap, but Fable was a step
  change in problem size per run.
- Conversation has shifted to model efficiency: Fable for the big problem,
  smaller models for code-change details. Axen calls this the first time the
  answer was not "always use the frontier model".
- Single-conversation tools do not keep up with ~45 concurrent agents; Buzz has
  multi-agent workflows. Vision: many people talking to many agents, with the
  organization picking efficient models for routine work.

## What's the hardest problem you've thrown at Fable?

1. Multi-thousand-PR migrations orchestrated end to end by Fable.
2. Keeping a ~1M-line codebase from accumulating tech debt as PR volume rises:
   agents make daily or weekly passes over the whole codebase to find cleanup and
   consolidation work.

## With broad access, how do you drive efficient use of frontier models?

Everyone in a technical role gets full frontier-model access. Using Fable for a
README typo wastes resources, so Block is building an **auto-selector** that
recommends a model per task, plus mixed-model multi-agent systems. Goal: operate
efficiently by default.

## Do you advise specific optimization strategies, like effort levels?

- Axen treats the same model at xhigh vs medium effort as almost different
  models; effort is not a linear spectrum. Fable on low may beat another model on
  xhigh.
- Block benchmarks every use case across every model and every effort level of
  each model (a grid).
- Wants clear central defaults ("this model on high for this kind of task"),
  applied automatically by tools, with experts free to explore.

## How are you thinking about incorporating safeguards?

- Some things need guarantees. Merges to main, production deploys, and related
  changes (feature flags) stay with people. Agent code changes must pass
  security checks, then **two humans** approve the deploy; an LLM cannot push
  such changes alone.
- Laptops allow risky actions; remote workstations are easier to secure (and
  avoid problems like agents filling disks). Secure by default: network
  allowlist rather than denylist.
- Move checks out of the model loop: cheap deterministic checks built into work
  interfaces, sometimes a regex; increasingly small classifiers.
- Where blocking is not worth it, agents are deliberately allowed to open PRs,
  review code, and query logging systems and analytical databases.
- There, model-level safeguards matter: model tuning against dangerous actions
  plus Anthropic's safety classifiers. In Block's tests, asked to "hack around"
  dual approval, Claude refused; Block benchmarks this.

## Any advice for other engineering teams?

Individuals accumulate local skills (Axen uses skills to work in Square's web
front end without being a front-end developer). Organizational maturity means
storing that context at system level, so every agent run gets the best
available context.
