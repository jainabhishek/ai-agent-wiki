# Vapi turns natural language into production voice agents with Claude — Anthropic (claude.com customer stories) (raw capture)

> Source: https://claude.com/customers/vapi
> Publisher: Anthropic (claude.com customer stories) · Date: none on page (accessed 2026-10-12)
> Captured: 2026-10-12 via curl (condensed).

Page tags: Industry Software; Company size Startup; Product Claude Platform, Claude Agent SDK, Claude Code; Partner AWS; Location North America. Headline stats: ~3x higher deep activation rate for users who build voice agents through Vapi's Claude-powered agent; 3x recovery rate after a failed first call.

Vapi: enterprise platform to build, deploy, and manage voice agents; API-native and configurable from audio ingestion and endpointing to tool-call structure and fallback logic.

## With Claude, Vapi (claimed results)
- Shipped Composer (assistant that builds and configures voice agents by conversation) from prototype to GA in 2.5 months, team of five engineers.
- Users building through Composer nearly 3x more likely to reach 100 call minutes (Vapi's "sustained usage" milestone).
- Recovery rate tripled for users who use Composer guidance after a failed first call.
- Initial activation (10 call minutes) doubled for users onboarded through natural language.
- Natural-language debugging of live agents: hours to minutes.

## The challenge — strong signups, soft activation
- Platform exposes more than a dozen configuration points. Example customers: a healthcare company with strict data-residency needs handling 250,000 monthly patient calls; a labor marketplace screening 50,000 applicants a month.
- Technical users reached a prototype in a day or two; others went to support, sales, or churned (CEO and co-founder Jordan Dearsley).
- Activation relied on docs, example code, and field engineers. Goal: non-technical user from signup to working voice agent in under 30 minutes using natural language only.

## The solution — selecting Claude for function-calling reliability
- Production experiments across Claude Opus, Sonnet, and Haiku plus other providers' models. Feature flags split live traffic between models; measured tool success rate, error classes, and user-level outcomes.
- Criteria in order: function-calling reliability, output consistency under tool orchestration, latency; cost only after those three.
- Dearsley claims Claude gets tool schemas right on the first try more consistently (e.g. updating an assistant's prompt, adding a squad member, running a simulation, pulling a call log).
- Second factor: Claude Agent SDK. Dearsley built the original prototype on it, reducing agent-loop and context-management code.

## Composer turns natural language into working voice agents
- First prototype built in one evening; GA 2.5 months later; team of five led by Dev Seth (Manager, Product Engineering).
- User states the goal in plain language; Claude has a tool suite mirroring the full Vapi API, picks and invokes tools, streams results with an approve/deny step on any state-mutating action. Multi-turn, persistent across sessions.
- Architecture problem: v1 was one large system prompt with tools attached; the system prompt used more than 50% of the context window before any user message. Fix: modular architecture with a runtime router, shared chat kernel, pluggable UI shell. Adding Composer to a new product surface dropped from ~700 lines of frontend code to ~30.
- Team built the architecture, observability, and fallback between the direct Anthropic API and Amazon Bedrock.
- Now 10+ skills and 100+ tools (web search for prompt details, provisioning phone numbers, simulations against proposed changes, transcript analysis, fleet metrics such as p95 latency). Claude reaches the catalog through tool search; only tools relevant to the current turn enter context.
- Seth: the accuracy gap versus other tested models grows with chain length and tool specialization; Composer often chains a dozen tools in order.
- Vapi customers can also choose Claude Sonnet or Opus (direct API or Bedrock) as the intelligence layer of their own voice agents.

## The outcome — 3x more likely to reach deep activation
- Composer users: 2x more likely to reach 10 call minutes; nearly 3x more likely to reach 100 call minutes vs non-users. After a failed first call, Composer users 3x more likely to reach deep activation instead of churning.
- Solutions engineers build customer-specific demo agents live on prospect calls. Composer reads call transcripts, diagnoses failures, suggests or applies fixes.
- Example: a config option existed in the API with no UI; Composer changed it via the API without waiting for a UI.
