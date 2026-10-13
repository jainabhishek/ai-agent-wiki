# Wondr Health scales trusted health coaching with Claude — Anthropic (claude.com customer stories) (raw capture)

> Source: https://claude.com/customers/wondr-health
> Publisher: Anthropic (claude.com customer stories) · Date: none on page (accessed 2026-10-12)
> Captured: 2026-10-12 via curl (condensed).

Page tags: Industry Software; Company size Startup; Product Claude Platform; Partners AWS, Blank Metal; Location North America. Headline stats: 700+ questions tested by Wondr's team before any real participant met the AI coach; onboarding from 30–60 minutes to a 10-minute guided conversation.

Wondr Health: digital, behavior-based weight-management program sold as an employer benefit (curriculum + human coaches + accountability tools). With AI engineering firm Blank Metal, over a three-sprint engagement, it built "Wonda", an AI coaching layer that extends human coaches. Runs on Claude through Amazon Bedrock. Phase 1 (onboarding) is built and tested and heading into beta.

## With Claude, Wondr Health built
- AI onboarding: 30–60 minutes to a 10-minute guided conversation.
- A testing console where clinical and coaching teams ran 700+ questions across six user personas without engineering support.
- A parallel safety subagent monitoring every turn, escalating to human coaches through Zendesk.
- Onboarding grounded in Wondr's curriculum via a RAG pipeline.
- Continuous improvement through automated evaluators, scored human evaluation rounds, and full conversation tracing.

## The challenge — earning trust in a 10-minute window
- Trust-building that took a coach 30–60 minutes must happen in a 10-minute digital window; early drop-off hurts participant, employer, and retention.
- Coaches overloaded with repetitive questions and cross-system data lookups.
- Wondr's existing Zendesk bot showed participants asked anonymous questions they would not ask a human.
- Blank Metal (Elli Rader, CRO) brought in; it runs its own operations on Claude.

## The solution — a model to trust with sensitive conversations
- Requirement (Jason Dehler, Blank Metal healthcare lead): clinically accurate coach that knows when to hand off to a human.
- Wondr says it chose Claude for empathy, accuracy, and no hallucinations in emotionally loaded conversations; Bedrock chosen for production reliability.
- The parallel safety-agent design depends on the primary model staying on task and the safety model having clear signal; they credit instruction-following.

## Production architecture with safety at the center
- Wonda collects a participant's "My Why", guides goal setting, answers curriculum questions, hands off to human coach.
- Built production-first, not as a prototype. Behavior established on synthetic data outside Wondr's systems, keeping real participant health data out of the build.
- Model roles, all via Bedrock: Claude Opus 4.5 = coaching agent reasoning; Claude Sonnet = escalation detection in the safety subagent; Claude Haiku = automated evaluations as LLM judge.
- Each turn, the safety subagent checks input and history for clinical risk, off-topic behavior, and escalation triggers. On trigger it creates a Zendesk ticket with risk level and full conversation summary, gated for human follow-up by severity.
- API gateway screens every request: authentication, rate limiting, participant-data filtering before the model.
- LangGraph for orchestration; LangSmith for full conversation tracing.
- Custom automated evaluators: verbosity checks, content-accuracy scoring.
- Next.js testing console on Vercel: clinical/coaching teams test across six personas with realistic simulated metadata.
- Wondr arrived with personas, program content, escalation guidelines, and a personality document, compressing weeks of discovery into days.
- Trust problem on two fronts: end users, and Wondr's clinical team. Evaluation: internal employees adopted personas and ran 700+ questions (onboarding, escalations, Wondr content), plus automated evaluators and two rounds of scored human evaluation. Team view: involve clinicians early as evaluation partners, not as a final gate.

## The outcome
- 10-minute onboarding vs 30–60 minutes. Scored response quality improved between the two human evaluation rounds; good reception on tone, empathy, personalization.
- Evaluators told Wonda things they would not tell a human coach.
- Design principle: "AI handles scale, humans handle depth."
- Phase 2: beta rollout measuring retention and activation. The page cites published research on comparable programs (AI onboarding 13.6 percentage points higher completion; roughly 2x retention with empathetic persona design) as targets, not Wonda results.
