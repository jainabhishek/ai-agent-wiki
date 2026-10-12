# The "think" tool: Enabling Claude to stop and think in complex tool use situations — Anthropic (Engineering blog) (raw capture)

> Source: https://www.anthropic.com/engineering/claude-think-tool
> Publisher: Anthropic (Engineering blog) · Date: 2025-03-20
> Captured: 2026-10-12 via curl (condensed).
> Author: Anthropic (no individual byline on the page).
> The page shows two dates: "Published Mar 20, 2025" and an "Extended thinking
> update" note dated Dec 15, 2025. The publication date (2025-03-20) is used for
> the source; the update note is recorded below.

## Extended thinking update (Dec 15, 2025, banner at top of the post)

- Extended thinking has improved since its release. Anthropic now recommends
  using extended thinking instead of a dedicated think tool "in most cases". It
  gives similar benefits (space to reason through complex problems) with better
  integration and performance. Points to the extended thinking docs.

## Intro

- A "think" tool gives Claude dedicated space for structured thinking during
  complex tasks. Claimed gains: policy following, consistent decisions,
  multi-step problems, with minimal implementation overhead.

## What is the "think" tool?

- Adds a thinking step, with its own space, on the way to the final answer.
- Difference from extended thinking (as of March 2025): extended thinking
  happens before Claude starts its response. The think tool lets Claude, mid
  response, stop and check whether it has the information it needs. Useful in
  long tool-call chains and long multi-step conversations.
- Best when the needed information is not in the user query and must come from
  tool results. Its reasoning is less comprehensive than extended thinking and
  focuses on newly discovered information.
- Recommendation at the time: extended thinking for simpler tool use
  (non-sequential calls, straightforward instruction following) and for
  tool-free coding/math/physics; think tool for complex tools, careful analysis
  of tool output in long chains, policy-heavy environments, and costly
  sequential decisions.
- Tool definition (from τ-Bench): name `think`; description says it gets no new
  information and does not change the database, it only appends the thought to
  the log; use for complex reasoning or "some cache memory". Input schema: one
  required string property `thought`.

## Performance on τ-Bench

- τ-bench tests tool use in realistic customer-service scenarios: simulated
  users, complex agent policies, tools that read and change a database. The
  think tool is part of its standard environment.
- Metric pass^k: probability that all k independent trials succeed, averaged
  over tasks (unlike pass@k, which needs only one success). Measures
  consistency.

### Performance Analysis

- Configurations: baseline (no think tool, no extended thinking); extended
  thinking alone; think tool alone; think tool with optimized prompt (airline
  only). Model: Claude 3.7 Sonnet.
- Headline: airline pass^1 0.570 with think + optimized prompt vs. 0.370
  baseline (54% relative improvement); retail think tool alone 0.812 vs. 0.783
  baseline. (The airline table below lists slightly different k=1 values.)
- Airline table (k=1..5):
  - Think + prompt: 0.584, 0.444, 0.384, 0.356, 0.340
  - Think: 0.404, 0.254, 0.186, 0.140, 0.100
  - Extended thinking: 0.412, 0.290, 0.232, 0.192, 0.160
  - Baseline: 0.332, 0.206, 0.148, 0.116, 0.100
- Optimized airline prompt (system prompt section "Using the think tool"):
  before acting or replying after tool results, use the tool as a scratchpad to
  list applicable rules, check required information is collected, verify the
  planned action complies with policy, and iterate over tool results for
  correctness. Two worked examples: cancelling a flight (verify user ID,
  reservation ID, reason; 24h rule; ticket class and insurance; no flown
  segments) and booking 3 tickets with 2 bags each (membership tier bag
  allowances; payment rules: max 1 travel certificate, 1 credit card, 3 gift
  cards; all methods in profile; 5-step plan ending with explicit confirmation).
- Think + optimized prompt beat extended thinking by a wide margin; extended
  thinking performed about like the unprompted think tool. Attributed to the
  complexity of the airline policy, where examples of how to think helped most.
- Retail table (k=1..5):
  - Think, no prompt: 0.812, 0.735, 0.685, 0.650, 0.626
  - Extended thinking: 0.770, 0.681, 0.623, 0.581, 0.548
  - Baseline: 0.783, 0.695, 0.643, 0.607, 0.583
- Retail policy is easier; space to think alone helped.

### Key Insights from τ-Bench Analysis

- Prompting matters a lot on difficult domains; easier domains may gain from
  access alone.
- Gains held for pass^k up to k=5, i.e., better consistency on edge cases.

## Performance on SWE-Bench

- A similar think tool was in the SWE-bench setup for Claude 3.7 Sonnet,
  contributing to a state-of-the-art score of 0.623.
- Adapted description: no new information, no repository changes, only logs the
  thought; use for complex reasoning or brainstorming, for example to brainstorm
  several bug fixes and pick the simplest, or ways to fix failing tests. Schema:
  required string `thought` ("Your thoughts.").
- Isolated effect: +1.6% on average (n=30 samples with the tool, n=144
  without; Welch's t-test t(38.89) = 6.71, p < .001, d = 1.47).

## When to use the "think" tool

- Tool output analysis (may need to backtrack); policy-heavy environments;
  sequential decision making where mistakes are costly.

## Implementation best practices

### 1. Strategic prompting with domain-specific examples
- Give clear instructions on when and how to use it, with domain examples
  covering: expected reasoning detail, breaking down complex instructions,
  decision trees for common cases, checking all needed information is
  collected.

### 2. Place complex guidance in the system prompt
- Long or complex think-tool instructions worked better in the system prompt
  than in the tool description.

## When not to use the "think" tool

- Costs extra prompt length and output tokens. No improvement found for
  non-sequential tool calls (single call or parallel calls) or simple
  instruction following.

## Getting started

- Test on hard agentic cases (policy compliance, long chains); add a
  domain-customized tool definition plus system-prompt guidance with examples;
  monitor and refine. Claimed minimal downside: it changes nothing unless Claude
  calls it.

## Conclusion

- The think tool improved Claude 3.7 Sonnet on policy adherence and long
  tool-call chains; not one-size-fits-all.
- Footnote: Claude 3.5 Sonnet (New) also gained with the same configuration,
  which Anthropic reads as generalizing to other Claude models.
