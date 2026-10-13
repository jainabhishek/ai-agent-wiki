# Index

The content catalog for this wiki. The LLM updates this on every ingest. Each
page is listed with a wikilink and a one-line summary. When answering a query,
read this first to find relevant pages, then drill in.

## Overview

- [[overview]] — building effective LLM agents; current thesis + map of the wiki

## Sources

- [[anthropic-building-effective-agents]] — Anthropic's field guide: workflows vs.
  agents, five patterns, ACI, start-simple (Dec 2024)
- [[openai-practical-guide-to-building-agents]] — OpenAI's 34-page guide:
  components, orchestration, guardrails (2025)
- [[anthropic-steering-claude-code]] — seven mechanisms to steer an agent: CLAUDE.md, rules, skills, subagents, hooks, styles (Jun 2026)
- [[anthropic-lessons-building-claude-code-skills]] — skills best practices: gotchas, progressive disclosure, model-facing descriptions (Jun 2026)
- [[harnessing-claudes-intelligence]] — three patterns: use what Claude knows, stop doing, set boundaries (Apr 2026)
- [[anthropic-evolution-of-agentic-surfaces]] — brain–hands separation, sessions, harness–model co-evolution (Jun 2026)
- [[anthropic-eng-context-engineering]] — *primary source*: context rot, prompt altitude, just-in-time retrieval, compaction/memory/sub-agents
- [[anthropic-eng-writing-tools-for-agents]] — *primary source*: tool selection, namespacing, token efficiency, eval-with-agents
- [[anthropic-eng-effective-harnesses-long-running-agents]] — *primary source*: two-agent harness, JSON state, human-like verification
- [[anthropic-eng-demystifying-evals]] — *primary source*: grader types, real eval sets, pass@k vs pass^k, eval pitfalls
- [[anthropic-eng-multi-agent-research-system]] — *primary source*: orchestrator-worker, 90.2% gain, ~15× tokens, token-usage explains 80% of variance
- [[anthropic-eng-agent-skills]] — *primary source*: SKILL.md, three-level progressive disclosure, composability, cross-surface support
- [[cursor-agent-swarm-model-economics]] — *practitioner case study*: coding-swarm coordination, context isolation, review lenses, and model economics (Jul 2026)

### Harness, runtime, and containment

- [[anthropic-eng-scaling-managed-agents]] — Managed Agents internals: session, harness, sandbox behind small interfaces; vaulted credentials (Apr 2026)
- [[anthropic-eng-how-we-contain-claude]] — sandboxing Claude across products; environment first, model second; missed risks (May 2026)
- [[anthropic-eng-claude-code-sandboxing]] — Claude Code sandbox launch: filesystem + network isolation, 84% fewer prompts, git proxy (Oct 2025)
- [[anthropic-eng-building-c-compiler]] — 16 parallel agents, no orchestrator, wrote a C compiler; the verifier did most of the work (Feb 2026)
- [[anthropic-eng-claude-code-best-practices]] — original Claude Code guide; many mechanisms since superseded (Apr 2025)
- [[anthropic-eng-claude-code-auto-mode]] — auto mode: injection probe + transcript classifier; measured false blocks and misses (Mar 2026)
- [[anthropic-eng-harness-design-long-running-apps]] — planner / generator / evaluator for multi-hour builds; prune parts as models improve (Mar 2026)
- [[anthropic-harness-for-every-task]] — Claude Code writes per-task multi-agent harnesses; six composable patterns (Jun 2026)
- [[anthropic-prompt-caching-is-everything]] — Claude Code built around the prompt cache: prefix order, cache-safe compaction (Apr 2026)
- [[anthropic-claude-code-in-the-cloud]] — cloud sessions: one VM and branch per task, credentials outside the VM (Oct 2026)
- [[anthropic-building-effective-agent-automations]] — scheduled agent on Managed Agents: bookmarks, confirm-then-record, budget caps (Oct 2026)
- [[openai-agents-api-guide]] — Agents API vs. Agents SDK vs. Responses API; computer-use approvals; Aug–Oct 2026 changelog
- [[openai-codex-as-a-platform]] — the open Codex harness as an embeddable runtime: `codex exec`, SDK, app-server (Aug 2026)
- [[openai-one-year-of-responses]] — five Responses API case studies: background jobs, gather-then-reason, multi-agent (Mar 2026)

### Tools, MCP, and context

