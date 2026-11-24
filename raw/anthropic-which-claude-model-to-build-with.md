# Which Claude model should you build with? Fable, Opus, Sonnet, or Haiku — Anthropic (claude.dev blog) (raw capture)

> Source: https://claude.dev/blog/which-claude-model-should-you-build-with/
> Publisher: Anthropic (claude.dev blog) · Date: 2026-11-09
> Captured: 2026-11-24 via curl of the HTML, with tags stripped to text (condensed). Byline: Addy Osmani; category "Playbooks"; 15 min read. JSON-LD `datePublished` is 2026-11-09.
> Capture policy: prose is paraphrased and data is regrouped into tables and bullets; every figure is kept. The one code sample (a Claude Code subagent file) keeps its frontmatter keys and values, with its description and body text paraphrased in angle brackets. Figures A, B, C, D, and E are demo images/videos (by Lance Martin, Addy Osmani, and Dan Fein); only their captions are summarized.
> Scope: no API model ID strings appear in the body. Models named: Claude Haiku 5.5, Sonnet 5.5, Opus 5.5, Fable 5.2, Mythos 5.2 (current); Fable 5.1, Opus 5, Opus 4.8, Sonnet 5, Haiku 4.5 (comparators or fallbacks).

Subtitle: which Claude model to pick, what each costs, and how to combine them.

Opening: four models are generally available (GA) today — Haiku 5.5, Sonnet 5.5, Opus 5.5, Fable 5.2. Mythos 5.2 is positioned as the strongest model for cybersecurity and life-sciences research and is reached through verification programs. Audience: people building on the Claude Platform or using Claude Code.

Fig A: the same alley photo redrawn in code by each of the four models (each wrote a Python program plus its own drawing engine).

## TL;DR

- Default recommendation: Opus 5.5 at its default effort (`medium`) for most coding and knowledge work. Reasons given: it is what Claude Code uses by default, and its per-token price (input and output) is 50% of Fable 5.2's.
- Step down to Sonnet 5.5 for well-scoped everyday jobs such as a bug fix or a spec-driven feature. Caveat: having a clear spec does not by itself make a task Sonnet-sized; a migration or performance job can be well specified yet hard enough for Opus 5.5, or Fable 5.2 if it is large.
- Step down again to Haiku 5.5 for the simplest high-volume jobs (classification, routing, extraction) and for subagents handling side work for a bigger model.
- Step up to Fable 5.2 for: the hardest technical projects (coding, finance, sciences); cases where Opus 5.5 at `high` is not enough; long runs with nobody watching.
- Adjust effort before changing model — it is the finer control over cost and capability. Above `high`, an extra effort level may cost about as much as the next model, so test the larger model at reduced effort instead. Dropping one level may still meet the bar more cheaply.
- What effort buys: longer thinking, more tool calls, more self-checking — plus latency. What it cannot buy: knowledge or skill the model lacks; for that, change model.

## Pick a model by task

| Task | Starting model | Starting effort | Rationale (paraphrased) |
|---|---|---|---|
| Everyday engineering, debugging, multi-PR features | Opus 5.5 | `medium` (default) → `high` | Best cost/capability balance |
| Classification, routing, tagging, bulk extraction | Haiku 5.5 | `medium` (default) | Cheapest and lowest latency |
| Subagents for file search, log reading, summaries | Haiku 5.5 or Sonnet 5.5 | model default | Errors are easy to notice; judgment stays with the main model |
| Chat, interactive sessions | Sonnet 5.5 (Haiku 5.5 for simple high-volume chat) | `low` or `medium` | Quick at those levels |
| Scoped coding: bug fixes, iteration, spec work | Sonnet 5.5 | `medium` → `high` if harder | Half Opus 5.5's per-token price |
| Everyday docs, slides, spreadsheets | Sonnet 5.5 | `high` (default; `medium` in Claude Code) | Fast iteration, design sense; use Opus 5.5 for a complex financial model or a doc synthesized from many sources |
| Repeated agent jobs (investigate, review, draft) | Sonnet 5.5 | `medium` | Defined repeat work seldom needs more |
| Computer use, vision-heavy flows | Opus 5.5 | `medium` | Long agent loops over many screenshots/images |
| Big refactors/migrations, architecture, directing many subagents | Fable 5.2 | `medium` → `high` (API default `high`) | Strongest GA model for technical domains |
| Deep research, scientific/quantitative analysis | Fable 5.2 | `medium` → `high` (API default `high`) | Aimed at the hardest technical work |
| Undecided | Opus 5.5 | `medium` (default) | Claude Code default on Pro, Max, Ultra, Team, Enterprise and Anthropic API; docs name it the starting point |

