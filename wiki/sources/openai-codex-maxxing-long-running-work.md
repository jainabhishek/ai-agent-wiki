---
title: "OpenAI: Codex-maxxing for long-running work"
type: source
created: 2026-10-12
updated: 2026-10-12
author: OpenAI (white paper featuring creator Jason Liu)
date: 2026-06-22
source_url: https://openai.com/index/codex-maxxing-long-running-work/
source_path: raw/openai-codex-maxxing-long-running-work.md
tags: [openai, codex, long-running-agents, memory, human-in-the-loop, automation, steering]
---

# OpenAI: Codex-maxxing for long-running work

> A 27-page OpenAI white paper (Jun 22, 2026) that uses creator Jason Liu's
> daily practice to show Codex as a persistent workspace. It covers durable
> threads, a reviewable memory vault, scheduled thread automations, and
> bounded "you decide" loops.

## Summary

OpenAI published this white paper as a PDF behind a landing page. It follows
how creator Jason Liu uses [[openai-codex]] beyond coding: for presentations,
transcripts, spreadsheets, browser tasks, and recurring work. The thesis is that
Codex gives work "somewhere to live". A prompt becomes an operating loop that
combines context, tools, memory, recurrence, and human review. The paper is
practitioner guidance from one power user, not a measured study. It gives no
metrics, and it names no model.

The ten sections, in order, are: durable threads, voice input, steering, memory,
computer and browser use, remote control, thread automations, three example
loops, verifiable goals, and the side panel.

## Key points

- **Durable threads.** Pin a thread per important workstream (for example "Chief
  of Staff" or "Agents SDK") so that context, preferences, decisions, and open
  loops accumulate there. Tradeoff: a long thread carries context and may cost
  more than a fresh short thread. See [[context-engineering]].
- **Memory as a reviewable artifact.** Message history is not enough. A **vault**
  holds rolling context: people, decisions, open loops, and project state.
  Repositories hold code. If the vault lives in GitHub, memory diffs become a
  review surface. The memory instruction asks Codex to record what changed, not
  vague impressions: update people notes, project pages, closed loops, and each
  decision with its reason.
- **Voice input** gives the model the "messy version" of intent (half-remembered
  names, uncertainty). Transcripts of calls and notes become starting material.
- **Steering** queues the next instruction while Codex works: correct, add
  context, approve, or chain the next action ("once this is done, open a PR").
  See [[agent-steering]].
- **Surface selection.** Use `$browser` for local previews, `@chrome` for
  signed-in or multi-tab work, `@computer` for GUI-only apps (with clear
  permissions and review), connectors for Slack, Gmail, Calendar, and GitHub,
  and skills for repeatable workflows. Package a workflow as a skill once it
  succeeds. See [[tool-design]] and [[agent-skills]].
- **Thread automations** are heartbeat-style wake-ups attached to a thread.
  Codex returns to the same conversation on a cadence instead of starting fresh.
  A thread can hold several schedules, run until a condition holds, and change
  its cadence. Example: every 30 minutes, check Slack and Gmail and draft
  replies, but send nothing without approval.
- **Bounded loops.** In all three example loops (Chief of Staff, Monitor for
  feedback, Get a refund), Codex prepares the context, drafts, and evidence. The
  human keeps approval, tone, consent, publishing, and "any irreversible action".
  See [[guardrails]].
- **Verifiable goals.** "Implement the plan in this file" is a weak goal. A strong
  goal gives a test standard. Example: port Rich to Rust, keep the public API,
  and treat the original unit tests as the success check. See
  [[agent-instructions]] and [[agent-evals]].
- **Remote control** lets a run continue on the local machine while the user
  reviews decision points from a phone. The paper says this is not a reason to
  skip reviews.
- **Side panel.** Codex and the user inspect the same artifact (Markdown,
  spreadsheets, CSVs, PDFs, slides, or a single `index.html`). Comments become
  instructions, and the artifact becomes context.

## Entities

[[openai]], [[openai-codex]]

## Concepts

[[context-engineering]], [[agent-steering]], [[agent-skills]], [[tool-design]],
[[guardrails]], [[agent-instructions]], [[agent-harness]]

## Notable claims & data

- No quantitative results. All claims are one practitioner's workflow, presented
  by OpenAI.
- The cost tradeoff of durable threads is stated qualitatively only.

## Connections

Complements [[openai-run-long-horizon-tasks-codex]] (long-horizon mechanics) and
[[openai-automating-repetitive-work-codex]] (recurring work). The "goal you can
verify" advice parallels the "prescriptive about persistence" area in
[[openai-practical-guide-building-with-gpt-6]]. Scheduled, bounded loops
parallel Anthropic's [[anthropic-getting-started-with-loops]].