- [[anthropic-eng-advanced-tool-use]] — Tool Search, Programmatic Tool Calling, Tool Use Examples (Nov 2025)
- [[anthropic-eng-think-tool]] — a no-op "think" tool for reasoning between tool calls; superseded by built-in thinking (Mar 2025)
- [[anthropic-eng-code-execution-with-mcp]] — MCP servers as code files in a sandbox; one task ~150K → ~2K tokens (Nov 2025)
- [[anthropic-seeing-like-an-agent]] — Claude Code tool-design case studies: AskUserQuestion, TodoWrite → Tasks, Grep over RAG (Apr 2026)
- [[anthropic-new-rules-context-engineering-claude-5]] — Claude Code system prompt cut >80% for the Claude 5 generation; judgement over rules (Jul 2026)
- [[openai-private-mcp-servers]] — Secure MCP Tunnel: outbound-only client for private MCP servers (Jun 2026)
- [[openai-automating-repetitive-work-codex]] — Codex + Runme notebooks: plan, approve, execute, keep the notebook as context (Aug 2026)

### Skills and evals

- [[openai-shell-skills-compaction]] — Responses API skills, hosted shell, server-side compaction: ten tips (Feb 2026)
- [[openai-skills-for-oss-maintenance]] — Agents SDK repos run on repo-local skills, `AGENTS.md` triggers, Codex in CI (Mar 2026)
- [[openai-testing-agent-skills-with-evals]] — skill evals: trigger tests, trace grading, schema-bound rubric grading (Jan 2026)
- [[anthropic-automating-eval-design-hillclimbing]] — four eval properties, the adversarial-sampling trap, train/test hillclimbing (Sep 2026)
- [[anthropic-eng-infrastructure-noise-evals]] — container limits alone move agentic eval scores up to 6 points (Feb 2026)
- [[anthropic-eng-eval-awareness-browsecomp]] — Opus 4.6 recognized BrowseComp and decrypted its answer key; eval integrity is adversarial (Mar 2026)
- [[anthropic-eng-ai-resistant-evaluations]] — a hiring take-home fell to two Claude generations; unusual puzzles last longest (Jan 2026)

### Model-scoped prompting guidance

Per-model contracts, not general theory. Each carries `models:` + `as_of:`. When a
vendor stops listing a model as current, its page moves to "Legacy" below with
`status: legacy` and a pointer to its replacement (see `CLAUDE.md`).

- [[anthropic-prompting-claude-fable-5-1]] — Fable 5.1 / Mythos 5.1: append-only history, call batching, finish-whole-task, compaction (as of Oct 2026)
- [[anthropic-prompting-claude-opus-5-5]] — Opus 5.5: effort-only thinking control, unattended early stops, pasted-text tags, time budgets (as of Oct 2026)
- [[anthropic-prompting-claude-sonnet-5-5]] — Sonnet 5.5: initiative and scope vary with effort, `between_tools`, mid-turn messages, refusals (as of Oct 2026)
- [[anthropic-prompting-claude-haiku-5-5]] — Haiku 5.5: first Haiku with effort, date-grounded search, JSON with tools, chatbot adherence (as of Oct 2026)
- [[anthropic-building-with-sonnet-5-5]] — Sonnet 5.5 launch playbook: choosing vs. Opus, migration steps, effort re-sweep (Sep 2026)
- [[anthropic-getting-most-out-of-opus-5-5]] — Opus 5.5 in Claude apps and Claude Code: define done, name the stops; differs from docs in four places (Sep 2026)
- [[openai-prompting-gpt-6-astra]] — GPT-6 family (observed on Astra): initiative, instruction precedence, style, delegation, testing; migration checklist (as of Oct 2026)
- [[openai-rethinking-skills-prompts-gpt-6-astra]] — audit skills, `AGENTS.md`, and boundary language for GPT-6 Astra (Sep 2026)

- [[anthropic-opus-5-5-long-coding-sessions]] — longer sessions; Opus 5.5 pricing + harness caching changes (2026-09)
- [[anthropic-spending-your-effort]] — what effort changes in Claude Code; Terminal-Bench 3.0 evidence (2026-09)
- [[anthropic-what-a-task-costs-opus-5-5]] — cost of a Claude Code task (turns, cache reads, output, model); effort + routing rules (2026-09)
- [[openai-practical-guide-building-with-gpt-6]] — GPT-6 model choice, prompts, long tasks, computer use, production readiness (2026-10)

#### Legacy (vendor no longer lists the model as current)