## The four models side by side

| | Haiku 5.5 | Sonnet 5.5 | Opus 5.5 | Fable 5.2 |
|---|---|---|---|---|
| Positioning | Cost-sensitive volume | Quick help, scoped tasks | Daily driver, complex coding/knowledge work | Most ambitious open-ended technical work |
| Latency | Fastest | Fast | Moderate | Moderate |
| Input $/M (Haiku: prompt ≤100K) | 0.10 | 2 | 4 | 8 |
| Output $/M (Haiku: prompt ≤100K) | 0.50 | 10 | 20 | 40 |
| Input / output $/M (prompt >100K) | 0.50 / 2.50 | flat (no tier) | flat (no tier) | flat (no tier) |
| Cache read $/M | 0.01 (≤100K), 0.05 (>100K) | 0.10 | 0.20 | 0.20 |
| Context / max output | 1M / 128K | 1M / 128K | 1M / 128K | 1M / 128K |
| API thinking | Adaptive; default on; can disable | Adaptive; default on; `between_tools` skips upfront thinking | Adaptive; always on | Adaptive; always on |
| API default effort | `medium` | `high` (Claude Code: `medium`) | `medium` | `high` (Claude Code: `medium`) |
| Fast mode | No | No | Yes | Yes |

Notes: list prices for the Claude API. Claude Code defaults may differ (`/effort` shows yours). Benchmarks live on the Fable 5.2 page. Fig B: each model builds the same portfolio site.

## The trade-offs

### Capability and cost per finished task
- Per-token price and capability usually rise together, yet at task level a pricier token need not mean a pricier or better result.
- Data points:
  - Terminal-Bench 3.0 (from "Spending your effort"): Fable 5.1 @ `max` = 58.0%; Opus 5.5 @ `high` = 58.9%, using half the tokens.
  - FrontierCode 2.0: Fable 5.2 @ `high` = 45.3%; Opus 5.5 @ `max` = 45.5%; Fable's cost per task was roughly half. Implication: on a hard task, try Fable 5.2 before pushing Opus 5.5 beyond `high`. Everyday default stays Opus 5.5 @ `medium`.
  - One 20-problem search benchmark: 2 problems = 43% of spend. So price your hardest tasks, not only typical ones.
- Small models (per Claude Platform cost/intelligence data): strong on high-volume jobs whose outputs can be checked; weaker on long agent loops.
- Fig C: Fable 5.2 renders a 3D scene in sixteen labeled styles.

### Latency against accuracy
- Choose by how long the person can wait; for replies someone is waiting on, begin with Sonnet 5.5 at `low`/`medium`.
- Speed-ups vs predecessors: Sonnet 5.5 runs 30% faster than Sonnet 5; Fable 5.2 produces output as much as 30% faster than Fable 5.1.
- SWE-bench Pro, Opus 5.5, relative to `high`:

| Level | Score vs `high` | Cost vs `high` |
|---|---|---|
| `low` | ≈ −8 points | ≈ 1/3 |
| `medium` | ≈ −2.5 points | ≈ 70% |
| `xhigh` | ≈ +1.4 points | 2.5x |

- Self-verification is often a cheaper, lower-latency fix than more effort. Escalation ladder when quality falls short: (1) let the model check itself (test, build, or a script hitting the endpoint); (2) one effort level up; (3) next model up, beginning below the effort used on the smaller one.
- Cheap-first, retry-failures: with automatic outcome checks, run all at low and only failures at high. Same SWE-bench Pro subset: Opus 5.5 `low` + `high` retries ≈ 97% pass, ≈ $0.17/task; all at `high` = 95.3%, $0.29/task.
- To get speed without losing capability, buy it: fast mode (premium price, faster output) exists for Opus 5.5 and Fable 5.2 on the Claude API.

