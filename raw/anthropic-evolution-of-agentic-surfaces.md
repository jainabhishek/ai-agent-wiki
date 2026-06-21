# The evolution of agentic surfaces: building with Claude Managed Agents (raw capture)

> Source: https://claude.com/blog/building-with-claude-managed-agents
> Publisher: Anthropic (Claude blog) · Date: 2026-06-10
> Captured: 2026-06-21 via WebFetch (condensed).

## Architectural evolution

1. **2023 — "tokens in, tokens out":** developers built their own agent loops.
2. **2025 — Claude Agent SDK:** a tuned harness, but deployment complexity remained.
3. **2026 — Claude Managed Agents:** decouples the reasoning engine from the
   execution environment.

## Key pattern: brain–hands separation

Decouple the **harness** (which calls Claude) from the **sandbox** (where code
executes). "The harness that calls Claude runs separately from the sandbox where
code executes, and the session — an append-only log of every model call, tool
call, and result — connects the two."

Benefits:
- **Latency** — Claude begins reasoning while environments spin up in parallel
  (~60% p50, ~90% p95 improvement).
- **Security isolation** — credentials live in separate vaults, not in sandboxes.
- **Session durability** — runs persist as immutable event logs, enabling
  resumption and observability.

## Engineering guidance: harness–model co-evolution

Harnesses must evolve with models. "Context anxiety" example: Claude Sonnet 4.5
rushed completions near context limits, so harnesses added context resets. On
Claude Opus 4.5 the behavior vanished, making those resets pure overhead.

**Best practice:** delegate harness tuning to the platform rather than maintaining
custom loops, freeing teams to focus on domain expertise and context management.

## Three core resources for production agents

- **Agents** — model, prompt, tools, guardrails.
- **Environments** — sandbox, networking, pre-installed packages (Anthropic-managed
  or self-hosted).
- **Sessions** — isolated runs with persistent event history; pause/resume + audit.

## Security & infrastructure

- Credentials via **Vaults** with envelope encryption; access via signed request
  tokens; secrets stay outside sandboxes.
- Deployment options: Anthropic-managed cloud containers; self-hosted sandboxes
  (execution inside your VPC); MCP tunnels to private network servers.