- [[anthropic-prompting-claude-opus-5]] — Opus 5: verbosity, over-verification, subagent caps (as of Aug 2026; legacy since Oct 2026)
- [[anthropic-prompting-claude-sonnet-5]] — Sonnet 5: literal instruction following, effort remapping, new tokenizer (as of Aug 2026; legacy since Oct 2026)
- [[anthropic-prompting-claude-fable-5]] — Fable 5 / Mythos 5: long-horizon autonomy, memory, `reasoning_extraction` refusals (as of Aug 2026; legacy since Oct 2026)
- [[openai-prompt-guidance-gpt-5-6]] — GPT-5.6 Sol/Terra/Luna: outcome-first prompts, staged migration (as of Aug 2026; legacy since Oct 2026)

### Batch of 2026-10-12: remaining Anthropic and OpenAI guidance

Sorted from all claude.com articles and customer stories, OpenAI's openai.com
Engineering and Security posts, and its learning-hub guides. Case studies are
self-reported by the company that wrote them.

#### Anthropic: harness, runtime, and loops

- [[anthropic-anatomy-of-commerce-agents]] — skills over subagents, latency/caching, memory, safety in harness, snapshot evals (2026-09)
- [[anthropic-sales-inbound-managed-agents]] — Anthropic buying agent on Managed Agents: goal prompts, versioned iteration, escalation reasons as feedback (2026-09)
- [[anthropic-abc-legal-managed-agents]] — 50+ agents as code on Managed Agents; Slack feedback → PRs (2026-08)
- [[anthropic-choosing-claude-model]] — start with smartest model, tune effort, cost per task, own evals (2026-07)
- [[anthropic-outtake-cyber-investigator]] — long-running investigator prototyped in Claude Code → Agent SDK; invariants moved from prompt to harness (2026-07)
- [[anthropic-getting-started-with-loops]] — four loop types (turn, goal, time, proactive): trigger, stop, primitive (2026-06)
- [[anthropic-kepler-verifiable-ai]] — Claude interprets/plans, deterministic engines retrieve/compute, every number traces to a filing (2026-04)
- [[anthropic-building-agents-claude-agent-sdk]] — Claude Code SDK renamed Agent SDK; loop gather→act→verify→repeat (2025-09)

#### Anthropic: coding agents and Claude Code practice

- [[anthropic-agentic-coding-ci-test-impact]] — CI jobs grew 25x in 6 months; stateless redesign beat three patches (2026-09)
- [[anthropic-ai-code-modernization]] — six steps: target, certificate, promotion policy, prerequisites, workflow, pilot-then-scale (2026-09)
- [[anthropic-ai-native-sdlc-playbook]] — SDLC as loop of committed artifacts; governance enforced at action time (2026-08)
- [[anthropic-claude-code-session-cost]] — token cost model: prefill/decode, cache breakers, context volume (2026-08)
- [[anthropic-datadog-universal-machine-tool]] — Temper: agents emit specs a deterministic kernel verifies then runs (2026-07)
- [[anthropic-fable-field-guide-unknowns]] — finding unknowns before/during/after Claude Code work: blind-spot pass, interviews, quizzes (framed on Fable 5) (2026-07)
- [[anthropic-self-service-data-analytics]] — Anthropic analytics agent: governed data, skills, evals, ablations (2026-06)
- [[anthropic-claude-code-large-codebases]] — agentic search, extension-point order, LSP, config ownership (2026-05)
- [[anthropic-unreasonable-effectiveness-of-html]] — HTML beats Markdown for human-facing plans, reviews, reports, throwaway editors (personal opinion) (2026-05)
- [[anthropic-claude-code-session-management]] — five options per turn: continue, rewind, /clear, compact, subagent (2026-04)
- [[anthropic-onboarding-claude-code-legacy-codebase]] — MacCoss Lab: 700k-line C# with context repo and skills (2026-04)
- [[anthropic-configure-hooks]] — Claude Code hooks: eight events, matchers, stdin/exit-code contract, security (2025-12)

#### Anthropic: multi-agent systems

- [[anthropic-block-orchestrates-fable]] — Fable 5 plans thousand-PR migrations directing Opus/Sonnet workers; two human approvers for deploys (2026-10)
- [[anthropic-coderabbit-agent-orchestration]] — Opus/Sonnet/Haiku planning layer writes PRD before Claude Code; LLM judges score plan quality (2026-05)
- [[anthropic-advisor-strategy]] — advisor tool: cheap executor escalates hard decisions to Opus advisor in one request (2026-04)
- [[anthropic-multi-agent-coordination-patterns]] — five patterns: generator-verifier, orchestrator-subagent, agent teams, message bus, shared state (2026-04)
- [[anthropic-subagents-in-claude-code]] — when subagents help/hurt; .claude/agents; steering ladder (2026-04)
- [[anthropic-building-multi-agent-systems]] — single agent first; multi only for context protection, parallelism, specialization; decompose by context (2026-01)