### Context against cost
- Every current model: 1M-token window. Context is re-sent each turn, so it costs every turn; on long runs, though, most input is billed at cache-read rates.
- Cache-read rates ($/M): Opus 5.5 0.20, Sonnet 5.5 0.10, Fable 5.2 0.20. Consequence: on long cache-heavy runs, Fable vs Opus differs mainly on uncached input and on output, where Fable is double.
- Per "What a task costs on Opus 5.5": per-turn cache read ≈ $0.03 at 150K context, ≈ $0.004 at 20K.
- Lesson: the larger the main model, the more a lean main context matters. Reserve its context for decisions; push bulky reading to cheaper subagents.
- Haiku 5.5 alone has length-tiered pricing: >100K-token prompts bill at 5x the ≤100K rate. Even that tier is 1/4 of Sonnet 5.5 per token; short-prompt Haiku input is 1/20 of Sonnet 5.5's. If every call carries a long prompt, compare Haiku and Sonnet on cost per completed task rather than list price.

## Mixing models

Fig D: one shop project split across four models — Fable 5.2 ports it from JavaScript to TypeScript; Opus 5.5 adds a subscription feature once that lands; Sonnet 5.5 writes product pages; Haiku 5.5 triages customer messages.

### Switch at a natural break
- Caches are per model, so the new model's first turn pays cache-write price for the entire conversation. Make that turn small: `/compact` in Claude Code, or a fresh session seeded with a brief written plan; on the API, seed the new model with a summary rather than the full history.
- Thinking blocks are stamped with their producing model; readability between models:

| Reader | Can read blocks from | Where |
|---|---|---|
| Opus 5.5 | Sonnet 5.5, Haiku 5.5 | Claude API; Claude Models on Google Cloud (Google managed) |
| Sonnet 5.5 | Haiku 5.5 | same |
| Fable 5.2 | Opus 5.5, Sonnet 5.5, Haiku 5.5 | same |
| Fable 5.1 | Opus 5.5 | Claude API |

- Rule: no model reads blocks from a higher-tier model, so moving down always loses prior reasoning; some other moves lose it as well. Unreadable blocks are silently dropped by the API (request succeeds, reasoning gone). The "Preserved thinking" docs enumerate cases. Leaving Fable 5.2 for any other GA model drops its reasoning.

### Put subagents on smaller models
- Subagent = separate context window that returns a summary; billed at its own model's rates. Claude Code settings: `model: haiku` or `model: sonnet` in the definition; `CLAUDE_CODE_SUBAGENT_MODEL` for subagents without one.
- Example file `.claude/agents/log-reader.md`:

```markdown
---
name: log-reader
description: <scan test output/logs after a run; list every failing case>
tools: Read, Grep, Glob, Bash
model: haiku
---

<body, paraphrased: go through the supplied logs; per failure give file, test name, first error line; make no file edits>
```

- Give small models only tasks where errors surface quickly (locating files, running tests, log reading). Code edits and judgment belong to the main model — a misread search result from a small model costs the main model tokens chasing the wrong file.
- Fig E: Opus 5.5 plans map layers; parallel Haiku 5.5 subagents draw them.
- Explore: in current Claude Code the built-in Explore subagent uses the session's model (no longer fixed to Haiku), capped at Opus on the Claude API. For cheap exploration, define a custom subagent named Explore with `model: haiku`. `ANTHROPIC_DEFAULT_HAIKU_MODEL` pins the `haiku` alias.
- `haiku` alias resolution:

| Platform | Resolves to |
|---|---|
| Anthropic API (Claude Code v2.1.293+) | Haiku 5.5 |
| Amazon Bedrock, Google Cloud, Microsoft Foundry, Claude Platform on AWS | Haiku 4.5 |

- `opusplan` (Opus plans in plan mode, Sonnet executes) places edits on Sonnet — opposite to this advice. Measure before adopting as default.

