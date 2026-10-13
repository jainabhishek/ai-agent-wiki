# How we used Codex to build Sora for Android in 28 days — OpenAI (raw capture)

> Source: https://openai.com/index/shipping-sora-for-android-with-codex/
> Publisher: OpenAI (Engineering) · Date: 2025-12-12
> Authors: Patrick Hum, RJ Marsan.
> Captured: 2026-10-12 via built-in browser (condensed). Case study; figures are
> self-reported. The page carries a later banner: as of 2026-04-26 the Sora
> product is no longer available.

## Introduction

- The Sora Android app launched in November 2025, reached #1 in the Play Store
  on launch day, and users generated over a million videos in the first 24 hours.
- From October 8 to November 5, 2025, a lean team with Codex, using roughly 5
  billion tokens, took the app from prototype to global launch. Reported
  crash-free rate: 99.9%. Model: an early version of GPT-5.1-Codex, the same one
  available publicly via CLI, IDE extension, or web.

## Embracing Brooks' Law: Staying nimble to move fast

- iOS had launched with heavy usage; Android had only an internal prototype.
- Instead of adding people (Brooks' Law: adding people to a late project makes it
  later), the team used four engineers, each with Codex.
- Internal build to employees in 18 days; public launch 10 days later. Same
  engineering and reliability bar as a traditional project; Codex is still used
  for new features.

## Onboarding a new senior engineer

Treat Codex like a newly hired senior engineer; spend more time directing and
reviewing than writing.

### Where Codex needs guidance

- It does not infer what it is not told: preferred architecture, product
  strategy, real user behavior, internal norms.
- It could not see the app run on a device (scroll feel, confusing flows); only
  humans covered experiential checks.
- Each session needs onboarding: goals, constraints, "how we do things".
- Deep architectural judgment is weak: left alone it might add an extra view
  model instead of extending one, or put repository logic in the UI. Its
  instinct is to get something working, not long-term cleanliness.
- Codex maintained many `AGENTS.md` files in the codebase. Example top-level
  rule: always run `./gradlew detektFix` before committing, because CI fails on
  formatting or detekt issues.

### Where Codex excels

- Reading large codebases quickly; knows the major languages.
- Broad unit-test coverage (not always deep, but helps against regressions).
- Applying feedback: paste CI failure logs and ask for fixes.
- Massively parallel, disposable execution: test several ideas at once.
- New perspective in design: e.g. surveying several SDKs for video-player memory
  optimizations.
- Code review: often caught bugs before merge.
- Working model: Codex does heavy lifting inside well-understood patterns and
  bounded scopes; humans own architecture, UX, systemic changes, final quality.

## Laying the foundation by hand

- Humans designed architecture, modularization, dependency injection,
  navigation, authentication, and base networking, then wrote a few
  representative features end to end and documented patterns.
- About 85% of the code is estimated to be Codex-written; the planned foundation
  avoided backtracking and was called one of the most important decisions.
- Goal: show Codex what is "correct" for this team rather than dictate each step.
- A test prompt to build the Android app from the iOS code in one go was
  abandoned: it technically worked but gave a poor product experience and
  unreliable code without knowledge of endpoints, data, and flows.
- "Build this settings screen" with little context was unreliable; "build it
  using the same architecture and patterns as this other screen" worked much
  better. Humans set structure and invariants; Codex filled in code.

## Planning with Codex before coding

- Goal: let Codex run long and unsupervised (the post links to a run of more
  than 24 hours).
- "Here is the feature, here are some files, build it" compiled but drifted from
  architecture.
- New workflow for non-trivial changes: ask Codex to read related files and
  summarize how the feature works (data flow from API through repository, view
  model, UI); correct its understanding; co-write an implementation plan like a
  mini design doc (files to change, new states, logic flow); then apply the plan
  step by step.
- Tip: for tasks exceeding the context window, have Codex save its plan to a file
  so other instances can reuse it.
- Benefits: safe long unsupervised runs, easier review against the plan,
  debugging the plan before the code.

## Distributed engineering

- At peak, several parallel sessions (playback, search, error handling, tests,
  refactors), each reporting progress; it felt like being a tech lead of several
  new engineers.
- The review queue was always full. Codex was not blocked by context switching,
  but the humans were. The bottleneck moved from writing code to decisions,
  feedback, and integration.
- Brooks' Law applies again: adding sessions does not give linear speedup; each
  adds coordination overhead.

## Codex as a cross-platform superpower

- Codex was pointed at the iOS and backend codebases. Joke: Codex is the new
  cross-platform framework.
- Principles: logic is portable (Swift → Kotlin preserving semantics); concrete
  examples are strong context.
- iOS, backend, and Android repos were in one environment. Typical prompt shape:
  read the iOS models and endpoints, then propose an Android plan that reuses the
  existing API client and model classes.
- Tip: describe in `~/.codex/AGENTS.md` where local repos live and what they
  contain.
- Cross-platform by translation instead of shared abstraction. Without context,
  Codex was guessing, not refusing.

## The software engineering of tomorrow, today

- Codex became the default loop: understand code, plan, implement, review like a
  teammate's work.
- AI-assisted development increases the need for rigor; Codex's objective is to
  get from A to B now, so humans supply real-world constraints and long-term
  architecture.
- Not a universal recipe; the authors do not claim to have solved AI-assisted
  development.
