---
title: "OpenAI: One Year of Responses"
type: source
created: 2026-10-12
updated: 2026-10-12
author: OpenAI (Developers blog); case studies by Raindrop AI, Repo Prompt, Collxn, Arcade, Hexagon
date: 2026-03-11
source_url: https://developers.openai.com/blog/one-year-of-responses
source_path: raw/openai-one-year-of-responses.md
tags: [openai, responses-api, case-studies, tools, background-jobs, context-engineering]
---

# OpenAI: One Year of Responses

> OpenAI's one-year retrospective on the Responses API, told through five
> developer case studies. Useful for how teams combine hosted tools,
> background jobs, and multi-agent loops, not for API reference detail.

## Summary

[[openai]] presents the Responses API as its foundation for agents: hosted
tools let models act, not only chat. Five builders describe their designs.
Raindrop AI monitors production agents and runs long background analysis.
Repo Prompt separates context gathering from deep reasoning. Collxn runs a
stateful tool-calling chat over web search and 16 custom tools. Arcade turns
screen recordings into demos with the computer-use tool. Hexagon simulates
thousands of shopping prompts daily to track brand visibility. The post closes
with planned additions: better orchestration, richer tool ecosystems, OpenAI
hosted containers with networking, and shell tools. Publication date comes from
the page HTML ("Mar 11, 2026"); the text extraction showed no byline.

## Key points

- **Gather, then reason (Repo Prompt).** A context-builder agent produces a
  structured context package; an "Oracle" model reasons over it with **no tool
  calls and no retrieval**; a reviewer agent decides whether to loop again. See
  [[context-engineering]] and [[agent-orchestration]].
- **Responses API capabilities named by builders:** background jobs (minutes to
  hours), orchestration of multi-step loops, observability, stateful multi-turn
  chat, built-in web search, computer use, User Location, Reasoning Effort, Max
  Output Tokens, and context persistence across calls.
- **Tools instead of RAG (Collxn).** The developer found built-in web search
  plus 16 custom Discogs/account tools less complex than a full RAG system. See
  [[tool-design]].
- **Agent monitoring (Raindrop).** Developer-defined bad-outcome conditions,
  alerts with context, per-version behavior diffs, and trace/tool-call
  inspection. Accessed via the Vercel AI SDK for provider portability. See
  [[agent-evals]].
- **Multi-agent pipeline (Hexagon).** Four specialized agents in sequence with
  refinement loops. See [[workflow-patterns]].

## Entities

[[openai]], [[openai-agents-sdk]], [[openai-agents-api]], [[openai-codex]]

## Concepts

[[agent-core-components]], [[context-engineering]], [[agent-orchestration]],
[[tool-design]], [[agent-evals]], [[workflow-patterns]]

## Notable claims & data

- Arcade: median actions before publishing fell 50%; P80 from about 230 to
  about 120, after adding the computer-use workflow.
- Models named: GPT-5.2, GPT-5.4, GPT-5 nano, GPT-5.2 Chat, GPT-5.3-Codex,
  computer-use-preview (case-study context only, not guidance).
- Collxn used the [[openai-agents-sdk]] with web search for its artist-news
  agent, alongside the Responses API for chat.
- All claims are self-reported by the featured companies; the post gives no
  methodology.

## Connections

- Practitioner counterpart to [[openai-practical-guide-to-building-agents]]
  (model + tools + instructions) — the case studies show those components on
  the Responses API.
- Repo Prompt's gather/reason split parallels the subagent-for-search and
  isolated-context ideas in [[anthropic-eng-context-engineering]] and
  [[anthropic-eng-multi-agent-research-system]].
- Hosted containers with networking and shell tools are the OpenAI side of the
  hosted-sandbox direction in [[anthropic-eng-scaling-managed-agents]]; see also
  [[openai-shell-skills-compaction]] and [[openai-agents-api-guide]].