### Escalate hard decisions to an advisor
- Advisor tool (beta): a quicker, cheaper executor runs the job and may consult a stronger advisor mid-task. Billing is mostly at executor rates. Value appears only if the advisor brings missing capability and the executor actually consults — which it does less at low effort.
- Candidate use: agent work dominated by routine turns. But the platform cost guide's advisor table had four pairings, and no pairing clearly outperformed its executor alone. First measure how often your executor consults.
- Accepted advisors (examples): Sonnet 5.5 executor → Fable 5.2, Opus 5.5, Opus 5, Sonnet 5.5. Fable 5.2 executor → Fable 5.2 or Mythos 5.2 only.
- Weak case: Opus 5.5 executor (`high`) + Fable 5.1 advisor, internal coding benchmark → 90.1%, $2.92/attempt; +1.7 points vs Opus 5.5 solo at `high`, ≈2.1x cost. That margin is within run-to-run noise territory and roughly what one more effort level would give.

### Delegate bulk work to cheaper workers
- Different from side-task subagents: for jobs exceeding one context window, a top model leads, partitions the work, fans it out to many cheap parallel workers, and merges results.
- Data: internal defect-search benchmark, ≈22M tokens of source; Opus 5.5 lead + Sonnet 5.5 workers (max 25 concurrent) ≈ one-third cheaper than Opus 5.5 solo at default effort, similar score.
- Claude Platform option: multiagent orchestration in Claude Managed Agents (coordinator plus worker roster). Not worth it for a single dependent chain or work that fits one window — coordination overhead exceeds savings. See the post on folding subagents into the main loop.

## Check compatibility before migrating

All current models support tools and image input; still, swapping the model name is not always enough. Differences to test:

| Area | Behavior |
|---|---|
| Preserved thinking | Fable 5.2 applies it to all API accounts. Any change before a Fable 5.2 thinking block (system prompt, tools, earlier message) → 400, unless you opt in to dropping affected thinking. Nothing to change via Claude Code, Claude Agent SDK, or Claude Managed Agents. Own history-editing code: make it append-only and test first. |
| Thinking | Opus 5.5, Fable 5.2: always on; disabling → error. Sonnet 5.5: on by default; `between_tools` confines thinking to between tool calls. Haiku 5.5: on by default; can be disabled at effort ≤ `high`. All: parse content blocks by type — a reply may open with thinking. |
| Forced tool use | `tool_choice` `any` or `tool` → 400 on Sonnet 5.5, Opus 5.5, Fable 5.2. Instead: `auto` + `strict: true` on the tool + a prompt line saying when to call it. |
| Computer use | All four current GA models: supported solely through `computer_toolset_20260801`; available on Claude Models on Google Cloud (Google managed) and the Claude API. |
| Haiku 4.5 → Haiku 5.5 | `budget_tokens` → effort level; non-default `temperature`/`top_p`/`top_k` → 400; trailing assistant turn (prefill) → 400, so finish on a user turn. |
| Safety fallbacks | Opus 5.5, Sonnet 5.5, Fable 5.2 classifiers mostly flag cyber and bio. Claude Code may rerun a flagged request on an older model and note it in the transcript. Fable 5.2 inherits Fable 5.1's fallbacks: cyber → Opus 4.8; bio → Opus 5. |

- Systems with several models: design each request for the strictest one (append-only history; `tool_choice: auto` with strict tools; type-based block parsing; prompts and tool descriptions exact enough for the most literal model). Then steps can change tier with no code change. For simple routing (e.g. one model per step type), route in code, not via a model.

## Measure on your own work

Public numbers (SWE-bench Pro, Terminal-Bench above) only pick a starting candidate. Procedure:
1. Take a sample of real tasks, each with an outcome check (test passes, ticket closed, row count right).
2. Run every candidate at 2–3 effort levels, one session each so no cache is shared; take cost per completed task from each response's usage field.
3. Chart score versus spend; a multi-model setup stays only if it dominates every single-model point.
4. Shadow the winner on part of live traffic before switching.

Quick Claude Code version: one backlog task, two models via `/model`, compare `/usage`.

## Learn more (links listed)

Posts: building on Sonnet 5.5; getting the most from Opus 5.5 in Claude and Claude Code; the Opus 5.5 task-cost post; Claude blog posts on choosing a model and on model/effort choice in Claude Code. Docs: model choice, cost-vs-intelligence optimization, effort, Claude Code model configuration, subagents.
