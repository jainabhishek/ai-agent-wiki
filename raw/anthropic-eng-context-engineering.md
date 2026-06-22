# Effective context engineering for AI agents — Anthropic Engineering (raw capture)

> Source: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
> Publisher: Anthropic Engineering
> Captured: 2026-06-21 via WebFetch (condensed).

## What it is

Context engineering is the evolution beyond prompt engineering: "what
configuration of context is most likely to generate our model's desired
behavior?" It is "curating and maintaining the optimal set of tokens
(information) during LLM inference" — managing system instructions, tools,
external data, and message history across multi-turn agents, not just isolated
prompts.

## Why it matters: context rot

"As the number of tokens in the context window increases, the model's ability to
accurately recall information from that context decreases" — **context rot**, a
consequence of n² attention and less training on long sequences. A gradient, not
a cliff. Treat context as **finite and precious**.

## System prompts: the right altitude

A Goldilocks zone between two failure modes:
- **Brittle**: hardcoded if-else logic in the prompt.
- **Vague**: overly general guidance assuming shared understanding.
Optimal: "specific enough to guide behavior effectively, yet flexible enough to
provide the model with strong heuristics."

Recommendations: organize prompts into sections (XML tags / Markdown headers like
`<background_information>`, `<instructions>`, `## Tool guidance`); start minimal
with your best model; add instructions/examples only to address identified
failure modes; "minimal does not necessarily mean short."

## Tools

Efficient on two dimensions: **information efficiency** (token-economical
results) and **behavioral efficiency** (encourage efficient navigation). Tools
should be "self-contained, robust to error, and extremely clear." Parameters
"descriptive, unambiguous." Avoid bloated/overlapping sets. **Human clarity
test:** "If a human engineer can't definitively say which tool should be used in
a given situation, an AI agent can't be expected to do better."

## Examples / few-shot

Curate "diverse, canonical examples." Don't stuff exhaustive edge cases.
"For an LLM, examples are the 'pictures' worth a thousand words."

## Context retrieval: just-in-time vs pre-loading

- **Just-in-time**: maintain lightweight identifiers (paths, queries, URLs) and
  load at runtime; mirrors human cognition; metadata (folders, names, timestamps)
  guides behavior; progressive disclosure. e.g. Claude Code uses `head`/`tail` on
  large data instead of loading whole objects.
- **Pre-loading** (embeddings): faster but risks staleness and indexing complexity.
- **Hybrid (recommended)**: retrieve some data upfront, explore autonomously for
  the rest. "Do the simplest thing that works."

## Long-horizon techniques

1. **Compaction** — summarize near the context limit and reinitialize. Preserve
   architectural decisions, unresolved bugs, implementation details; discard
   redundant tool outputs. Tune for recall first, then precision. Clearing old
   tool-call results is the lightest-touch form (now an automated platform feature).
2. **Structured note-taking (agentic memory)** — persist notes outside context,
   retrieve when needed. e.g. Claude playing Pokémon tracks objectives, maps,
   achievements across resets. Anthropic released a file-based **memory tool**
   (public beta).
3. **Sub-agent architectures** — specialized sub-agents explore with clean context
   (tens of thousands of tokens) and return condensed summaries (~1–2k tokens);
   main agent synthesizes. Substantial gains on complex research.

Selection: compaction for extensive back-and-forth; note-taking for iterative
dev with milestones; multi-agent for complex parallel research.

## Core principle

"Find the smallest set of high-signal tokens that maximize the likelihood of your
desired outcome." Context stays precious even as models improve.