#### Anthropic: skills and MCP

- [[anthropic-warp-builds-self-improving-agents]] — scheduled improver agent turns PR/issue feedback into reviewed edits to base skill (2026-08)
- [[anthropic-verification-loops-with-skills]] — turn repeated manual checks into verification skills: standalone, embedded, chained, per-PR (2026-07)
- [[anthropic-agents-production-systems-mcp]] — API vs CLI vs MCP; server/client patterns; MCP + skills via plugins (2026-04)
- [[anthropic-improving-skill-creator]] — skill-creator evals, benchmark mode, isolated runs, blind A/B, description tuning (2026-03)
- [[anthropic-building-agents-with-skills]] — one general code agent + skills library over specialized agents; four-layer architecture (2026-01)
- [[anthropic-complete-guide-building-skills]] — 33-page skills guide: frontmatter rules, three test types, five MCP+skill patterns (2026-01)
- [[anthropic-improving-frontend-design-through-skills]] — distributional convergence; ~400-token aesthetics skill (2025-11)

#### Anthropic: evals and model choice

- [[anthropic-cresta-agent-builder]] — Conductor: agent that builds agents on Agent SDK; 4 eval axes; rerun gate per model (2026-10)
- [[anthropic-balyasny-evaluates-fable-5]] — hedge fund evaluates on real tasks; controls around the model (2026-09)
- [[anthropic-jetbrains-evaluates-fable-5]] — private-repo evals, cost per task, Fable 5 vs Opus 4.8 (2026-08)
- [[anthropic-cursor-evaluates-models]] — CursorBench underspecified prompts; read traces; route by uncertainty (2026-07)

#### Anthropic: security and identity

- [[anthropic-comcast-booz-allen-exploit-chains]] — Mythos Preview finds exploit chains; validation is the bottleneck (2026-10)
- [[anthropic-auto-mode-default]] — auto mode default; 1,053-tester study, harm re-grading, red-team, cross-vendor injection test (2026-08)
- [[anthropic-auto-mode-production]] — Nuro, Gusto, Garner: deny rules, MCP proxies, manual tier for high-stakes (2026-08)
- [[anthropic-ciso-guide-agentic-ai]] — Deputy CISO: four risk questions, identity spectrum, seven controls (2026-07)
- [[anthropic-securing-ai-native-sdlc]] — stage-by-stage security where Claude writes ~80% of merged code (2026-07)
- [[anthropic-agent-identity-access-model]] — Claude Tag acts as own per-channel principal; creds injected at network boundary (2026-06)
- [[anthropic-cybersecurity-triage-agents]] — CLUE alert triage w/ internal context + parallel subagents; FP share 1/3 → 7% (2026-05)
- [[anthropic-llms-secure-source-code]] — six-step find-and-fix loop; discovery (recall) and verification (precision) in separate agents (2026-05)
- [[anthropic-zero-trust-for-ai-agents]] — Zero Trust framework: threat taxonomy, three control tiers, eight-phase workflow (2026-05)

#### Anthropic: human-agent teams

- [[anthropic-asana-coachable-agents]] — AI teammates w/ scoped roles, access bounded by triggering user, editor-only memory (2026-09)
- [[anthropic-ai-ci-cd-on-call]] — Claude Tag as CI/CD on-call first responder: skills, lessons.md, orchestrator + executors (2026-08)
- [[anthropic-claude-tag-analytics-in-slack]] — Slack analytics agent: live-refreshed skills, scoped service account, telemetry per answer (2026-08)
- [[anthropic-monday-agent-first-platform]] — monday.com from bolt-on AI to agents as assignable teammates; five lessons (2026-08)
- [[anthropic-slack-human-agent-teams]] — Slack CPO: public-by-default channels, handoff loops, clear roles, outcomes over usage (2026-08)
- [[anthropic-building-effective-human-agent-teams]] — multiplayer agents: work in public, one roster, north star, autonomy earned per task (2026-06)
- [[anthropic-running-ai-native-engineering-org]] — Claude Code eng director: JIT planning, review split, blurred roles, three metrics (2026-06)

#### Customer stories (claude.com; self-reported)

