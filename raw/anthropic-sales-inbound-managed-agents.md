# How Anthropic's sales team rebuilt inbound with Claude Managed Agents — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/how-anthropics-sales-team-rebuilt-inbound-with-claude-managed-agents
> Publisher: Anthropic (claude.com articles) · Date: 2026-09-30
> Captured: 2026-10-12 via curl (condensed).

Category: Best practices. Product: Claude Platform. Author: Carl Johnson (sales
development leader, Anthropic), with Izzy Lee, Bobby P., Lina Ochman, Yana
Gevorgyan, Jerico Johns, Taylre Duarte. Internal build story; results
self-reported.

## Intro

- Before: Contact Sales form submitters sometimes waited days. Most questions
  were simple (plan price, seat minimum, HIPAA contract requirements) and already
  answered in docs.
- Built a buying agent on Claude Managed Agents (beta) that takes a prospect from
  interest to completed purchase. It holds thousands of conversations a day.
- Escalated leads convert to opportunities more than twice as often as old-form
  leads and close about five days faster.
- Opt-in: customers choose an agent or a sales rep at the start.

## Why the old inbound process broke

Form → BDR qualifies → account executive. Works only if the team can talk to
everyone. Tens of thousands of inbound requests per month overwhelmed the BDR
team; reps answered questions the docs already covered. Goal: knowledgeable
answers at any hour in any language, buying without a rep if preferred, and rep
time spent where it changes outcomes.

## A buying agent that closes the gap

- Deployed on Contact Sales and Pricing pages, in the product (Claude.ai), and in
  emails.
- Flow: customer describes needs → agent asks follow-ups → answers pricing,
  security, and data questions → recommends plan and seat count.
- Three endings: **purchase** (straight to checkout); **hand-off** to a rep with
  full conversation details (larger or complex deals); **quick answer**.
- Modeled on what reps do: understand the customer's problem, current Claude
  usage, and how to help.

## Why did we use Claude Managed Agents?

The agent is a prompt, a handful of tools, and Claude on Managed Agents; the
platform handles hosting, sessions, and tool orchestration. Reasons:
- **Fast to production:** one engineer built the first version in a few weeks.
- **Technical and non-technical contributors:** engineering owned code; sales and
  content leads edited the system prompt directly in the Console. Changes went
  to a staging agent first.
- **Domain over harness:** time went to the prompt, tools, and knowledge base.
- **Versioning:** every change is a saved version; v7 about a week into internal
  testing; weekly prompt changes after launch; new sessions can be pointed back
  to an earlier version.
- **Flexibility:** scheduled runs give a path to other engagement types.

## What we learned building the buying agent

- **Give Claude a goal, not rules.** A short goal statement (understand
  requirements, qualify, recommend the best plan) beat a flowchart of
  qualification rules.
- **Less is more.** Shorter prompts worked best; supply knowledge and context
  (what seat pricing covers, when billing cycles run) instead of procedures.
- **SMEs in the development loop.** Time saved by Managed Agents and Claude Code
  went into working with sales; early and frequent testing.
- **Do what is right for the customer.** The agent often recommends Team over
  Enterprise for small teams; treated as a feature (better retention).
- **Treat every escalation as feedback.** The agent states why it escalates.
  Early reasons were mostly things customers could not yet do self-serve; fixing
  those cut the share of conversations needing a person by about half.

## What changed for customers

Instant answers around the clock; many customers prefer the agent. Self-serve
Enterprise buyers who talked to the agent first understood their purchase
better.

## How the agent changed our sales organization

- Reps spend more time on early education, live conversations, and in-person
  events.
- Leads arrive better informed, convert more often, close about five days faster.
- One inside sales rep went from about 10 emails per deal to about six and
  raised closed-won output 2.5x.
- Described as a first step toward agents across the whole customer relationship.
