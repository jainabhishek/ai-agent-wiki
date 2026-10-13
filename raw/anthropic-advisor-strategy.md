# The advisor strategy: Give agents an intelligence boost — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/the-advisor-strategy
> Publisher: Anthropic (claude.com articles) · Date: 2026-04-09
> Captured: 2026-10-12 via curl (condensed).

Category: Announcements. Product: Claude Platform. No author byline. Reading
time 4 min. Subtitle: pair Opus as advisor with Sonnet or Haiku as executor for
near-Opus intelligence at a fraction of the cost.

## Intro

Anthropic says developers have converged on an "advisor strategy": Opus advises,
Sonnet or Haiku executes. Claimed effect: near-Opus intelligence at near-Sonnet
cost. The post announces the **advisor tool** on the Claude Platform, which makes
the strategy a one-line change to an API call.

## Build cost-effective agents with the advisor strategy

- The executor (Sonnet or Haiku) runs the task end to end: calls tools, reads
  results, iterates.
- When the executor hits a decision it cannot reasonably solve, it consults Opus
  (the advisor). Opus reads the shared context and returns a plan, a correction,
  or a stop signal. The executor then resumes.
- The advisor never calls tools and never produces user-facing output. It only
  gives guidance to the executor.
- This inverts the common sub-agent pattern (large orchestrator decomposes and
  delegates to small workers). Here the small model drives and escalates. There
  is no decomposition, no worker pool, and no orchestration logic. Frontier
  reasoning is spent only when the executor asks for it.
- Result: Sonnet + Opus advisor scored +2.7 percentage points on SWE-bench
  Multilingual over Sonnet alone, and cost per agentic task fell 11.9%.

## The advisor tool

- A server-side tool. Sonnet and Haiku know to invoke it when they need guidance
  on a specific task.
- Sonnet + Opus advisor improved scores on BrowseComp and Terminal-Bench 2.0
  while costing less per task than Sonnet alone.
- Haiku as executor: on BrowseComp, Haiku + Opus advisor scored 41.2% vs 19.7%
  solo (more than double). It trails Sonnet solo by 29% in score but costs 85%
  less per task. Positioned for high-volume tasks.
- Declare `advisor_20260301` in the Messages API request. The hand-off happens
  inside one `/v1/messages` request: no extra round trips, no context management
  by the caller. The executor decides when to invoke. The platform routes curated
  context to the advisor model, returns the plan, and the executor continues.
- Example request shape: `model="claude-sonnet-4-6"` (executor); a tools entry
  `{"type": "advisor_20260301", "name": "advisor", "model": "claude-opus-4-6",
  "max_uses": 3}` alongside other tools. Advisor tokens are reported separately
  in the `usage` block.
- **Pricing.** Advisor tokens bill at the advisor model's rates; executor tokens
  at the executor's. The advisor typically generates a short plan of 400–700
  text tokens, so total cost stays well below running the advisor end to end.
- **Cost controls.** `max_uses` caps advisor calls per request. Separate usage
  reporting lets you track spend per tier.
- **Works with existing tools.** The advisor is one more tools entry; the agent
  can search the web, run code, and consult Opus in the same loop.
- Customer quotes (self-reported): Bolt (CEO Eric Simmons) — better architectural
  decisions on complex tasks, no overhead on simple ones. Genspark (CTO Kay Zhu)
  — improvements in agent turns, tool calls, and score; better than an in-house
  planning tool. Eve Legal (Anuraj Pandey) — on structured document extraction,
  Haiku 4.5 consulting Opus 4.6 matched frontier quality at 5x lower cost.

## Get started

Beta, native on the Claude Platform. Steps:
1. Add beta header `anthropic-beta: advisor-tool-2026-03-01`.
2. Add `advisor_20260301` to the Messages API request.
3. Modify the system prompt for the use case.

Recommendation: run your existing eval suite against three configurations —
Sonnet solo, Sonnet executor + Opus advisor, and Opus solo.

## Footnotes (benchmark conditions)

- **SWE-bench Multilingual:** Sonnet 4.6 solo used adaptive thinking. Sonnet 4.6
  + advisor used Anthropic's suggested coding system prompt with thinking OFF.
  Both at high effort with bash and file-editing tools. Average of 5 trials over
  300 problems in 9 languages. Opus 4.6 was the advisor in all runs.
- **BrowseComp:** all runs thinking off, with web search and web fetch. Sonnet
  4.6 runs at medium effort. Sonnet + advisor used the suggested coding system
  prompt; Haiku 4.5 + advisor did not. No programmatic tool calling, no context
  compaction. 1,266 problems, one attempt each. Opus 4.6 advisor.
- **Terminal-Bench 2.0:** all runs thinking off with bash and file editing.
  Sonnet 4.6 at medium effort. Neither advisor run used the suggested coding
  prompt. Each task in an isolated pod with 3x resources and 1x timeout. Average
  of 5 attempts over 89 tasks. Opus 4.6 advisor.