- [[claude-customer-caylent]] — migration pipeline on Agent SDK: one agent per stage, Haiku/Sonnet routing, validator agent; 90% fewer hours
- [[claude-customer-cognition]] — Devin Q&A: trajectory monitoring, harness tuned per model, component evals before model swaps
- [[claude-customer-dust]] — tool-call cap raised to 24; three-tier prompt cache; spend -18% (~$10K/day)
- [[claude-customer-esentire]] — security investigations vs expert review in production: >90% agreement on 500+ cases
- [[claude-customer-genspark]] — fixed workflow graph → agent loop over 150+ tools; correct stopping + error recovery enabled it
- [[claude-customer-greptile]] — code review on Agent SDK: memory subagent, hooks ensure every PR file read, ~90% cache hits
- [[claude-customer-lg-cns]] — YAML task decomposition, file-chained context, thin harness for legacy migration (99.1% APIs, ~50% cost)
- [[claude-customer-n8n]] — one-shot workflow JSON → incremental tool calls; ~80% workflow automated
- [[claude-customer-offdeal]] — 12+ fixed workflows → one Agent SDK agent with skills; eval 25→60→85%
- [[claude-customer-rocket-money]] — classifier routes to single-purpose subagents; procedures as code repaired by agent
- [[claude-customer-shortcut]] — parallel per-sheet subagents, then fresh agent executes; benchmark 7.29→8.08 (Opus 4.6)
- [[claude-customer-spotify-boris-office-hours]] — Honk on Agent SDK with CI verification; 73% PRs AI-authored; LLM judge removed
- [[claude-customer-twilio]] — Twilio PM's Claude Code subagent pipeline: hooks, four-tier risk model, staged autonomy
- [[claude-customer-vapi]] — Vapi Composer: model chosen by live tool-call A/B; tool search over 100+ tools
- [[claude-customer-wondr-health]] — parallel safety subagent per turn; role-split models; clinician persona testing

#### OpenAI: Engineering (openai.com)

- [[openai-codex-windows-sandbox]] — offline/online local users, write-restricted tokens, firewall rules, separate setup/runner binaries (2026-05)
- [[openai-self-improving-tax-agents-codex]] — Thrive tax AI: practitioner corrections → reviewed evals; Codex fixes product in bounded tasks (2026-05)
- [[openai-symphony-codex-orchestration]] — open spec: Linear board as control plane; every open ticket gets a Codex agent in its own workspace (2026-04)
- [[openai-websockets-agentic-workflows]] — Responses WebSocket mode caches prior state per connection; ~40% faster loops (2026-04)
- [[openai-responses-api-computer-environment]] — hosted runtime: server-side loop, shell, container, compaction, egress proxy, skill loading (2026-03)
- [[openai-codex-app-server-harness]] — App Server: JSON-RPC protocol exposing one harness to all Codex clients (2026-02)
- [[openai-harness-engineering]] — internal product with zero hand-written code; engineers' job became the agent's environment (2026-02)
- [[openai-in-house-data-agent]] — OpenAI's GPT-5.2 data agent: six context layers, golden-SQL evals (2026-01)
- [[openai-unrolling-codex-agent-loop]] — how Codex CLI builds Responses requests, protects prompt cache, compacts (2026-01)
- [[openai-sora-android-with-codex]] — 4 engineers + GPT-5.1-Codex shipped Sora Android in 28 days, ~85% Codex code (Sora discontinued 2026-04-26) (2025-12)

#### OpenAI: Security and prompt injection

- [[openai-running-codex-safely]] — Codex internal deployment: sandbox, Auto-review subagent, network proxy, keyring creds, rules, managed configs, OTel logs (2026-05)
- [[openai-designing-agents-resist-prompt-injection]] — injections look like social engineering; filters miss; cap damage via source-sink analysis, Safe Url (2026-03)
- [[openai-agent-link-safety]] — URL exfiltration: auto-fetch only exact URLs an independent public crawler has seen (2026-01)
- [[openai-hardening-atlas-prompt-injection]] — RL attacker w/ simulated victim rollouts drives adversarial training + stack fixes (2025-12)
- [[openai-agent-security-enterprise]] — CISO white paper: task-scoped authority, reach and blast radius, task tokens, capability governance, incident response (2026-08)
- [[openai-understanding-prompt-injections]] — seven defense layers, four user steps (logged-out mode, Watch Mode, narrow instructions) (2025-11)

#### OpenAI: developer blog and guides

