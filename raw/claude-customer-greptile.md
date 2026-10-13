# Greptile builds truly agentic code review with Claude Agent SDK — Anthropic (claude.com customer stories) (raw capture)

> Source: https://claude.com/customers/greptile
> Publisher: Anthropic (claude.com customer stories) · Date: none on page (accessed 2026-10-12)
> Captured: 2026-10-12 via curl (condensed).

Page labels: Case study | Claude Agent SDK. Products: Claude Agent SDK, Claude Code. Industry: software. Company size: small. Location: North America. Speaker: Daksh Gupta, co-founder and CEO. Model: Opus 4.5. All figures are self-reported by Greptile through Anthropic.

## Headline figures
- ~90% prompt-cache hit rate through the Agent SDK.
- 1 million issues caught per month.
- 2,000+ organizations served (startups to NVIDIA, Brex, Coinbase); reviews over a billion lines of code per month.
- Team of 10 engineers.

## The problem
Most AI code review tools follow fixed paths: scan PR, run a checklist, emit findings. Greptile treats review as investigation. It had built specialized tools (codebase context retrieval, semantically similar functions, git history, more) but its orchestration layer forced them into a rigid flowchart, so new information from a step could not change the next step. Goal (Gupta): a multi-hop, autonomous system where each step can depend on what the previous one found.

## Building on the Agent SDK
- Considered building their own harness; decided the value was in better review tools, not harness infrastructure.
- Gupta's reasoning: models and harnesses would be coupled, and Anthropic's models were best, which favored the Anthropic SDK.

## Multi-hop investigation
- When the agent sees an unusual calculation or a function that differs from similar ones, it decides what to investigate: git history for why it changed, trace a commit to its original PR for context, compare against patterns elsewhere in the repo. Gupta's framing: detective with tooling, needing a strong orchestrator.
- Runs on Opus 4.5 (Gupta: best coding model for their bug and anti-pattern detection). Prompt caching works well; MCP integration valuable.
- Sub-agents: one handles memory retrieval from a bank of team coding standards, learned codebase idiosyncrasies, and documentation, claude.md files, and cursor rules.
- Hooks inject determinism: ensure every file in a PR is examined — a coverage guarantee enterprise customers need.

## The outcome
- Cache hit rates near 90%; self-hosting customers using their own Anthropic instances can scale review without proportional cost increase.
- Engineering time moved from harness maintenance to tools: codebase understanding, similarity detection, git-history analysis.
- Example: in NVIDIA's open-source PhysicsNeMo, Greptile flagged a precision calculation bug; the author disputed it; the agent replied with evidence (similar functions, git history) and the engineer agreed.
- Customer quote (Jarrod Ruhdland, Principal Engineer, Brex): consistent insights with good signal-to-noise on a stack hard for AI.
