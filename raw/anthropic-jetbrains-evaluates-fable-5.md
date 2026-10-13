# Securing the frontier: How JetBrains evaluates and deploys Claude Fable 5 — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/how-jetbrains-evaluates-and-deploys-claude-fable-5
> Publisher: Anthropic (claude.com articles) · Date: 2026-08-13
> Captured: 2026-10-12 via curl (condensed).

Interview format. Category: Best practices. Reading time 7 min. Subject:
Vladislav Tankov, CTO (Agent Systems) at JetBrains. Context given: JetBrains
makes IntelliJ IDEA, PyCharm, and Kotlin; 12.5M+ active users; 88 of the
Fortune Global 100. All results below are self-reported by JetBrains.

## How has frontier AI changed for JetBrains in 2026?
- Tankov (10 years at JetBrains) says the company was among the first LLM
  provider customers. Over the past year, internal and customer skeptics
  changed their view; he says every skeptic in the company changed.

## How do you evaluate new models and decide when to use them?
- Large eval sets built on private repositories, including the JetBrains
  monorepo. Purpose: check whether a model's real-work performance matches its
  public benchmark scores; some models are tuned for public benchmarks and fail
  on actual tasks. Private repos make that easier to check.
- Three leaderboards: best quality, best cost per task, fastest model.
- Fable 5 costs more per token, but its cost per task is lower in some cases,
  especially for complicated, long-running work.

## How did Claude Fable 5 score on your evals relative to previous models?
- Best Python pass rate in the suite: Fable 5 44.3% vs Opus 4.8 28.2% (16-point
  gain).
- Head-to-head: Fable 5 solved 18 Python tasks Opus 4.8 missed; lost 2.
- When its code ran, it passed JetBrains' tests more often than either Opus
  model. Tankov calls code that runs but gives wrong answers the most expensive
  failure to catch.
- About 22% fewer steps than Opus 4.8 to reach a solution.
- On Java tasks, Opus 4.8 repeatedly tried to fetch outside resources that
  rarely help in JetBrains' environment; Fable 5 did not, and worked with the
  code in front of it.

## When do you use Claude Fable 5 over other models?
- Opus is the "workhorse"; Fable 5 is for hard reasoning, when the engineer is
  unsure how to do the task. Example: a tech lead's rich text editor component,
  attempted several times over the years, which Fable 5 nearly one-shotted.
- Long-running agentic-coding experiments: an agent on Fable 5 gets
  specifications (text and images) and builds sophisticated IDE-like apps. The
  agent can also generate the specifications from an existing app. Combining
  both lets JetBrains port an app between runtimes, frameworks, or languages in
  a nearly black-box setup.

## How are you thinking about safety and data retention with today's frontier models?
- JetBrains relies on Anthropic's red teaming for model safety and puts its own
  effort into infrastructure and a safety net around the model and the harness,
  not into changing the model.
- Security is a main Fable 5 use: white-box testing of JetBrains products to find
  vulnerabilities, while preparing for outsiders running similar-class models
  against those products.
- Tension named: a less aggressive classifier lets defenders find more
  vulnerabilities.
- JetBrains would prefer zero data retention, but accepts limited retention as
  the way Anthropic can investigate classifier errors, provided reviews cover
  only the most serious flagged cases. Tankov calls it a fair trade for frontier
  access.

## What's next on JetBrains's AI roadmap?
- Expects models to keep improving. Focus is a "cockpit" for software
  development where agents and people collaborate and people manage the
  process; products across the agentic SDLC; more non-technical roles in
  software creation; governance and ROI clarity for organizations.
