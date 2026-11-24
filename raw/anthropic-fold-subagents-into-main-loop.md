# Building agents: When to fold subagents into your main agent loop — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop
> Publisher: Anthropic (claude.com articles) · Date: 2026-10-22
> Author: Diane Sarkis (Member of Technical Staff, per page metadata)
> Captured: 2026-11-24 via curl (HTML stripped to text). Condensed paraphrase, not a copy.

Page labels: Category Best practices, Perspectives · Product Claude Platform · Reading time 18 min.

Subtitle (paraphrased): on Claude Platform, an agent that uses fewer subagents and instead discloses context and tools progressively can gain quality and lose cost and latency. The post says when and how to migrate.

Intro:
- Anthropic offers a "migration kit": a guided workflow that finds your patterns, evaluates alternatives, and verifies the chosen approach. It ships with a demo on a mock system.
- Definition used: a subagent has its own context window, tools, and instructions, and a coordinator orchestrates it. Subagents work well for verification, parallel work, and modular permissions. Anthropic uses them in its own agents, for example its multi-agent research system.
- Anthropic's Applied AI team saw a pattern in enterprise deployments: folding routers, planners, and domain subagents into the main loop helped. Across several enterprise comparisons, one agent with skills often beat both a single all-purpose prompt and a subagent design on quality, often with lower cost and latency per task.
- Example: one company's customer-facing agent had a dozen specialist subagents. They made a consistent brand voice hard to keep and added latency that hurt users.
- A common proposed design stacks: intent classifier → fixed multi-step reasoning pipeline → user-segment buckets → separate recommendation branches → multi-agent orchestrator. Reviewer feedback was that most of this structure did work the model no longer needs. Most of the need would be met by a single clear system prompt, 4-5 thin data tools, and strict guardrails on output.
- Keep subagents when (three conditions):
  - context bloat causes measurable degradation in a single loop;
  - several tasks must run in parallel in fresh, disposable context windows;
  - a single agent picks tools badly, or the system prompt holds conflicting instructions.
- Anti-pattern: one subagent per team or problem type, so the architecture copies the org chart ("Conway's law at work").

## Agent building failure modes for large organizations

Setup: a company wants one customer interface over many products. Each team builds its own agent; a central platform team adds an orchestrator (orchestrator-subagent, or one agent that calls team agents as MCP tools). Resulting problems:
- **Context management** — someone must decide what passes between agents; details get lost in the exchanges.
- **Subagent sprawl** — each team ships a subagent; firms end up with hundreds that overlap, with no standards and no owner.
- **The Frankenprompt** — each team adds a sentence to the system prompt; rules conflict and the voice drifts.
- **Unvetted, overly localized evals** — each team writes evals tuned to its subtask; nobody owns the full set; leaders decide from diluted local scores.
- **Latency** — one customer compared its multi-agent harness with a single agent loop and found the single loop ran roughly 2x faster.

## Using an agent loop with progressive disclosure

Alternative: disclose context progressively through skills, and tools progressively through tool search. The agent sees short descriptions and loads the full item only when needed. Three reasons:
- **Shared context produces better answers** — in long-running agents, results of earlier tasks stay in the main window, so the agent can connect them. This beats summaries returned by subagents, and means fewer windows and fewer lossy handoffs.
- **Progressive disclosure prevents context bloat** — one agent can cover many tasks without one huge system prompt, which removes the main old reason to split. Anthropic cut Claude Code's system prompt for more advanced models by over 80%, partly by disclosing skills and tools progressively.
- **Models are more capable** — from Opus 4.5 on, models handle far more in one loop than teams expected. Thinking cannot be turned off on Opus 5.5 and Fable 5.1. Recent models narrate progress and check their own work, which makes some harness parts redundant. Each new model lets more decisions move from harness to model. A simpler loop also migrates more easily; in customer migrations, rigid multi-agent structures often kept the new model from taking on more work.

Discipline required: a tightly managed system prompt; skill and tool descriptions that fire when they should; deliberate handling of context windows, memory, and note-taking.

Ownership: one small central team owns end-to-end quality and the system prompt and vets each new tool and eval before release. Small size keeps iteration fast and coordination cheap.

If you still choose multi-agent: start from the simplest pattern that could work (generator-verifier, orchestrator-subagent, or another). Split by context: hand each subagent a job with few dependencies on the rest of the system, and ask for a compact result back (independent research paths, separate components with clean interfaces, black-box verification). Splitting by problem type causes a "telephone game", where each handoff loses fidelity.

## How to fold subagents into the main agent loop

Target single-loop design:
- One model, one context window, an open-ended tool loop. The harness sets limits: turn and cost budgets, write gates.
- Per turn, the model issues several tool calls at once. The harness executes them concurrently and hands unprocessed results back to that same model, which then picks the next move: more calls, a user question, or a final reply.
- The loop ends on an answer or a budget hit. A goal or verifier check may run after the answer.
- On turn one the model writes its plan into context and revises it as results arrive. Main difference from orchestrator plus specialists: the planner is also the executor, so it can change the plan mid-turn.
- The agent manages its own context loading:
  - No code step that rewrites the plan from a rule catalog; the model picks each step.
  - Ordering and domain procedure go into skills.
  - Hard limits (validation, approval gates) and mid-conversation needs (e.g. memory lookup) go into tools.
  - Code still loads cheap, almost-always-relevant context (e.g. entity resolution) and handles mechanical work (payload construction, stream parsing, resuming a clarification) inside tools.

