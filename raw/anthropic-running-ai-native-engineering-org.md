# Running an AI-native engineering org — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/running-an-ai-native-engineering-org
> Publisher: Anthropic (claude.com articles) · Date: 2026-06-03
> Captured: 2026-10-12 via curl (condensed).

Page labels: Category Best practices, Perspectives · Product Claude Code · Reading time 9 min. No author field on the page; the article is a first-person write-up of a Code w/ Claude SF 2026 talk by Fiona Fung, Director of Engineering for Claude Code and Claude Cowork. No model version is named. Claims describe Anthropic's own team.

Intro: planning and shipping processes (waterfall, then agile) were built around expensive engineering bandwidth. Fung started on Visual Studio when software shipped on CD-ROMs, then saw the move to continuous online updates; now the change is in the time and people needed to write code. On the Claude Code team, writing code, tests, and refactors rarely slows work; the bottlenecks moved to verification, code review, and security. A common question from other leaders: how do humans keep up with code review?

## The processes that quietly stopped working

Processes outlive the gaps they closed. When agentic coding became the team's default, many stopped working; these are the rewritten norms.

### Planning: shift roadmaps to just in time
- Old norm: heavy pre-planning because coding was expensive. A six-month roadmap written when Fung joined was out of date by month three.
- New norm: "just-in-time (JIT) planning" — the right amount at the right time. Planning moved from design docs to discussion in PRs or prototypes; few product reviews. Process: prototype, put many internal users on it, act on their feedback.

### Context gathering: ask Claude, not the author
- Old norm: find who wrote the code. With every PR Claude-assisted, "who made this change?" is insufficient.
- New norm: identify what you need (regression cause, an expert for a customer question, decision context), ask Claude, and check whether Claude can answer directly with more data.
- Also ask whether the question can be automated. Example: a daily Claude summary of customer-feedback channels replaced a manual morning ritual.

### Code review: trust but verify
- The team uses Code Review heavily: Claude handles style and linting, PR feedback requests, catching and fixing bugs before a full commit, and adding tests.
- Humans review where expertise matters: legal partner for risk tolerance; domain experts for trust boundaries and security-sensitive code; PMs and designers for product sense and taste.
- Re-evaluate continually: the trust-vs-verify balance shifts as models improve.

### Team makeup: blurring roles
- PMs code a lot; non-traditional coders do more engineering; engineers take on content and design.
- Fung hires for two profiles: creative builders with product sense, and engineers with deep systems expertise (e.g. systems experts were needed to build Claude Code on the Web and run Claude everywhere). She indexes less on raw throughput, which models supply.
- Before/after table: Planning (six-month roadmaps → JIT: prototype, internal users, act on feedback); Context gathering (ask the author → ask Claude first, then ask if it can be automated); Code review (humans review everything → Claude does style, bugs, tests; humans review where domain expertise matters); Team makeup (fixed roles → blurred roles; hire creative builders and deep systems experts).

## How we rolled out our new norms

Some norms were mandated as team principles; others were left to small sub-teams ("pods"). Non-negotiable core principles:
- Relentlessly dogfood: every team member, including cross-functional partners, uses Claude Code (and Claude Cowork).
- Keep the team as flat as possible: every manager starts as an IC and ships first; one overall mission across Claude Code and Claude Cowork; managers support pods while people move to where the work is.
- Don't hesitate to kill processes that no longer work: explicit permission to question and kill old processes.
Within these, pods choose how to use Claude for triage, how to run planning rituals or standups, and which workflows to "Claudify" first.

## How to know your new processes are sticking

Three metrics to track:
- Onboarding ramp time down: engineers now ship real code in their first week.
- PR cycle time down: digging in shows where the pipeline fails to scale; with more code, build systems and CI may lag.
- Claude-assisted commits up: every commit is Claude-assisted by default; Fung has not seen a non-assisted commit in four months.
Caveat: do not confuse throughput with success; measure the problem you are trying to solve.

## Getting started

- Pick your noisiest workflow (most expensive or most dreaded). Ask whether it still serves its purpose; if so, can it be automated?
- Anecdote: a costly weekly status meeting where people only looked up to give status was cancelled after one person asked why it existed.
