# Shell + Skills + Compaction: Tips for long-running agents that do real work — OpenAI (raw capture)

> Source: https://developers.openai.com/blog/skills-shell-tips
> Publisher: OpenAI (Developers blog) · Date: 2026-02-11
> Captured: 2026-10-12 via the OpenAI blog full-text export plus curl of the page for byline (condensed).

Author: Charlie Guo. Category tag: API. Subtitle: practical patterns for
skills, hosted shell, and server-side compaction in the Responses API.

## Introduction

OpenAI frames a shift from single-turn assistants to long-running agents
that read large datasets, update files, and write apps. Based on developer
feedback and its experience building Codex and internal agents, OpenAI
announces three agent primitives:

- **Skills** — aligned with the Agent Skills open standard: reusable,
  versioned instruction bundles that can be mounted into containers.
- **Upgraded shell tool** — an OpenAI-hosted container with controlled
  internet access, where an agent installs dependencies, runs scripts, and
  writes outputs.
- **Server-side compaction** — automatic compaction of long runs so they do not
  hit context limits.

The post covers non-obvious patterns seen at OpenAI and at Glean (an early
skills customer).

## A brief mental model

### Skills: "Procedures" the model can load on demand

A skill is a bundle of files plus a `SKILL.md` manifest (frontmatter plus
instructions) — a versioned playbook. The platform exposes each skill's
`name`, `description`, and `path` to the model, which uses that metadata to
decide whether to invoke it; on invocation it reads `SKILL.md`.

### Shell tool: "Execution" for agents

The shell tool runs either in OpenAI-hosted containers or as a local shell
runtime you execute yourself (same tool semantics, your machine). Hosted shell
runs through the Responses API, so it comes with stateful work, tool calls,
multi-turn continuation, and artifacts.

### Compaction: Keep long runs moving

Two options in the Responses API:
- **Server-side compaction (new):** when context crosses a threshold,
  compaction runs automatically in-stream; no separate call.
- **Standalone compact endpoint:** `/responses/compact` for explicit control
  over timing.

### Why they're better together

Skills move stable procedures and examples out of the prompt; shell gives a
full execution environment; compaction preserves continuity. Together they
avoid turning the system prompt into a brittle "megadoc".

## Tips and tricks

### 1) Write skill descriptions like routing logic (not marketing copy)

The description is the model's decision boundary. It should state when to
use the skill, when not to, and the outputs and success criteria. Pattern: a
short "use when vs. don't use when" block in the description, concrete about
inputs, tools, and expected artifacts.

### 2) Add negative examples and edge cases to reduce misfires

Making skills available can at first reduce correct triggering. Fix: explicit
"don't call this skill when..." cases plus what to do instead, especially
when several skills look alike. Glean: skill-based routing first dropped
triggering by about **20%** in targeted evals, then recovered after adding
negative examples and edge-case coverage to descriptions.

### 3) Put templates and examples inside the skill

Stop putting templates in the system prompt. Inside a skill they load only
when the skill is invoked and cost no tokens for unrelated queries. Good fit
for structured reports, escalation triage summaries, account plans, and data
analysis write-ups. Glean reported some of its biggest quality and latency
gains from this, because examples load only when the skill triggers.

### 4) Design for long runs early with container reuse and compaction

- Reuse the same container across steps for stable dependencies, cached
  files, and intermediate outputs.
- Pass `previous_response_id` so the model continues in the same thread.
- Treat compaction as a default long-run primitive, not an emergency fallback.

### 5) When you need determinism, explicitly tell the model to use the skill

Default: the model decides when to use a skill. For a production workflow
with a clear contract, instruct "Use the `<skill name>` skill." — turning
fuzzy routing into an explicit contract.

### 6) Treat skills plus networking as a high-risk combo (design for containment)

Skills combined with open network access create a high-risk path for data
exfiltration. Keep network allowlists strict, assume tool output is
untrusted, and avoid open internet plus powerful procedures in consumer flows
that need strong confirmation controls. Recommended default posture: skills
allowed; shell allowed; network enabled only with a minimal allowlist, per
request, for narrowly scoped tasks.

### 7) Make `/mnt/data` your handoff boundary for artifacts

In hosted shell, write retrievable outputs (reports, cleaned datasets,
spreadsheets) to `/mnt/data`. Mental model: tools write to disk, models
reason over disk, developers retrieve from disk.

### 8) Understand allowlists as a two-layer system (org-level and request-level)

- Org-level allowlist (set by an admin): the maximum allowed destinations.
- Request-level `network_policy`: must be a subset of the org allowlist.
Keep the org list small and stable; keep request lists smaller still. A
request naming a domain outside the org allowlist errors.

### 9) Use `domain_secrets` for authenticated calls (avoid credential leakage)

With `domain_secrets` the model sees only placeholders (for example
`$API_KEY`); a sidecar injects the real value only for approved destinations.

### 10) Use the same APIs in the cloud and locally

- Skills work with hosted shell and local shell mode.
- Local shell mode: you execute `shell_call` yourself and return
  `shell_call_output` to the model.
- The Agents SDK accepts a custom shell executor.
Suggested loop: start local (fast iteration, internal tools, easy debugging),
move to hosted containers for repeatability, isolation, and deployment
consistency, and keep the skills identical across both.

## Three build patterns

### Pattern A: Install -> fetch -> write artifact

Install libraries, scrape or call an API, write a report to
`/mnt/data/report.md`. The artifact is a clean review boundary: the app can
show, log, diff, or feed it forward.

### Pattern B: Skills + shell for repeatable workflows

When reliability degrades as prompts drift: (1) encode the workflow (steps,
guardrails, templates) in a skill; (2) mount it into the shell environment;
(3) have the agent follow it to produce artifacts deterministically. Fits
spreadsheet analysis or editing, dataset cleaning plus summary, and
standardized recurring reports.

### Pattern C (advanced): Skills as enterprise workflow carriers

Accuracy drops in the gap between single tool calls and multi-tool
orchestration; skills make tool reasoning more procedural without bloating the
system prompt. Glean example: a Salesforce-oriented skill raised eval accuracy
from **73% to 85%** and cut time-to-first-token by **18.1%**, using careful
routing, negative examples, and templates inside the skill. Glean also uses
skills for account planning, escalation triage, and brand-aligned content.
Skills become "living SOPs" executed consistently by agents.

## Build once, run anywhere

Recap: skills encode the how; shell executes the do; compaction keeps long
runs coherent; start locally, move to hosted containers for isolated
repeatable runs; lock networking down with org- and request-level allowlists
and use domain secrets for authenticated calls.
