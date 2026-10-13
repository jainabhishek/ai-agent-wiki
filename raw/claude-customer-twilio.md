# A Twilio PM on building a self-learning development platform with Claude Code — Anthropic (claude.com customer stories) (raw capture)

> Source: https://claude.com/customers/twilio-qa
> Publisher: Anthropic (claude.com customer stories) · Date: none on page (accessed 2026-10-12)
> Captured: 2026-10-12 via curl (condensed).

Format: Q&A between Anthropic and Michael Carpenter, Director of Product, Programmable Voice, Twilio (11 years at Twilio). Page tags: Industry Software; Company size Large; Product Claude Code; Location North America. Headline stats on page: "425 API tools packaged into a Claude Code plugin"; "Full AI voice agent built in 10 minutes, one iteration".

Intro: Carpenter, working alone with Claude Code, built the "Feature Factory", a self-learning development system. A brainstorm idea goes through a subagent pipeline and comes out as specs, tests, working code, and documentation. The output is a Claude Code plugin that packages Twilio domain knowledge. The intro says "over 51 days"; a later answer says "more than 1,000 commits over 90 days" (the page gives both figures).

## What made you start this project?
- He knew the platform (dozens of products, thousands of parameters). His question was how to structure AI collaboration to produce shippable work: production serverless functions with tests, error handling, and docs, not prototypes.

## What developer-experience problem were you solving?
- Large surface area and silent failure modes. Examples: a misconfigured webhook does not error, it just does not fire; a call can show `completed` because the parent call completed although the child call never answered; a recording callback with a relative URL logs an error only in the Twilio debugger.

## What does the Feature Factory do?
- Pipeline of specialized subagents: architect, spec, test generation, development, review, documentation.
- Hooks capture new learnings whenever an error occurs; custom skills capture domain knowledge from each session.
- First attempt, a plain learnings file of API quirks, failed within four sessions. Replacement: a "documentation flywheel" — hooks write suggestions to a file Claude can read, and the file auto-clears when the docs are updated. Principle: knowledge capture must be lower-friction than the discipline it replaces.
- Results claimed: self-service IVR went from multiple iterations to 5 minutes, one pass; a pizza-ordering AI voice agent (recording, transcription, SMS confirmation) in 10 minutes.

## Building as a PM, not an engineer
- Totals claimed: 1,000+ commits over 90 days, 425 MCP tools, a published npm package, a Claude Code plugin. He credits his domain knowledge plus Claude Code holding the codebase in context.

## The MCP server broken for 35 days
- The MCP server wrapping Twilio APIs failed silently from day one: Claude Code spawned the process, got EOF, and continued with no error or warning.
- During those 35 sessions: 8 validated use cases, 31 documented architectural decisions, 7 specialized subagents, an npm package — all without the tools.
- Fix: 53 lines of TypeScript. Once working, tool-based deep validation caught bugs manual testing missed.

## What surprised you?
- Cross-codebase pattern search: a bug passed a response body as an object instead of a string, which crashes the serverless runtime. A second unrelated bug produced the same error code. After both root causes were known, Claude searched the codebase with one regex and found 29 more instances of the pattern.
- Pushback with evidence, e.g. noting a check tested property existence where the property is always present and the value must be checked.

## Autonomy boundaries set before business logic
- Rule: "CLI is for humans. MCP is for agents." The MCP server reads logs, sends test messages, checks call status, validates configs; it never invokes Twilio CLI commands (deploy, buy numbers, manage infrastructure).
- Four-tier risk model: (1) fully autonomous — read-only queries such as logs and status; (2) controlled with guardrails — e.g. rate-limited test SMS; (3) human approval required — deploying code, configuring webhooks, purchasing numbers; (4) never autonomous — deleting resources, force-pushing, skipping hooks.
- Later "chaos validation" tested whether the system would recommend operations that trigger billable API activity; the tier model caught it.

## Prompt quality over infrastructure
- Session analysis found friction events: misdiagnosed failures, skipped validation phases, wrong tools. First instinct was more infrastructure (queue runner, retry logic, forced orchestration).
- Actual fix: a 40-line markdown file naming the tools to use, saying "do not skip live call phases", and setting per-phase retry budgets.
- Other cases: headless sessions wasting money on infrastructure validation fixed by a different prompt; scope gating for chaos validation fixed by one sentence in the architect prompt. He calls CLAUDE.md the most powerful tool because it loads every session.

## From approving every step to autonomous
- 23 design decisions over 40 days. Day one: human approval gates after every pipeline phase (six interruptions per feature). By day 45: headless, no human in the loop, real phone calls, real validation.
- Stall detection: surveyed other autonomous coding systems; none rely on fixed turn limits. Pattern rules: same tool called three times with the same input = stall; alternating patterns = oscillation; no file changes = idle.
- Then: safety floors replaced infinite budget defaults; sandbox mode for isolation; phase retry to keep partial progress when an agent hits its turn limit.

## Building memory/dreaming vs managed infrastructure
- "Build core pieces or an MVP, then integrate." He built local memory and "dreaming" himself (mostly API calls) to understand the abstraction and costs (dreaming cost, memory search latency, curation rules), so he can evaluate Managed Agents from first principles.
- Single-developer memory is a file-system problem; multi-tenant agent memory with audit trails is an infrastructure problem.

## Advice for a first serious Claude Code project
- Treat CLAUDE.md as the project's constitution, written for a brilliant colleague who forgets everything between sessions.
- Document what burns you; automate what you forget; build the flywheel early.
- Graduate trust with evidence: start supervised, raise autonomy one step at a time.
- Write collaboration guidelines early. On day four he added a CLAUDE.md line framing the pair as collaborators and encouraging evidence-based pushback; he never revised it and calls it the most important instruction in the project.
