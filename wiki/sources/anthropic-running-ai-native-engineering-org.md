---
title: "Anthropic: Running an AI-native engineering org"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Fiona Fung (Anthropic; Code w/ Claude SF 2026 talk)
date: 2026-06-03
source_url: https://claude.com/resources/articles/running-an-ai-native-engineering-org
source_path: raw/anthropic-running-ai-native-engineering-org.md
tags: [engineering-management, claude-code, code-review, planning, organizational-practice, metrics]
---

# Anthropic: Running an AI-native engineering org

> The Claude Code team's engineering director on which processes broke once agentic coding became the default, and the norms and metrics that replaced them.

## Summary

Anthropic published this write-up on claude.com on 2026-06-03. It records a Code w/ Claude SF 2026 talk by Fiona Fung, Director of Engineering for Claude Code and Claude Cowork. The page has no author field, and the article is written in Fung's first person. No model version is named, and the claims describe Anthropic's own team. Fung's thesis: writing code, tests, and refactors rarely slows the team now, so the bottlenecks moved to verification, code review, and security. Processes built for expensive engineering time outlive their purpose and must be removed on purpose.

## Key points

- **Just-in-time planning.** A six-month roadmap was out of date by month three. Planning moved from design docs to PRs and prototypes: prototype, put internal users on it, and act on their feedback.
- **Ask Claude, not the author.** Every PR is Claude-assisted, so the team asks Claude what it needs to know, then asks whether the question can be automated (for example, a daily summary of the customer-feedback channels).
- **Trust but verify in code review.** Claude handles style, linting, bug catching, and test addition. Humans review legal risk, trust boundaries, security-sensitive code, and product taste. Fung says to re-evaluate this split as models improve. (see [[guardrails]], [[agent-evals]])
- **Blurred roles.** PMs code, and engineers take on content and design. Fung hires creative builders with product sense and deep systems experts, and indexes less on raw throughput.
- **Few mandated principles, pod autonomy for the rest.** The team mandates three things: dogfood relentlessly, keep the team flat (managers start as ICs), and give explicit permission to kill obsolete processes.
- **Three adoption metrics:** onboarding ramp time down, PR cycle time down, and Claude-assisted commits up. Fung warns that throughput is not success. PR cycle time can show where CI and build systems fail to scale.

## Notable claims & data

Self-reported: engineers ship real code within their first week; every commit is Claude-assisted by default, and Fung has seen no non-assisted commit in four months. Getting-started advice: pick the noisiest workflow and ask whether it should be automated or dropped.

## Entities

[[anthropic]], [[claude-code]], [[claude]]

## Concepts

[[guardrails]], [[agent-evals]], [[agent-design-principles]]

## Connections

Same bottleneck shift (verification and review over code generation): [[anthropic-ai-native-sdlc-playbook]], [[anthropic-securing-ai-native-sdlc]], [[anthropic-agentic-coding-ci-test-impact]], [[anthropic-ai-ci-cd-on-call]]. OpenAI's internal counterpart: [[openai-how-openai-uses-codex]], [[openai-harness-engineering]].
