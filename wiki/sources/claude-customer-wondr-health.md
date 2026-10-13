---
title: "Claude customer story: Wondr Health builds an AI coaching layer with a parallel safety subagent"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic (claude.com customer stories)
date: accessed 2026-10-12 (no date on page)
source_url: https://claude.com/customers/wondr-health
source_path: raw/claude-customer-wondr-health.md
tags: [case-study, healthcare, guardrails, safety-subagent, llm-as-judge, evals, human-escalation]
---

# Claude customer story: Wondr Health builds an AI coaching layer with a parallel safety subagent

> Healthcare case study: a coaching agent paired with a per-turn safety
> subagent, a tiered model split, and clinician-run persona testing.

## Summary

Anthropic published this customer story on claude.com; the page has no date
(accessed 2026-10-12). All results are self-reported by Wondr Health and its
build partner Blank Metal via Anthropic. Wondr built "Wonda", an onboarding
coach that extends human coaches. It runs on Claude through Amazon Bedrock. Phase
1 is built and tested but has not met real participants; the retention figures
on the page come from cited external research, not from Wonda.

## Key points

- **Model split by role:** Claude Opus 4.5 for coaching reasoning, Claude Sonnet
  for escalation detection, Claude Haiku as the LLM judge for automated evals.
  See [[multi-agent-economics]].
- **Parallel safety subagent on every turn.** It checks input and history for
  clinical risk, off-topic behavior, and escalation triggers. On a trigger it
  opens a Zendesk ticket with risk level and conversation summary, routed by
  severity. A concrete parallel-guardrail pattern for [[guardrails]].
- **Layered controls outside the model:** an API gateway handles auth, rate
  limits, and participant-data filtering before the model sees a request.
- **Synthetic data for the build.** Real participant health data stayed out of
  development.
- **Domain experts run the evals.** A no-code console let clinicians test 700+
  questions across six personas. Automated evaluators (verbosity, content
  accuracy) and two scored human rounds ran alongside. Clinicians were partners
  in evaluation, not a final gate. See [[agent-evals]].
- **Prepared inputs shorten discovery:** personas, curriculum, escalation
  guidelines, and a personality document.
- **Claimed result:** onboarding from 30–60 minutes to 10 minutes.

## Connections

Human-handoff design relates to [[openai-practical-guide-to-building-agents]]
(high-risk actions to humans) and [[anthropic-building-effective-human-agent-teams]].
Entities: [[anthropic]], [[claude]].
