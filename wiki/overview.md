---
title: Overview
type: overview
created: 2026-06-21
updated: 2026-10-13
tags: [meta, agents]
---

# Overview

A research wiki on **building effective LLM agents**, synthesized from primary
guidance published by frontier labs and attributed practitioner case studies.

## Scope

How to design, build, and safely deploy LLM agents — the architecture choices,
tooling, orchestration, context engineering, harness design, and guardrails.
Grounded in the canonical practitioner guides from [[anthropic]] and [[openai]],
both vendors' operational posts on harness, runtime, containment, skills, MCP,
evals, and context (Nov 2025 – Oct 2026), vendor-published customer case
studies, and [[cursor]]'s large-scale coding-swarm case study; expandable to other labs, frameworks, and case studies.

## Current thesis

Across independent guidance, the labs **strongly agree** on a few load-bearing
principles (see [[agent-design-principles]] and the full comparison in
[[agent-building-best-practices-anthropic-vs-openai]]):

1. **Don't build an agent unless you need one.** Most tasks are better served by a
   workflow or a single LLM call. ([[agents-vs-workflows]])
2. **Start with the simplest design and add complexity only when evals show it
   helps.** Maximize a single agent before going multi-agent.
   ([[agent-orchestration]])
3. **Tools are the highest-leverage surface.** Invest in clear, documented,
   well-tested tools; clarity beats count. ([[tool-design]])
4. **Instructions must be unambiguous**, derived from real procedures.
   ([[agent-instructions]])
5. **Safety is layered** — guardrails plus human-in-the-loop for high-risk or
   repeatedly-failing actions. ([[guardrails]])
6. **Engineer the context and the harness, then prune them.** Load instructions
   on demand, let the agent manage/persist its own context, and delete harness
   scaffolding the model has outgrown. ([[context-engineering]], [[agent-harness]])
7. **Optimize the whole agent system, not an isolated model call.** Planner
   decisions shape worker volume, retries, conflicts, and total cost.
   ([[multi-agent-economics]])
8. **Contain at the environment layer; keep secrets out of the agent's reach.**
   Sandboxes and egress controls bound what an agent *can* do; model-level
   defenses only shape what it *tends* to do. Both vendors' hosted runtimes keep
   credentials outside the sandbox. ([[guardrails]],
   [[anthropic-eng-how-we-contain-claude]], [[model-context-protocol]],
   [[prompt-injection]])
9. **Verification, not generation, is the bottleneck.** An autonomous agent
   solves whatever the checks define, so the checks decide the quality of the
   result. Sources from both vendors and their customers report this:
   machine-checked certificates for code migrations, validation ladders for
   security findings, and near-perfect test suites for long runs.
   ([[agent-verification]], [[anthropic-eng-building-c-compiler]],
   [[anthropic-datadog-universal-machine-tool]],
   [[anthropic-comcast-booz-allen-exploit-chains]],
   [[anthropic-ai-code-modernization]], [[openai-harness-engineering]])

Since late 2025 the vendors have also converged on architecture: a hosted agent
runtime ([[claude-managed-agents]], [[openai-agents-api]]), the harness as a
reusable runtime with stable interfaces ([[openai-codex]]), and skills as routed,
on-demand context. See the 2026-10-12 update in
[[agent-building-best-practices-anthropic-vs-openai]].

They differ mainly in emphasis: Anthropic is deeper on **composable workflow
patterns** ([[workflow-patterns]]), **context engineering**, **harness design**,
and **skills/steering** ([[agent-skills]], [[agent-steering]]); OpenAI is deeper on
**production guardrails** and a crisp **Model/Tools/Instructions** component model
([[agent-core-components]]). Full comparison:
[[agent-building-best-practices-anthropic-vs-openai]].

## Key entities

- [[anthropic]] — *Building Effective Agents* + operational blog posts; maker of
  [[claude]], [[claude-code]], [[claude-agent-sdk]], [[claude-managed-agents]]
- [[openai]] — *A Practical Guide to Building Agents*; [[openai-agents-sdk]],
  [[openai-agents-api]], [[openai-codex]]
- [[cursor]] — practitioner evidence on coding swarms, coordination, and model
  economics

## Key concepts

- [[agents-vs-workflows]] · [[agent-design-principles]] · [[agent-core-components]]
  · [[tool-design]] · [[workflow-patterns]] · [[agent-orchestration]] ·
  [[agent-instructions]] · [[guardrails]] · [[agent-skills]] · [[agent-steering]] ·
  [[context-engineering]] · [[agent-harness]] · [[agent-evals]] ·
  [[multi-agent-economics]] · [[prompt-tuning-axes]] · [[model-context-protocol]]
  · [[prompt-injection]] · [[agent-memory]] · [[agent-identity-and-access]]
  · [[agent-verification]] · [[tool-placement]] · [[human-agent-teams]]

## Scope note: prompting vs. architecture

Cross-lab comparison is evidence for **architecture** claims — two independent
labs converging on "start simple" raises confidence the principle is real. It is
*not* useful for **prompting**, which is written against one model's behavior and
is therefore a per-model contract. Model-scoped prompting guidance is filed in
`wiki/sources/` with `models:`/`as_of:` frontmatter and is never synthesized
across vendors or generations. When a vendor stops listing a model as current,
its page is marked `status: legacy` and points to its replacement; on
2026-10-12 the Opus 5, Sonnet 5, Fable 5, and GPT-5.6 pages became legacy. The
durable framework is [[prompt-tuning-axes]], whose axes held steady across that
change while several settings reversed.

## Wiki health

- Current graph topology, hubs, and Obsidian filter caveats:
  [[obsidian-graph-analysis]].

## Open questions

- **Done:** the six core Anthropic *engineering* posts are ingested — building
  effective agents, context engineering, writing tools, long-running harnesses,
  demystifying evals ([[agent-evals]]), multi-agent research
  ([[agent-orchestration]]), and Agent Skills ([[agent-skills]]).
- **Done:** [[cursor-agent-swarm-model-economics]] adds practitioner evidence
  about coordination-heavy coding and whole-system model economics; its custom
  VCS and single benchmark limit generalization.
- **Done (2026-10-12):** 30 further Anthropic and OpenAI sources (Nov 2025 –
  Oct 2026), including advanced tool use and code execution with MCP. **MCP**
  now has a page: [[model-context-protocol]].
- **Done (2026-10-12):** the six remaining agent-relevant Anthropic Engineering
  posts, including [[anthropic-eng-building-c-compiler]] (16 agents with no
  orchestrator) and [[anthropic-eng-eval-awareness-browsecomp]] (an agent that
  found its benchmark's answer key).
- Add further perspectives (Google, LangChain, academic) to test how universal
  these "best practices" really are.
- **Done (2026-10-12):** a full sweep of claude.com (257 articles and 284
  customer stories, of which 68 had agent-design content), OpenAI's openai.com
  Engineering and Security posts, and its learning-hub guides. New concept
  pages: [[prompt-injection]] and [[agent-memory]].
- OpenAI-side harness coverage now includes the Codex agent loop, App Server,
  and harness engineering. It still lacks a counterpart to Anthropic's
  eval-noise post ([[anthropic-eng-infrastructure-noise-evals]]).
- **Done (2026-10-13):** OpenAI's "Agent security in the enterprise" white
  paper, from a PDF the human supplied ([[openai-agent-security-enterprise]]).
  Still not ingested: the OpenAI cookbook (code examples, not guidance) and both
  vendors' research papers.
- Customer stories make up a large share of the new sources. They are
  self-reported and vendor-published, so concept pages phrase their claims as
  reports, not rules.
