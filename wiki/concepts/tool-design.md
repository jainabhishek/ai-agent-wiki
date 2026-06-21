---
title: Tool Design
type: concept
created: 2026-06-21
updated: 2026-06-21
tags: [tools, aci, best-practices, agents]
---

# Tool Design

> Both guides treat tools as the highest-leverage surface to get right. Anthropic
> calls it the **Agent-Computer Interface (ACI)** and gives it equal weight to
> the human-computer interface; OpenAI emphasizes standardized, well-documented,
> testable tools and warns against tool *overlap*.

## Tool types (OpenAI)

| Type | Purpose | Examples |
|------|---------|----------|
| **Data** | Retrieve context | Query a CRM/DB, read PDFs, web search |
| **Action** | Take actions in systems | Send email, update a record, hand off a ticket |
| **Orchestration** | Other agents used as tools | Refund agent, research agent (see [[agent-orchestration]]) |

Each tool should have a **standardized definition**, enabling many-to-many
relationships between tools and agents. Well-documented, tested, reusable tools
improve discoverability, simplify versioning, and prevent redundant definitions.
(see [[openai-practical-guide-to-building-agents]])

## ACI best practices (Anthropic)

- Give the model **enough tokens to think** before it commits to output.
- Keep formats close to **text seen naturally on the internet**.
- Avoid **formatting overhead** (line counting, heavy escaping).
- Write tool descriptions as if for a new engineer: **example usage, edge cases,
  input formats, clear boundaries.**
- Apply **poka-yoke** (mistake-proofing) — shape arguments so misuse is hard.
- **Test extensively** and iterate on definitions in a workbench.
(see [[anthropic-building-effective-agents]])

## Clarity over count

OpenAI's key finding: the problem isn't the *number* of tools but their
**similarity/overlap**. Some teams handle 15+ distinct, well-defined tools; others
struggle with fewer than 10 overlapping ones. Improve names, parameters, and
descriptions first; only split into multiple agents if clarity doesn't help. (see
[[openai-practical-guide-to-building-agents]], [[agent-orchestration]])

## Use what the model already knows

A complementary Anthropic principle: prefer **general-purpose tools the model is
already good at** (bash, a text editor) over bespoke interfaces — they keep
improving as the model improves. "Claude 3.5 Sonnet reached 49% on SWE-bench
Verified with only a bash tool and a text editor tool." Higher-level capabilities
(programmatic tool calling, [[agent-skills]], memory) compose from these
foundations. Add **declarative/dedicated tools strategically** — for
security-sensitive actions, UX presentation, or observability — and re-evaluate
their necessity as the model advances. (see [[harnessing-claudes-intelligence]],
[[agent-harness]])

## Why it matters

Most agent failures trace back to ambiguous tools or instructions, not model
capability. Investing here pays off before any orchestration complexity. See
[[agent-design-principles]].

## Related concepts

- [[agent-core-components]], [[agent-instructions]], [[agent-orchestration]],
  [[agent-skills]], [[agent-harness]]

## Key entities

- [[anthropic]], [[openai]], [[claude]]

## Appears in

- [[anthropic-building-effective-agents]]
- [[openai-practical-guide-to-building-agents]]
- [[harnessing-claudes-intelligence]]

## Contradictions / open questions

- _None — the two are complementary: OpenAI on tool taxonomy, Anthropic on
  interface craft._