This design also suits the goal of an agent that understands a user's high-level aims and acts for them, because all learned context stays in one window. The sections below describe a staged migration and how several teams keep contributing.

### Task-completion evals

- First step: an eval set that tells you whether to fold a given subagent. Working structure: one shared end-to-end set owned by the central team, plus small per-skill sets shipped by each owning team. 10 golden examples is enough to start.
- Start by grading the final message against a rubric. While an orchestrator exists, also track routing accuracy (right subagent chosen?). After folding, check that the correct skill was loaded or the correct tool was called. Move toward task-completion evals over time; they matter most for comparing architectures.
- Where internal systems are hard to replay and users hard to simulate: Anthropic records timestamps on key events so it can replay them later as targeted evals.

### Reducing subagents over time

Path to a single loop: fold subagents into tools and skills, in one of three ways: merge domain subagents together, invoke them as tools, or swap them for skills plus tools.

### Combining domain agents

- Before merging anything, have a small end-to-end eval in place. Fold by shared context, starting with the most-used subagents.
- Good merge candidates: specialists where one consumes another's output, where both read the same data, or where both are usually invoked together. If a large share of production traffic is specialist A then specialist B, that pair is tightly coupled and a merge candidate.

### Subagents called as tools

- When one of the three keep-conditions holds, let the main agent call the subagent as a tool, so the main agent keeps the user conversation.
- Use a full handoff (subagent takes over the conversation) only when the subagent must talk to the user directly. All other cases can become skills and tools inside the main loop.
- Benefits: a shared response schema for subagents; the main agent checks conclusions against real data; smaller input to any final synthesis step. No subagent rewrite needed, and it gives a task-completion baseline before folding.
- Remaining failure modes: specialists still have separate prompts, contexts, owner teams, and evals; every call still returns a lossy summary; every call nests another model loop, which costs latency.

### Folding subagents into the main agent via skills and tools

- Migrate subagents one by one: each one's prompts become skills and its API calls become MCP tools. Compare eval scores with and without that subagent, then decide.
- Look at which tasks flipped, not only the final score. In a sample support agent, folding one subagent into another cut latency but broke a passing process: the main agent held the order-lookup tool and answered alone, and never consulted the shipping specialist about the delivery date.
- Before each change, make sure the eval has a task for each agent chain that runs together in production and for each rule the agent must not break. Run each task more than once; in the support example the break showed up in just one run out of two.

## How several teams can contribute to a single agent

Knowledge bases, skills, and MCP tools can supply domain reasoning. Teams move from owning agents to owning skills and tools. One small central team keeps the system prompt and end-to-end quality and vets new skills, tools, and evals.

### MCP tools

- Use tools when the agent must act, read live system data, or return a fixed-shape result. Tools can also keep calling subagents during migration.
- Group tools by user intent, not one per API. Once the system prompt holds more than 30-50 tool definitions, the model starts choosing tools worse.
- Turn on tool search with deferred loading. Keep hard preconditions few and put the needed ones inside tools: when tool Y depends on X's result, Y verifies that result exists and, if not, tells the model what to do next.
- Per-user permissions follow the same pattern. Every tool looks up the caller's rights and, when access is missing, answers with a readable refusal. So a single loop handles users at different access levels, with no separate agent per level.

### Skills

- Use skills when the agent must know how a team works: the steps, rules, and judgment calls that previously lived in a specialist subagent's prompt.
- Give skill maintenance back to skill authors; Claude can build, test, and prune skills with other skills.
- Against skill sprawl: a DRI per team owns its skills and keeps them well made, distinct, and shipped with evals.
  - `/skill-creator` — author new well-formed skills; audit existing ones to trim, deduplicate, restructure.
  - `/skill-doctor` — shows each skill's cost and usage frequency so dead weight can be deleted.

### Knowledge bases

Use for reference material needed only some of the time (policies, metric definitions, product specs). Put it behind a search or lookup tool the model calls, or ship it as reference files inside a skill. Do not have code fetch it and paste it into prompts.

## Tools to accelerate this work

Anthropic released Claude API skills; the migration kit chains them into one guided workflow for assessing and moving a multi-agent system to a single loop, with a demo:
- `/claude-api build-eval` — builds a first end-to-end set for the central team, or the small per-skill evals.
- `/claude-api prompt-audit` — flags instructions written for older models in prompts, skills, and tool descriptions and proposes fixes as a diff; finds rules that now make the agent slower or more rigid. Each team's DRI can run it on its own skills and tool descriptions.
- `/claude-api hillclimb` — iteratively improves an app against an existing eval. Use for the "folded in vs kept" comparison (after folding, let it iterate on skill and tool descriptions and see whether the folded version matches or beats the subagent), and for the system prompt.
- `/claude-api cost-optimize` — profiles where calls go and proposes savings one change at a time: prompt caching, trimming unneeded input and output tokens, effort, model choice.

Closing: guidance changes as models change, so the principle matters more than any architecture: measure, change one thing at a time, keep what holds up. As models improve and agents run longer, more subagents can become skills and tools. Do it in steps: build a small end-to-end eval, fold one subagent, retain the subagent only when the folded version scores lower, and repeat.
