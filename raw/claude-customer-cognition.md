# Building an autonomous AI engineer: A Q&A with Cognition — Anthropic (claude.com customer stories) (raw capture)

> Source: https://claude.com/customers/cognition
> Publisher: Anthropic (claude.com customer stories) · Date: none on page (accessed 2026-10-12)
> Captured: 2026-10-12 via curl (condensed).

Page labels: Q&A | Claude Platform. Industry: software. Company size: startup. Location: North America. Interviewees: Scott Wu (CEO) and Walden Yan (co-founder, CPO). All figures are self-reported by Cognition through Anthropic.

Headline figure: 3.5x increase in merged PRs per week after adopting "Claude Sonnet 3.6" (the page's name; it says this model came out in 2024).

Context: Cognition makes Devin, an autonomous AI software engineer launched early 2024; deployed at enterprises including Goldman Sachs, Mercedes-Benz, and the US Army.

## What is hard about an autonomous agent
- Wu: the bar differs from code completion. Users under-specify tasks and hold context the agent lacks; the agent must clarify, ask questions back, and infer intent, because a wrong start derails the whole trajectory.
- The agent must stay on task over long horizons. Much engineering goes into trajectory monitoring: detecting when an agent drifts and steering it back. Before current frontier models, the main failure was inconsistency: quality degraded over long contexts and variance was high.
- Success criterion: a well-scoped ticket comes in, the agent ships it, the PR is merged.
- Yan: a long set of evals gives confidence that swapping in a new model does not regress important product behaviors.

## The Devin experience
- Goal: humans work at the level of decisions and trade-offs. Devin can send a screen recording showing it clicked through the fix to verify it works.

## Why Claude for long-horizon work (Cognition routes across several models)
1. Long-running tasks: other models get confused or forget the task over time.
2. Intelligent tool use: Devin exposes the PR, commit history, codebase files, and a clarifying-question tool; knowing when to use a tool, or none, matters.
3. Expanding a two-line description into the intended details.

## Model evaluation process
- Internal evals by component: mechanical file-edit accuracy; locating the right files for an issue; end-to-end software-engineer tasks.
- Sonnet 3.6 (2024) was the largest benchmark jump they had seen; merged PRs per week rose 3.5x.

## Speed of adoption
- If a new model is strictly better, they swap on day one. Anthropic engineers worked with them on new capabilities; their feedback and examples improved later models (per Yan).

## Harness engineering
- Changing which model handles which part of the workflow forces harness changes: prompts, tool definitions, context management, trajectory monitoring, and guardrails are all tuned to the specific model.
- About 50 to 70 engineers work on the model integration surface.
- VM sandboxing rebuilt many times; hard problem is readiness time: latest code, dependencies, right repos, not only spin-up.

## Growth
- Yan: Devin usage up at least 7x since late last year; new uses include debugging and security scanning; longer consistency lets people let agents run longer. Newer Claude models use third-party MCP servers well to read logs and incidents.

## Focus and outlook
- Wu: no single product covers all of software engineering; Cognition focuses on the full remote-agent workflow. Cognition engineers no longer type code; specs and diagrams, in English, become the source of truth.
- Yan: long-term vision is Devin taking higher-level goals, creating its own tasks, and spinning up its own engineering team.