- [[openai-codex-code-review-rules]] — Codex Code Review reads scoped AGENTS.md rules; 98% vs 58.3%; invariant + safe-path rule style (2026-07)
- [[openai-codex-maxxing-long-running-work]] — white paper: Codex durable threads, memory vault, thread automations, bounded loops (2026-06)
- [[openai-run-long-horizon-tasks-codex]] — Codex ran ~25h on one spec; four Markdown memory files + per-milestone checks (GPT-5.3-Codex, dated) (2026-02)
- [[openai-how-openai-uses-codex]] — seven Codex use cases, six habits (content predates byline) (2026-01)
- [[openai-skyscanner-codex-jetbrains-mcp]] — Codex CLI + JetBrains MCP cuts fix loop 5→3 steps (2026-01)
- [[anthropic-prompt-injection-defenses-browser]] — three-layer defense for Claude for Chrome; ASR measured on Opus 4.5 (legacy) (2025-11)
- [[openai-why-we-built-responses-api]] — Responses replaced Chat Completions/Assistants: encrypted reasoning state, typed items, hosted tools (2025-09)

## Entities

- [[anthropic]] — AI lab; *Building Effective Agents* + operational blog posts
- [[openai]] — AI lab; *A Practical Guide to Building Agents*
- [[openai-agents-sdk]] — OpenAI's code-first agent library (run loop, handoffs, guardrails)
- [[openai-agents-api]] — OpenAI's hosted agent runtime on the Codex harness (beta Sep 2026)
- [[openai-codex]] — OpenAI's coding agent and open-source agent harness
- [[claude]] — Anthropic's LLM family; current: Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5
- [[claude-code]] — Anthropic's agentic coding tool (steering + skills example)
- [[claude-agent-sdk]] — Anthropic's tuned agent harness (2025)
- [[claude-managed-agents]] — Anthropic's managed agent platform (2026)
- [[cursor]] — AI coding product; practitioner research on coding-agent swarms

## Concepts

- [[agents-vs-workflows]] — when to use a dynamic agent vs. a predefined workflow
- [[agent-design-principles]] — start simple, eval, prune scaffolding, design for cache hits
- [[agent-core-components]] — Model, Tools, Instructions
- [[prompt-injection]] — why injection is unsolved; source-sink defense, exfiltration, layered vendor defenses
- [[agent-memory]] — memory across runs and sessions: files, stores, write controls, integrity
- [[tool-design]] — ACI craft + tool types; clarity beats count; scaling large tool libraries
- [[tool-placement]] — where a tool runs: hosted vs client, API vs computer use, IDE/browser tools, app legibility
- [[model-context-protocol]] — MCP at scale: deferred loading, tools as code, credentials and private servers
- [[workflow-patterns]] — Anthropic's five: chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer
- [[agent-orchestration]] — run loop; single-agent first; coordination patterns; subagents; routing
- [[human-agent-teams]] — how people and agents work together: review limits, delegation units, agent teammates
- [[agent-instructions]] — unambiguous, action-oriented instructions from real SOPs
- [[guardrails]] — layered safety: risk assessment, containment, harness controls, human-in-the-loop, incidents
- [[agent-identity-and-access]] — who the agent acts as, task-scoped authority, least agency, credentials
- [[agent-skills]] — on-demand procedural know-how; gotchas, progressive disclosure
- [[agent-steering]] — choosing the right instruction mechanism (CLAUDE.md/rules/skills/hooks/...)
- [[context-engineering]] — load on demand, let the agent manage/persist context, design for cache hits
- [[agent-harness]] — brain–hands separation, sessions, harness–model co-evolution; two-agent long-running pattern
- [[agent-evals]] — measuring agents: eval sets, graders, model-swap gates, production signals, eval integrity
- [[agent-verification]] — checking a single run: verifiers, certificates, validation ladders, separate verifiers
- [[multi-agent-economics]] — optimize cost per accepted outcome across planner, workers, review, and coordination
- [[boundary-contracts]] — the bug class tests can't catch: wrong models of external systems; ground-truth-before-code, fail-loud, ratchet
- [[prompt-tuning-axes]] — the knobs you re-tune on a model migration; axes only, no values (those expire)

## Synthesis

- [[agent-building-best-practices-anthropic-vs-openai]] — where the two guides
  agree/differ + a distilled best-practices checklist
- [[obsidian-graph-analysis]] — wiki graph topology (refreshed 2026-10-13: 184 pages, 3,367 links), hubs, caveats, and
  recommended Obsidian filters
