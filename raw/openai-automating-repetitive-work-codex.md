# Automating repetitive work at OpenAI with Codex — OpenAI (Developers blog) (raw capture)

> Source: https://developers.openai.com/blog/automating-repetitive-work-at-openai-with-codex
> Publisher: OpenAI (Developers blog) · Date: 2026-08-25 (page byline "Aug 25, 2026"; category tag "Codex")
> Author: Jeremy Lewi
> Subtitle: how Runme and WebMCP turn recurring engineering tasks into reviewable, reusable workflows.
> Captured: 2026-10-12 via curl of the .md endpoint plus the HTML page for the byline (condensed and paraphrased).

## (Intro)

- First-person post. The author's earlier OpenAI roles were repetitive: bringing up batches of Kubernetes clusters on the cloud infrastructure team (private links, quota, Terraform), then running evaluations on the API team (graders, quota, configuration, PyTorch) for each model release.
- Now uses Codex for that work. Instead of a separate automation per task, he builds **Runme** (web.runme.dev) to: collect and curate context around a workflow; keep review and approval boundaries in place; improve future Codex runs with what earlier runs learned.

## Running evaluations with Codex

- To run an eval, he creates a Runme notebook with a short goal outline. Example outline items (paraphrased): review a previous run to learn the workflow; write a detailed plan in the notebook; wait for review and approval of the plan; document commands, output, and interpretation.
- He then tells Codex (paraphrased) to read the goal cell in the open Runme notebook, treat it as the goal, write its plan in the notebook, and wait for approval.
- Codex updates the notebook as work progresses. He reviews/revises the plan. His most useful input is choosing between alternatives: which eval system, whether to provision new infrastructure, whether existing resources suffice.
- He monitors progress, sometimes from a phone, and nudges when stuck — e.g. if a dev environment cannot be provisioned because quota is exhausted, suggest reusing an existing environment or another approved option.
- Output: a notebook documenting the steps and the dead ends. Before finishing, he and Codex record decisions that would otherwise vanish in the conversation: why an option was chosen, which approach is preferred now, what to do differently next time.

## Collaborating on notebooks with Codex

- Runme (github.com/runmedev/web) is an open-source web app for notebooks with Codex; like Jupyter/Colab it supports Markdown, code cells, and HTML.
- Notebooks save directly to Google Drive for familiar sharing.
- For each notebook Runme writes a companion Markdown index `*.index.md`; Google Drive indexes it, so agents can discover earlier notebooks for examples, operational context, or past outcomes.
- Agents interact with Runme through **WebMCP**. On load, the app registers browser-side tools letting an agent: read instructions for Runme and its notebooks; run bounded JavaScript programs that read or update notebook content; read the app's documentation.
- Rationale: Runme is a client-side static website. Adding a server just to expose a traditional MCP endpoint would add infrastructure and ops complexity and change where notebook data is handled; WebMCP exposes capabilities directly from the browser.

## Collecting and curating useful context

- Each eval run is a chance to document the work and make the next run easier; better workflow → more useful context → better next Codex run (illustrated as a flywheel: run eval, document, improve Codex workflows, run next eval faster).
- Useful agent context already exists but is scattered across terminal history, Slack, runbooks, documents, dashboards. The hard part is making documentation cheap to produce while working, not proving it is useful.
- Runme puts intent, actions, decisions, and outcomes in one artifact. A **persistent goal** (Codex long-running work) keeps Codex on task; **automatic approval review** (Codex auto-review) reviews eligible actions without changing existing permission boundaries.
- The human still decides when a plan is ready and when a consequential choice needs judgment. Codex does repetitive execution and records more detail than he would have. The notebook is shareable, so knowledge is not trapped in one chat history.

## Getting my heartbeats back

- Reflection: cloud infra and Kubernetes were meant to simplify operations but produced a sprawling tool ecosystem (CNCF landscape); solving one problem creates another.
- The appeal of Codex: help with repetitive operational work while keeping the human in the consequential decisions.
