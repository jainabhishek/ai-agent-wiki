# Coding sessions are longer and use more context. Claude Opus 5.5 is built with that in mind. — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/claude-opus-5-5-built-for-coding-sessions-that-use-more-context
> Publisher: Anthropic (claude.com articles) · Date: 2026-09-24
> Captured: 2026-10-12 via curl (condensed). Two in-body figures transcribed from images.

Author: Michael Segner. Category: Best practices, Perspectives, Insights.
Product: Claude Code, Claude Enterprise. Listed reading time 6 min. Subtitle:
Opus 5.5 is priced and trained to optimize costs for how developers code now.

## Introduction
- Anthropic estimates Claude Opus 5.5 costs about 40% less to run than Opus 5
  for typical token-billed workloads.
- Largest difference for token-billed users: longer, higher-context sessions,
  which became more common in the prior six months.

## Claude Code trends
Aggregate Claude Code usage, March to September 2026. Prompts per session were
steady. Text figures:
- Claude works 3.3x longer per prompt, with more than 40% more model calls per
  prompt (the figure labels this "~50%"); 68% fewer interruptions.
- Developers are about 2x as likely to connect a tool server or use a skill, and
  a third less likely to paste text into a prompt.
- Context per request grew 2.6x; input-to-output token ratio moved from 189:1 to
  324:1.
- Conclusion: Claude reads more tokens; ensure context is necessary and as much
  as possible is served from cache.

## What makes Opus 5.5 cost effective for long, context heavy sessions
Three changes: pricing, model behavior, and the Claude Code harness.

### Cache is cheap
- For token billing: input and output prices cut 20%; cached-read price cut 60%
  (relative to Opus 5). Cache reads are the majority of agentic and coding cost.
- Because context per request grew ~2.6x, the same price change saves more on
  current traffic than six months earlier.
- Claim: at publication, an Opus 5.5 cached token costs a fifth of competing
  models' while outperforming them.
- Figure "Claude Opus 5.5 and GPT-6 Astra" (price per million tokens; sources
  anthropic.com/claude-opus-5-5 and OpenAI API pricing, standard tier, short
  context, 2026-09-22):
  - Input $4.00 vs $10.00 (60% less); output $20.00 vs $50.00 (60% less);
    cache read $0.20 vs $1.00 (80% less).
  - Evals (Opus 5.5 at max effort unless noted): Terminal-Bench 4.0 66.4% vs
    57.9% (Opus 5.5 at xhigh, Astra at high, each model's highest; Astra scores
    as reported by OpenAI); FrontierCode v1.1 54.4% vs 53.3%; GDPval-AA v2.1
    1846 vs 1542; AutomationBench 40.0% vs 41.4% (scores from Zapier);
    Terminal-Bench-Science 0.1 58.7% vs 64.6%.

### Claude Code is better at using the cache
- Described as less specific to Opus 5.5; result of Claude Code features from
  the prior six months. Despite the trends, input that misses the cache
  decreased by more than 50%.
- Fewer accidental cache breaks: small ones (refreshing a login) and larger ones
  (adding instructions mid-conversation, loading tools on demand).
- For newer models such as Opus 5.5 and Fable 5.1, effort level can be changed
  mid-session without resetting the cache.
- API-key and cloud-provider users can now set a one-hour cache lifetime
  (subscribers already had it). Forked subagents start from the parent's cache.

### The same task, but with fewer turns
- Opus 5.5 can need fewer turns. Zeta Labs reported fewer turns and tool calls
  per task than Opus 5, at nearly half the cost, with twice as many of their
  hardest tasks completed.
- Quotes Addy's post "The cost of a task on Opus 5.5": on well-scoped tasks both
  models take about the same turns and only the price cut applies; the gap is
  largest on open-ended tasks; measure on your codebase.
- A saved turn is more cost-efficient than a cached token.
- Opus 5.5 generates output more than 30% faster than Opus 5 (less waiting, not
  fewer tokens).

## Protect your cached reads
- Organizations now ask developers to scale efficiently. Run `/usage` in Claude
  Code to see the cached-read share, then:
  - pick the model at session start, not midway;
  - compact before stepping away, not after;
  - on an API key or cloud provider, set the one-hour cache lifetime for long
    sessions.
- Points to "What a task costs on Opus 5.5" for worked numbers.
