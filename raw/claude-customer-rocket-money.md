# Rocket Money on building agents that fix their own code — Anthropic (claude.com customer stories) (raw capture)

> Source: https://claude.com/customers/rocket-money-qa
> Publisher: Anthropic (claude.com customer stories) · Date: none on page (accessed 2026-10-12)
> Captured: 2026-10-12 via curl (HTML converted to text locally, then condensed).

Format: Q&A interview by Anthropic with Aaron Dignan (VP of Product & AI) and Chase Adams (VP of AI Engineering), Rocket Money. Subject: Rowan, a financial assistant built on Claude that users reach by text message.

## The bet behind Rowan

Dignan: technology brings to everyone what used to be exclusive to the wealthy; Rowan aims to put a personal finance expert in everyone's pocket for people who will not sit in an app.

## What Rowan does

- Sits on top of the Rocket Money app (spending tracking, subscription cancellation, bill negotiation, automated savings). Reached by SMS; in-app version coming.
- Users ask in plain language (spend on X? negotiate this bill? cancel this subscription?) and Rowan does the work.
- Upcoming: free-trial tracking — reads the user's Gmail, notices a trial, texts the day before renewal.
- Adams: proactive by design — notice forgotten subscriptions or odd charges without the user opening a dashboard.

## Why Claude

Dignan: as former co-founders of an AI automation platform they integrated every provider's models; Claude's agentic engineering gave higher quality and reliability and was most natural to build on, plus rate of progress, consistency, and philosophical fit.

## Product bets under improving models

Plan for models 10–20% better over the next couple of years, not only today's models.

## Architecture — agent-workflow hybrid

- Not a monolithic agent with all tools. A classifier on Haiku 4.5 reads each request and routes to a subagent.
- Sonnet 5 for most subagents; Opus for financial tasks needing real reasoning.
- A single response-formatter subagent at the end keeps voice and tone consistent.
- Everything single-responsibility. Adams prefers five back-to-back small-context calls over one huge-context call, citing recency and primacy effects; quote: "With the least context, Claude tends to get the most things right."
- Dignan: the common pattern (simple harness, many tools on an orchestrator, hope) is not enough in finance where accuracy must be 100%; their design lets them trace a failure to a specific classifier or call and fix it for everyone.

## "Third way engineering"

- Neither fully agent-driven nor purely programmatic. A superintelligence would not cancel a subscription by hand repeatedly; it would write code. So repeated tasks become code; the agent's job is to fix the programmatic part when it breaks.
- Adams: a cancellation is codified as a procedure a computer reruns until it breaks (usually a website change). Then an agent finds the break, self-heals the process, and turns it back into code.
- Agent Skills made this click because skills can contain scripts, not only markdown; they wrote it up as a team-wide document.

## Accuracy and what to automate

- Heavy use of structured output so evals run against deterministic results instead of a model grading itself.
- Distinct classifier fall-throughs catch off-topic requests early, keeping conversations on money.
- No meaningful hallucination patterns with beta users so far; suspected cases turned out to be data problems.
- For agentic actions, Claude classifies whether the work completed (e.g., did the cancellation succeed); if not, it classifies why, then hands off to a human in the loop.

## Disagreeing with the industry

Adams: by the time agents are good enough they will not need most of today's scaffolding, but for focused products where correctness matters, a generic harness hides the complexity of keeping the agent on the rails; 70%-there is not acceptable.

## Agents meeting other agents

Dignan: at scale (e.g., calling a company 30,000 times a day) the better move is an API-level agreement; agent-to-agent interactions (their agent calling an insurer's bot) raise game-theory questions.

## Where Rowan goes

Adams: offload small mental tasks (e.g., budget flex for clustered birthdays). Dignan: people will hire a handful of specialized agents rather than one for everything; Rowan stays walled to money.
