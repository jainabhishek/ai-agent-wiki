# Building Effective Agents — Anthropic (raw capture)

> Source: https://www.anthropic.com/engineering/building-effective-agents
> Authors: Erik Schluntz and Barry Zhang, Anthropic Engineering (December 2024)
> Captured: 2026-06-21 via WebFetch (condensed — see URL for the authoritative full text).

## Workflows vs. agents

Anthropic distinguishes **workflows** from **agents** as two kinds of *agentic
system*:
- **Workflows** orchestrate LLMs and tools through predefined code paths. They
  offer predictability and consistency for well-defined tasks.
- **Agents** are systems where LLMs dynamically direct their own processes and
  tool usage, maintaining control over how they accomplish tasks. Suited to
  scenarios requiring flexibility and model-driven decision-making at scale.

## Five workflow patterns

1. **Prompt chaining** — decompose a task into a sequence of steps, each LLM call
   processing the previous output. Add programmatic checks ("gates") between
   steps. Best when a task cleanly decomposes into fixed subtasks; trades latency
   for higher accuracy.
2. **Routing** — classify an input and direct it to a specialized follow-up.
   Enables separation of concerns and specialized prompts. Best with distinct
   categories that classify accurately.
3. **Parallelization** — run subtasks simultaneously (*sectioning*) or run the
   same task multiple times for diverse outputs/votes (*voting*). Good for speed
   or multiple perspectives.
4. **Orchestrator-workers** — a central LLM dynamically breaks a task into
   subtasks, delegates to workers, and synthesizes results. Better than
   parallelization when subtasks aren't predictable in advance.
5. **Evaluator-optimizer** — one LLM generates, another evaluates and gives
   feedback in a loop. Best when there are clear evaluation criteria and
   iterative refinement adds value.

## Agents

Agents begin with a command or discussion from a human, then plan and operate
independently, returning to the human for information or judgment as needed. They
need "ground truth" from the environment (tool results, code execution) at each
step to assess progress.

**Use agents when:** problems are open-ended, the number of steps is hard to
predict, you can't hardcode a fixed path, and the agent operates in a trusted
environment over many turns.

**Avoid agents when:** a single optimized LLM call suffices, or when the latency
and cost of autonomy isn't justified.

## Three core principles

1. **Simplicity** — keep the agent's design simple.
2. **Transparency** — explicitly show the agent's planning steps.
3. **Agent-Computer Interface (ACI)** — invest in good tool documentation and
   testing, just as you would a human-computer interface.

## Tool design (ACI) best practices

- Give the model enough tokens to "think" before it commits to an output.
- Keep formats close to text the model has seen naturally on the internet.
- Avoid formatting overhead (e.g., counting lines, heavy escaping).
- Put yourself in the model's shoes: write clear tool descriptions with example
  usage, edge cases, input formats, and boundaries.
- Apply *poka-yoke* (mistake-proofing) — design tool arguments so it's hard to
  make mistakes.
- Test extensively; iterate on tool definitions in a workbench.

## Key takeaway

Build the *simplest* solution that works, and increase complexity only when it
demonstrably improves outcomes. Start with simple prompts, optimize with thorough
evaluation, and add agents/workflows only when needed. Frameworks can help you
start but can also add layers of abstraction that obscure behavior — understand
the underlying code.
