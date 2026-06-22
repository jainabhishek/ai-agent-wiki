# How we built our multi-agent research system — Anthropic Engineering (raw capture)

> Source: https://www.anthropic.com/engineering/multi-agent-research-system
> Publisher: Anthropic Engineering
> Captured: 2026-06-21 via WebFetch (condensed).

## Orchestrator-worker architecture

A **lead agent** coordinates: analyzes the query, develops a strategy, and spawns
**subagents** that explore different aspects in parallel, each with its own
context window, then returns findings for synthesis.

## When multi-agent excels vs struggles

- **Excels** on breadth-first queries needing parallel investigation. A
  multi-agent system (Opus 4 lead + Sonnet 4 subagents) **outperformed
  single-agent Opus 4 by 90.2%**.
- **Struggles** on tasks needing shared context or heavy coordination (e.g. most
  coding). Token cost is large: agents use ~4× chat tokens; multi-agent ~15×.

## Token usage drives performance

On BrowseComp, "**token usage by itself explains 80% of the variance**" in
performance (model choice + tool-call frequency explain the rest). Multi-agent
gains come largely from distributing work across separate context windows.

## Prompt-engineering principles (7)

1. Develop agent intuition (Console simulations, step-by-step).
2. Explicit delegation: give subagents objective, output format, tool guidance,
   boundaries.
3. Effort-scaling rules: guidelines for agent count by query complexity.
4. Tool-design rigor: "agent-tool interfaces are as critical as human-computer
   interfaces."
5. Self-improvement: let Claude diagnose failures and refine prompts.
6. Search progression: broad → progressively narrow.
7. Extended thinking as a controllable planning scratchpad.
Philosophy: "instilling good heuristics rather than rigid rules."

## Parallelization

Lead spawns 3–5 subagents at once (not serially); each makes 3+ parallel tool
calls — cut research time up to **90%** for complex queries.

## Evaluation

Three layers: small-sample (~20 queries) early; LLM-as-judge with a structured
rubric (factual accuracy, citation accuracy, completeness, source quality, tool
efficiency); human verification for edge cases (hallucinations on unusual
queries; bias toward SEO content farms).

## Production & reliability lessons

- **State management:** resume from the failure point, not full restart.
- **Debugging:** non-determinism → full production tracing of decision patterns
  (without reading conversation content).
- **Rainbow deployments:** shift traffic gradually so running agents aren't broken.
- **Synchronous bottleneck:** lead runs subagents synchronously today; async would
  add parallelism but complicate coordination/state/error propagation.
- "The last mile often becomes most of the journey" from prototype to production.
