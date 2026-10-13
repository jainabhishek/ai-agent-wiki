# n8n turns natural language into workflow automations with Claude — Anthropic (claude.com customer stories) (raw capture)

> Source: https://claude.com/customers/n8n
> Publisher: Anthropic (claude.com customer stories) · Date: none on page (accessed 2026-10-12)
> Captured: 2026-10-12 via curl (HTML converted to text locally, then condensed).

Page metadata: Industry: software. Company size: medium. Product: Claude Platform. Location: EMEA. Speakers: JP van Oosten (Engineering Manager, AI team), Oleg Ivaniv (Lead Engineer, AI Workflow Builder), Ophir Prusak (Product Marketing).

## Headline numbers (self-reported)

- 2 months from concept to first production of the AI Workflow Builder.
- Cuts 80% of the work of building a workflow; engineers do final refinements.

## Company

n8n is a workflow-automation platform (visual builder plus custom code) for AI workflows and agents; 170,000+ GitHub stars (top 50 projects of all time, per the page); users from solo founders to Fortune 100.

## Results list

- AI Workflow Builder built on Claude in two months; architecture later became a multi-agent system with specialized agents for different tasks.
- Chat-based workflow creator and debugger replaces the "two-tab" habit (LLM chat in one tab, n8n in another).
- About 80% of a target workflow delivered without manual assembly.
- Reliable function calling for multi-step workflow assembly; Claude rated best on precise instruction following among models tested.

## The challenge — generating a precise structured format

Users used to copy workflows from an external chatbot, paste into n8n, hit errors, and repeat; the external model lacked in-tool context. n8n has shipped AI features since 2023. A workflow is a precise object: nodes found, connected in order, configured with parameters. First approach: have the model emit the workflow JSON directly. This was hard because a one-shot generation needs the full schema, all node definitions, and all connection logic at once. Van Oosten: models have seen perhaps 10,000 n8n workflows versus millions of TypeScript files.

## Selecting Claude for instruction following

- Switched to a tool-based architecture: Claude adds nodes one at a time, connects them, and configures them through discrete function calls — "much more digestible for the model".
- Across evaluated models, others either over-relied on function calls or ignored them; Claude sat in a "sweet spot" of following instructions while using tools as intended.
- Ivaniv: latency and quality were good.
- Anthropic docs helped with prompt caching; Anthropic's team reviewed the implementation for rate limits before launch. First version: about two months to production.

## Results — assembling workflows by conversation

- Users describe the automation; Claude picks and assembles pieces. First generation takes about 3 minutes versus 10–30 minutes manually.
- Van Oosten: tool calling and coding capability are essential to the approach.
- The in-product assistant has context about the user's actual workflow, so errors are easier to diagnose.
- Since launch: multi-agent system with specialized agents; prompts now heavily tailored to Claude Sonnet 4.5; early experiments with a code-based approach (Claude writes code instead of making tool calls) look promising with more capable models.
- Experienced users gain speed (about 80% done automatically); first-time users get a starting point past "I don't know what I don't know" (Prusak).
- Also used for debugging broken workflows. Internal example: a complex engineering-progress workflow used multiple form nodes correctly on the first try, which van Oosten attributes to per-node-type prompt optimization.

## Future use cases

- Exploring node-by-node or subgraph-by-subgraph building that mirrors how experts build, for a tighter feedback loop; today the user sees a completed workflow at the end.
- Expanding multi-agent architecture and code-based generation.
