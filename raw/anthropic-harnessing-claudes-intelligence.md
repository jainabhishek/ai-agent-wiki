# Harnessing Claude's intelligence (raw capture)

> Source: https://claude.com/blog/harnessing-claudes-intelligence
> Publisher: Anthropic (Claude blog) · Date: 2026-04-02
> Captured: 2026-06-21 via WebFetch (condensed).

Three core patterns for building applications/agents with Claude that balance
intelligence, latency, and cost, and adapt as Claude's capabilities evolve.

## 1. Use what Claude knows

Build with tools Claude already understands well — bash and text editors — rather
than bespoke tool interfaces. General-purpose tools improve as Claude improves.
("Claude 3.5 Sonnet reached 49% on SWE-bench Verified with only a bash tool and a
text editor tool.") Higher-level features (programmatic tool calling, skills,
memory) compose from these foundational tools.

## 2. Ask "what can I stop doing?"

Re-evaluate assumptions baked into agent harnesses as capabilities expand:

- **Let Claude orchestrate actions** — don't push all tool results through the
  context window; give Claude code execution so it decides what to filter or pipe
  between tools without consuming tokens.
- **Let Claude manage context** — skills for progressive disclosure instead of
  loading all instructions into the system prompt; context editing to remove
  stale info; subagents for isolated task work.
- **Let Claude persist context** — let Claude choose what to remember via
  compaction, memory folders, and strategic summarization rather than relying
  solely on retrieval infrastructure.

## 3. Set boundaries carefully

- **Design for cache hits** — static content first, use messages for updates,
  don't switch models mid-session, manage tools carefully, update breakpoints.
- **Use declarative tools strategically** — dedicated tools for
  security-sensitive actions, UX presentation, or observability — but re-evaluate
  necessity as Claude improves.

## Key guidance

Continuously re-evaluate: "Assumptions about what Claude can't do need to be
re-tested with each step change in its capability." Prune dead weight in harnesses
(e.g. context resets built for older models) as Claude advances.
